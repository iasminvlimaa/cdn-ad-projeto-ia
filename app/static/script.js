document.addEventListener('DOMContentLoaded', () => {
    // --- ESTADO GLOBAL E ELEMENTOS PRINCIPAIS ---
    const estado = {
        ano: 2025,
        regiao: 'Todas'
    };
    const filtroAno = document.getElementById('filtro-ano');
    const filtroRegiao = document.getElementById('filtro-regiao');
    let chartInstance = null;
    let historicoChartInstance = null;
    const sidebarLinks = document.querySelectorAll('.sidebar-link');
    const pages = document.querySelectorAll('.page-content');

    // --- ROTEAMENTO SPA (Single Page Application) ---
    function showPage(pageId) {
        pages.forEach(page => page.classList.add('hidden'));
        const activePage = document.getElementById(pageId);
        if (activePage) {
            activePage.classList.remove('hidden');
        }

        sidebarLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${pageId}`) {
                link.classList.add('active');
            }
        });

        // Carrega os dados da página específica quando ela é exibida
        switch (pageId) {
            case 'dashboard':
                atualizarDashboards();
                break;
            case 'analises':
                initAnalises();
                break;
            case 'relatorios':
                carregarRelatorioCompleto();
                break;
        }
    }

    sidebarLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const pageId = link.getAttribute('href').substring(1);
            showPage(pageId);
        });
    });

    // --- FUNÇÃO PRINCIPAL DE ATUALIZAÇÃO DO DASHBOARD ---
    function atualizarDashboards() {
        const ano = estado.ano;
        const regiao = estado.regiao;
        console.log(`Atualizando Dashboard para Ano: ${ano}, Região: ${regiao}`);
        carregarKpiMediaGeral(ano, regiao);
        carregarKpiMelhoriaAnual(ano, regiao);
        carregarKpiBenchmark(ano, regiao);
        carregarGraficoRegioes(ano);
        carregarRankingEscolas(ano, regiao);
        carregarRankingAlunos(ano, regiao);
    }

    // --- OUVINTES DE EVENTOS DOS FILTROS ---
    function handleFilterChange() {
        const paginaAtiva = document.querySelector('.page-content:not(.hidden)')?.id;
        if (paginaAtiva === 'dashboard') {
            atualizarDashboards();
        } else if (paginaAtiva === 'relatorios') {
            carregarRelatorioCompleto();
        } else if (paginaAtiva === 'analises') {
            initAnalises();
        }
    }
    filtroAno.addEventListener('change', (e) => {
        estado.ano = parseInt(e.target.value);
        handleFilterChange();
    });
    filtroRegiao.addEventListener('change', (e) => {
        estado.regiao = e.target.value;
        handleFilterChange();
    });

    // --- FUNÇÕES DE CARREGAMENTO DE DADOS (DASHBOARD) ---
    async function carregarKpiMediaGeral(ano, regiao) {
        const el = document.getElementById('media-geral');
        if (!el) return;
        try {
            const response = await fetch(`/api/desempenho/geral?ano=${ano}&regiao=${regiao}`);
            const data = await response.json();
            el.textContent = data.media_geral_premio.toFixed(2);
        } catch (error) { console.error('Erro KPI Média:', error); }
    }

    async function carregarKpiMelhoriaAnual(ano, regiao) {
        const el = document.getElementById('melhoria-anual');
        if (!el) return;
        try {
            const response = await fetch(`/api/desempenho/melhoria-anual?ano=${ano}&regiao=${regiao}`);
            const data = await response.json();
            const valor = data.melhoria_percentual;
            el.textContent = `${valor >= 0 ? '+' : ''}${valor.toFixed(1)}%`;
            el.className = valor >= 0 ? 'positivo' : 'negativo';
        } catch (error) { console.error('Erro KPI Melhoria:', error); }
    }

    async function carregarKpiBenchmark(ano, regiao) {
        const el = document.getElementById('benchmark-ideb');
        if (!el) return;
        try {
            const response = await fetch(`/api/desempenho/benchmark-ideb?ano=${ano}&regiao=${regiao}`);
            const data = await response.json();
            const valor = data.diferenca_ideb;
            el.textContent = `${valor >= 0 ? '+' : ''}${valor.toFixed(2)}`;
            el.className = valor >= 0 ? 'positivo' : 'negativo';
        } catch (error) { console.error('Erro KPI Benchmark:', error); }
    }

    async function carregarRankingEscolas(ano, regiao) {
        const tabelaBody = document.getElementById('ranking-body');
        if (!tabelaBody) return;
        try {
            tabelaBody.innerHTML = '<tr><td colspan="4">Carregando...</td></tr>';
            const response = await fetch(`/api/escolas/top10?ano=${ano}&regiao=${regiao}`);
            const escolas = await response.json();
            tabelaBody.innerHTML = '';
            if (escolas.length === 0) {
                tabelaBody.innerHTML = '<tr><td colspan="4">Nenhum dado encontrado.</td></tr>';
                return;
            }
            escolas.forEach((escola, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `<td>${index + 1}º</td><td>${escola.nome}</td><td>${escola.pontuacao_premio.toFixed(2)}</td><td>${escola.regiao}</td>`;
                tabelaBody.appendChild(row);
            });
        } catch (error) { console.error('Erro Ranking Escolas:', error); }
    }

    async function carregarRankingAlunos(ano, regiao) {
        const tabelaBody = document.getElementById('ranking-alunos-body');
        if (!tabelaBody) return;
        try {
            tabelaBody.innerHTML = '<tr><td colspan="4">Carregando...</td></tr>';
            const responseAlunos = await fetch(`/api/alunos/destaques?ano=${ano}&regiao=${regiao}`);
            const alunos = await responseAlunos.json();
            if (alunos.length === 0) {
                tabelaBody.innerHTML = '<tr><td colspan="4">Nenhum dado encontrado.</td></tr>';
                return;
            }
            const responseEscolas = await fetch(`/api/escolas?ano=${ano}&regiao=Todas`);
            const listaEscolas = await responseEscolas.json();
            const mapaEscolas = new Map(listaEscolas.map(e => [e.id, e.nome]));
            tabelaBody.innerHTML = '';
            alunos.forEach((aluno, index) => {
                const row = document.createElement('tr');
                const nomeEscola = mapaEscolas.get(aluno.escola_id) || 'Não encontrada';
                row.innerHTML = `<td>${index + 1}º</td><td>${aluno.nome_anonimizado}</td><td>${aluno.nota_geral.toFixed(2)}</td><td>${nomeEscola}</td>`;
                tabelaBody.appendChild(row);
            });
        } catch (error) { console.error('Erro Ranking Alunos:', error); }
    }
    
    async function carregarGraficoRegioes(ano) {
        const canvas = document.getElementById('regiaoChart');
        if (!canvas) return;
        try {
            const response = await fetch(`/api/desempenho/regioes?ano=${ano}`);
            const data = await response.json();
            const ctx = canvas.getContext('2d');
            
            if(chartInstance) chartInstance.destroy();
            
            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(item => item.regiao),
                    datasets: [{
                        label: `Pontuação Média (${ano})`,
                        data: data.map(item => item.media_pontuacao),
                        backgroundColor: 'rgba(255, 103, 0, 0.7)',
                        borderColor: 'rgba(255, 103, 0, 1)',
                        borderWidth: 1,
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: { y: { beginAtZero: true } },
                    onClick: (event, elements) => {
                        if (elements.length > 0) {
                            const index = elements[0].index;
                            const regiaoClicada = chartInstance.data.labels[index];
                            estado.regiao = regiaoClicada;
                            filtroRegiao.value = regiaoClicada;
                            atualizarDashboards();
                        }
                    }
                }
            });
        } catch (error) { console.error('Erro Gráfico:', error); }
    }

    // --- LÓGICA DA PÁGINA DE ANÁLISES ---
    async function initAnalises() {
        const selectEscolas = document.getElementById('analise-escolas-select');
        const compararBtn = document.getElementById('analise-comparar-btn');
        const anoSpan = document.getElementById('analise-ano-selecionado');
        const selectHistorico = document.getElementById('analise-historico-select');
        if (!selectEscolas) return;
        
        anoSpan.textContent = estado.ano;

        const responseEscolas = await fetch(`/api/escolas?ano=${estado.ano}&regiao=Todas`);
        const todasEscolas = await responseEscolas.json();
        
        selectEscolas.innerHTML = '';
        selectHistorico.innerHTML = '<option value="">Selecione uma escola</option>';

        todasEscolas.forEach(escola => {
            const option = document.createElement('option');
            option.value = escola.id;
            option.textContent = escola.nome;
            selectEscolas.appendChild(option);
            selectHistorico.appendChild(option.cloneNode(true));
        });

        compararBtn.onclick = async () => {
            const selectedIds = Array.from(selectEscolas.selectedOptions).map(opt => parseInt(opt.value));
            if (selectedIds.length === 0 || selectedIds.length > 3) {
                return alert('Por favor, selecione de 1 a 3 escolas para comparar.');
            }
            const response = await fetch(`/api/escolas/comparar?ano=${estado.ano}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(selectedIds)
            });
            const escolasParaComparar = await response.json();
            const containerResultado = document.getElementById('analise-resultado-container');
            containerResultado.innerHTML = '';
            escolasParaComparar.forEach(escola => {
                const card = document.createElement('div');
                card.className = 'kpi-card';
                card.innerHTML = `<h2>${escola.nome}</h2><p style="color: var(--cor-principal)">${escola.pontuacao_premio.toFixed(2)}</p><small>IDEB Público: ${escola.ideb_publico.toFixed(2)}</small>`;
                containerResultado.appendChild(card);
            });
        };

        selectHistorico.onchange = async (event) => {
            const escolaId = event.target.value;
            if (historicoChartInstance) historicoChartInstance.destroy();
            if (!escolaId) return;
            
            const response = await fetch(`/api/escolas/${escolaId}/historico`);
            const historicoData = await response.json();
            const ctx = document.getElementById('historicoChart').getContext('2d');
            
            historicoChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: historicoData.map(d => d.ano),
                    datasets: [{
                        label: 'Pontuação no Prêmio',
                        data: historicoData.map(d => d.pontuacao),
                        borderColor: 'var(--cor-principal)',
                        backgroundColor: 'rgba(255, 103, 0, 0.1)',
                        fill: true,
                        tension: 0.2
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });
        };
    }

    // --- LÓGICA DA PÁGINA DE RELATÓRIOS ---
    let dadosRelatorio = [];
    async function carregarRelatorioCompleto() {
        const tabelaBody = document.getElementById('relatorio-body');
        if (!tabelaBody) return;
        tabelaBody.innerHTML = '<tr><td colspan="6">Carregando...</td></tr>';
        
        const response = await fetch(`/api/escolas?ano=${estado.ano}&regiao=${estado.regiao}`);
        dadosRelatorio = await response.json();
        
        tabelaBody.innerHTML = '';
        if (dadosRelatorio.length === 0) {
            tabelaBody.innerHTML = '<tr><td colspan="6">Nenhum dado encontrado para esta seleção.</td></tr>';
            return;
        }

        dadosRelatorio.forEach(escola => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${escola.id}</td><td>${escola.nome}</td><td>${escola.regiao}</td>
                <td>${escola.ano}</td><td>${escola.pontuacao_premio.toFixed(2)}</td>
                <td>${escola.ideb_publico.toFixed(2)}</td>
            `;
            tabelaBody.appendChild(row);
        });
    }

    function exportarParaCSV() {
        if (dadosRelatorio.length === 0) return alert("Não há dados para exportar.");
        const headers = ['ID', 'Nome da Escola', 'Região', 'Ano', 'Pontuação Prêmio', 'IDEB Público'];
        const csvRows = [headers.join(',')];
        dadosRelatorio.forEach(escola => {
            const nomeFormatado = `"${escola.nome.replace(/"/g, '""')}"`;
            const values = [escola.id, nomeFormatado, escola.regiao, escola.ano, escola.pontuacao_premio, escola.ideb_publico];
            csvRows.push(values.join(','));
        });
        
        const csvString = csvRows.join('\n');
        const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.setAttribute('href', url);
        a.setAttribute('download', `relatorio_escolas_${estado.ano}_${estado.regiao}.csv`);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }
    document.getElementById('export-csv-btn')?.addEventListener('click', exportarParaCSV);

    // --- LÓGICA DA PÁGINA DE CONFIGURAÇÕES ---
    function initConfiguracoes() {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;

        if (!themeToggle.getAttribute('listener')) {
            themeToggle.setAttribute('listener', 'true');
            themeToggle.addEventListener('change', () => {
                document.body.classList.toggle('dark-mode');
                localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
            });
        }
    }

    // --- FUNÇÕES DE INICIALIZAÇÃO E POPULAÇÃO ---
    function popularFiltroRegioes() {
        const regioes = ["Nordeste", "Sudeste", "Sul", "Norte", "Centro-Oeste"];
        const filtroRegiaoSelect = document.getElementById('filtro-regiao');
        if (filtroRegiaoSelect.options.length <= 1) {
            regioes.forEach(r => {
                const option = document.createElement('option');
                option.value = r;
                option.textContent = r;
                filtroRegiaoSelect.appendChild(option);
            });
        }
    }
    
    function initApp() {
        const themeToggle = document.getElementById('theme-toggle');
        if (localStorage.getItem('theme') === 'dark') {
            document.body.classList.add('dark-mode');
            if(themeToggle) themeToggle.checked = true;
        } else {
            document.body.classList.remove('dark-mode');
            if(themeToggle) themeToggle.checked = false;
        }
        
        initConfiguracoes(); 
        popularFiltroRegioes();
        showPage('dashboard');
    }

    // Inicializa a aplicação
    initApp();
});
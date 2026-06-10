# 🔥 PyroWatch — Sistema de Monitoramento de Queimadas

Dashboard interativo desenvolvido para a **Global Solution 2026/1 — Front-end em Sistemas de IA (FIAP)**.

## Problema

Queimadas no Brasil causam impactos ambientais, econômicos e sociais devastadores. Tomadores de decisão precisam de informações em tempo real sobre focos ativos, nível de risco e área afetada para acionar protocolos de resposta. O PyroWatch transforma dados satelitais brutos em visualizações acionáveis.

## Fonte de Dados

Dados simulados com base nos padrões do **INPE (Programa de Queimadas)** e **NASA FIRMS** (Fire Information for Resource Management System). Em produção, a camada `providers/` seria substituída por chamadas HTTP reais a essas APIs.

## Framework

**Streamlit** — escolhido pela robustez no gerenciamento de estado (`st.session_state`), facilidade de cache (`@st.cache_data`) e suporte nativo a Plotly e Matplotlib.

## Arquitetura

```
pyrowatch/
├── app.py                  # Entry point
├── providers/
│   └── fire_provider.py    # Acesso a dados (fetch + cache)
├── pipelines/
│   └── fire_pipeline.py    # Filtragem, agregação e transformação
├── features/
│   ├── overview.py         # Tela: Visão Geral
│   ├── fire_monitor.py     # Tela: Mapa & Risco
│   └── alerts.py           # Tela: Central de Alertas (Human-in-the-loop)
├── state/
│   └── session_state.py    # Gerenciamento centralizado de estado
├── ui/
│   ├── components.py       # Componentes reutilizáveis (metric_card, alert_card, risk_badge)
│   ├── charts.py           # Gráficos Plotly + Matplotlib
│   └── sidebar.py          # Sidebar com filtros
└── requirements.txt
```

## Instalação e Execução

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Requisitos Atendidos

| Requisito | Implementação |
|-----------|--------------|
| Ciclo de execução | `st.session_state` + `@st.cache_data` em `providers/` |
| Arquitetura em camadas | `providers/`, `pipelines/`, `features/`, `state/`, `ui/` |
| 3+ filtros interativos | Data, Estado, Bioma, Nível de Risco (sidebar) |
| 2+ gráficos (Plotly obrigatório) | Line, Bar, Donut, Scatter Map (Plotly) + Area (Matplotlib) |
| Componente reutilizável | `metric_card()` em `ui/components.py` — usado em 3 features |
| Tabs + layout organizado | 3 tabs: Visão Geral, Mapa & Risco, Central de Alertas |
| Design para latência | `st.spinner` em cada feature |
| Cores semânticas | Verde/Amarelo/Laranja/Vermelho por nível de risco |
| Human-in-the-loop | Central de Alertas: aprovar/descartar alertas gerados pelo sistema |

# 🇧🇷 Sistema de Rotas entre Capitais Brasileiras

Este projeto implementa e compara diferentes algoritmos de busca para encontrar rotas entre as 27 capitais brasileiras, com visualização interativa em mapa do Brasil e suporte para transporte aéreo e terrestre.

## ✨ Funcionalidades Principais

### 🗺️ Visualização Interativa
- **Mapa completo do Brasil** com todas as 27 capitais
- **Rotas visualizadas** com diferentes cores para aéreo/terrestre
- **Posicionamento inteligente** de labels para evitar sobreposições
- **Zoom otimizado** para melhor visualização dos detalhes
- **Legenda dinâmica** que se posiciona automaticamente

### 🔍 Algoritmos de Busca Implementados
- **BFS (Busca em Largura)**: Encontra caminho com menor número de conexões
- **DFS (Busca em Profundidade)**: Explora caminhos em profundidade
- **UCS (Busca de Custo Uniforme)**: Encontra rota de menor distância (ótimo)
- **Greedy (Busca Gulosa)**: Usa heurística de distância euclidiana
- **A* (A-Star)**: Combina custo real + heurística (ótimo e eficiente)

### 🚗✈️ Tipos de Transporte
- **Aéreo**: Conexões diretas por linha reta
- **Terrestre**: Rotas inteligentes que evitam oceano, usando pontos intermediários

### 📊 Análise Comparativa
- **Execução simultânea** de todos os algoritmos
- **Comparação detalhada** de distância, nós expandidos e otimalidade
- **Identificação automática** da melhor solução

## 🚀 Execução

### Opção 1: Docker (Recomendado)
```bash
# Execute diretamente com Docker
./run_docker_gui.sh
```

### Opção 2: Ambiente Local
```bash
# Instale dependências
sudo apt-get install python3-tk  # Ubuntu/Debian
pip install -r requirements.txt

# Execute a aplicação
python3 run_map_gui.py
```

## 🏗️ Arquitetura do Sistema

```
rotas-capitais/
├── 📋 Aplicação Principal
│   ├── main_gui_maps.py      # Interface gráfica com mapa (PRINCIPAL)
│   ├── run_map_gui.py        # Script de execução com verificações
│   └── geo_coordinates.py    # Coordenadas das 27 capitais brasileiras
│
├── 🧠 Algoritmos de Busca
│   └── search/
│       ├── interface.py      # Interface base (SearchAlgorithm)
│       ├── bfs.py           # Busca em Largura
│       ├── dfs.py           # Busca em Profundidade  
│       ├── ucs.py           # Busca de Custo Uniforme
│       ├── greedy.py        # Busca Gulosa
│       └── astar.py         # Algoritmo A*
│
├── 📊 Modelos de Dados
│   └── models/
│       ├── city.py          # Classe City
│       └── graph.py         # Classe Graph com conectividades
│
├── 🛠️ Utilitários
│   └── utils/
│       ├── data_loader.py   # Carregamento de dados
│       ├── comparison.py    # Comparação de algoritmos
│       └── report_generator.py # Geração de relatórios
│
├── 🗃️ Dados
│   └── data/
│       ├── distances.json   # Distâncias entre todas as capitais
│       ├── brazil_country.geojson # Mapa do Brasil (1.1 MB)
│       └── brazil_states.geojson  # Estados detalhados (3.2 MB)
│
└── 🐳 Docker
    ├── Dockerfile           # Configuração Docker
    ├── docker-compose.yml   # Orquestração
    └── run_docker_gui.sh    # Script de execução
```

## 🎯 Princípios SOLID Aplicados

| Princípio | Implementação |
|-----------|---------------|
| **S** - Single Responsibility | `City` gerencia cidades, `Graph` gerencia conexões, cada algoritmo tem função específica |
| **O** - Open/Closed | Novos algoritmos podem ser adicionados implementando `SearchAlgorithm` |
| **L** - Liskov Substitution | Todos os algoritmos são intercambiáveis via interface comum |
| **I** - Interface Segregation | Interface `SearchAlgorithm` contém apenas método `search()` |
| **D** - Dependency Inversion | Aplicação depende de abstrações, não implementações concretas |

## 📈 Análise de Performance

### Exemplo: São Paulo → Manaus

| Algoritmo | Distância | Nós Expandidos | Caminho | Ótimo |
|-----------|-----------|----------------|---------|-------|
| UCS | 2,689 km | 15 | SP→Brasília→Manaus | ✅ |
| A* | 2,689 km | 8 | SP→Brasília→Manaus | ✅ |
| Greedy | 2,689 km | 3 | SP→Brasília→Manaus | ✅ |
| BFS | 3,971 km | 12 | SP→Manaus (direto) | ❌ |
| DFS | 4,250 km | 18 | SP→múltiplas paradas | ❌ |

## 🗺️ Capitais Incluídas (27)

### Região Norte
- Belém (PA), Boa Vista (RR), Macapá (AP), Manaus (AM), Palmas (TO), Porto Velho (RO), Rio Branco (AC)

### Região Nordeste  
- Aracaju (SE), Fortaleza (CE), João Pessoa (PB), Maceió (AL), Natal (RN), Recife (PE), Salvador (BA), São Luís (MA), Teresina (PI)

### Região Centro-Oeste
- Brasília (DF), Campo Grande (MS), Cuiabá (MT), Goiânia (GO)

### Região Sudeste
- Belo Horizonte (MG), Rio de Janeiro (RJ), São Paulo (SP), Vitória (ES)

### Região Sul
- Curitiba (PR), Florianópolis (SC), Porto Alegre (RS)

## 🛠️ Requisitos Técnicos

### Python 3.9+
```bash
# Dependências principais
matplotlib>=3.5.0    # Visualização de gráficos
networkx>=2.8       # Manipulação de grafos  
geopandas>=0.12.0   # Processamento geoespacial
tkinter             # Interface gráfica (incluído no Python)
```

### Sistema
- **Linux**: X11 para interface gráfica
- **Docker**: Para execução isolada (recomendado)
- **Memória**: ~100MB para mapas em cache

## 🎓 Contexto Acadêmico

**Disciplina**: Fundamentos de Sistemas Inteligentes  
**Instituição**: UTFPR - Campus Dois Vizinhos  
**Objetivo**: Implementar e comparar algoritmos de busca em grafos  
**Aplicação**: Sistema prático com dados reais das capitais brasileiras

## 📄 License

Copyright (C) 2025-2026 Gabriel Felipe Guarnieri. All rights reserved.

This project is dual-licensed under the **AGPL-3.0 + Commercial License** model:

- **Open-source use**: Licensed under the [GNU Affero General Public License v3.0 (AGPL-3.0)](LICENSE).
- **Commercial use**: A proprietary commercial license is available for use cases incompatible with the AGPL-3.0. See [LICENSE-COMMERCIAL.md](LICENSE-COMMERCIAL.md) for details.

> **Retroactive clause**: This license applies retroactively to all past commits and versions of this repository, superseding any previously stated license.

For commercial licensing inquiries, contact the author via [LinkedIn](https://www.linkedin.com/in/oguarni/).

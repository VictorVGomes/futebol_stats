# futebol_stats
Um app simples para leitura e visualização de estatísticas básicas sobre futebol, com foco em  times individuais

## Rodando o app

Primeiro, é necessário fazer o download do repositório. Isso deve ser feito nesta página do github.

1. Baixando o repositório:
    - com o comando `git clone https://github.com/VictorVGomes/futebol_stats.git` (caso você tenha o git bash instalado)
    - clicando em **<> code** e depois em Download ZIP

2. Acessando o repositório
    - Se você baixou via git clone, basta acessar o repositório local de nome "futebol_stats"
    - se você baixou o .zip, extraia o repositório usando algum extrator de arquivos do tipo .zip em uma pasta e acesse o conteúdo

3. Rodando o app
    - dentro do repositório local, clique no arquivo install.cmd
    - verifique que tudo ocorreu como o esperado no prompt de comando que foi aberto
    - agora, basta clicar em "run.cmd" para rodar o app

## Mais detalhes

O app (dashboard) pode ser alimentado com um dataset personalizado. É necessário, no entanto, que esse dataset tenha as colunas nomeadas da mesma forma que o dataset de exemplo usado como base neste app. Na aba **Dados usados**, mais detalhes sobre quais dados são essenciais são dados.

É possível, também, criar um arquivo novo e alimentar o dashboard com ele por meio do aplicativo. A única restrição é que o nome das colunas e o tipo de dado contido em cada uma delas seja compatível (até certo ponto) com os dados usados originalmente no app.

## Estrutura das pastas

```
│   install.cmd
│   main.py
│   README.md
│   run.cmd
│
├───checks
│   │   checks_and_installs_env.py
│   │
│   └───output
│
├───requirements
│       requirements.txt
│
└───src
    ├───datasets
    │       brasileirao_serie_a.csv
    │
    ├───stats
    │       stats.py
    │
    └───utils
            futils.py
            useful_strings.py
```

### descrição dos arquivos

- **install.cmd**
    - é usado para instalar os requerimentos do aplicativo
- **main.py**
    - o aplicativo principal
- **run.cmd**
    - usado para inicializar o aplicativo principal
- **checks/checks_and_installs_env.py**
    - checa se o ambiente python já foi instalado. Se não, instala ele
- **src/datasets/brasileirao_serie_a.csv**
    - arquivo .csv com os dados usados no app
- **src/stats/stats.py**
    - funções utilitárias para agregar estatísticas
- **src/utils/futils.py**
    - funções utilitárias de manejamento de arquivos
- **src/utils/useful_strings.py**
    - agregador de textos usados no app

## dados usados:

A base de dados usada neste app foi adquirida no site **basedosdados.org** (disponíveis clicando [aqui](https://basedosdados.org/dataset/c861330e-bca2-474d-9073-bc70744a1b23?table=18835b0d-233e-4857-b454-1fa34a81b4fa)) e é sobre os jogos ocorridos no Brasileirão Série A com cobertura temporal indo desde 2003-03-29 até 2023-10-26.

As colunas disponíveis são:
<> code
- **ano_campeonato** : int64 *
- data : object
- rodada : int64
- estadio : object
- arbitro : object
- publico : float64
- publico_max : float64
- **time_mandante** : object *
- **time_visitante** : object *
- tecnico_mandante : object
- tecnico_visitante : object
- colocacao_mandante : float64
- colocacao_visitante : float64
- valor_equipe_titular_mandante : float64
- valor_equipe_titular_visitante : float64
- idade_media_titular_mandante : float64
- idade_media_titular_visitante : float64
- **gols_mandante** : float64 *
- **gols_visitante** : float64 *
- gols_1_tempo_mandante : float64
- gols_1_tempo_visitante : float64
- *escanteios_mandante* : float64 **
- *escanteios_visitante* : float64 **
- *faltas_mandante* : float64 **
- *faltas_visitante* : float64 **
- *chutes_bola_parada_mandante* : float64 **
- *chutes_bola_parada_visitante* : float64 **
- *defesas_mandante* : float64 **
- *defesas_visitante* : float64 **
- *impedimentos_mandante* : float64 **
- *impedimentos_visitante* : float64 **
- *chutes_mandante* : float64 **
- *chutes_visitante* : float64 **
- *chutes_fora_mandante* : float64 **
- *chutes_fora_visitante* : float64 **

Muitas delas contém valores nulos, e algumas são imprescindíveis para as análises feitas neste aplicativo. Outras variáveis podem ser adicionadas sem causar problemas no funcionamento do app. Algumas, no entanto, não estarão disponíveis para todas as análises desejadas. As variáveis básicas e necessárias para o app estão em negrito e com um único asterisco (*). As variáveis importantes, mas não necessárias, estão em itálico, com 2 asteriscos (**). As outras variáveis não são necessárias, mas podem trazer informações importantes ao usuário.
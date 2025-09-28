# Credit Scoring - EBAC Project

Este projeto é uma aplicação web desenvolvida em Streamlit para análise de credit scoring, permitindo tanto o upload de dados em lote quanto a simulação individual de scores de crédito.

## Funcionalidades

- **Upload de dados em lote**: Processamento de arquivos .ftr para cálculo de scores de crédito
- **Simulador individual**: Interface para calcular score de crédito de clientes individuais
- **Download de resultados**: Exportação dos resultados em formato Excel

## Como usar

### Upload em Lote
1. Acesse a aba "Upload"
2. Faça upload de um arquivo .ftr contendo os dados dos clientes
3. O sistema processará os dados e disponibilizará download dos resultados

### Simulação Individual
1. Acesse a aba "Simulador"
2. Preencha os dados do cliente:
   - Informações pessoais (sexo, idade, estado civil)
   - Situação financeira (renda, tipo de renda, posses)
   - Características residenciais
3. Clique em "Calcular Score" para obter o resultado

## Variáveis do Modelo

O modelo utiliza as seguintes variáveis para cálculo do score:
- Sexo
- Posse de veículo e imóvel
- Quantidade de filhos
- Tipo de renda
- Educação
- Estado civil
- Idade
- Tempo de emprego
- Quantidade de pessoas na residência
- Renda
- Categoria de residência

## Tecnologias Utilizadas

- **Streamlit** - Framework para aplicações web
- **PyCaret** - Biblioteca para machine learning
- **Pandas** - Manipulação de dados
- **XlsxWriter** - Geração de arquivos Excel
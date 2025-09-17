# Desafio-Ray
O desafio foi elaborado com o intuito de criar um dashboard interativo para análise de vídeos da Fórmula 1 2024, utilizando a API do YouTube para extrair e visualizar dados de uma playlist específica.

## Funcionalidades
-> Coleta de dados automática da API do YouTube

-> Dashboard interativo com métricas de visualizações, curtidas e comentários

-> Filtros por data e número de visualizações

-> Rankings dos vídeos mais populares

-> Gráficos interativos da evolução das visualizações

## Decisões Técnicas
Dois arquivos foram criados, um destinado diretamente para os códigos que suportar a aplicação da API e outro constituído pela interface. Além disso, foi implementado o @st.cache_data para evitar chamadas desnecessárias à API e melhorar performance, assim como diversos tratamentos de erro, incluindo validações para situações onde a API não consegue retornar dados esperados.

## Desafios Enfrentados
De primeira instância, achar uma biblioteca que atendesse meus requisitos pessoais foi um grande desafio. Pois do mesmo modo que eu gostaria de implementar um front-end composto pelo dashboard em python, queria que conseguisse lidar com toda a coleta e organização dos dados do back-end.

Com isso, o Streamlit foi a melhor opção, porque mesmo havendo certo atraso na hora da instalação das dependências, me permitiu construir toda a aplicação usando apenas Python, sem ter que ficar pulando entre várias tecnologias, tornando o processo bem mais rápido e direto.

## Técnologias Utilizadas
-> Streamlit: Framework escolhido por sua simplicidade para criar dashboards interativos rapidamente

-> Plotly Express: Para gráficos interativos e visualmente atraentes

-> Pandas: Manipulação e transformação eficiente dos dados

-> Google API Client: Cliente oficial para integração com APIs do Google

## Autor do projeto
- Caio Lima - clb@cesar.school / caiolbezerra2005@gmail.com

## Como executar o projeto
- Clone o repositório
- Instale: pip install -r requirements.txt
- Execute: streamlit run app_streamlit.py
  

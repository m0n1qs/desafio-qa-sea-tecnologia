# Plano de Testes — SEA Tecnologia

## 1. Identificação do projeto

| Informação | Descrição |

| Projeto | Desafio QA — SEA Tecnologia |

| Aplicação | Sistema de cadastro e consulta de trabalhadores |

| Tipo de aplicação | Interface Web e API REST |

| Responsável | Monique |

## 2. Objetivo

Definir a estratégia e os critérios para testar a aplicação de cadastro e consulta de trabalhadores da SEA Tecnologia, avaliando o funcionamento dos principais fluxos, a validação dos dados, a consistência entre interface e API e aspectos relacionados à segurança e privacidade.

O objetivo também é identificar e documentar defeitos, avaliar riscos e implementar testes automatizados que contribuam para a verificação da qualidade da aplicação.

## 3. Aplicação e ambiente de teste

| Item | Configuração |

| Aplicação Web | https://analista-teste.seatecnologia.com.br/ |

| API REST | https://analista-teste.seatecnologia.com.br/employees |

| Navegador | Google Chrome / Chromium |

| Linguagem | Python |

| Framework de testes | pytest |

| Automação Web | Playwright |

| Automação de API | Requests |

| Especificação de cenários | Gherkin |


Os testes manuais foram realizados por meio da interface da aplicação e de ferramentas de exploração de API. Os testes automatizados foram desenvolvidos em Python, utilizando pytest, Playwright e Requests.

## 4. Escopo dos testes

### 4.1. Funcionalidades contempladas

**Cadastro de trabalhadores**
- Verificar a apresentação, o preenchimento e a obrigatoriedade dos campos.
- Validar CPF e demais dados pessoais.
- Verificar datas de nascimento, incluindo datas passadas, inválidas e futuras.
- Validar o cadastro de trabalhadores ativos e inativos.
- Verificar os campos de cargo, atividade, EPI e número do CA.
- Validar a opção de trabalhador que não utiliza EPI.
- Verificar o envio de anexo de ASO.
- Testar a inclusão de múltiplas atividades e EPIs.
- Verificar o salvamento e a consistência das informações cadastradas.

**Listagem e consulta**
- Verificar a apresentação dos trabalhadores cadastrados.
- Validar a identificação de trabalhadores ativos e inativos.
- Verificar os filtros por situação e a opção de limpar filtros.
- Avaliar a rolagem, a paginação e a navegação da listagem.
- Verificar a seleção e a possibilidade de edição de registros existentes.
- Comparar as informações exibidas na interface com os dados retornados pela API.

**API REST**
- Validar as requisições GET, HEAD e OPTIONS.
- Verificar o status HTTP, os cabeçalhos e a estrutura das respostas.
- Avaliar o acesso aos dados sem credenciais.
- Verificar a exposição de dados pessoais e aspectos de privacidade.
- Testar a criação de trabalhadores por POST.
- Avaliar as operações de atualização por PUT e PATCH.
- Verificar a possibilidade de exclusão por DELETE.
- Confirmar alterações por meio de consultas GET posteriores.
- Comparar os dados e totais retornados pela API com as informações da interface.

### 4.2. Fora do escopo ou com cobertura limitada

- Testes de carga, estresse e desempenho em larga escala.
- Testes de compatibilidade em diferentes navegadores e dispositivos.
- Testes de infraestrutura e configuração interna do servidor.
- Operações destrutivas ou alterações em registros reais sem autorização e ambiente isolado.
- Validações que dependam de regras de negócio ou contratos técnicos não documentados.

Esses pontos não foram priorizados devido ao escopo e ao tempo disponíveis para a execução do desafio.


## 5. Dados de teste

Foram utilizados dados fictícios para os cadastros e as verificações, evitando o uso desnecessário de informações pessoais reais.

Os dados foram selecionados para contemplar diferentes condições, como:

- Trabalhadores ativos e inativos.
- Campos preenchidos e não preenchidos.
- Dados válidos e inválidos.
- Diferentes datas de nascimento.
- Diferentes cargos e atividades.
- Condições relacionadas ao uso de EPI.
- Campos numéricos e entradas de texto.

## 6. Riscos, premissas e limitações

Durante o planejamento, foram considerados os seguintes pontos:

- Ausência de documentação detalhada das regras de negócio e do contrato da API.
- Possibilidade de comportamentos não especificados serem interpretados de maneiras diferentes.
- Ambiente compartilhado, que exige cuidado com operações de criação, atualização e exclusão.
- Ausência de credenciais ou informações sobre mecanismos de autenticação.
- Necessidade de confirmar regra de negócio.

Quando não houver um critério documentado, o comportamento observado será registrado como dúvida, observação ou oportunidade de melhoria, evitando classificações sem evidência suficiente.

## 7. Entregáveis

Ao final da atividade, serão disponibilizados:

- Plano de testes.
- Cenários de teste em Gherkin.
- Código-fonte dos testes automatizados.
- Evidências das execuções.
- Relatório de execução dos testes.
- Relatório de defeitos identificados.
- Registro de dúvidas, limitações e oportunidades de melhoria.
- Diário de utilização de IA, quando aplicável.

## 8. Considerações finais

Este plano estabelece a abordagem utilizada para avaliar a qualidade da aplicação, considerando os principais fluxos funcionais, a comunicação entre interface e API, a integridade dos dados e aspectos de segurança e privacidade.

A execução dos testes seguirá as prioridades definidas, respeitando as limitações do ambiente e os critérios disponíveis. Comportamentos sem especificação serão registrados para esclarecimento, evitando assumir regras que não foram formalmente estabelecidas.

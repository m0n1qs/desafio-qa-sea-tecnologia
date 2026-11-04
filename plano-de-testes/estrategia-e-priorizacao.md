## Estratégia de testes

Foram utilizadas as seguintes abordagens:

-Testes manuais e exploratórios: investigação dos fluxos de cadastro, listagem, filtros, validações e comportamentos da aplicação.

-Testes de interface: automação com Python, pytest e Playwright.

-Testes de API: utilização de Requests para verificar requisiçõe-, respostas e operações de consulta e atualização.

-Testes de consistência: comparação dos dados apresentados na interface com os retornados pela API.

-Validação de persistência: realização de GET após operações de gravação para conferir os dados efetivamente armazenados.

-Registro de evidências: capturas organizadas por cenário, com resultados e informações necessárias para reprodução.


## Priorização dos testes

A prioridade foi definida considerando o impacto de cada problema sobre os dados e os principais fluxos da aplicação.

| Prioridade        | Área                      | Testes e pontos de atenção                                                                                                                                                                                                     

| P1 – Alta         | Integridade dos dados     | CT-012 / BUG-008: divergência na opção de não utilização de EPI; CT-005 e CT-006 / BUG-006 e BUG-007: validação de datas; CT-015 / BUG-009: interrupção do cadastro ao adicionar atividade; consistência dos dados persistidos. |

| P1 – Alta         | Segurança e privacidade   | Acesso à API sem credenciais e exposição de dados pessoais.                                                                                                                                                                     |
| P2 – Média        | Consulta e listagem       | Cadastro de trabalhadores ativos e inativos, comparação entre interface e API, rolagem, paginação e identificação de registros.                                                                                                 |

| P2 – Média        | Gestão de trabalhadores   | Possibilidade de selecionar e editar registros, melhorar os filtros e disponibilizar consulta exclusiva de inativos.                                                                                                            |

| P3 – Complementar | Atividades, EPIs e anexos | Inclusão de múltiplas atividades e EPIs, associação com CA e persistência de anexos de ASO.                                                                                                                                     |

| P3 – Complementar | Validações e usabilidade  | Formatos numéricos, limites de texto, mensagens de erro, rótulos e estados dos controles.                                                                                                                                       |

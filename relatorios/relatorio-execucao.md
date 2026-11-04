# Relatório de Execução de Testes — SEA Tecnologia

## 1. Informações do projeto

| Informação | Valor |
| Projeto | SEA Tecnologia |
| Sistema operacional | Windows |
| Navegador de automação | Chromium |
| Linguagem | Python |
| Framework | pytest |
| Automação web | Playwright |
| Testes de API | Requests |
| Evidências | PDFs por cenário em `evidences/` |

## 2. Escopo e situação da execução

O inventário documentado contém 33 cenários: 20 automatizados e 13 manuais. 

| Resultado confirmado | Cenários |
| Aprovados | CT-002, CT-003, CT-007, CT-008, CT-013, CT-020, CT-026, CT-028, CT-030, CT-031, CT-032 e CT-033 |
| Reprovados por comportamento observado | CT-005, CT-006, CT-012 e CT-015 |
| Sem resultado final consolidado neste relatório | CT-001, CT-017, CT-018 e CT-019 |

- CT-030: PUT atualizou cargo e atividade com os valores de 01 a 05; cada alteração foi conferida por GET.
- CT-031: PATCH atualizou cargo e atividade com os valores de 01 a 05; cada valor enviado foi conferido por GET.
- CT-032: PATCH definiu `usesEpi=true`, confirmado por GET.
- CT-033: PATCH definiu `usesEpi=false`, confirmado por GET.

O comportamento dos campos não enviados nas requisições PATCH foi registrado como observação, e não como falha, pois não há documentação que especifique se esses campos devem ser preservados ou omitidos após a atualização.

## 3. Resultados dos cenários automatizados

| ID | Resultado | Resultado observado / evidência |
| CT-001 | Aprovado | PDF disponível em [CT001](../evidences/prints/automatizados/CT001.pdf). |
| CT-002 | Aprovado | Campos obrigatórios impediram o envio vazio. [Evidência](../evidences/prints/automatizados/CT002.pdf). |
| CT-003 | Aprovado | CPF com caracteres inválidos foi rejeitado pela validação do campo. [Evidência](../evidences/prints/automatizados/CT003.pdf). |
| CT-005 | Reprovado | A aplicação aceitou a data `0001-01-01` e concluiu o cadastro. [BUG-006](./relatorio-de-bug.md). [Evidência](../evidences/prints/automatizados/CT005.pdf). |
| CT-006 | Reprovado | A aplicação aceitou uma data de nascimento futura e concluiu o cadastro. [BUG-007](./relatorio-de-bug.md). [Evidência](../evidences/prints/automatizados/CT006.pdf). |
| CT-007 | Aprovado | Cadastro ativo localizado pela API e exibido ao ativar “Ver apenas ativos”. [Evidência](../evidences/prints/automatizados/CT007.pdf). |
| CT-008 | Aprovado | Cadastro inativo confirmado pela API; oculto com filtro de ativos e exibido ao limpar o filtro. [Evidência](../evidences/prints/automatizados/CT008.pdf). |
| CT-012 | Reprovado | A interface foi marcada como sem EPI, mas a API retornou `usesEpi=true`. [BUG-008](./relatorio-de-bug.md). [Evidência](../evidences/prints/automatizados/CT012.pdf). |
| CT-013 | Aprovado | O formulário bloqueou o salvamento sem número de CA. [Evidência](../evidences/prints/automatizados/CT013.pdf). |
| CT-015 | Reprovado | Após clicar “Adicionar outra atividade”, a tela retornou à listagem e os dados do formulário deixaram de estar disponíveis. [BUG-009](./relatorio-de-bug.md). [Evidência](../evidences/prints/automatizados/CT015.pdf). |
| CT-017 | Aprovado | PDF disponível em [CT017](../evidences/prints/automatizados/CT017.pdf). |
| CT-018 | Aprovado | PDF de API disponível em [CT018](../evidences/api/automatizados/CT018.pdf). |
| CT-019 | Aprovado | PDF de API disponível em [CT019](../evidences/api/automatizados/CT019.pdf). |
| CT-020 | Aprovado | OPTIONS retornou status não 5xx e cabeçalhos CORS/métodos para análise. O valor observado `Access-Control-Allow-Origin: *,*` é inválido, registrado como BUG-002 da API. [Evidência](../evidences/api/automatizados/CT020.pdf). |
| CT-026 | Aprovado | Totais de trabalhadores e ativos da listagem comparados com GET da API. A captura expandida da interface está no PDF. [Evidência](../evidences/api/automatizados/CT026.pdf). |
| CT-028 | Aprovado | Total de inativos inferido a partir da listagem completa e do resumo de ativos comparado com `isActive=false` no GET. Não equivale a exibir ou filtrar individualmente os inativos. [Evidência](../evidences/api/automatizados/CT028.pdf). |
| CT-030 | Aprovado | PUT de cargo e atividade para os valores 01–05, confirmado por GET. Registro fictício mantido. [Evidência](../evidences/api/automatizados/CT030.pdf). |
| CT-031 | Aprovado | PATCH de cargo e atividade para os valores 01–05, confirmado por GET. Registro fictício mantido. [Evidência](../evidences/api/automatizados/CT031.pdf). |
| CT-032 | Aprovado | PATCH `usesEpi=true`, confirmado por GET. Registro fictício mantido. [Evidência](../evidences/api/automatizados/CT032.pdf). |
| CT-033 | Aprovado | PATCH `usesEpi=false`, confirmado por GET. Registro fictício mantido. [Evidência](../evidences/api/automatizados/CT033.pdf). |

## 4. Cenários manuais e investigação exploratória

| ID / área | Resultado observado |
| CT-004 — CPF duplicado | Foi observado cadastro com CPF repetido, mas a regra que define se CPF deve ser único não está documentada. Confirmar com a área de negócio antes de tratar a expectativa de rejeição como requisito. |
| CT-010 — Múltiplas atividades | O fluxo para adicionar outra atividade apresentou falha; relacionado ao comportamento reproduzido em CT-015 e ao BUG-001/BUG-009. |
| CT-011 — Múltiplos EPIs | Na exploração manual, selecionar outro tipo de EPI recarregou a tela e voltou a mostrar a primeira seleção. A inclusão de vários EPIs continua sendo uma melhoria a confirmar e investigar. |
| CT-014 — | Foi possível anexar durante o cadastro, mas não foi possível confirmar a persistência após salvar. |
| CT-016 — Dados da listagem | Foram observadas inconsistências na exibição de CPF, cargo e atividade entre registros (BUG-004). |
| CT-021/CT-022 — API sem credenciais | GET retornou dados pessoais sem autenticação. O comportamento e os controles de acesso precisam de avaliação; ver relatório de bugs. |
| CT-023 — POST | Foi observado HTTP 201 e um ID na resposta. A execução automatizada posterior também usou POST para criar massas fictícias e consultá-las por ID. |
| CT-024/CT-025 — Edição/exclusão pela interface | Não foi identificada uma ação acessível para selecionar e editar ou excluir um trabalhador existente pela interface. |
| CT-027 — Rolagem | A listagem não permitiu rolar para alcançar todos os registros (BUG-005). |
| Campos numéricos e limites de texto | Durante a exploração, foram realizados testes com caracteres não numéricos em campos que aparentam aceitar apenas números (como CPF e RG), além de entradas com textos muito longos. Essas verificações foram exploratórias e não foram formalizadas como cenários de teste nem registradas como defeitos.

## 5. Comportamento e oportunidade de melhoria da listagem

O botão mantém o rótulo **“Ver apenas ativos”** tanto quando o filtro está desativado quanto quando está ativado:

- **Filtro desativado:** a listagem não possui filtro por situação e pode exibir trabalhadores ativos e inativos.
- **Filtro ativado:** a listagem exibe somente trabalhadores ativos, e o botão recebe a classe visual `isActive`.
- **Limpar filtros:** remove o filtro aplicado e restaura a listagem completa.

A permanência do mesmo rótulo nos dois estados pode gerar ambiguidade, pois o texto descreve uma ação, mas não informa claramente se o filtro já está aplicado. Além disso, a interface não oferece uma opção equivalente para visualizar somente os trabalhadores inativos.

O **CT-028** compara a quantidade de trabalhadores inativos, inferida a partir dos dados da listagem, com o resultado retornado pela API. Essa verificação não comprova quais trabalhadores inativos são exibidos individualmente na interface.

**Recomendação:** tornar o estado do filtro mais explícito e disponibilizar opções claras para visualizar todos os trabalhadores, somente os ativos ou somente os inativos, com contadores correspondentes e navegação funcional.

## 6. Bugs registrados e questões a confirmar

Os bugs reproduzidos estão detalhados em [relatorio-de-bug.md](./relatorio-de-bug.md). Entre eles estão os problemas de CPF duplicado (BUG-002), datas aceitas (BUG-006/007), EPI divergente (BUG-008), atividade interrompendo o cadastro (BUG-009) e rolagem da listagem (BUG-005).

**Atenção à regra de CPF:** apesar de o comportamento de aceitar duplicados ter sido observado e registrado, não existe documentação confirmando se a regra é um CPF por trabalhador. A expectativa de bloqueio deve ser validada com o responsável pelo produto.

**Observação sobre autenticação:** a API retorna informações sobre métodos HTTP e configurações CORS sem exigir autenticação. Embora isso seja esperado para OPTIONS, a divulgação dessas informações merece atenção. O cabeçalho Access-Control-Allow-Origin: *,* também apresenta uma configuração incomum.

## 7. Considerações finais

Foram testados fluxos importantes da aplicação, como validação de dados, criação de trabalhadores ativos e inativos, comparação entre interface e API e atualização de informações por PUT/PATCH. Também foram identificados problemas relacionados a datas, sincronização de EPI e adição de atividades.

Apesar de a quantidade de trabalhadores inativos ter sido conferida por meio da API, seria interessante melhorar a interface para permitir que esses trabalhadores sejam encontrados e visualizados com mais facilidade.

Como sugestões de melhoria, seria importante esclarecer algumas regras de negócio, principalmente sobre a validação e a unicidade do CPF, o comportamento dos campos não enviados em requisições PATCH, os limites de preenchimento e o cadastro de múltiplas atividades e EPIs.

Também seria interessante corrigir as falhas identificadas, permitir a edição de trabalhadores diretamente pela interface, melhorar os filtros e a listagem e definir melhor os critérios de validação dos campos numéricos e dos limites de texto.

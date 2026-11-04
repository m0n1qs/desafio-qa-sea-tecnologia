## BUG-001[Desktop][Chrome] - Não é possível cadastrar mais de uma atividade

**Cenário Associado:** CT-010 - Adicionar múltiplas atividades 

**Descrição:**
Ao tentar cadastrar mais de uma atividade, sistema direciona usuário para página de listagem de funcionários, não permitindo concluir cadastro de funcionário com mais de uma atividade

**Passos para reprodução:**

**1.** Preencha campos obrigatórios para cadastro de funcionário 

**2.** Clique em adicionar outra atividade atividade

**Resultado esperado:**

O sistema direciona usuário para tela de listagem de funcionário

**Resultado real:**

O sistema deve exibir novo campo de atividade e permitir que salv cadastro de funcionário com mais de uma atividade

**Evidência:** 

[Abrir PDF enviado originalmente como CT-010](../evidences/prints/CT-010_evidencia.pdf)


## BUG-002[Desktop][Chrome] - Sistema permite cadastrar funcionário com mesmo CPF

**Cenário Associado:** CT-004 - Impedir CPF duplicado

**Descrição:**

Sistema permite cadastrar funcionários com mesmo cpf

**Passos para reprodução:**

**1.** Faça o cadastro de um funcionário e salve

**2.** Faça cadastro de outro funcionário com o mesmo CPF

**3.** Salve funcionário

**Resultado esperado:**

O sistema permite cadastrar mais de um funcionário com o mesmo CPF

**Resultado real:**

O sistema não dee permitir cadastro de funcionário com cpf já cadastrado

**Evidência:** 
[Abrir PDF enviado originalmente como CT-004](../evidences/prints/CT-004_evidencia.pdf)


## BUG-003[Desktop][Chrome] - Nada acontece ao registrar clicar no botão Adicionar EPI

**Cenário Associado:** CT-011 - Adicionar múltiplos EPIs 

**Descrição:**

Nada acontece ao tetnar cadastrar mais de um EPI

**Passos para reprodução:**

**1.** Preencha campos obrigatórios para cadastro de funcionário 

**2.** Preencha campos de EPI

**3.** Clique em "Adiconar EPI"

**Resultado esperado:**

Nada acontece

**Resultado real:**

Sistema exibe novo campo paraselecionar e preencher CA de EPI e permite salvar dados do cadastro com m´lutimplos EPI's

**Evidência:** 
[Abrir PDF enviado originalmente como CT-011](../evidences/prints/CT-011_evidencia.pdf)

## BUG-004[Desktop][Chrome] - Dados como cpf, atividade e cargo não são exibidos corretamente na listagem de funcionários 

**Cenário Associado:** CT-016 - Verificar exposição de dados na listagem

**Descrição:**

Funcionário cadastrado é exibido na listagem alguns com exbição de cpf apenas, outros com cpf, cargo e atividade. Todos os funcionários na listagem devem ser exibidos com cpf, cargo e atividade

**Passos para reprodução:**

**1.** Preencha campos obrigatórios para cadastro de funcionário, com cargo e atividade

**2.** Salve cadastro

**Resultado esperado:**

Listagem de funcionários ativos ou inativos exibe alguns funcionários com dados de cpf, cargo e atividade, outros funcioários exibe apenas cpf

**Resultado real:**

Sistema deve exibir dados de cpf, cargo e atividade para todos os funcionários cadastrados

**Evidência:** 
[Abrir PDF enviado originalmente como CT-016](../evidences/prints/CT-016_evidencia.pdf)

### BUG-005[Desktop][Chrome] - Impossibilidade de rolar a listagem de funcionários

**Cenário Associado:** CT-027 - Verificar navegação e rolagem da listagem de funcionários

**Descrição:** Acessar a listagem com quantidade de funcionários superior ao espaço disponível na tela.

**Passos para reprodução:**

**1.** Acessar a tela de listagem de funcionários

**2.** Tentar rolar a tela para visualizar todos os funcionários cadastrados

**Resultado esperado:**

A listagem deve permitir a rolagem da tela ou disponibilizar outra forma de navegação, como paginação, para visualizar todos os funcionários.

**Resultado obtido:**

A listagem apresenta uma quantidade de registros superior ao espaço visível, porém não permite rolar a tela para visualizar os demais funcionários.

**Evidência:** [Abrir PDF enviado originalmente como CT-027](../evidences/prints/CT-027_evidencia.pdf)

### BUG-006[Desktop][Chrome] - Sistema permite salvar cadastro com data de nascimento inválida

**Cenário Associado:** CT-005 - Validar data de nascimento inválida

**Descrição:** Ao inserir data de nascimento inválida após preencher todos os campos obrigatórios, sistema permite salvar cadastro de funcionário

**Passos para reprodução:**

**1.** Preencha todos os campos obrigatórios

**2.** Na data de nascimento inisira 01/01/0001

**3.** Clique em Salvar

**Resultado esperado:**

Sistema deve informar que formato da data não é permitido e deve bloquear ação de salvar

**Resultado obtido:**

Sistema permite salvar cadastro de usuário com data inválida

**Evidência:** [Abrir PDF enviado originalmente como CT-005](../evidences/prints/CT-005.pdf)


### BUG-007[Desktop][Chrome] - Sistema permite salvar cadastro com data de nascimento inválida

**Cenário Associado:** CT-006 - Validar data de nascimento futura

**Descrição:** Ao inserir data de nascimento inválida após preencher todos os campos obrigatórios, sistema permite salvar cadastro de funcionário

**Passos para reprodução:**

**1.** Preencha todos os campos obrigatórios

**2.** Na data de nascimento inisira 01/01/0001

**3.** Clique em Salvar

**Resultado esperado:**

Sistema deve informar que formato da data não é permitido e deve bloquear ação de salvar

**Resultado obtido:**

Sistema permite salvar cadastro de usuário com data inválida

**Evidência:** [Abrir PDF enviado originalmente como CT-006](../evidences/prints/CT-006.pdf)

## BUG-008[Desktop][Chrome] - Cadastro marcado como sem EPI é salvo como usesEpi=true

**Cenário Associado:** CT-012 - Cadastrar trabalhador sem EPI

**Descrição:**

Ao marcar a opção indicando que o trabalhador não usa EPI e salvar o cadastro, a API retorna `usesEpi=true` para o trabalhador criado.

**Passos para reprodução:**

**1.** Acesse o formulário de cadastro de trabalhador.

**2.** Preencha os campos obrigatórios.

**3.** Marque a opção “O trabalhador não usa EPI”.

**4.** Salve o cadastro e consulte o registro correspondente na API.

**Resultado esperado:**

O cadastro deve refletir a opção selecionada de não utilização de EPI.

**Resultado obtido:**

A automação confirmou que a opção “O trabalhador não usa EPI” foi marcada. Após salvar, consultou o trabalhador pela API e recebeu `usesEpi=true`; por essa divergência, o cenário falhou.

**Impacto:**

O cadastro armazenado não corresponde à opção selecionada na interface, podendo levar consumidores da API a interpretar incorretamente a utilização de EPI.

**Evidência:** [Abrir PDF do CT-012](../evidences/prints/automatizados/CT012.pdf)

## BUG-009[Desktop][Chrome] - Botão de adicionar atividade interrompe o cadastro

**Cenário Associado:** CT-015 - Adicionar atividade sem perder dados

**Descrição:**

Ao clicar em “Adicionar outra atividade” durante o preenchimento do cadastro, a aplicação sai do formulário e volta à listagem. A automação não encontra mais os campos de CA para verificar a preservação dos dados.

**Passos para reprodução:**

**1.** Inicie o cadastro de um trabalhador e preencha os dados básicos e a primeira atividade.

**2.** Role até o botão “Adicionar outra atividade”.

**3.** Clique no botão.

**Resultado esperado:**

O formulário deve apresentar um novo conjunto de campos para adicionar outra atividade, mantendo os dados da primeira atividade e do cadastro.

**Resultado obtido:**

Após o clique, a tela retorna à listagem; os campos do formulário, incluindo o CA da primeira atividade, deixam de estar disponíveis. A automação falha ao tentar confirmar que os dados foram preservados.

**Impacto:**

Não é possível adicionar uma atividade adicional pelo fluxo testado, e o usuário pode perder o progresso do cadastro.

**Evidência:** [Abrir PDF do CT-015](../evidences/prints/automatizados/CT015.pdf)


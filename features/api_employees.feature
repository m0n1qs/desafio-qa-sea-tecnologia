# language: en

@api @employees
Feature: API de trabalhadores

  Como consumidor da API
  Quero consultar e comparar trabalhadores
  Para verificar contrato, segurança e consistência

  @CT018 @automatizado @api
  Scenario: CT-018 - Consultar trabalhadores com GET
    When envio GET para "/employees"
    Then recebo HTTP 200 e uma lista JSON de trabalhadores

  @CT019 @automatizado @api
  Scenario: CT-019 - Consultar cabeçalhos com HEAD
    When envio HEAD para "/employees"
    Then recebo uma resposta válida sem corpo

  @CT020 @automatizado @api
  Scenario: CT-020 - Consultar métodos com OPTIONS
    When envio OPTIONS para "/employees"
    Then a API deve retornar um status HTTP válido
    And devo identificar os métodos HTTP anunciados
    And devo identificar os cabeçalhos CORS retornados

  @CT021 @manual @api
  Scenario: CT-021 - Avaliar dados pessoais retornados
    When consulto "/employees" sem credenciais
    Then identifico os campos pessoais retornados
    And avalio sua necessidade e exposição

  @CT022 @manual @api
  Scenario: CT-022 - Verificar acesso sem credenciais
    When consulto "/employees" sem credenciais
    Then verifico se a API exige autenticação

  @CT023 @manual @api
  Scenario: CT-023 - Criar trabalhador com POST
    Given que tenho autorização e ambiente isolado
    When crio um trabalhador fictício com POST
    Then verifico a resposta e a persistência do cadastro

  @CT024 @manual @api
  Scenario: CT-024 - Atualizar trabalhador com PUT 
    Given que tenho um funcionário cadastrado
    When atualizo o registro com PUT 
    Then verifico os campos alterados e preservados

  @CT025 @manual @api
  Scenario: CT-025 - Excluir trabalhador com DELETE
    Given que tenho um funcionário cadastrado
    When excluo o registro com DELETE
    Then verifico a resposta e a remoção do registro

  @CT026 @automatizado @api
  Scenario: CT-026 - Comparar interface com API
    When consulto o resumo da listagem e a resposta GET
    Then os totais de trabalhadores e ativos devem ser iguais

  @CT028 @automatizado @api
  Scenario: CT-028 - Comparar total de inativos inferido com API
    Given que a interface não oferece um filtro exclusivo para inativos
    When calculo os inativos pela listagem completa e consulto o GET
    Then o total inferido deve coincidir com registros isActive false na API

@CT029 @manual @api
  Scenario: CT-029 - Atualizar trabalhador com PATCH 
    Given que tenho um funcionário cadastrado
    When atualizo o registro com PATCH 
    Then verifico os campos alterados e preservados

  @CT030 @automatizado @api
  Scenario: CT-030 - Atualizar cargo e atividade com PUT
    Given que o cenário cria um trabalhador fictício via POST e guarda o ID retornado
    When atualizo o cargo e a atividade pelos valores de 1 a 5 com PUT
    Then verifico cada valor persistido na resposta GET
   

  @CT031 @automatizado @api
  Scenario: CT-031 - Atualizar cargo e atividade com PATCH
    Given que o cenário cria um trabalhador fictício via POST e guarda o ID retornado
    When atualizo parcialmente o cargo e a atividade pelos valores de 1 a 5
    Then verifico cada valor enviado pela resposta GET
    

  @CT032 @automatizado @api
  Scenario: CT-032 - Habilitar uso de EPI com PATCH
    Given que o cenário cria um trabalhador fictício sem EPI e guarda o ID retornado
    When altero usesEpi para true com PATCH
    Then a resposta GET deve apresentar usesEpi true
    

  @CT033 @automatizado @api
  Scenario: CT-033 - Desabilitar uso de EPI com PATCH
    Given que o cenário cria um trabalhador fictício com EPI e guarda o ID retornado
    When altero usesEpi para false com PATCH
    Then a resposta GET deve apresentar usesEpi false
    

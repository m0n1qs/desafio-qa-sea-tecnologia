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
    Then verifico os métodos e os cabeçalhos CORS retornados

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
  Scenario: CT-024 - Atualizar trabalhador com PUT ou PATCH
    Given que tenho autorização e um registro fictício isolado
    When atualizo o registro com PUT ou PATCH
    Then verifico os campos alterados e preservados

  @CT025 @manual @api
  Scenario: CT-025 - Excluir trabalhador com DELETE
    Given que tenho autorização e um registro fictício isolado
    When excluo o registro com DELETE
    Then verifico a resposta e a remoção do registro

  @CT026 @automatizado @api
  Scenario: CT-026 - Comparar interface com API
    When consulto o resumo da listagem e a resposta GET
    Then os totais de trabalhadores e ativos devem ser iguais

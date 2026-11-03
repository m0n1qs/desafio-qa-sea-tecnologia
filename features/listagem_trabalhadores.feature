# language: en

@web @listagem
Feature: Listagem de trabalhadores

  Como usuário da aplicação
  Quero consultar os trabalhadores cadastrados
  Para conferir os dados e a situação

  @CT016 @manual @web
  Scenario: CT-016 - Verificar exposição de dados na listagem
    Given que acesso a listagem
    Then funcioários são exibidos com nome e dados de cpf, atividade e cargo

  @CT017 @automatizado @web
  Scenario: CT-017 - Identificar trabalhadores ativos e inativos
    Given que existem trabalhadores ativos e inativos
    When uso o filtro de situação da listagem
    Then consigo distinguir os trabalhadores por situação

  @CT027 @manual @web
  Scenario: CT-027 - Verificar navegação e rolagem da listagem de funcionários
  Given que acesso a listagem de funcionários
  When a lista apresenta mais registros do que o espaço visível na tela
  Then devo conseguir rolar a tela para visualizar os demais funcionários
  And devo conseguir acessar os registros exibidos na listagem


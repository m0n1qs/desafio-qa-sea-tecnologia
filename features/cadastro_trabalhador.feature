# language: en

@web @cadastro
Feature: Cadastro de trabalhadores

  Como responsável pelo cadastro
  Quero cadastrar trabalhadores e seus EPIs
  Para manter informações de segurança do trabalho

  @CT001 @automatizado @web
  Scenario: CT-001 - Exibir campos do cadastro
    Given que abro o formulário de cadastro
    Then vejo os campos pessoais, cargo, atividade, EPI, CA e atestado

  @CT002 @automatizado @web
  Scenario: CT-002 - Validar campos obrigatórios
    Given que abro o formulário sem preencher dados
    Then os campos obrigatórios devem impedir o envio do formulário

  @CT003 @automatizado @web
  Scenario: CT-003 - Validar CPF inválido
    Given que informo um CPF inválido
    When tento validar o cadastro
    Then o sistema deve rejeitar o CPF

  @CT004 @manual @web
  Scenario: CT-004 - Impedir CPF duplicado
    Given que já existe um trabalhador com o CPF de teste
    When tento cadastrar outro trabalhador com o mesmo CPF
    Then o sistema deve informar que o CPF já está cadastrado

  @CT005 @automatizado @web
  Scenario: CT-005 - Validar data de nascimento inválida
    Given que informo uma data de nascimento inexistente
    Then o sistema deve rejeitar a data

  @CT006 @automatizado @web
  Scenario: CT-006 - Validar data de nascimento futura
    Given que informo uma data de nascimento futura
    Then o sistema deve aplicar a regra de validação de data

  @CT007 @automatizado @web
  Scenario: CT-007 - Cadastrar trabalhador ativo
    Given que preencho campos obrigatórios para cadastro de funcionário
    When cadastro o trabalhador como ativo
    Then ele deve aparecer na listagem como ativo

  @CT008 @automatizado @web
  Scenario: CT-008 - Cadastrar trabalhador inativo
    Given que preencho campos obrigatórios para cadastro de funcionário
    When cadastro o trabalhador como inativo
    Then ele deve aparecer na listagem como inativo

  @CT009 @manual @web
  Scenario: CT-009 - Cadastrar atividade e EPI e CA
    Given preencho todos os campos obrigatórios para cadastro 
    When cadastro uma atividade, um EPI e seu CA
    Then a listagem deve apresentar os dados cadastrados

  @CT010 @manual @web
  Scenario: CT-010 - Adicionar múltiplas atividades
    Given preencho todos os campos obrigatórios para cadastro
    When adiciono duas atividades e seus EPIs
    Then as duas atividades devem ser mantidas no cadastro

  @CT011 @manual @web
  Scenario: CT-011 - Adicionar múltiplos EPIs
    Given que tenho dados fictícios autorizados para cadastro
    When associo mais de um EPI à atividade
    Then todos os EPIs e seus CAs devem ser mantidos

  @CT012 @automatizado @web
  Scenario: CT-012 - Cadastrar trabalhador sem EPI
    Given que abro o formulário de cadastro
    When marco que o trabalhador não utiliza EPI
    Then os campos de atividade e EPI devem ser ocultados ou desabilitados

  @CT013 @automatizado @web
  Scenario: CT-013 - Impedir EPI sem CA
    Given que seleciono um EPI e deixo o CA vazio
    Then o formulário deve indicar que o CA é obrigatório

  @CT014 @manual @web
  Scenario: CT-014 - Anexar atestado
    Given que tenho um arquivo de teste autorizado
    When anexo o atestado
    Then o sistema deve aceitar o formato permitido

  @CT015 @automatizado @web
  Scenario: CT-015 - Adicionar atividade sem perder dados anteriores
    Given que preenchi os dados de uma atividade
    When adiciono outra atividade
    Then os dados da primeira atividade devem permanecer preenchidos

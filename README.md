# Projeto de QA — Cadastro de Trabalhadores | SEA Tecnologia

Objetivo: avaliar a aplicação de cadastro de trabalhadores por meio de testes manuais, exploratórios e automatizados, verificando funcionalidades, regras de negócio, comunicação entre interface e API, integridade dos dados e aspectos de segurança e privacidade.

## 1. Aplicação e tecnologias

**Aplicação:** https://analista-teste.seatecnologia.com.br/
**API:** https://analista-teste.seatecnologia.com.br/employees

**Tecnologias e ferramentas utilizadas:**
- Python
- pytest
- Playwright
- Requests
- Gherkin
- Git e GitHub
- Visual Studio Code
- Hoppscotch

## 2. Escopo do projeto

A análise contempla:

- Testes funcionais e exploratórios da interface.
- Validação dos fluxos de cadastro de trabalhadores.
- Testes de API com diferentes métodos HTTP.
- Verificação da consistência dos dados entre interface e API.
- Testes automatizados com Python, pytest e Playwright.
- Análise de possíveis problemas relacionados à segurança e privacidade.
- Registro de defeitos, evidências e oportunidades de melhoria.

Os cenários foram organizados por identificadores, facilitando a rastreabilidade entre os testes, as evidências e os defeitos encontrados.

## 3. Configuração do ambiente

### Pré-requisitos

- Python 3.11 ou superior
- Git
- Visual Studio Code (recomendado)

Durante a instalação do Python, marque a opção `Add python.exe to PATH`, caso esteja disponível.

### Clonar o repositório

```bash
git clone https://github.com/m0n1qs/desafio-qa-sea-tecnologia.git
cd desafio-qa-sea-tecnologia
```

### Criar e ativar o ambiente virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Caso utilize o Prompt de Comando (CMD):

```cmd
.venv\Scripts\activate.bat
```

Se o PowerShell bloquear a ativação, execute:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Em seguida, tente ativar o ambiente novamente.

### Instalar as dependências

Com o ambiente virtual ativado:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Instalar o navegador do Playwright

```bash
python -m playwright install chromium
```

O Chromium é utilizado na execução dos testes automatizados de interface.

## 5. Execução dos testes

Os comandos devem ser executados na pasta raiz do projeto, com o ambiente virtual ativado.

**Executar todos os testes:**

```bash
python -m pytest -v
```

**Executar testes de interface:**

```bash
python -m pytest -m web
```

**Executar testes de API:**

```bash
python -m pytest -m api
```

**Executar testes de interface com o navegador visível:**

```bash
python -m pytest -m web --headed --slowmo 500 -v -s
```

**Executar um cenário específico:**

```bash
python -m pytest -k CT021 -v -s
```

**Visualizar os testes identificados pelo pytest:**

```bash
python -m pytest --collect-only -q
```

**Gerar relatório HTML de execução:**

```bash
python -m pytest --html=relatorios/relatorio-execucao.html --self-contained-html -v
```

O resultado também pode ser acompanhado diretamente pelo terminal.

## 6. Dúvidas e limitações identificadas

Durante a exploração, foram encontrados pontos sem documentação formal ou que precisam de confirmação da equipe responsável.

As principais dúvidas estão relacionadas a:

- Regras de obrigatoriedade, formatos e limites dos campos.
- Validação e unicidade do CPF.
- Regras para datas, atividades e associação de EPIs.
- Comportamento esperado da opção de não utilização de EPI.
- Formatos e limites para anexos de ASO.
- Métodos, rotas e contrato da API.
- Regras de autenticação e autorização.
- Comportamento esperado das operações PUT, PATCH e DELETE.
- Existência de ambiente isolado e procedimento de limpeza dos dados de teste.

Na ausência de requisitos ou documentação, os comportamentos observados foram registrados como ponto de investigação.

As limitações e os questionamentos identificados estão documentados nos materiais complementares do projeto.

## 7. Sugestões de melhoria

A partir da exploração da aplicação, foram identificadas oportunidades que podem contribuir para a qualidade e a usabilidade do sistema:

- Melhorar os filtros da listagem, permitindo consultar todos os trabalhadores, somente ativos ou somente inativos.
- Tornar mais clara a identificação do estado dos filtros.
- Corrigir problemas de rolagem e navegação na listagem.
- Disponibilizar opções para consultar e editar trabalhadores cadastrados.
- Melhorar o fluxo de inclusão de múltiplas atividades e EPIs.
- Garantir a consistência entre as informações exibidas na interface e os dados persistidos na API.
- Documentar as regras de negócio e o contrato dos endpoints da API.
- Definir critérios de validação para os campos e mensagens de erro.
- Revisar as configurações de CORS e garantir que operações de consulta, criação, alteração e exclusão tenham autenticação e autorização adequadas

Essas sugestões devem ser avaliadas e alinhadas aos requisitos esperados do produto.

## 8. Documentação complementar

Para consultar os detalhes da análise e dos resultados, estão disponíveis os seguintes documentos:

- [Plano de testes](./plano-de-testes/plano-de-testes.md) — objetivo, escopo, abordagem, critérios e condições de teste.
- [Estratégia e priorização](./plano-de-testes/estrategia-e-priorizacao.md) — prioridades, áreas de atenção e direcionamento dos testes.
- [Relatório de execução](./relatorios/relatorio-execucao.md) — cenários executados, resultados e evidências.
- [Relatório de bugs](./relatorios/relatorio-de-bug.md) — defeitos identificados e informações sobre sua reprodução.
- [Diário de utilização de IA](./AI_DIARY/) — registro da utilização de inteligência artificial durante o desenvolvimento do desafio.

## 9. Considerações finais

O projeto reúne atividades de testes manuais, exploratórios e automatizados, com foco na avaliação da qualidade da aplicação e na identificação de possíveis riscos.

Os resultados, defeitos, evidências, dúvidas de requisitos e sugestões de melhoria estão organizados nos documentos complementares, permitindo acompanhar a análise e consultar os detalhes de cada etapa.

A documentação também diferencia os comportamentos efetivamente reproduzidos daqueles que ainda dependem de confirmação dos requisitos.
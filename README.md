# Projeto de QA — Cadastro de Trabalhadores | SEA Tecnologia

O objetivo é avaliar a aplicação de cadastro de trabalhadores por meio de atividades de Quality Assurance, utilizando testes manuais, exploratórios e automatizados.

## 1. Objetivo do projeto

Avaliar a qualidade da aplicação, considerando seu funcionamento, suas regras de negócio, a comunicação entre interface e API e o tratamento das informações cadastradas.

O trabalho contempla atividades de testes funcionais, exploratórios, testes de API, automação e análise de segurança e privacidade, com registro das evidências e dos resultados obtidos.

## 2. Informações do projeto

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

## 3. Estrutura do projeto

```text
features/          Documentação em Gherkin
tests/             Scripts de testes automatizados e fixtures
plano-de-testes/   Plano de testes, estratégia e premissas
relatorios/        Relatórios de execução
evidences/         Evidências, capturas de tela e logs
diario-ia/         Diário de utilização de inteligência artificial
```

## 4. Configuração do ambiente

### Pré-requisitos

Para executar o projeto, é necessário ter instalado:

- Python 3.11 ou superior;
- Git;
- Visual Studio Code (recomendado).

Links para instalação:

- [Python](https://www.python.org/downloads/windows/)
- [Git](https://git-scm.com/downloads/win)
- [Visual Studio Code](https://code.visualstudio.com/Download)

Durante a instalação do Python, marque a opção `Add python.exe to PATH`, caso esteja disponível.

Para verificar as instalações, abra o terminal e execute:

```powershell
python --version
python -m pip --version
git --version
```

### Clonar o repositório

```bash
git clone https://github.com/m0n1qs/desafio-qa-sea-tecnologia.git
cd desafio-qa-sea-tecnologia
```

### Criar o ambiente virtual

No terminal, dentro da pasta do projeto, execute:

```powershell
python -m venv .venv
```

### Ativar o ambiente virtual

No PowerShell:

```powershell
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

Com o ambiente virtual ativado, execute:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Instalar o navegador do Playwright

```bash
python -m playwright install chromium
```

O Chromium é utilizado pelo Playwright para executar os testes automatizados de interface.

## 5. Como executar os testes

Todos os comandos devem ser executados no terminal, a partir da pasta raiz do projeto, com o ambiente virtual ativado.

### Executar todos os testes automatizados

```bash
python -m pytest -v
```

### Executar testes de interface

```bash
python -m pytest -m web
```

### Executar testes de API

```bash
python -m pytest -m api
```

### Executar os testes de interface com o navegador visível

```bash
python -m pytest -m web --headed --slowmo 500 -v -s
```

O parâmetro `--headed` permite acompanhar a execução no navegador, enquanto `--slowmo 500` adiciona um intervalo entre as ações para facilitar a visualização.

### Executar um teste específico

Para executar um teste individual, utilize o identificador correspondente com o parâmetro `-k`. Por exemplo:

```bash
python -m pytest -k CT021 -v -s
```

### Visualizar os testes identificados pelo pytest

```bash
python -m pytest --collect-only -q
```

### Gerar relatório HTML de execução

```bash
python -m pytest --html=relatorios/relatorio-execucao.html --self-contained-html -v
```

O resultado da execução também pode ser acompanhado diretamente pelo terminal.

## 6. Dúvidas de requisitos e ausência de documentação

Durante a análise da aplicação, foram identificados pontos que não possuem especificação formal disponível ou que precisam de confirmação sobre as regras de negócio esperadas.

As principais dúvidas estão relacionadas a:

- **Validações dos campos:** não há documentação detalhada sobre os formatos aceitos, obrigatoriedade e mensagens esperadas para os campos do cadastro.
- **Regras de negócio:** é necessário confirmar as regras para cadastro de trabalhadores ativos e inativos, datas de nascimento, atividades e associação de EPIs.
- **Atividades e EPIs:** não foram disponibilizadas informações completas sobre os valores permitidos, a relação entre atividades e equipamentos e a obrigatoriedade do número do Certificado de Aprovação (CA).
- **API:** não há documentação formal dos endpoints, parâmetros, estruturas de requisição, respostas esperadas e regras de autenticação e autorização.
- **Operações de alteração e exclusão:** é necessário confirmar quais operações estão disponíveis, suas rotas e os critérios de autorização.
- **Persistência dos dados:** é necessário esclarecer quais campos devem ser armazenados e como deve ocorrer a atualização e consulta das informações.
- **Ambiente de testes:** não foram fornecidas informações sobre a existência de um ambiente isolado, massa de dados fictícia ou procedimento de limpeza dos registros.

Na ausência dessas definições, as expectativas de comportamento são tratadas como premissas a confirmar, evitando considerar uma funcionalidade incorreta apenas com base em suposições.

Operações que possam criar, alterar ou excluir registros dependem de autorização explícita, ambiente apropriado e utilização de dados fictícios. A falta dessas condições deve ser considerada uma limitação para a execução, e não como aprovação do comportamento.


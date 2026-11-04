# Evidências de teste

Organização dos arquivos:

```text
evidences/
├── prints/   Capturas de tela e documentos PDF
├── videos/   Gravações de reprodução
└── logs/     Logs de API sem dados pessoais
```

## Evidência disponível

Os arquivos estão em `prints/`. PDFs nessa pasta são mantidos pelo Git.

Os cenários automatizados de interface salvam as capturas como arquivos PNG individuais e também montam um PDF único por cenário em `prints/automatizados/` (por exemplo, `CT005.pdf`), com uma imagem por página. Abra o PDF no visualizador integrado do VS Code e role para percorrer as capturas; os PNGs continuam disponíveis para visualização individual no VS Code. Uma nova execução substitui as evidências daquele cenário. As evidências são geradas localmente e não são adicionadas ao Git.

Os cenários automatizados de API geram um PDF por cenário em `api/automatizados/` (por exemplo, `CT018.pdf`). O documento registra método e URL, cabeçalhos, status HTTP, corpo retornado pela API e o resultado final do pytest, incluindo a falha da asserção quando houver. No cenário HEAD, o corpo vazio também é registrado. Cabeçalhos de autenticação e cookies são ocultados. Abra os PDFs no visualizador integrado do VS Code para consultar os registros e a execução.

## Visualizar imagens e gravações

- **PDF de evidências:** abra o arquivo do cenário (por exemplo, `CT005.pdf`) no visualizador de PDF do VS Code e role para visualizar as capturas; cada página contém uma imagem.
- **PDF de API:** abra `api/automatizados/CT018.pdf` (ou o ID desejado) para ver a requisição, a resposta e o resultado do teste.
- **PNG/JPG:** abra o arquivo no VS Code; a pré-visualização de imagens já é integrada, sem precisar instalar uma extensão.
- **PDF:** se abrir como texto, use `Ctrl+Shift+P` → **Reopen Editor With...** → escolha um visualizador de PDF. Também é possível usar o leitor padrão do Windows.
- **Vídeo ou trace:** o CT001 não grava vídeo nem trace. Para visualizar uma gravação `.webm`, use um player compatível; para abrir um trace Playwright `.zip`, execute `python -m playwright show-trace caminho\do\trace.zip`.

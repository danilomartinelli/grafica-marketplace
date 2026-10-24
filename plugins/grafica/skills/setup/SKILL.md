---
name: setup
description: "Prepara o computador ou a sessão para o plugin grafica — confere o Python e as bibliotecas (reportlab, Pillow, fontTools, numpy, pypdf, pypdfium2), explica em linguagem simples o que falta, instala com a permissão do usuário e testa gerando um cartão de exemplo. Use na primeira vez que alguém for usar o grafica, quando um script do plugin falhar por módulo ou programa ausente, ou quando pedirem para instalar, configurar ou consertar o plugin grafica."
allowed-tools: "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py) Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/check_deps.py *)"
license: "MIT (código e textos); fontes empacotadas sob SIL OFL 1.1 — ver LICENSE"
---

# /grafica:setup

**Pedido:** $ARGUMENTS
**Uso:** `/grafica:setup`

> **RAIZ** = pasta do plugin: `${CLAUDE_PLUGIN_ROOT}`. Se a variável não aparecer resolvida, use a pasta-base informada ao carregar esta skill e suba dois níveis.

Deixa tudo pronto para os outros comandos funcionarem. A pessoa pode não ser técnica: explique cada passo em uma frase simples, sem jargão, e **peça confirmação antes de instalar qualquer coisa**. Nunca rode `sudo`, nunca mude configurações do sistema além do que este roteiro diz, e não instale nada que não esteja aqui.

## 1. Achar o Python

Rode `python3 --version`. Se não funcionar, tente `python --version` e, no Windows, `py -3 --version`. Use o comando que responder **3.9 ou mais novo** no lugar de `python3` em todos os passos seguintes (e lembre-se dele nos outros comandos do plugin).

Sem Python (ou mais antigo que 3.9), explique que o plugin precisa dele para montar os arquivos e ofereça instalar:

| Sistema | Como instalar |
|---|---|
| Windows | `winget install -e --id Python.Python.3.12` — ou o instalador de python.org/downloads marcando **"Add python.exe to PATH"**. Depois feche e abra o app/terminal. |
| macOS | o instalador de python.org/downloads (mais simples) — ou `brew install python` se a pessoa usa Homebrew. Se aparecer o aviso das "ferramentas de linha de comando", aceite a instalação. |
| Linux (Debian/Ubuntu) | `sudo apt-get install -y python3 python3-pip` — só com o ok explícito da pessoa, que vai digitar a senha. |

No app do Claude (Cowork) o Python já vem instalado; pule para o passo 2.

## 2. Conferir o que falta

```
python3 RAIZ/scripts/check_deps.py --json
```

Leia o JSON:
- `ok: true` → vá para o passo 4.
- `faltam_obrigatorios` → bibliotecas que faltam. O campo `comandos` traz o comando exato, já com os ajustes do sistema (`--user --break-system-packages` quando o Python do sistema é protegido).
- `avisos` → coisas opcionais (poppler, perfil CMYK). Não instale opcionais sem a pessoa pedir.

## 3. Instalar (com permissão)

Diga em uma linha o que vai instalar e por quê (ex.: "Vou instalar 6 bibliotecas Python que o plugin usa para montar o PDF e as imagens; leva um ou dois minutos. Posso?"). Com o ok, rode o comando de `comandos` e depois repita o passo 2.

Se der erro:

| Mensagem | O que fazer |
|---|---|
| `externally-managed-environment` | acrescente `--user --break-system-packages` ao comando do pip |
| `No module named pip` | `python3 -m ensurepip --upgrade` e repita |
| `Permission denied` / acesso negado | acrescente `--user` |
| `python3` não é reconhecido (Windows) | use `py -3` ou `python` |
| rede bloqueada / sem acesso ao PyPI | diga à pessoa que a rede não deixou baixar as bibliotecas; numa empresa, o TI precisa liberar `pypi.org` e `files.pythonhosted.org` |

**Opcionais** (só se a pessoa quiser):
- **poppler** — o kit funciona sem ele (usa o pypdfium2). macOS: `brew install poppler`; Debian/Ubuntu: `sudo apt-get install -y poppler-utils`.
- **Perfil CMYK** — só se a gráfica exigir arquivo em CMYK. Peça o arquivo `.icc` à gráfica e defina a variável `GRAFICA_ICC` com o caminho dele (macOS/Linux: `export GRAFICA_ICC="/caminho/perfil.icc"` no `~/.zshrc` ou `~/.bashrc`; Windows: `setx GRAFICA_ICC "C:\caminho\perfil.icc"` e reabra o app). Sem a variável, o kit procura um perfil CMYK genérico do sistema (macOS e Windows costumam trazer um) — serve para conferir, mas o da gráfica é o certo.

## 4. Testar de ponta a ponta

```
python3 RAIZ/scripts/check_deps.py --teste
```

Gera um cartão de visita de exemplo numa pasta temporária, faz a prévia e roda a pré-impressão. Tem que terminar com três ✓ e "dependências ok". Se algum passo der ✗, leia a saída, corrija e repita.

## 5. Fechar

Diga em duas linhas que está tudo pronto (e qual comando do Python usar, se não for `python3`) e sugira um próximo passo: `/grafica:teach` para cadastrar a marca, ou `/grafica:craft <tipo>` para criar a primeira peça.

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

Deixa tudo pronto para os outros comandos funcionarem. A pessoa pode não ser técnica: explique cada passo em uma frase simples, sem jargão, e **peça confirmação antes de instalar qualquer coisa**. Não instale nada que não esteja neste roteiro.

**Comandos com `sudo` você não roda:** eles pedem a senha de administrador, que o seu terminal não consegue digitar. Quando um passo precisar de `sudo`, mostre o comando e peça para a pessoa rodá-lo no terminal dela; depois continue.

## 1. Achar o Python

Rode `python3 --version`. Se não funcionar, tente `python --version` e, no Windows, `py -3 --version`. Use o comando que responder **3.9 ou mais novo** no lugar de `python3` em todos os passos seguintes (e lembre-se dele nos outros comandos do plugin).

Se nenhum responder (no Windows a mensagem costuma ser *"Python was not found; run without arguments to install from the Microsoft Store"*), ou se a versão for mais antiga que 3.9, explique que o plugin precisa do Python para montar os arquivos e ofereça instalar:

| Sistema | Como instalar |
|---|---|
| Windows | com a permissão da pessoa, `winget install -e --id Python.Python.3.12`; ou ela baixa o instalador de python.org/downloads e marca **"Add python.exe to PATH"**. Depois é preciso fechar e abrir o app. |
| macOS | o instalador de python.org/downloads (mais simples); ou `brew install python`, se a pessoa usa Homebrew. Se o Mac oferecer instalar as "ferramentas de linha de comando", ela pode aceitar. |
| Debian/Ubuntu | a pessoa roda `sudo apt-get install -y python3 python3-pip` no terminal dela |
| Fedora | a pessoa roda `sudo dnf install -y python3 python3-pip` no terminal dela |

No Cowork o Claude trabalha num ambiente próprio que costuma já ter o Python; o passo 2 confirma.

## 2. Conferir o que falta

```
python3 RAIZ/scripts/check_deps.py --json
```

Leia o JSON:
- `ok: true` → vá para o passo 4.
- `faltam_obrigatorios` / `desatualizados` → bibliotecas que faltam ou estão antigas demais.
- `comandos` → os comandos para rodar, nesta ordem, exatamente como estão (já vêm com o caminho do Python entre aspas e com os ajustes deste sistema).
- `notas` → explicações para você repassar à pessoa em palavras simples (por exemplo, por que aparece `--user --break-system-packages`: este Python é o do sistema e é protegido, e com `--user` as bibliotecas vão só para a pasta do usuário, sem mexer no que o sistema usa).
- `avisos` → coisas opcionais (poppler, perfil CMYK). Não instale opcionais sem a pessoa pedir.

## 3. Instalar (com permissão)

Diga em uma linha o que vai instalar e por quê (ex.: "Vou instalar 6 bibliotecas Python que o plugin usa para montar o PDF e as imagens; leva um ou dois minutos. Posso?"). Com o ok, rode os `comandos` e repita o passo 2. Se um comando começa com `sudo`, siga a regra do topo.

Se der erro:

| Mensagem | O que fazer |
|---|---|
| `externally-managed-environment` | acrescente `--user --break-system-packages` ao comando do pip (e explique a nota acima) |
| `No module named pip` no Debian/Ubuntu | a pessoa roda `sudo apt-get install -y python3-pip` |
| `No module named pip` em outros sistemas | `python3 -m ensurepip --upgrade` e repita |
| `Permission denied` / acesso negado | acrescente `--user` |
| rede bloqueada / sem acesso ao PyPI | diga à pessoa que a rede não deixou baixar as bibliotecas; numa empresa, o TI precisa liberar `pypi.org` e `files.pythonhosted.org` |

**Opcionais** (só se a pessoa quiser):
- **poppler** — o kit funciona sem ele (usa o pypdfium2). macOS: `brew install poppler`; Debian/Ubuntu: a pessoa roda `sudo apt-get install -y poppler-utils`.
- **Perfil CMYK** — só se a gráfica exigir arquivo em CMYK. O jeito simples: pedir o arquivo `.icc` à gráfica e colocá-lo na pasta de trabalho (ou anexá-lo à conversa e salvar na pasta); o kit acha sozinho. Quem prefere pode definir a variável `GRAFICA_ICC` com o caminho. Sem nada disso, o kit procura um perfil CMYK genérico do sistema (macOS e Windows costumam trazer um): serve para conferir, mas o da gráfica é o certo.

## 4. Testar de ponta a ponta

```
python3 RAIZ/scripts/check_deps.py --teste
```

Gera um cartão de visita de exemplo numa pasta temporária, faz a prévia e roda a pré-impressão. Tem que terminar com três ✓ e "dependências ok". Se algum passo der ✗, leia a saída, corrija e repita.

## 5. Fechar

Diga em duas linhas que está tudo pronto (e qual comando do Python usar, se não for `python3`) e sugira um próximo passo: `/grafica:teach` para cadastrar a marca, ou `/grafica:craft <tipo>` para criar a primeira peça.

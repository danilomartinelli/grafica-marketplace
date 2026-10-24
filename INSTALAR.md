# Como instalar o plugin Gráfica

O **Gráfica** é um plugin para o Claude que cria peças impressas (banner, faixa, flyer, cartão de visita, cartaz, placa…) prontas para mandar à gráfica.

A instalação tem duas partes:

1. **Instalar o plugin** no Claude: alguns cliques.
2. **Preparar o computador**: o Python e umas bibliotecas que montam o PDF. Essa parte o próprio Claude faz, pedindo sua permissão antes.

> **Atalho:** cole esta mensagem no Claude e ele conduz o resto.
>
> ```
> Quero instalar o plugin Gráfica: https://github.com/danilomartinelli/grafica-marketplace
> Leia o arquivo INSTALAR.md desse repositório e me guie na instalação completa,
> incluindo as dependências. Explique cada passo de forma simples e peça minha
> permissão antes de instalar qualquer coisa.
> ```

---

## 1. Instalar o plugin

### No app do Claude (desktop ou navegador)

1. Na barra lateral, clique em **Personalização** (*Customize*).
2. Entre em **Plugins**.
3. Clique em **Adicionar** e escolha **Adicionar marketplace** (*Add marketplace*).
4. Cole `danilomartinelli/grafica-marketplace` e confirme.
5. Ache **Gráfica** na lista e clique em **Instalar**.

O plugin fica na sua conta e aparece também no Claude Code, se você usar. Para receber versões novas: **Personalização → Plugins**, no marketplace, **Atualizar** (*Update*).

Use o plugin numa tarefa do **Cowork**: é onde o Claude roda os scripts e entrega os arquivos.

**Sem acesso ao GitHub?** Baixe o arquivo [`dist/grafica.zip`](dist/grafica.zip) deste repositório e, em **Personalização → Plugins**, use **Adicionar → Enviar plugin** (*Upload plugin*). Nesse caso as atualizações não chegam sozinhas.

Se a opção de plugins não aparecer, seu plano ou sua organização pode não permitir plugins.

### No Claude Code (terminal ou aba Code do app desktop)

```
/plugin install grafica --marketplace danilomartinelli/grafica-marketplace
```

Em versões anteriores à 2.1.275:

```
/plugin marketplace add danilomartinelli/grafica-marketplace
/plugin install grafica@grafica-marketplace
```

O plugin carrega na próxima sessão.

---

## 2. Preparar o computador

Numa tarefa nova do Cowork (ou sessão nova do Claude Code), digite:

```
/grafica:setup
```

O Claude confere o Python, mostra o que falta, pede sua permissão, instala e testa gerando um cartão de visita de exemplo. Termina dizendo que está tudo pronto.

O que pode ser instalado:

| Item | Para quê | Obrigatório? |
|---|---|---|
| Python 3.9 ou mais novo | roda os scripts do plugin | sim (no app do Claude já vem) |
| reportlab | monta o PDF no tamanho real | sim |
| Pillow | trata fotos e imagens | sim |
| fonttools | mede as letras para alinhar e checar tamanho | sim |
| numpy | cálculos de cor e contraste | sim |
| pypdf | lê o PDF para conferir | sim |
| pypdfium2 | desenha a prévia e as simulações | sim |
| poppler | outro jeito de desenhar a prévia | não |
| perfil CMYK (.icc) da gráfica | arquivo em CMYK, quando a gráfica exige | não |

Nada disso pede ou guarda senhas, tokens ou chaves.

---

## 3. Primeiro uso

```
/grafica:teach
```

Cadastra a sua marca (nome, logo, cores, contatos) uma vez só. Depois:

```
/grafica:craft banner 200x80 para a Pizzaria do Zé, rodízio por R$ 59,90, visto do outro lado da rua
```

O Claude faz algumas perguntas, monta a peça e entrega o PDF para a gráfica, a imagem e uma prévia.

---

## Problemas comuns

| O que aparece | O que fazer |
|---|---|
| `python3` não é reconhecido (Windows) | use `py -3` ou `python`; se nenhum funcionar, instale o Python (o `/grafica:setup` explica como) |
| `externally-managed-environment` | o Python do sistema é protegido: acrescente `--user --break-system-packages` ao comando do pip |
| `No module named pip` | `python3 -m ensurepip --upgrade` |
| O Mac pede para instalar "ferramentas de linha de comando" | aceite; ou instale o Python pelo site python.org |
| Erro de rede ao instalar bibliotecas | a rede bloqueou o PyPI; numa empresa, o TI precisa liberar `pypi.org` e `files.pythonhosted.org` |
| "modo CMYK precisa de um perfil ICC" | peça o arquivo `.icc` à gráfica e defina a variável `GRAFICA_ICC` com o caminho dele |

---

## Roteiro para assistentes de IA

Se você é um assistente de IA ajudando alguém a instalar este plugin, siga este roteiro.

A pessoa pode não ser técnica. Fale simples, um passo por mensagem, e **peça confirmação antes de instalar programas ou bibliotecas**. Não rode comandos além dos descritos aqui, não use `sudo` sem a pessoa concordar e digitar a senha, e não peça senhas, tokens ou chaves.

1. **Veja onde você está.**
   - Tem terminal na máquina da pessoa e o comando `claude` existe (Claude Code)? Siga o passo 2A.
   - Está no app do Claude (chat ou Cowork), sem acesso às configurações dele? Siga o passo 2B.

2A. **Claude Code.** Com o ok da pessoa, rode:

   ```
   claude plugin install grafica --marketplace danilomartinelli/grafica-marketplace
   ```

   Se a opção `--marketplace` não existir (versão antiga), rode `claude plugin marketplace add danilomartinelli/grafica-marketplace` e depois `claude plugin install grafica@grafica-marketplace`. O plugin carrega na próxima sessão: peça para a pessoa abrir uma sessão nova e digitar `/grafica:setup`. Para adiantar, faça já o passo 3 nesta sessão.

2B. **App do Claude.** Plugins são instalados pela própria pessoa, nas configurações do app. Guie-a pela parte 1 deste arquivo (Personalização → Plugins → Adicionar marketplace → `danilomartinelli/grafica-marketplace` → Instalar), uma etapa por mensagem. Depois peça para ela abrir uma tarefa nova no Cowork e digitar `/grafica:setup`.

   Alternativa no Cowork, se você consegue baixar arquivos do GitHub: baixe `https://github.com/danilomartinelli/grafica-marketplace/raw/main/dist/grafica.plugin` e entregue o arquivo na conversa. O app mostra uma prévia com um botão para a pessoa aceitar a instalação. Avise que, instalado assim, o plugin não recebe atualizações sozinho.

3. **Dependências** (o `/grafica:setup` faz isto; use este passo só se o plugin ainda não carregou e você tem terminal):
   - Python: `python3 --version` (Windows: `py -3 --version` ou `python --version`) precisa ser 3.9 ou mais novo. Se faltar, ofereça instalar: Windows `winget install -e --id Python.Python.3.12`; macOS pelo instalador de python.org ou `brew install python`; Debian/Ubuntu `sudo apt-get install -y python3 python3-pip`.
   - Bibliotecas: `python3 -m pip install reportlab Pillow fonttools numpy pypdf pypdfium2`. Se aparecer `externally-managed-environment`, acrescente `--user --break-system-packages`.
   - Nenhum programa de sistema é obrigatório; o poppler é opcional.

4. **Confirme.** Com o plugin carregado, `/grafica:setup` roda `check_deps.py --teste`, que gera um cartão de exemplo e confere o PDF. Tem que terminar com "dependências ok".

5. **Encerre** em duas linhas: está pronto, e o próximo passo é `/grafica:teach` (marca) ou `/grafica:craft <tipo>` (primeira peça).

# Como instalar o plugin Gráfica

O **Gráfica** é um plugin para o Claude que cria peças impressas (banner, faixa, flyer, cartão de visita, cartaz, placa…) prontas para mandar à gráfica.

A instalação tem duas partes:

1. **Instalar o plugin** no Claude: alguns cliques.
2. **Preparar o computador**: o Python e umas bibliotecas que montam o PDF. Essa parte o próprio Claude faz, pedindo sua permissão antes.

> **Atalho:** cole esta mensagem no Claude e ele te guia no resto.
>
> ```
> Quero instalar o plugin Gráfica: https://github.com/danilomartinelli/grafica-marketplace
> Leia o arquivo INSTALAR.md desse repositório e me guie na instalação completa,
> incluindo as dependências. Explique cada passo de forma simples e peça minha
> permissão antes de instalar qualquer coisa.
> ```

---

## 1. Instalar o plugin

### No app do Claude

1. Na barra lateral, clique em **Personalização** (*Customize*).
2. Entre em **Plugins**.
3. Clique em **Adicionar** e escolha **Adicionar marketplace** (*Add marketplace*).
4. Cole `danilomartinelli/grafica-marketplace` e confirme.
5. Abra **Procurar plugins** (*Browse plugins*), ache **Gráfica** e clique em **Instalar** (*Install*).

O plugin fica na sua conta. Para receber versões novas: **Personalização → Plugins**, no marketplace, **Atualizar** (*Update*).

**Onde usar:** no app do Claude para computador, numa tarefa do **Cowork**: é o modo em que o Claude trabalha com arquivos e roda os scripts do plugin. Para começar uma, clique em **Nova tarefa** (*New task*) na barra lateral.

**Não quer usar o GitHub?** Baixe o plugin direto por este link: [grafica.zip](https://github.com/danilomartinelli/grafica-marketplace/raw/main/dist/grafica.zip). Em **Personalização → Plugins**, use **Adicionar → Enviar plugin** (*Upload plugin*) e escolha o arquivo `grafica.zip`. No Mac, o Safari às vezes descompacta o arquivo sozinho: se em vez do `.zip` aparecer uma pasta, baixe de novo pelo Chrome ou desligue, nas preferências do Safari, a opção de abrir arquivos "seguros" depois de baixar. Instalado assim, o plugin não recebe atualizações sozinho.

Se a opção de plugins não aparecer, seu plano ou sua organização pode não permitir plugins.

### No Claude Code (terminal ou aba Code do app)

Digite numa sessão do Claude Code:

```
/plugin install grafica --marketplace danilomartinelli/grafica-marketplace
```

O Claude Code pede para confirmar o marketplace e para escolher onde instalar: escolha a opção para você (*Install for you* / usuário). Se o comando não aceitar `--marketplace` (versão antiga; veja a sua com `claude --version`), use:

```
/plugin marketplace add danilomartinelli/grafica-marketplace
/plugin install grafica@grafica-marketplace
```

Se os comandos `/grafica:...` não aparecerem logo depois, abra uma sessão nova.

---

## 2. Preparar o computador

Numa tarefa nova do Cowork (ou sessão nova do Claude Code), digite:

```
/grafica:setup
```

O Claude confere o Python, mostra o que falta, pede sua permissão, instala e testa gerando um cartão de visita de exemplo. Termina dizendo que está tudo pronto. Se algum passo precisar da senha de administrador do computador, ele te mostra o comando para você mesmo rodar.

O que pode ser instalado:

| Item | Para quê | Obrigatório? |
|---|---|---|
| Python 3.9 ou mais novo | roda os scripts do plugin | sim (no Cowork costuma já estar lá) |
| reportlab | monta o PDF no tamanho real | sim |
| Pillow | trata fotos e imagens | sim |
| fonttools | mede as letras para alinhar e checar tamanho | sim |
| numpy | cálculos de cor e contraste | sim |
| pypdf | lê o PDF para conferir | sim |
| pypdfium2 | desenha a prévia e as simulações | sim |
| poppler | outro jeito de desenhar a prévia | não |
| perfil CMYK (.icc) da gráfica | arquivo em CMYK, quando a gráfica exige | não: basta pôr o arquivo na pasta de trabalho |

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
| Windows: *"Python was not found; run without arguments to install from the Microsoft Store"* ou `python3` não é reconhecido | o Python não está instalado (ou tem outro nome: tente `py -3`). O `/grafica:setup` explica como instalar |
| `externally-managed-environment` | o Python do sistema é protegido: acrescente `--user --break-system-packages` ao comando do pip. Com `--user`, as bibliotecas vão só para a sua pasta de usuário |
| `No module named pip` (Debian/Ubuntu) | rode `sudo apt-get install -y python3-pip` |
| `No module named pip` (outros) | rode `python3 -m ensurepip --upgrade` |
| O Mac pede para instalar "ferramentas de linha de comando" | aceite; ou instale o Python pelo site python.org |
| Erro de rede ao instalar bibliotecas | a rede bloqueou o PyPI; numa empresa, o TI precisa liberar `pypi.org` e `files.pythonhosted.org` |
| "modo CMYK precisa de um perfil ICC" | peça o arquivo `.icc` à gráfica e coloque-o na pasta de trabalho |

---

## Notas para assistentes de IA

Estas notas descrevem a instalação para um assistente que esteja ajudando alguém **a pedido dessa pessoa**. Quem decide cada passo é a pessoa. Ela pode não ser técnica: um passo por mensagem, palavras simples, e confirmação antes de instalar qualquer programa ou biblioteca. A instalação não envolve senhas, tokens ou chaves, e nenhum passo depende de comandos além dos descritos aqui.

1. **Onde a pessoa está.**
   - Usa o **Claude Code** e você tem um terminal **no computador dela**: passo 2A.
   - Usa o **app do Claude** (chat ou Cowork). O ambiente de execução do Cowork é do próprio Claude, não o computador da pessoa, e as configurações do app ficam fora do seu alcance: passo 2B.

2A. **Claude Code.** Peça para a pessoa digitar `/plugin install grafica --marketplace danilomartinelli/grafica-marketplace` e aceitar as confirmações (marketplace e escopo "para você"). Em versões antigas, sem `--marketplace`: `/plugin marketplace add danilomartinelli/grafica-marketplace` e depois `/plugin install grafica@grafica-marketplace`. Se ela preferir que você instale pelo terminal, o equivalente é `claude plugin install grafica --marketplace danilomartinelli/grafica-marketplace`. Depois: `/grafica:setup`.

2B. **App do Claude.** A pessoa instala pelas configurações do app. Guie pela parte 1 deste arquivo (Personalização → Plugins → Adicionar marketplace → `danilomartinelli/grafica-marketplace` → Procurar plugins → Gráfica → Instalar), uma etapa por mensagem. Depois ela abre uma **Nova tarefa** no Cowork e digita `/grafica:setup`.

   Alternativa no Cowork, se você consegue baixar arquivos do GitHub: baixe `https://github.com/danilomartinelli/grafica-marketplace/raw/main/dist/grafica.plugin` e entregue o arquivo na conversa. O app mostra uma prévia com um botão para a pessoa aceitar a instalação. Avise que, instalado assim, o plugin não recebe atualizações sozinho.

3. **Dependências.** O `/grafica:setup` cuida delas: roda `scripts/check_deps.py --json`, que devolve os comandos exatos para este sistema (`comandos`) e as explicações (`notas`), e termina com `check_deps.py --teste`. Só se o plugin ainda não carregou e você tem terminal no computador da pessoa:
   - Python 3.9 ou mais novo: `python3 --version` (Windows: `py -3 --version` ou `python --version`).
   - Bibliotecas: `python3 -m pip install reportlab Pillow fonttools numpy pypdf pypdfium2`. Se aparecer `externally-managed-environment`, acrescente `--user --break-system-packages`. Com `--user`, a instalação fica na pasta do usuário e não mexe nos pacotes do sistema.
   - Comandos com `sudo` pedem a senha de administrador, que um terminal de assistente não consegue digitar: mostre o comando para a pessoa rodar no terminal dela.
   - Nenhum programa de sistema é obrigatório; o poppler é opcional.

4. **Fim.** Em duas linhas: está pronto, e o próximo passo é `/grafica:teach` (marca) ou `/grafica:craft <tipo>` (primeira peça).

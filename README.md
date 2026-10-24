# grafica-marketplace

Marketplace de plugins para o Claude com o plugin **Gráfica**: criação de peças impressas de comunicação visual (banner, faixa, flyer, cartão de visita, cartaz, placa…) em português, prontas para a gráfica.

## Instalar

**Jeito mais fácil:** cole isto no Claude.

```
Quero instalar o plugin Gráfica: https://github.com/danilomartinelli/grafica-marketplace
Leia o arquivo INSTALAR.md desse repositório e me guie na instalação completa,
incluindo as dependências. Explique cada passo de forma simples e peça minha
permissão antes de instalar qualquer coisa.
```

**App do Claude:** em **Personalização → Plugins**, clique em **Adicionar → Adicionar marketplace** (*Add marketplace*), cole `danilomartinelli/grafica-marketplace` e instale **Gráfica**. Depois, numa **Nova tarefa** do Cowork, digite `/grafica:setup`.

**Claude Code:**

```
/plugin install grafica --marketplace danilomartinelli/grafica-marketplace
```

Depois, rode `/grafica:setup` (se o comando ainda não aparecer, abra uma sessão nova).

Passo a passo completo, problemas comuns e notas para assistentes de IA: **[INSTALAR.md](INSTALAR.md)**.

## Usar

`/grafica:teach` cadastra a marca; `/grafica:craft banner ...` cria uma peça; `/grafica:audit arquivo.pdf` confere um arquivo antes da gráfica. Todos os comandos em [`plugins/grafica/README.md`](plugins/grafica/README.md).

# grafica-marketplace

Marketplace de plugins para o Claude com o plugin **grafica** — criação de peças impressas de comunicação visual (banner, faixa, flyer, cartão de visita, cartaz, placa…) em português, prontas para a gráfica.

## Instalar no Claude Code

```
/plugin marketplace add danilomartinelli/grafica-marketplace
/plugin install grafica@grafica-marketplace
```

(No Claude Code 2.1.275+ também funciona em um passo: `/plugin install grafica --marketplace danilomartinelli/grafica-marketplace`.)

Depois: `/grafica:craft banner ...`, `/grafica:grill`, `/grafica:audit arquivo.pdf` etc. Detalhes em [`plugins/grafica/README.md`](plugins/grafica/README.md).

## Instalar no app do Claude

Use o arquivo `dist/grafica.plugin` (gerado a partir de `plugins/grafica/`): abra-o numa conversa e aceite a instalação, ou, em organizações, peça ao administrador para adicioná-lo ao catálogo de plugins da organização.

# Wild West Pioneers — Tradução PT-BR

Tradução completa para português do Brasil de **Wild West Pioneers**: interface, missões, diálogos e legendas, tutoriais, FAQ, tecnologias e conquistas. Mais de 6.500 textos traduzidos.

> O jogo não tem suporte oficial a português. Esta tradução é feita por fã e não tem ligação com os desenvolvedores.

## Instalação

1. Tenha o [Python 3](https://www.python.org/downloads/) instalado (marque **Add Python to PATH** na instalação).
2. Baixe este repositório e coloque a pasta `Traducao_WildWestPioners_PTBR` dentro da pasta do jogo:
   ```
   Steam\steamapps\common\Wild West Pioneers\Traducao_WildWestPioners_PTBR\
   ```
3. Dê dois cliques em `aplicar_traducao.bat` (ou rode `python aplicar_traducao.py`).
   Na primeira vez ele instala sozinho a dependência `UnityPy`.
4. Abra o jogo e, em **Configurações › Idioma do Texto**, escolha **Português (Brasil)**.

A tradução ocupa o lugar do polonês na lista de idiomas. O áudio das falas continua no idioma original; só texto e legendas mudam.

## Depois de uma atualização do jogo

Quando o Steam atualiza o jogo ou você usa "Verificar integridade dos arquivos", o arquivo traduzido é substituído. Basta rodar o `aplicar_traducao.bat` de novo. Textos novos que ainda não estiverem no `ptbr.json` aparecem em inglês.

## Voltar ao original

Rode `restaurar_original.bat` (ou `python aplicar_traducao.py --restaurar`). O script guarda o arquivo original em `WWP_Data\resources.assets.original` na hora de aplicar.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `ptbr.json` | Todas as traduções, no formato `"chave do termo": "texto"`. Pode editar à vontade. |
| `aplicar_traducao.py` | Injeta o `ptbr.json` no `resources.assets` do jogo. |
| `aplicar_traducao.bat` / `restaurar_original.bat` | Atalhos para aplicar e desfazer. |
| `requirements.txt` | Dependência Python (`UnityPy`). |

## Como funciona

O jogo é feito em Unity e usa o plugin **I2 Localization**. Todos os textos ficam em um único asset chamado `I2Languages` dentro de `WWP_Data\resources.assets`, com uma coluna por idioma. O script abre esse asset com o UnityPy, reescreve a coluna do polonês com os textos em português, renomeia o idioma para `Portuguese (Brazil)` (`pt-BR`) e regrava o arquivo. Ele também desliga a sincronização semanal de textos com o Google Sheets dos desenvolvedores, que senão sobrescreveria a tradução.

## Contribuindo

Achou um erro ou texto estranho? Edite a linha correspondente no `ptbr.json`, rode o script de novo e abra um pull request. Ao traduzir, mantenha intactas as tags (`<b>`, `<br>`, `<sprite ...>`) e as variáveis entre `{[ ]}`.

## Licença

Os textos traduzidos são distribuídos livremente para uso com uma cópia legítima do jogo. Wild West Pioneers e todo o seu conteúdo pertencem aos seus respectivos donos.

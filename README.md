# Wild West Pioneers — Tradução PT-BR

Tradução completa para português do Brasil de **Wild West Pioneers**: interface, missões, diálogos e legendas, tutoriais, FAQ, tecnologias e conquistas. Mais de 6.500 textos traduzidos, e as falas dos personagens dubladas em português com vozes geradas por IA.

> O jogo não tem suporte oficial a português. Esta tradução é feita por fã e não tem ligação com os desenvolvedores.

## Download

O pacote pronto, com o script de legendas e o gerador de áudio, está aqui:

**[Release.zip (v1.0.1)](https://github.com/r7born/Traducao_WildWestPioners_PTBR/releases/download/v1.0.1/Release.zip)**

Dentro dele vem a pasta `Translate_PT_BR` com tudo o que você precisa. As vozes em português não vêm prontas no zip: elas são geradas na sua máquina pelo `gerar_vozes.bat`, que está dentro da pasta (veja [Vozes em português](#vozes-em-português)).

## Instalação

1. Tenha o [Python 3](https://www.python.org/downloads/) instalado (marque **Add Python to PATH** na instalação).
2. Baixe o `Release.zip` acima, extraia e coloque a pasta `Translate_PT_BR` dentro da pasta do jogo:
   ```
   Steam\steamapps\common\Wild West Pioneers\Translate_PT_BR\
   ```
3. Dê dois cliques em `aplicar_traducao.bat` (ou rode `python aplicar_traducao.py`).
   Na primeira vez ele instala sozinho a dependência `UnityPy`. Isso já deixa textos e legendas em português.
4. Quer as falas em português também? Rode o `gerar_vozes.bat` (demora, veja abaixo) e depois o `aplicar_traducao.bat` de novo.
5. Abra o jogo e, em **Configurações › Idioma do Texto**, escolha **Português (Brasil)**.

A tradução ocupa o lugar do polonês na lista de idiomas. Se a pasta `Audio_PTBR` existir, as falas em português também são copiadas para o jogo.

## Depois de uma atualização do jogo

Quando o Steam atualiza o jogo ou você usa "Verificar integridade dos arquivos", os arquivos traduzidos são substituídos. Basta rodar o `aplicar_traducao.bat` de novo. Textos novos que ainda não estiverem no `ptbr.json` aparecem em inglês.

## Voltar ao original

Rode `restaurar_original.bat` (ou `python aplicar_traducao.py --restaurar`). Os textos voltam do backup `WWP_Data\resources.assets.original` e as falas voltam de `WWP_Data\StreamingAssets\_backup_ptbr`.

## Vozes em português

As falas de `Dialogue` e `Bark` são geradas com o [XTTS-v2](https://github.com/idiap/coqui-ai-TTS), usando o áudio original em inglês de cada fala como referência de voz. Assim cada personagem mantém um timbre próprio, parecido com o original.

As vozes são geradas na sua máquina pelo `gerar_vozes.bat` que vem no `Release.zip`. Na primeira vez ele monta o ambiente sozinho (baixa uns 4 GB) e depois gera as 1.600 falas, o que leva em torno de 1h30 a 2h numa placa NVIDIA. Requisitos: placa NVIDIA (uns 4 GB de VRAM) e cerca de 6 GB de espaço para o ambiente e o modelo. Depois de gerar, rode o `aplicar_traducao.bat`.

| Comando | O que faz |
|---|---|
| `gerar_vozes.bat` | Prepara o ambiente na primeira vez (Python 3.11 isolado, PyTorch com CUDA, XTTS) e gera em `Audio_PTBR` o que ainda não existe. |
| `gerar_vozes.bat --forcar` | Gera tudo de novo. |
| `gerar_vozes.bat --limite 10` | Gera só 10 falas, para testar. |
| `gerar_vozes.bat --refazer` | Gera de novo só as falas listadas em `vozes_ruins.txt`. |
| `conferir_vozes.bat` | Transcreve as falas geradas com o Whisper e compara com o texto esperado. Gera `conferencia_vozes.txt` com as piores primeiro. |

Fluxo para caprichar: `gerar_vozes.bat`, depois `conferir_vozes.bat` (marca as falas ruins em `vozes_ruins.txt`), depois `gerar_vozes.bat --refazer` para regenerar só essas. No fim, `aplicar_traducao.bat`.

Grunhidos e sons sem palavras ("Ughhh...", "Grrr!") ficam com o áudio original, porque não têm idioma e o modelo se atrapalha com eles.

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `ptbr.json` | Todas as traduções, no formato `"chave do termo": "texto"`. Pode editar à vontade. |
| `aplicar_traducao.py` | Injeta o `ptbr.json` no `resources.assets` e copia as vozes de `Audio_PTBR` para o jogo. |
| `aplicar_traducao.bat` / `restaurar_original.bat` | Atalhos para aplicar e desfazer. |
| `gerar_vozes.py` / `gerar_vozes.bat` | Gera as falas em português com clonagem de voz. |
| `conferir_vozes.py` / `conferir_vozes.bat` | Confere as falas geradas com reconhecimento de fala. |
| `Audio_PTBR/` | Falas em português geradas pelo `gerar_vozes.bat`, com os mesmos nomes dos arquivos do jogo. |
| `requirements.txt` | Dependência dos textos (`UnityPy`). |
| `requirements-vozes.txt` | Dependências das vozes (instaladas em um ambiente separado). |

## Como funciona

O jogo é feito em Unity e usa o plugin **I2 Localization**. Todos os textos ficam em um único asset chamado `I2Languages` dentro de `WWP_Data\resources.assets`, com uma coluna por idioma. O script abre esse asset com o UnityPy, reescreve a coluna do polonês com os textos em português, renomeia o idioma para `Portuguese (Brazil)` (`pt-BR`) e regrava o arquivo. Ele também desliga a sincronização semanal de textos com o Google Sheets dos desenvolvedores, que senão sobrescreveria a tradução.

As falas ficam soltas em `WWP_Data\StreamingAssets\Dialogue` e `Bark`, um `.ogg` por fala, com o nome da chave do texto. Por isso basta gerar o áudio em português com o mesmo nome e copiar por cima.

## Contribuindo

Achou um erro ou texto estranho? Edite a linha correspondente no `ptbr.json`, rode o script de novo e abra um pull request. Ao traduzir, mantenha intactas as tags (`<b>`, `<br>`, `<sprite ...>`) e as variáveis entre `{[ ]}`.

## Licença

Os textos traduzidos e as vozes geradas são distribuídos livremente para uso com uma cópia legítima do jogo. O modelo XTTS-v2 segue a licença [Coqui Public Model License](https://coqui.ai/cpml), de uso não comercial. Wild West Pioneers e todo o seu conteúdo pertencem aos seus respectivos donos.

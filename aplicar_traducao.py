import argparse
import json
import os
import shutil
import struct
import subprocess
import sys

for fluxo in (sys.stdout, sys.stderr):
    if hasattr(fluxo, "reconfigure"):
        fluxo.reconfigure(encoding="utf-8", errors="replace")

PASTA = os.path.dirname(os.path.abspath(__file__))
PASTA_DATA = os.path.join(os.path.dirname(PASTA), "WWP_Data")
ASSET = os.path.join(PASTA_DATA, "resources.assets")
BACKUP = ASSET + ".original"
TRADUCAO = os.path.join(PASTA, "ptbr.json")

IDIOMA_SUBSTITUIDO = "Polish"
NOVO_NOME = "Portuguese (Brazil)"
NOVO_CODIGO = "pt-BR"

INICIO_TERMOS = 0x38

GOOGLE_NUNCA = 1


def garantir_unitypy():
    try:
        import UnityPy  # noqa: F401
    except ImportError:
        print("UnityPy não encontrado, instalando...")
        requisitos = os.path.join(PASTA, "requirements.txt")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requisitos])


class Leitor:
    """Lê os tipos básicos do formato serializado do Unity (little-endian, alinhado em 4 bytes)."""

    def __init__(self, dados, posicao=0):
        self.dados = dados
        self.pos = posicao

    def alinhar(self):
        self.pos = (self.pos + 3) & ~3

    def u32(self):
        valor = struct.unpack_from("<I", self.dados, self.pos)[0]
        self.pos += 4
        return valor

    def texto(self):
        tamanho = self.u32()
        valor = self.dados[self.pos:self.pos + tamanho].decode("utf-8")
        self.pos += tamanho
        self.alinhar()
        return valor

    def bytes_(self):
        tamanho = self.u32()
        valor = self.dados[self.pos:self.pos + tamanho]
        self.pos += tamanho
        self.alinhar()
        return valor


class Escritor:
    def __init__(self):
        self.saida = bytearray()

    def alinhar(self):
        while len(self.saida) % 4:
            self.saida += b"\x00"

    def crus(self, dados):
        self.saida += dados

    def u32(self, valor):
        self.saida += struct.pack("<I", valor)

    def texto(self, valor):
        codificado = valor.encode("utf-8")
        self.u32(len(codificado))
        self.saida += codificado
        self.alinhar()

    def bytes_(self, valor):
        self.u32(len(valor))
        self.saida += valor
        self.alinhar()


def ler_asset(dados):
    """Separa o asset I2Languages em cabeçalho, termos, idiomas e o restante."""
    leitor = Leitor(dados, INICIO_TERMOS)

    termos = []
    for _ in range(leitor.u32()):
        chave = leitor.texto()
        tipo = leitor.u32()
        textos = [leitor.texto() for _ in range(leitor.u32())]
        flags = leitor.bytes_()
        extra = leitor.u32()
        termos.append((chave, tipo, textos, flags, extra))

    inicio_config = leitor.pos
    leitor.pos += 8            
    leitor.texto()             
    fim_config = leitor.pos

    idiomas = []
    for _ in range(leitor.u32()):
        nome = leitor.texto()
        codigo = leitor.texto()
        flags = dados[leitor.pos:leitor.pos + 4]
        leitor.pos += 4
        idiomas.append([nome, codigo, flags])

    return {
        "cabecalho": dados[:INICIO_TERMOS],
        "termos": termos,
        "config": dados[inicio_config:fim_config],
        "idiomas": idiomas,
        "restante": dados[leitor.pos:],
    }


def desligar_sincronizacao_google(restante):
    """Troca GoogleUpdateFrequency para 'Never', senão o jogo baixa os textos originais de novo."""
    marca = restante.find(b"I2Loc FoundersOfWildWest")
    if marca < 0:
        return restante
    leitor = Leitor(restante, marca - 4)
    leitor.texto()   # nome da planilha
    leitor.texto()   # versão da última atualização
    pos = leitor.pos
    return restante[:pos] + struct.pack("<I", GOOGLE_NUNCA) + restante[pos + 4:]


def montar_asset(asset, traducoes):
    """Reconstrói o asset com o português no lugar do idioma substituído."""
    idiomas = asset["idiomas"]
    indice = next(i for i, (nome, _, _) in enumerate(idiomas) if nome == IDIOMA_SUBSTITUIDO)
    idiomas[indice][0] = NOVO_NOME
    idiomas[indice][1] = NOVO_CODIGO

    escritor = Escritor()
    escritor.crus(asset["cabecalho"])
    escritor.u32(len(asset["termos"]))

    traduzidos = 0
    for chave, tipo, textos, flags, extra in asset["termos"]:
        if chave in traducoes:
            textos[indice] = traducoes[chave]
            traduzidos += 1
        else:
            textos[indice] = ""  
        escritor.texto(chave)
        escritor.u32(tipo)
        escritor.u32(len(textos))
        for texto in textos:
            escritor.texto(texto)
        escritor.bytes_(flags)
        escritor.u32(extra)

    escritor.crus(asset["config"])
    escritor.u32(len(idiomas))
    for nome, codigo, flags in idiomas:
        escritor.texto(nome)
        escritor.texto(codigo)
        escritor.crus(flags)
    escritor.crus(desligar_sincronizacao_google(asset["restante"]))

    return bytes(escritor.saida), traduzidos


def encontrar_i2languages(ambiente):
    for objeto in ambiente.objects:
        if objeto.type.name == "MonoBehaviour" and b"I2Languages" in objeto.get_raw_data()[:200]:
            return objeto
    raise RuntimeError("asset I2Languages não encontrado em resources.assets")


def aplicar():
    garantir_unitypy()
    import UnityPy

    if not os.path.exists(ASSET):
        sys.exit(f"Arquivo não encontrado: {ASSET}\nA pasta Traducao_PTBR precisa ficar dentro da pasta do jogo.")

    with open(TRADUCAO, encoding="utf-8") as arquivo:
        traducoes = json.load(arquivo)

    with open(ASSET, "rb") as arquivo:
        ambiente = UnityPy.load(arquivo.read())

    objeto = encontrar_i2languages(ambiente)
    original = objeto.get_raw_data()
    if NOVO_NOME.encode() in original[-2000:]:
        print("A tradução já está aplicada.")
        return

    if os.path.exists(BACKUP):
        os.remove(BACKUP)
    shutil.copy2(ASSET, BACKUP)
    print(f"Backup criado: {BACKUP}")

    novo, traduzidos = montar_asset(ler_asset(original), traducoes)
    objeto.set_raw_data(novo)

    temporario = ASSET + ".tmp"
    with open(temporario, "wb") as arquivo:
        arquivo.write(ambiente.file.save())
    os.replace(temporario, ASSET)

    total = len(ler_asset(original)["termos"])
    print(f"Pronto: {traduzidos} de {total} termos traduzidos.")
    print(f'No jogo, escolha "{NOVO_NOME}" em Idioma do Texto (fica no lugar de {IDIOMA_SUBSTITUIDO}).')


def restaurar():
    if not os.path.exists(BACKUP):
        sys.exit("Não há backup para restaurar. Use 'Verificar integridade dos arquivos' no Steam.")
    shutil.copy2(BACKUP, ASSET)
    os.remove(BACKUP)
    print("Arquivo original restaurado.")


def main():
    parser = argparse.ArgumentParser(description="Aplica ou remove a tradução pt-BR de Wild West Pioneers.")
    parser.add_argument("--restaurar", action="store_true", help="volta ao resources.assets original")
    argumentos = parser.parse_args()

    if argumentos.restaurar:
        restaurar()
    else:
        aplicar()


if __name__ == "__main__":
    main()

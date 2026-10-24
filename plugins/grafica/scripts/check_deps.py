#!/usr/bin/env python3
"""Confere se esta máquina tem o que o plugin grafica precisa e diz exatamente como instalar o que faltar.

  python3 check_deps.py            # relatório legível
  python3 check_deps.py --json     # o mesmo em JSON (para assistentes de IA)
  python3 check_deps.py --teste    # além de conferir, gera um cartão de exemplo e confere o PDF de ponta a ponta

Não instala nada sozinho: mostra o comando para você (ou o assistente, com a sua permissão) rodar.
Sai com código 0 se o essencial estiver ok, 1 se faltar algo obrigatório.
"""
import importlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile

for _s in (sys.stdout, sys.stderr):  # Windows: saída em UTF-8 sem quebrar no cp1252
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
REQ = os.path.join(RAIZ, "requirements.txt")

# (módulo para importar, pacote no pip)
OBRIGATORIOS = [("reportlab", "reportlab"), ("PIL", "Pillow"), ("fontTools", "fonttools"),
                ("numpy", "numpy"), ("pypdf", "pypdf"), ("pypdfium2", "pypdfium2")]
POPPLER = ["pdftoppm", "pdfimages"]


def sistema():
    s = platform.system()
    if s == "Darwin":
        return "macos"
    if s == "Windows":
        return "windows"
    if s == "Linux":
        try:
            txt = open("/etc/os-release", encoding="utf-8").read().lower()
        except OSError:
            txt = ""
        if any(k in txt for k in ("debian", "ubuntu", "mint")):
            return "debian"
        if any(k in txt for k in ("fedora", "rhel", "centos")):
            return "fedora"
        return "linux"
    return s.lower()


def ambiente_gerenciado():
    """PEP 668: Python do sistema (Debian/Ubuntu, Homebrew) recusa `pip install` sem um sinalizador."""
    import sysconfig

    return os.path.exists(os.path.join(sysconfig.get_path("stdlib"), "EXTERNALLY-MANAGED"))


def python_cmd():
    """Caminho deste Python, sempre entre aspas e com barras normais (funciona no bash, no Git Bash do Windows e no zsh)."""
    return '"' + sys.executable.replace("\\", "/") + '"'


def comando_pip():
    em_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    extra = " --user --break-system-packages" if ambiente_gerenciado() and not em_venv else ""
    req = REQ.replace("\\", "/")
    return f'{python_cmd()} -m pip install{extra} -r "{req}"'


def minimos():
    """Versões mínimas de requirements.txt: {"reportlab": (4, 0), ...}."""
    m = {}
    for linha in open(REQ, encoding="utf-8"):
        linha = linha.strip()
        if ">=" in linha and not linha.startswith("#"):
            nome, ver = linha.split(">=", 1)
            m[nome.strip().lower()] = versao(ver)
    return m


def versao(txt):
    partes = []
    for p in txt.strip().split("."):
        num = "".join(ch for ch in p if ch.isdigit())
        if not num:
            break
        partes.append(int(num))
    return tuple(partes)


def instalar_python(so):
    return {
        "macos": ("brew install python", "ou o instalador de https://www.python.org/downloads/ (mais simples sem Homebrew)"),
        "windows": ("winget install -e --id Python.Python.3.12",
                    "ou o instalador de https://www.python.org/downloads/ marcando \"Add python.exe to PATH\"; depois reabra o app"),
        "debian": ("sudo apt-get install -y python3 python3-pip", "precisa de senha de administrador: a própria pessoa roda no terminal dela"),
        "fedora": ("sudo dnf install -y python3 python3-pip", "precisa de senha de administrador: a própria pessoa roda no terminal dela"),
    }.get(so, ("", "instale o Python 3.9 ou mais novo pelo gerenciador de pacotes do sistema"))


def comando_poppler(so):
    return {
        "macos": "brew install poppler (precisa do Homebrew: https://brew.sh)",
        "debian": "sudo apt-get install -y poppler-utils (a própria pessoa roda, com a senha dela)",
        "fedora": "sudo dnf install -y poppler-utils (a própria pessoa roda, com a senha dela)",
        "windows": "não precisa no Windows — sem ele o kit usa o pypdfium2 e funciona igual",
    }.get(so, "instale o pacote poppler (poppler-utils) do seu sistema")


def conferir():
    so = sistema()
    r = {"sistema": so, "python": sys.executable, "python_versao": platform.python_version(),
         "faltam_obrigatorios": [], "desatualizados": [], "avisos": [], "comandos": [], "notas": [], "ok": True}

    if sys.version_info < (3, 9):
        r["ok"] = False
        cmd, nota = instalar_python(so)
        r["avisos"].append(f"Python {platform.python_version()} é antigo demais: o plugin precisa do 3.9 ou mais novo")
        if cmd:
            r["comandos"].append(cmd)
        r["notas"].append(nota)

    try:
        from importlib.metadata import PackageNotFoundError, version as versao_instalada
    except ImportError:  # Python < 3.8
        versao_instalada, PackageNotFoundError = None, Exception
    mins = minimos() if os.path.exists(REQ) else {}
    for mod, pkg in OBRIGATORIOS:
        try:
            importlib.import_module(mod)
        except ImportError:
            r["faltam_obrigatorios"].append(pkg)
            continue
        if versao_instalada and pkg.lower() in mins:
            try:
                v = versao_instalada(pkg)
                if versao(v) < mins[pkg.lower()]:
                    r["desatualizados"].append(f"{pkg} {v}")
            except PackageNotFoundError:
                pass
    tem_pip = importlib.util.find_spec("pip") is not None

    if r["faltam_obrigatorios"] or r["desatualizados"]:
        r["ok"] = False
        if not tem_pip:
            em_venv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
            if so in ("debian", "fedora") and not em_venv:
                gerenciador = "apt-get" if so == "debian" else "dnf"
                r["comandos"].append(f"sudo {gerenciador} install -y python3-pip")
                r["notas"].append("o pip não está instalado neste Python; o comando acima precisa de senha de "
                                  "administrador: a própria pessoa roda no terminal dela")
            else:
                r["comandos"].append(f"{python_cmd()} -m ensurepip --upgrade")
                r["notas"].append("o pip não está instalado neste Python; o primeiro comando instala o pip")
        r["comandos"].append(comando_pip())
        if "--break-system-packages" in r["comandos"][-1]:
            r["notas"].append("--user --break-system-packages: este Python é o do sistema e é protegido; com --user as "
                              "bibliotecas vão só para a pasta do seu usuário, sem mexer no que o sistema usa")
        if r["desatualizados"]:
            r["notas"].append("bibliotecas antigas demais: " + ", ".join(r["desatualizados"])
                              + " — o mesmo comando atualiza")

    r["poppler"] = all(shutil.which(b) for b in POPPLER) and os.environ.get("GRAFICA_MOTOR", "").lower() != "pdfium"
    r["motor_pdf"] = "poppler" if r["poppler"] else "pypdfium2"
    if not r["poppler"]:
        r["avisos"].append("poppler não encontrado (opcional): prévias e checagens usam o pypdfium2. "
                           "Para instalar mesmo assim: " + comando_poppler(so))

    r["perfil_cmyk"] = None
    if r["faltam_obrigatorios"]:
        return r
    sys.path.insert(0, AQUI)
    try:
        from grafica_kit import perfil_cmyk

        icc = perfil_cmyk()
    except Exception:  # noqa: BLE001
        icc = None
    r["perfil_cmyk"] = icc
    if not icc:
        r["avisos"].append("sem perfil ICC CMYK (só importa se a gráfica exigir CMYK): peça o arquivo .icc à gráfica "
                           "e coloque-o na pasta de trabalho (ou defina a variável GRAFICA_ICC com o caminho dele)")
    return r


def teste_ponta_a_ponta(r):
    """Gera o cartão de exemplo numa pasta temporária, rasteriza a prévia e roda a pré-impressão."""
    pasta = tempfile.mkdtemp(prefix="grafica-teste-")
    env = dict(os.environ, PYTHONPATH=AQUI + os.pathsep + os.environ.get("PYTHONPATH", ""))
    passos = [
        ("gerar o PDF do cartão de exemplo", [sys.executable, os.path.join(AQUI, "exemplo_cartao.py")]),
        ("rasterizar a prévia", [sys.executable, os.path.join(AQUI, "rasterizar.py"), "cartao.pdf", "--previa"]),
        ("pré-impressão do PDF", [sys.executable, os.path.join(AQUI, "preflight.py"), "cartao.pdf"]),
    ]
    r["teste"] = {"pasta": pasta, "passos": []}
    for nome, cmd in passos:
        p = subprocess.run(cmd, cwd=pasta, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        ok = p.returncode == 0
        r["teste"]["passos"].append({"passo": nome, "ok": ok, "saida": (p.stdout + p.stderr).strip()[-600:]})
        if not ok:
            r["ok"] = False
            break


def main():
    r = conferir()
    if "--teste" in sys.argv and not r["faltam_obrigatorios"]:
        teste_ponta_a_ponta(r)
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit(0 if r["ok"] else 1)

    print(f"Sistema: {r['sistema']} · Python {r['python_versao']} ({r['python']})")
    if r["faltam_obrigatorios"]:
        print("✗ Faltam pacotes Python:", ", ".join(r["faltam_obrigatorios"]))
    if r["desatualizados"]:
        print("✗ Pacotes antigos demais:", ", ".join(r["desatualizados"]))
    if not r["faltam_obrigatorios"] and not r["desatualizados"]:
        print("✓ Pacotes Python ok")
    if not r["faltam_obrigatorios"] or r["poppler"]:
        print(f"✓ Motor de PDF: {r['motor_pdf']}")
    if r["perfil_cmyk"]:
        print(f"✓ Perfil CMYK: {r['perfil_cmyk']}")
    for a in r["avisos"]:
        print("! " + a)
    if r["comandos"]:
        print("\nPara resolver, rode (nesta ordem):")
        for c in r["comandos"]:
            print("  " + c)
    for n in r["notas"]:
        print("  obs.: " + n)
    if "teste" in r:
        for p in r["teste"]["passos"]:
            print(("✓ " if p["ok"] else "✗ ") + "teste: " + p["passo"])
            if not p["ok"]:
                print("    " + p["saida"].replace("\n", "\n    "))
        if r["ok"]:
            print(f"  (arquivos do teste em {r['teste']['pasta']})")
    print("\n" + ("dependências ok" if r["ok"] else "FALTA ALGO — veja acima"))
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    main()

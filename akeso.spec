# PyInstaller recipe for Akeso.exe
#
#   pip install pyinstaller
#   pyinstaller akeso.spec --noconfirm
#
# Result: dist\Akeso\Akeso.exe (a folder build: start-up is quick and the
# built-in browser engine works; a single-file .exe would unpack ~400 MB on
# every start). Zip the whole dist\Akeso folder to share it.

from pathlib import Path

ROOT = Path(SPECPATH)

datas = [
    (str(ROOT / "assets" / "anatomy"), "assets/anatomy"),     # 3D body
    (str(ROOT / "assets" / "LIGHTLOGO.png"), "assets"),
    (str(ROOT / "assets" / "DARKLOGO.png"), "assets"),
    (str(ROOT / "assets" / "akeso.ico"), "assets"),
    (str(ROOT / "data" / "emergency_ph.json"), "data"),
    (str(ROOT / "data" / "health_tips.json"), "data"),
    (str(ROOT / "THIRD_PARTY_NOTICES.md"), "."),
]
# Supabase address + publishable key. Only the PUBLISHABLE (anon) key may be
# in this file: it is readable by anyone who has the .exe. A .env placed
# next to Akeso.exe overrides the bundled one.
if (ROOT / ".env").exists():
    datas.append((str(ROOT / ".env"), "."))

a = Analysis(
    ["main.py"],
    pathex=[str(ROOT)],
    datas=datas,
    hiddenimports=[
        "PySide6.QtSvg",
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngineWidgets",
        "PySide6.QtWebChannel",
    ],
    excludes=["tkinter", "matplotlib", "numpy", "pytest", "IPython"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Akeso",
    icon=str(ROOT / "assets" / "akeso.ico"),
    console=False,               # no black console window
    upx=False,                   # UPX-packed Qt DLLs trip antivirus scanners
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    name="Akeso",
    upx=False,
)

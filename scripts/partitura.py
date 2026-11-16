#!/usr/bin/env python3
"""Convierte las contribuciones del último año en una partitura animada: assets/partitura.svg.

Cada semana es una nota. Su altura sale de cuántas contribuciones hubo esa semana, comparada con
el resto del año, y una semana sin actividad es un silencio. Un cabezal recorre el pentagrama y
enciende las notas al pasar.

Lee el token de GITHUB_TOKEN o, si no existe, de `gh auth token`. Solo hace una consulta GET a la
API GraphQL de GitHub, sin escribir nada.

Uso: python3 scripts/partitura.py [USUARIO]
"""
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

USUARIO = sys.argv[1] if len(sys.argv) > 1 else "jeffangeloss"
DESTINO = Path(__file__).resolve().parent.parent / "assets" / "partitura.svg"
CONSULTA = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{contributionCount}}}}}}"""
W, H = 840, 200
X0, X1 = 104, 820
LINEAS = [60, 76, 92, 108, 124]  # pentagrama, de arriba abajo
DURACION = 14  # segundos que tarda el cabezal en recorrerlo


def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def semanas():
    cuerpo = json.dumps({"query": CONSULTA, "variables": {"u": USUARIO}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=cuerpo,
        headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        cal = json.load(r)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["totalContributions"], [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cal["weeks"]]


def altura(valor, cortes):
    # Nueve posiciones posibles: líneas y espacios del pentagrama, de grave a agudo.
    posiciones = [132, 124, 116, 108, 100, 92, 84, 76, 68]
    nivel = sum(valor > c for c in cortes)
    return posiciones[min(nivel, len(posiciones) - 1)]


def main():
    total, por_semana = semanas()
    activos = sorted(v for v in por_semana if v > 0)
    cortes = [activos[int(len(activos) * k / 9)] for k in range(1, 9)] if activos else []
    paso = (X1 - X0) / max(len(por_semana), 1)
    figuras = []
    for i, v in enumerate(por_semana):
        x = X0 + paso * (i + 0.5)
        retraso = DURACION * (x - X0) / (X1 - X0)
        if v == 0:
            figuras.append(f'<rect x="{x - 3:.1f}" y="88" width="6" height="3" class="silencio"/>')
            continue
        y = altura(v, cortes)
        figuras.append(
            f'<g class="nota" style="animation-delay:{retraso:.2f}s"><title>{v} contribuciones</title>'
            f'<ellipse cx="{x:.1f}" cy="{y}" rx="5.2" ry="3.8" transform="rotate(-20 {x:.1f} {y})"/>'
            f'<line x1="{x + 4.6:.1f}" y1="{y}" x2="{x + 4.6:.1f}" y2="{y - 26}"/></g>'
        )
    lineas = "".join(f'<line x1="{X0 - 30}" y1="{y}" x2="{X1}" y2="{y}" class="linea"/>' for y in LINEAS)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Partitura de contribuciones: {total} contribuciones en el último año">
<style>
.fondo {{ fill: #0d1117 }} .linea {{ stroke: #3b4470; stroke-width: 1 }}
.clave {{ fill: #8b93c9; font: 64px "Apple Symbols","Segoe UI Symbol",serif }}
.titulo {{ fill: #c9d1ff; font: 600 15px "Segoe UI",Helvetica,Arial,sans-serif }}
.pie {{ fill: #8b93c9; font: 12px "Segoe UI",Helvetica,Arial,sans-serif }}
.silencio {{ fill: #3b4470 }}
.nota ellipse {{ fill: #7c8cff }} .nota line {{ stroke: #7c8cff; stroke-width: 1.4 }}
.nota {{ animation: suena {DURACION}s linear infinite }}
@keyframes suena {{ 0% {{ opacity: 1; filter: none }} 2% {{ opacity: 1; filter: drop-shadow(0 0 6px #c8b6ff) }} 8%,100% {{ opacity: .75; filter: none }} }}
.cabezal {{ animation: avanza {DURACION}s linear infinite }}
@keyframes avanza {{ from {{ transform: translateX(0) }} to {{ transform: translateX({X1 - X0}px) }} }}
@media (prefers-reduced-motion: reduce) {{ .nota,.cabezal {{ animation: none }} .cabezal {{ opacity: 0 }} }}
@media (prefers-color-scheme: light) {{ .fondo {{ fill: #f6f8ff }} .linea,.silencio {{ stroke: #b9c0e6; fill: #b9c0e6 }} .titulo {{ fill: #1f2a5c }} .pie,.clave {{ fill: #5560a0 }} }}
</style>
<rect class="fondo" width="{W}" height="{H}" rx="12"/>
<text class="titulo" x="{X0 - 30}" y="32">Partitura de contribuciones · último año</text>
<text class="clave" x="{X0 - 34}" y="128">𝄞</text>
{lineas}
{"".join(figuras)}
<g class="cabezal"><line x1="{X0}" y1="52" x2="{X0}" y2="140" stroke="#c8b6ff" stroke-width="2" opacity=".8"/></g>
<text class="pie" x="{X0 - 30}" y="176">{total} contribuciones · cada nota es una semana, más alta cuanto más activa · los silencios son semanas sin actividad</text>
</svg>
'''
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_text(svg, encoding="utf-8")
    print(f"{DESTINO.name}: {len(por_semana)} semanas, {total} contribuciones, {DESTINO.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

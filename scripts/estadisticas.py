#!/usr/bin/env python3
"""Arma assets/estadisticas.svg: las estadísticas de GitHub del último año, sin servicios externos.

Lee la API GraphQL de GitHub con GITHUB_TOKEN o, si no existe, con `gh auth token`, y solo
consulta, sin escribir nada. Cuenta contribuciones, commits, pull requests, revisiones, issues,
rachas y estrellas, y los lenguajes de los repos públicos propios (sin forks), por bytes de código.
El flujo partitura.yml lo corre cada día y publica el SVG en la rama `output`.

Uso: python3 scripts/estadisticas.py [USUARIO]
"""
import datetime as dt
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

USUARIO = sys.argv[1] if len(sys.argv) > 1 else "jeffangeloss"
DESTINO = Path(__file__).resolve().parent.parent / "assets" / "estadisticas.svg"
CONSULTA = """query($u:String!){user(login:$u){
 followers{totalCount}
 contributionsCollection{
  totalCommitContributions totalPullRequestContributions totalIssueContributions
  totalPullRequestReviewContributions totalRepositoriesWithContributedCommits
  contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}
 repositories(ownerAffiliations:OWNER, privacy:PUBLIC, isFork:false, first:100){
  totalCount nodes{stargazerCount languages(first:10, orderBy:{field:SIZE, direction:DESC}){edges{size node{name color}}}}}}}"""
IGNORAR = {"Jupyter Notebook", "HTML", "CSS", "Batchfile", "PowerShell", "Shell", "Dockerfile", "Makefile", "SCSS"}
W, H = 840, 250


def token():
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True, check=True).stdout.strip()


def consultar():
    cuerpo = json.dumps({"query": CONSULTA, "variables": {"u": USUARIO}}).encode()
    req = urllib.request.Request("https://api.github.com/graphql", data=cuerpo,
                                 headers={"Authorization": f"bearer {token()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        datos = json.load(r)
    if "errors" in datos:
        raise SystemExit(f"GraphQL: {datos['errors'][0].get('message')}")
    return datos["data"]["user"]


def rachas(dias):
    hoy = dt.date.today().isoformat()
    cuentas = [d["contributionCount"] for d in dias if d["date"] <= hoy]
    larga = actual = 0
    for c in cuentas:
        actual = actual + 1 if c else 0
        larga = max(larga, actual)
    i = len(cuentas) - 1
    if i >= 0 and cuentas[i] == 0:
        i -= 1  # hoy todavía puede sumar
    actual = 0
    while i >= 0 and cuentas[i]:
        actual += 1
        i -= 1
    return actual, larga


def miles(n):
    return f"{n:,}".replace(",", " ")


def main():
    u = consultar()
    cc = u["contributionsCollection"]
    dias = [d for w in cc["contributionCalendar"]["weeks"] for d in w["contributionDays"]]
    actual, larga = rachas(dias)
    estrellas = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
    lenguajes = {}
    for r in u["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            if n in IGNORAR:
                continue
            tam, color = lenguajes.get(n, (0, e["node"]["color"] or "#8fa2ff"))
            lenguajes[n] = (tam + e["size"], color)
    top = sorted(lenguajes.items(), key=lambda kv: -kv[1][0])[:6]
    total_bytes = sum(v[0] for _, v in top) or 1

    cifras = [
        ("Contribuciones", cc["contributionCalendar"]["totalContributions"], "M3 12h4l3-8 4 16 3-8h4"),
        ("Commits", cc["totalCommitContributions"], "M12 8a4 4 0 1 0 0 8a4 4 0 1 0 0-8 M2 12h6 M16 12h6"),
        ("Pull requests", cc["totalPullRequestContributions"], "M6 4v16 M18 20V10a4 4 0 0 0-4-4H9 M11 3 8 6l3 3"),
        ("Estrellas", estrellas, "M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"),
        ("Issues", cc["totalIssueContributions"], "M12 3a9 9 0 1 0 0 18a9 9 0 1 0 0-18 M12 8v5 M12 16v.1"),
        ("Repos con commits", cc["totalRepositoriesWithContributedCommits"], "M4 5a2 2 0 0 1 2-2h12v16H6a2 2 0 0 0-2 2z M8 7h6"),
        ("Racha actual", f"{actual} d", "M12 2c2 4 6 6 6 11a6 6 0 0 1-12 0c0-3 2-4 2-7 2 2 3 3 4 4 0-3 0-5 0-8z"),
        ("Racha más larga", f"{larga} d", "M8 21h8 M12 17v4 M7 4h10v4a5 5 0 0 1-10 0z M7 6H4a3 3 0 0 0 3 4 M17 6h3a3 3 0 0 1-3 4"),
    ]
    celdas = []
    for k, (rot, val, icono) in enumerate(cifras):
        col, fila = k % 2, k // 2
        x, y = 26 + col * 200, 62 + fila * 44
        val = miles(val) if isinstance(val, int) else val
        celdas.append(
            f'<g class="cifra" style="animation-duration:{.6 + k * .12:.2f}s" transform="translate({x},{y})">'
            f'<path class="ico" d="{icono}" transform="translate(0,-15) scale(.78)"/>'
            f'<text class="val" x="26" y="0">{escape(val)}</text><text class="rot" x="26" y="15">{escape(rot)}</text></g>')
    barras = []
    for k, (nombre, (tam, color)) in enumerate(top):
        pct = tam / total_bytes
        y = 66 + k * 27
        largo = max(pct * 260, 4)
        barras.append(
            f'<text class="len" x="460" y="{y}">{escape(nombre)}</text>'
            f'<text class="pct" x="814" y="{y}" text-anchor="end">{pct * 100:.1f} %</text>'
            f'<rect class="riel" x="460" y="{y + 6}" width="354" height="7" rx="3.5"/>'
            f'<rect class="barra" x="460" y="{y + 6}" width="{largo * 354 / 260:.1f}" height="7" rx="3.5" fill="{color}" style="animation-duration:{1.2 + k * .15:.2f}s,4s"/>')
    hoy = dt.date.today()
    meses = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "set", "oct", "nov", "dic"]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Estadísticas de GitHub del último año: {cc["contributionCalendar"]["totalContributions"]} contribuciones, {cc["totalCommitContributions"]} commits, {cc["totalPullRequestContributions"]} pull requests, racha más larga de {larga} días. Lenguajes: {", ".join(n for n, _ in top)}.">
<style>
.tarjeta {{ fill: #11162a; stroke: #2a3263 }}
.titulo {{ fill: #c9d1ff; font: 600 15px "Segoe UI",Helvetica,Arial,sans-serif }}
.val {{ fill: #e6ebff; font: 700 17px "Segoe UI",Helvetica,Arial,sans-serif }}
.rot,.pie {{ fill: #8b93c9; font: 11px "Segoe UI",Helvetica,Arial,sans-serif }}
.len {{ fill: #c9d1ff; font: 600 12px "Segoe UI",Helvetica,Arial,sans-serif }}
.pct {{ fill: #8b93c9; font: 11px "Segoe UI",Helvetica,Arial,sans-serif }}
.ico {{ fill: none; stroke: #8fa2ff; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round }}
.riel {{ fill: #1c2342 }}
.cifra {{ animation: entra 1s ease-out }}
@keyframes entra {{ from {{ opacity: .15 }} to {{ opacity: 1 }} }}
.barra {{ transform-box: fill-box; transform-origin: left; animation: crece 1.6s cubic-bezier(.2,.8,.2,1), late 4s ease-in-out 2s infinite }}
@keyframes crece {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}
@keyframes late {{ 0%,100% {{ opacity: 1 }} 50% {{ opacity: .7 }} }}
.brillo {{ animation: barre 7s ease-in-out infinite }}
@keyframes barre {{ 0% {{ transform: translateX(-160px) }} 50%,100% {{ transform: translateX({W + 160}px) }} }}
@media (prefers-color-scheme: light) {{ .tarjeta {{ fill: #f6f8ff; stroke: #c9d0f2 }} .titulo,.len {{ fill: #1f2a5c }} .val {{ fill: #111a44 }} .rot,.pct,.pie {{ fill: #4a5390 }} .ico {{ stroke: #4d5fd6 }} .riel {{ fill: #dfe4fb }} }}
@media (prefers-reduced-motion: reduce) {{ .cifra,.barra,.brillo {{ animation: none }} .brillo {{ display: none }} }}
</style>
<defs><linearGradient id="gb" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#9ec1ff" stop-opacity=".08"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="marco"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12"/></clipPath></defs>
<rect class="tarjeta" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12"/>
<text class="titulo" x="26" y="34">Último año en GitHub</text>
<text class="titulo" x="460" y="34">Lenguajes de mis repos públicos</text>
<line x1="436" y1="24" x2="436" y2="{H - 40}" stroke="#2a3263"/>
{"".join(celdas)}
{"".join(barras)}
<text class="pie" x="26" y="{H - 14}">{u["repositories"]["totalCount"]} repos públicos propios · {u["followers"]["totalCount"]} seguidores · actualizado el {hoy.day} {meses[hoy.month - 1]} {hoy.year}</text>
<g clip-path="url(#marco)"><rect class="brillo" x="0" y="0" width="160" height="{H}" fill="url(#gb)"/></g>
</svg>
'''
    DESTINO.write_text(svg, encoding="utf-8")
    print(f"{DESTINO.name}: {cc['contributionCalendar']['totalContributions']} contribuciones, racha {actual}/{larga}, "
          f"lenguajes {[n for n, _ in top]}, {DESTINO.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

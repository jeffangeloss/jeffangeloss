#!/usr/bin/env python3
"""Arma assets/estante-animes.svg: un estante con el póster de cada anime favorito, cada uno con su
propio efecto animado encima (viento, destellos, nieve, cometa, pétalos, estrellas y lluvia).

Los pósters salen de ~/fotos/imagenes-anime (material promocional oficial, ver FUENTES.txt), se
recortan a 2:3, se reducen a miniatura y se incrustan en base64 porque GitHub no carga imágenes
externas dentro de un SVG. El crédito va al pie del estante.

Uso: python3 scripts/construir_estante.py
"""
import base64
import io
from pathlib import Path

from PIL import Image

FOTOS = Path.home() / "fotos" / "imagenes-anime"
DESTINO = Path(__file__).resolve().parent.parent / "assets" / "estante-animes.svg"
PW, PH = 108, 160  # tamaño de cada póster en el SVG
X0, Y0, PASO = 12, 18, 118
W, H = 840, 252
CICLO = 14  # segundos para que el foco recorra los siete pósters

ANIMES = [
    ("Shingeki no Kyojin", "01-snk/poster-01-sin-texto.jpg", "viento"),
    ("Las quintillizas", "02-quintillizas/poster-01-sin-texto.jpg", "chispas"),
    ("Rompiendo el hielo", "03-rompiendo-el-hielo/portada-temporada-1.jpg", "nieve"),
    ("Your Name", "04-your-name/poster-01-sin-texto.jpg", "cometa"),
    ("Your Lie in April", "05-your-lie-in-april/poster-01-sin-texto.jpg", "petalos"),
    ("Oshi no Ko", "06-oshi-no-ko/poster-01-sin-texto.jpg", "estrellas"),
    ("El tiempo contigo", "07-el-tiempo-contigo/poster-02-sin-texto.jpg", "lluvia"),
]


def miniatura(ruta):
    img = Image.open(ruta).convert("RGB")
    w, h = img.size
    objetivo = 2 / 3
    if w / h > objetivo:
        nw = int(h * objetivo)
        img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / objetivo)
        img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    img = img.resize((PW * 2, PH * 2), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=72, optimize=True, progressive=True)
    return base64.b64encode(buf.getvalue()).decode()


def efecto(tipo):
    # Coordenadas locales del póster: 0..108 por 0..160.
    if tipo == "viento":
        return "".join(
            f'<line class="raf" x1="{x}" y1="{y}" x2="{x+22}" y2="{y-3}" style="animation-delay:{d}s"/>'
            for x, y, d in [(90, 30, 0), (70, 70, -.7), (100, 110, -1.4), (60, 140, -2.1)])
    if tipo == "chispas":
        colores = ["#ff8fb1", "#ffd76e", "#8fe3a1", "#8fb8ff", "#c79bff"]
        return "".join(
            f'<circle class="chi" cx="{14+i*20}" cy="148" r="4" fill="{c}" style="animation-delay:{i*.5}s"/>'
            for i, c in enumerate(colores))
    if tipo == "nieve":
        return "".join(
            f'<circle class="copo" cx="{x}" cy="0" r="{r}" style="animation-delay:{d}s"/>'
            for x, r, d in [(12, 1.8, 0), (34, 1.2, -1.5), (55, 2.2, -3), (78, 1.4, -.8), (96, 1.9, -2.2), (66, 1.1, -3.8)])
    if tipo == "cometa":
        return ('<g class="com"><line x1="0" y1="0" x2="26" y2="14" stroke="#e6f4ff" stroke-width="1.6" stroke-linecap="round"/>'
                '<line x1="4" y1="9" x2="26" y2="14" stroke="#ffb3d1" stroke-width="1.1" stroke-linecap="round"/>'
                '<circle cx="27" cy="14.5" r="2.2" fill="#fff"/></g>')
    if tipo == "petalos":
        return "".join(
            f'<ellipse class="pet" cx="{x}" cy="0" rx="3.6" ry="2.2" style="animation-delay:{d}s"/>'
            for x, d in [(16, 0), (48, -1.6), (80, -3.2), (30, -4.4)])
    if tipo == "estrellas":
        return "".join(
            f'<path class="est" d="M{x} {y} l2.4 5.6 6 .4 -4.6 3.8 1.6 6 -5.4 -3.4 -5.4 3.4 1.6 -6 -4.6 -3.8 6 -.4z" style="animation-delay:{d}s"/>'
            for x, y, d in [(20, 14, 0), (88, 40, -.7), (24, 120, -1.3)])
    if tipo == "lluvia":
        return "".join(
            f'<line class="got" x1="{x}" y1="0" x2="{x-3}" y2="10" style="animation-delay:{d}s"/>'
            for x, d in [(10, 0), (28, -.5), (46, -.25), (64, -.75), (82, -.15), (100, -.6)])
    return ""


def main():
    defs, cuerpo = [], []
    ranura = CICLO / len(ANIMES)
    for i, (nombre, archivo, tipo) in enumerate(ANIMES):
        datos = miniatura(FOTOS / archivo)
        x = X0 + i * PASO
        d = i * ranura
        defs.append(f'<clipPath id="c{i}"><rect width="{PW}" height="{PH}" rx="9"/></clipPath>')
        cuerpo.append(f'''<g transform="translate({x},{Y0})">
<g class="flota" style="animation-delay:{-i*0.7:.1f}s"><g class="foco" style="animation-delay:{d:.2f}s">
<g clip-path="url(#c{i})">
<image href="data:image/jpeg;base64,{datos}" width="{PW}" height="{PH}" preserveAspectRatio="xMidYMid slice"/>
<rect width="{PW}" height="{PH}" fill="url(#vela)"/>
{efecto(tipo)}
<g class="reflejo" style="animation-delay:{d:.2f}s"><rect x="-40" y="-20" width="26" height="{PH+40}" fill="url(#brillo)" transform="rotate(14)"/></g>
</g>
<rect class="marco" width="{PW}" height="{PH}" rx="9"/>
<rect class="aura" width="{PW}" height="{PH}" rx="9" style="animation-delay:{d:.2f}s"/>
</g></g>
<text class="nom" x="{PW/2}" y="{PH+22}" text-anchor="middle">{nombre}</text>
</g>''')
    pct = 100 / len(ANIMES)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Estante de animes favoritos: {", ".join(a[0] for a in ANIMES)}">
<style>
.marco {{ fill: none; stroke: #2a3263; stroke-width: 1 }}
.aura {{ fill: none; stroke: #b693ff; stroke-width: 2; opacity: 0; animation: aura {CICLO}s ease-in-out infinite }}
@keyframes aura {{ 0%,{pct*1.1:.1f}%,100% {{ opacity: 0 }} {pct*0.3:.1f}% {{ opacity: 1 }} }}
.foco {{ transform-box: fill-box; transform-origin: center; animation: foco {CICLO}s ease-in-out infinite }}
@keyframes foco {{ 0%,{pct*1.1:.1f}%,100% {{ transform: scale(1) }} {pct*0.3:.1f}% {{ transform: scale(1.06) }} }}
.flota {{ animation: flota 6s ease-in-out infinite }}
@keyframes flota {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(-5px) }} }}
.reflejo {{ animation: refleja {CICLO}s ease-in-out infinite }}
@keyframes refleja {{ 0% {{ transform: translateX(0) }} {pct*0.8:.1f}%,100% {{ transform: translateX(190px) }} }}
.nom {{ fill: #c9d1ff; font: 600 10.5px "Segoe UI",Helvetica,Arial,sans-serif }}
.pie {{ fill: #6f78ad; font: 10px "Segoe UI",Helvetica,Arial,sans-serif }}
.raf {{ stroke: #e6edff; stroke-width: 1.3; stroke-linecap: round; opacity: 0; animation: raf 2.8s linear infinite }}
@keyframes raf {{ 0% {{ transform: translateX(30px); opacity: 0 }} 20% {{ opacity: .8 }} 100% {{ transform: translateX(-120px); opacity: 0 }} }}
.chi {{ opacity: .25; animation: chi 2.5s ease-in-out infinite }}
@keyframes chi {{ 0%,100% {{ opacity: .25 }} 50% {{ opacity: 1 }} }}
.copo {{ fill: #f2fbff; animation: cae 4.5s linear infinite }}
@keyframes cae {{ from {{ transform: translateY(-6px) }} to {{ transform: translateY(166px) }} }}
.com {{ opacity: 0; animation: com 4s ease-in infinite }}
@keyframes com {{ 0% {{ transform: translate(-30px,-10px); opacity: 0 }} 15% {{ opacity: 1 }} 60%,100% {{ transform: translate(90px,55px); opacity: 0 }} }}
.pet {{ fill: #ffc4dc; animation: pet 6s ease-in-out infinite }}
@keyframes pet {{ 0% {{ transform: translate(0,-6px) rotate(0) }} 100% {{ transform: translate(30px,166px) rotate(260deg); opacity: .2 }} }}
.est {{ fill: #ffe38a; transform-box: fill-box; transform-origin: center; animation: est 2s ease-in-out infinite }}
@keyframes est {{ 0%,100% {{ transform: scale(.6); opacity: .4 }} 50% {{ transform: scale(1.2) rotate(25deg); opacity: 1 }} }}
.got {{ stroke: #cfe6ff; stroke-width: 1.2; opacity: .8; animation: got 1.1s linear infinite }}
@keyframes got {{ from {{ transform: translateY(-12px) }} to {{ transform: translateY(166px) }} }}
@media (prefers-color-scheme: light) {{ .nom {{ fill: #1f2a5c }} .pie {{ fill: #5560a0 }} .marco {{ stroke: #c9d0f2 }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important }} .aura,.com,.raf {{ opacity: 0 }} }}
</style>
<defs>
<linearGradient id="vela" x1="0" y1="0" x2="0" y2="1"><stop offset=".6" stop-color="#0b1026" stop-opacity="0"/><stop offset="1" stop-color="#0b1026" stop-opacity=".45"/></linearGradient>
<linearGradient id="brillo" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
{"".join(defs)}
</defs>
{"".join(cuerpo)}
<text class="pie" x="{W/2}" y="{H-8}" text-anchor="middle">Pósters promocionales oficiales © de sus estudios y titulares, vía TMDB y AniList. Uso de fan, sin fines comerciales.</text>
</svg>
'''
    DESTINO.write_text(svg, encoding="utf-8")
    print(f"{DESTINO.name}: {DESTINO.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

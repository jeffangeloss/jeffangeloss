#!/usr/bin/env python3
"""Arma assets/portada-viva.svg: la portada de LinkedIn incrustada en base64 con capas animadas encima.

Busca assets/portada.webp, .png o .jpg. Si no la encuentra, usa un degradado de reemplazo para
poder ver la animación. El SVG no usa scripts, fuentes externas ni imágenes externas, porque
GitHub los bloquea dentro de una imagen.

Uso: python3 scripts/construir_portada.py
"""
import base64
import random
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"
W, H = 1400, 350
TIPOS = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def fondo():
    for ext, tipo in TIPOS.items():
        archivo = ASSETS / f"portada{ext}"
        if archivo.exists():
            datos = base64.b64encode(archivo.read_bytes()).decode()
            return f'<image href="data:{tipo};base64,{datos}" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>', True
    reemplazo = (
        '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#0b1026"/><stop offset=".55" stop-color="#1a1440"/>'
        '<stop offset="1" stop-color="#2a0f3d"/></linearGradient></defs>'
        f'<rect width="{W}" height="{H}" fill="url(#g)"/>'
        '<text x="700" y="160" text-anchor="middle" font-size="34" fill="#c9d1ff" opacity=".9" '
        'font-family="Segoe UI,Helvetica,Arial,sans-serif">Aquí va tu portada</text>'
        '<text x="700" y="200" text-anchor="middle" font-size="18" fill="#8b93c9" '
        'font-family="Segoe UI,Helvetica,Arial,sans-serif">guárdala como assets/portada.webp y vuelve a correr este script</text>'
    )
    return reemplazo, False


def particulas(n=46, semilla=7):
    rnd = random.Random(semilla)
    capas = []
    for i in range(n):
        x, y = rnd.uniform(0, W), rnd.uniform(0, H)
        r = rnd.choice([1.0, 1.2, 1.6, 2.0])
        color = rnd.choice(["#8fb8ff", "#b693ff", "#e6edff"])
        dur = rnd.uniform(2.5, 5.5)
        retraso = rnd.uniform(0, 5)
        capas.append(
            f'<circle class="p" cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{color}" '
            f'style="animation-duration:{dur:.1f}s;animation-delay:{retraso:.1f}s"/>'
        )
    return "\n".join(capas)


def pulso():
    # Trazo de electrocardiograma que recorre la franja inferior: la faceta biomédica.
    puntos, x = [], 0
    while x <= W:
        puntos += [(x, 322), (x + 60, 322), (x + 70, 312), (x + 80, 322), (x + 92, 322),
                   (x + 98, 296), (x + 104, 338), (x + 110, 322), (x + 170, 322)]
        x += 170
    d = " ".join(f"{px},{py}" for px, py in puntos if px <= W)
    return (
        f'<polyline class="ecg" points="{d}" fill="none" stroke="#7cc4ff" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round" opacity=".55"/>'
    )


def notas():
    # Notas que suben por el borde derecho: la viola.
    simbolos = [("♪", 1250, 0.0), ("♫", 1300, 1.6), ("♩", 1340, 3.1), ("♬", 1215, 4.4)]
    return "\n".join(
        f'<text class="nota" x="{x}" y="300" font-size="22" fill="#d6c2ff" '
        f'style="animation-delay:{d}s">{s}</text>'
        for s, x, d in simbolos
    )


def main():
    capa_fondo, real = fondo()
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Portada de Jefferson Sanchez: Ciencia + Tecnología + Arte = Impacto">
<style>
.p {{ animation-name: titila; animation-iteration-count: infinite; animation-timing-function: ease-in-out; opacity: .15; }}
@keyframes titila {{ 0%,100% {{ opacity: .1 }} 50% {{ opacity: .9 }} }}
.ecg {{ stroke-dasharray: 1400; stroke-dashoffset: 1400; animation: traza 6s linear infinite; }}
@keyframes traza {{ 0% {{ stroke-dashoffset: 1400 }} 70% {{ stroke-dashoffset: 0; opacity: .6 }} 100% {{ stroke-dashoffset: 0; opacity: 0 }} }}
.nota {{ opacity: 0; animation: sube 6s ease-out infinite; font-family: "Segoe UI Symbol","Apple Symbols",serif; }}
@keyframes sube {{ 0% {{ opacity: 0; transform: translateY(0) }} 20% {{ opacity: .85 }} 100% {{ opacity: 0; transform: translateY(-150px) }} }}
.barrido {{ animation: barre 9s ease-in-out infinite; }}
@keyframes barre {{ 0% {{ transform: translateX(-500px) }} 55%,100% {{ transform: translateX(1500px) }} }}
.cometa {{ opacity: 0; animation: cruza 11s ease-in infinite; animation-delay: 2s }}
@keyframes cruza {{ 0% {{ opacity: 0; transform: translate(150px,10px) }} 4% {{ opacity: 1 }} 22% {{ opacity: 0; transform: translate(700px,200px) }} 100% {{ opacity: 0; transform: translate(700px,200px) }} }}
@media (prefers-reduced-motion: reduce) {{ .p,.ecg,.nota,.barrido,.cometa {{ animation: none }} .ecg {{ stroke-dashoffset: 0 }} }}
</style>
<defs>
<linearGradient id="luz" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#9ec1ff" stop-opacity=".10"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="marco"><rect width="{W}" height="{H}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#marco)">
{capa_fondo}
<rect class="barrido" x="0" y="0" width="420" height="{H}" fill="url(#luz)"/>
{particulas()}
<g class="cometa"><line x1="0" y1="0" x2="90" y2="34" stroke="#bfe3ff" stroke-width="2" stroke-linecap="round"/><line x1="10" y1="16" x2="90" y2="34" stroke="#ffb3d1" stroke-width="1.4" stroke-linecap="round"/><circle cx="92" cy="35" r="3.2" fill="#ffffff"/></g>
{pulso()}
{notas()}
</g>
</svg>
'''
    destino = ASSETS / "portada-viva.svg"
    destino.write_text(svg, encoding="utf-8")
    print(f"{destino.name}: {destino.stat().st_size:,} bytes, portada real: {'sí' if real else 'no (reemplazo)'}")


if __name__ == "__main__":
    main()

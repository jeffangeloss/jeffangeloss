#!/usr/bin/env python3
"""Arma las piezas animadas del perfil: titular con tipeo, separador, pie y brillo de los botones.

Todo es SVG con CSS y SMIL, sin scripts, fuentes ni imágenes externas, porque GitHub los bloquea
dentro de una imagen. Respeta prefers-reduced-motion y prefers-color-scheme.

Uso: python3 scripts/construir_animaciones.py
"""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"
MONO = '"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace'

ROLES = [
    "Ingeniería de Sistemas · Universidad de Lima",
    "Full-stack · DevOps",
    "IA y machine learning",
    "IoT con ESP32",
    "Ciberseguridad",
    "Violista",
    "Ciencia + Tecnología + Arte = Impacto",
]


def titular():
    # Cada rol se escribe letra por letra, se queda un momento y se borra; luego entra el siguiente.
    W, H, fs = 840, 56, 22
    ancho_letra = fs * 0.602
    ranura = 3.6  # segundos por rol
    T = ranura * len(ROLES)
    piezas = []
    for i, rol in enumerate(ROLES):
        n = len(rol)
        w = n * ancho_letra
        x0 = (W - w) / 2
        inicio = i * ranura / T
        fin_tipeo = inicio + (ranura * 0.45) / T
        fin_pausa = inicio + (ranura * 0.82) / T
        fin_borrado = inicio + (ranura * 0.97) / T
        tiempos, anchos = [0.0], [0.0]
        for k in range(n + 1):
            tiempos.append(inicio + (fin_tipeo - inicio) * k / n)
            anchos.append(k * ancho_letra)
        tiempos.append(fin_pausa)
        anchos.append(w)
        pasos_borrado = 8
        for k in range(1, pasos_borrado + 1):
            tiempos.append(fin_pausa + (fin_borrado - fin_pausa) * k / pasos_borrado)
            anchos.append(w * (1 - k / pasos_borrado))
        tiempos.append(1.0)
        anchos.append(0.0)
        # keyTimes debe ser creciente y empezar en 0; se quitan duplicados conservando el último.
        pares = {}
        for t, a in zip(tiempos, anchos):
            pares[round(t, 5)] = a
        kt = sorted(pares)
        kts = ";".join(f"{t:.5f}" for t in kt)
        vals = ";".join(f"{pares[t]:.1f}" for t in kt)
        cursor = ";".join(f"{x0 + pares[t]:.1f}" for t in kt)
        visible = ";".join("1" if inicio <= t < fin_borrado else "0" for t in kt)
        piezas.append(f'''<clipPath id="r{i}"><rect x="{x0:.1f}" y="0" width="0" height="{H}">
<animate attributeName="width" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kts}" values="{vals}"/></rect></clipPath>
<text class="rol" x="{x0:.1f}" y="36" clip-path="url(#r{i})">{escape(rol)}</text>
<rect class="cursor" x="{x0:.1f}" y="17" width="2.5" height="25" opacity="0">
<animate attributeName="x" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kts}" values="{cursor}"/>
<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kts}" values="{visible}"/></rect>''')
    estatico = escape(" · ".join(["Full-stack", "DevOps", "IA", "IoT", "Ciberseguridad", "Violista"]))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(", ".join(ROLES))}">
<style>
.rol {{ fill: #c9d1ff; font: 500 {fs}px {MONO} }}
.cursor {{ fill: #b693ff }}
.quieto {{ display: none; fill: #c9d1ff; font: 500 18px {MONO} }}
@media (prefers-color-scheme: light) {{ .rol,.quieto {{ fill: #1f2a5c }} .cursor {{ fill: #6b4fd6 }} }}
@media (prefers-reduced-motion: reduce) {{ .rol,.cursor {{ display: none }} .quieto {{ display: inline }} }}
</style>
<defs>{"".join(p.split("</clipPath>")[0] + "</clipPath>" for p in piezas)}</defs>
{"".join(p.split("</clipPath>", 1)[1] for p in piezas)}
<text class="quieto" x="{W/2}" y="34" text-anchor="middle">{estatico}</text>
</svg>
'''
    return svg


def separador():
    # Línea fina con un latido que la recorre: el pulso biomédico convertido en divisor de secciones.
    W, H = 840, 28
    y = 14
    latido = f"M0 {y} h18 l4 -6 l4 6 h6 l3 -12 l4 22 l3 -10 h40"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Separador">
<style>
.base {{ stroke: #2a3263; stroke-width: 1 }}
.pulso {{ fill: none; stroke: url(#tr); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; animation: corre 4.5s linear infinite }}
@keyframes corre {{ from {{ transform: translateX(-90px) }} to {{ transform: translateX({W}px) }} }}
.nota {{ fill: #b693ff; font: 13px "Apple Symbols","Segoe UI Symbol",serif; animation: aparece 4.5s ease-in-out infinite }}
@keyframes aparece {{ 0%,40% {{ opacity: 0; transform: translateY(4px) }} 55% {{ opacity: .9; transform: translateY(0) }} 75%,100% {{ opacity: 0; transform: translateY(-6px) }} }}
@media (prefers-color-scheme: light) {{ .base {{ stroke: #c9d0f2 }} }}
@media (prefers-reduced-motion: reduce) {{ .pulso,.nota {{ animation: none }} .nota {{ opacity: 0 }} }}
</style>
<defs><linearGradient id="tr" x1="0" x2="1"><stop offset="0" stop-color="#7cc4ff" stop-opacity="0"/><stop offset=".7" stop-color="#8fa2ff"/><stop offset="1" stop-color="#e6edff"/></linearGradient></defs>
<line class="base" x1="0" y1="{y}" x2="{W}" y2="{y}"/>
<path class="pulso" d="{latido}"/>
<text class="nota" x="{W/2}" y="10" text-anchor="middle">♪</text>
</svg>
'''


def pie():
    # Ondas que avanzan en tres capas, con el lema de la portada de LinkedIn.
    W, H = 840, 120

    def onda(y, amp, largo):
        d = f"M0 {y}"
        x = 0
        while x < W * 2 + largo:
            d += f" q{largo/4} {-amp} {largo/2} 0 t{largo/2} 0"
            x += largo
        return d + f" V{H} H0 Z"

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Ciencia + Tecnología + Arte = Impacto">
<style>
.o1 {{ fill: #1b2a6b; opacity: .55; animation: ola 9s linear infinite }}
.o2 {{ fill: #3b1f5c; opacity: .6; animation: ola 6s linear infinite reverse }}
.o3 {{ fill: #2a3a8f; opacity: .5; animation: ola 12s linear infinite }}
@keyframes ola {{ from {{ transform: translateX(0) }} to {{ transform: translateX(-{W}px) }} }}
.lema {{ fill: #e6ebff; font: 600 16px "Segoe UI",Helvetica,Arial,sans-serif; letter-spacing: .5px; animation: respira 5s ease-in-out infinite }}
@keyframes respira {{ 0%,100% {{ opacity: .7 }} 50% {{ opacity: 1 }} }}
@media (prefers-reduced-motion: reduce) {{ .o1,.o2,.o3,.lema {{ animation: none }} }}
</style>
<defs><clipPath id="m"><rect width="{W}" height="{H}" rx="12"/></clipPath></defs>
<g clip-path="url(#m)">
<path class="o3" d="{onda(70, 16, 280)}"/>
<path class="o1" d="{onda(82, 12, 210)}"/>
<path class="o2" d="{onda(94, 10, 168)}"/>
</g>
<text class="lema" x="{W/2}" y="44" text-anchor="middle">Ciencia + Tecnología + Arte = Impacto</text>
</svg>
'''


def brillo_botones():
    # Un destello cruza cada botón por turnos, como un reflejo sobre metal.
    retrasos = {"boton-linkedin.svg": 0, "boton-correo.svg": 1.2, "boton-repos.svg": 2.4}
    for nombre, d in retrasos.items():
        ruta = ASSETS / nombre
        svg = ruta.read_text(encoding="utf-8")
        if "destello" in svg:
            continue
        ancho = float(svg.split('viewBox="0 0 ')[1].split()[0])
        estilo = (f".destello{{animation:cruza 4.5s ease-in-out {d}s infinite;transform:translateX(-60px)}}"
                  f"@keyframes cruza{{0%{{transform:translateX(-60px)}}30%,100%{{transform:translateX({ancho+20:.0f}px)}}}}"
                  f".borde{{fill:none;stroke:#b693ff;stroke-width:1.5;opacity:0;animation:aura 4.5s ease-in-out {d}s infinite}}"
                  f"@keyframes aura{{0%,100%{{opacity:0}}15%{{opacity:.9}}35%{{opacity:0}}}}"
                  "@media (prefers-reduced-motion: reduce){.destello,.borde{animation:none;opacity:0}}")
        svg = svg.replace("</style>", estilo + "</style>", 1)
        capa = (f'<defs><clipPath id="cb"><rect x="1" y="1" width="{ancho-2:.0f}" height="38" rx="10"/></clipPath>'
                '<linearGradient id="gd" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                '<stop offset=".5" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
                f'<g clip-path="url(#cb)"><g class="destello"><rect x="0" y="0" width="40" height="40" fill="url(#gd)" transform="skewX(-20)"/></g></g>'
                f'<rect class="borde" x="1" y="1" width="{ancho-2:.0f}" height="38" rx="10"/>')
        svg = svg.replace("</svg>", capa + "</svg>")
        ruta.write_text(svg, encoding="utf-8")


def main():
    for nombre, contenido in [("titular.svg", titular()), ("separador.svg", separador()), ("pie.svg", pie())]:
        (ASSETS / nombre).write_text(contenido, encoding="utf-8")
        print(f"{nombre}: {(ASSETS / nombre).stat().st_size:,} bytes")
    brillo_botones()
    print("botones: destello y aura agregados")


if __name__ == "__main__":
    main()

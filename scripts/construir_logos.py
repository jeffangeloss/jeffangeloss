#!/usr/bin/env python3
"""Arma assets/muro-logos.svg: un muro animado con los logos de las tecnologías que uso.

Los íconos vienen de skill-icons (licencia MIT, assets/iconos/LICENSE-skill-icons.txt) y se
guardan en el repo, así que el muro no depende de skillicons.dev ni de otro servicio. Cada ícono
entra como imagen en base64 para que sus ids internos no choquen entre sí. Los logos hacen una ola
y un brillo recorre cada fila. Respeta prefers-reduced-motion y prefers-color-scheme.

Uso: python3 scripts/construir_logos.py
"""
import base64
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
ICONOS = RAIZ / "assets" / "iconos"
DESTINO = RAIZ / "assets" / "muro-logos.svg"

FILAS = [
    ("Lenguajes", [("python", "Python"), ("ts", "TypeScript"), ("js", "JavaScript"), ("java", "Java"),
                   ("dart", "Dart"), ("c", "C"), ("cpp", "C++"), ("haxe", "Haxe"), ("bash", "Bash")]),
    ("Web y móvil", [("react", "React"), ("vite", "Vite"), ("tailwind", "Tailwind CSS"), ("nextjs", "Next.js"),
                     ("nodejs", "Node.js"), ("bun", "Bun"), ("fastapi", "FastAPI"), ("spring", "Spring Boot"),
                     ("flutter", "Flutter"), ("firebase", "Firebase"), ("html", "HTML"), ("css", "CSS")]),
    ("Datos, IA y DevOps", [("postgres", "PostgreSQL"), ("sqlite", "SQLite"), ("prisma", "Prisma"),
                            ("sklearn", "scikit-learn"), ("git", "Git"), ("github", "GitHub"),
                            ("githubactions", "GitHub Actions"), ("docker", "Docker"), ("vercel", "Vercel"),
                            ("aws", "AWS")]),
    ("Sistemas, IoT y herramientas", [("linux", "Linux"), ("redhat", "Red Hat"), ("kali", "Kali Linux"),
                                      ("arduino", "Arduino"), ("raspberrypi", "Raspberry Pi"), ("vscode", "VS Code"),
                                      ("figma", "Figma"), ("notion", "Notion")]),
]
W = 840
TAM, PASO = 46, 58
ALTO_FILA = 92


def main():
    capas = []
    y = 8
    for f, (titulo, iconos) in enumerate(FILAS):
        ancho = (len(iconos) - 1) * PASO + TAM
        x0 = (W - ancho) / 2
        capas.append(f'<text class="rot" x="{W/2}" y="{y + 14}" text-anchor="middle">{titulo}</text>')
        fila_y = y + 24
        for c, (clave, nombre) in enumerate(iconos):
            datos = base64.b64encode((ICONOS / f"{clave}.svg").read_bytes()).decode()
            retraso = c * 0.14 + f * 0.35
            capas.append(
                f'<g transform="translate({x0 + c * PASO:.1f},{fila_y})"><g class="ola" style="animation-delay:{retraso:.2f}s">'
                f'<title>{nombre}</title>'
                f'<image href="data:image/svg+xml;base64,{datos}" width="{TAM}" height="{TAM}"/>'
                f'<rect class="aro" x="-2" y="-2" width="{TAM + 4}" height="{TAM + 4}" rx="12" style="animation-delay:{c * 0.5 + f * 0.25:.2f}s"/>'
                '</g></g>')
        capas.append(
            f'<g clip-path="url(#f{f})"><rect class="luz" x="{x0 - 90}" y="{fila_y - 4}" width="70" height="{TAM + 8}" '
            f'fill="url(#gl)" style="animation-delay:{f * 1.3:.1f}s"/></g>')
        capas.insert(0, f'<clipPath id="f{f}"><rect x="{x0 - 4}" y="{fila_y - 6}" width="{ancho + 8}" height="{TAM + 12}" rx="12"/></clipPath>')
        y += ALTO_FILA
    H = y + 4
    defs = "".join(c for c in capas if c.startswith("<clipPath"))
    cuerpo = "".join(c for c in capas if not c.startswith("<clipPath"))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Tecnologías: {", ".join(n for _, ic in FILAS for _, n in ic)}">
<!-- Íconos de skill-icons (https://github.com/tandpfun/skill-icons), licencia MIT. -->
<style>
.rot {{ fill: #8b93c9; font: 600 12px "Segoe UI",Helvetica,Arial,sans-serif; letter-spacing: .6px; text-transform: uppercase }}
.ola {{ animation: ola 3.2s ease-in-out infinite }}
@keyframes ola {{ 0%,100% {{ transform: translateY(0) }} 25% {{ transform: translateY(-6px) }} 50% {{ transform: translateY(0) }} }}
.aro {{ fill: none; stroke: #b693ff; stroke-width: 1.6; opacity: 0; animation: aro 6s ease-in-out infinite }}
@keyframes aro {{ 0%,100% {{ opacity: 0 }} 8% {{ opacity: .9 }} 18% {{ opacity: 0 }} }}
.luz {{ animation: luz 5.2s ease-in-out infinite }}
@keyframes luz {{ 0% {{ transform: translateX(0) }} 60%,100% {{ transform: translateX({W}px) }} }}
@media (prefers-color-scheme: light) {{ .rot {{ fill: #4a5390 }} .aro {{ stroke: #6b4fd6 }} }}
@media (prefers-reduced-motion: reduce) {{ .ola,.aro,.luz {{ animation: none }} .aro {{ opacity: 0 }} .luz {{ display: none }} }}
</style>
<defs><linearGradient id="gl" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>{defs}</defs>
{cuerpo}
</svg>
'''
    DESTINO.write_text(svg, encoding="utf-8")
    print(f"{DESTINO.name}: {sum(len(i) for _, i in FILAS)} logos, {DESTINO.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()

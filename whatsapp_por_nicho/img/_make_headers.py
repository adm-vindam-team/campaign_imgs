#!/usr/bin/env python3
"""Genera las 14 imágenes de encabezado (1200x628) de las plantillas WhatsApp.

Sistema visual único: fondo oscuro tech, wordmark VINDAM, ícono y color de
acento por rubro, titular corto. Deja el .svg fuente junto a cada .png.

Uso (python no está en el PATH de esta máquina; requiere inkscape):
    /usr/bin/python3 _make_headers.py
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1200, 628

# Ícono = fragmento SVG en viewBox 24x24, stroke currentColor (se escala x10.5).
NICHOS = {
    "dentista": dict(
        kicker="CLÍNICAS DENTALES",
        l1="Su agenda dental,", l2="en automático",
        accent="#4FC3F7",
        icon='<path d="M12 5.5C10.5 4 9 3 7.5 3 4.5 3 3 5 3 7.5c0 4 1.5 5 2 8.5.3 2.2.8 5 2.2 5 1.7 0 1.3-3 2.3-5.5.4-1 .6-1.5 2.5-1.5s2.1.5 2.5 1.5c1 2.5.6 5.5 2.3 5.5 1.4 0 1.9-2.8 2.2-5 .5-3.5 2-4.5 2-8.5C21 5 19.5 3 16.5 3 15 3 13.5 4 12 5.5Z"/>',
    ),
    "gimnasio": dict(
        kicker="GIMNASIOS",
        l1="Ningún interesado", l2="se enfría",
        accent="#FF7043",
        icon=('<line x1="7.5" y1="12" x2="16.5" y2="12"/>'
              '<rect x="4.2" y="7.2" width="3" height="9.6" rx="1.2"/>'
              '<rect x="16.8" y="7.2" width="3" height="9.6" rx="1.2"/>'
              '<rect x="1.6" y="9.2" width="1.8" height="5.6" rx="0.9"/>'
              '<rect x="20.6" y="9.2" width="1.8" height="5.6" rx="0.9"/>'),
    ),
    "inmobiliaria": dict(
        kicker="INMOBILIARIAS",
        l1="Ningún lead", l2="sin respuesta",
        accent="#FFD54F",
        icon=('<path d="M3 11 12 3l9 8"/>'
              '<path d="M5.5 9.8V20h13V9.8"/>'
              '<path d="M10 20v-5.5h4V20"/>'),
    ),
    "veterinaria": dict(
        kicker="VETERINARIAS",
        l1="Citas y recordatorios,", l2="en piloto automático",
        accent="#81C784",
        icon=('<circle cx="7" cy="7.6" r="2"/>'
              '<circle cx="12" cy="5.8" r="2"/>'
              '<circle cx="17" cy="7.6" r="2"/>'
              '<path d="M12 11c-2.8 0-5.4 2.1-5.4 4.6 0 1.7 1.3 2.9 3 2.9 1 0 1.7-.4 2.4-.4s1.4.4 2.4.4c1.7 0 3-1.2 3-2.9C17.4 13.1 14.8 11 12 11Z"/>'),
    ),
    "salon_de_belleza": dict(
        kicker="SALONES DE BELLEZA",
        l1="Reservas sin", l2="soltar la tijera",
        accent="#F48FB1",
        icon=('<circle cx="6" cy="6" r="2.6"/>'
              '<circle cx="6" cy="18" r="2.6"/>'
              '<line x1="8.1" y1="7.6" x2="20" y2="17.5"/>'
              '<line x1="8.1" y1="16.4" x2="20" y2="6.5"/>'),
    ),
    "optica": dict(
        kicker="ÓPTICAS",
        l1="Exámenes y entregas,", l2="sin llamadas",
        accent="#64B5F6",
        icon=('<circle cx="6.8" cy="13.5" r="4"/>'
              '<circle cx="17.2" cy="13.5" r="4"/>'
              '<path d="M10.8 12.5c.7-.9 1.7-.9 2.4 0"/>'
              '<path d="M2.8 12.5 2 9.5"/><path d="M21.2 12.5 22 9.5"/>'),
    ),
    "dermatologo": dict(
        kicker="DERMATOLOGÍA",
        l1="Su consulta,", l2="siempre disponible",
        accent="#CE93D8",
        icon=('<path d="M11 4l1.8 5.2L18 11l-5.2 1.8L11 18l-1.8-5.2L4 11l5.2-1.8Z"/>'
              '<path d="M19 3l.8 1.7 1.7.8-1.7.8L19 8l-.8-1.7-1.7-.8 1.7-.8Z"/>'
              '<circle cx="18.6" cy="18" r="1" fill="currentColor" stroke="none"/>'),
    ),
    "pediatra": dict(
        kicker="PEDIATRÍA",
        l1="Los papás, atendidos", l2="a toda hora",
        accent="#4DD0E1",
        icon=('<circle cx="12" cy="13" r="6.5"/>'
              '<path d="M12 6.5c0-1.6 1-2.6 2.6-2.6"/>'
              '<path d="M9.5 15c.8.9 1.6 1.3 2.5 1.3s1.7-.4 2.5-1.3"/>'
              '<circle cx="9.8" cy="12.2" r="0.8" fill="currentColor" stroke="none"/>'
              '<circle cx="14.2" cy="12.2" r="0.8" fill="currentColor" stroke="none"/>'),
    ),
    "ginecologo": dict(
        kicker="GINECOLOGÍA",
        l1="Citas y controles,", l2="en automático",
        accent="#F06292",
        icon=('<circle cx="12" cy="8.5" r="5.5"/>'
              '<line x1="12" y1="14" x2="12" y2="21.5"/>'
              '<line x1="8.8" y1="18.2" x2="15.2" y2="18.2"/>'),
    ),
    "cardiologo": dict(
        kicker="CARDIOLOGÍA",
        l1="Cada cita,", l2="confirmada a tiempo",
        accent="#EF5350",
        icon=('<path d="M12 20.5C7 16.5 3.5 13.5 3.5 9.7 3.5 7 5.6 5 8.2 5c1.6 0 3 .8 3.8 2 .8-1.2 2.2-2 3.8-2 2.6 0 4.7 2 4.7 4.7 0 3.8-3.5 6.8-8.5 10.8Z"/>'
              '<path d="M6.5 11.5h3l1.3-2.6 2.3 5.2 1.5-2.6h3"/>'),
    ),
    "oftalmologo": dict(
        kicker="OFTALMOLOGÍA",
        l1="Su agenda,", l2="siempre clara",
        accent="#7986CB",
        icon=('<path d="M2.5 12S6 5.8 12 5.8 21.5 12 21.5 12 18 18.2 12 18.2 2.5 12 2.5 12Z"/>'
              '<circle cx="12" cy="12" r="3"/>'
              '<circle cx="12" cy="12" r="1" fill="currentColor" stroke="none"/>'),
    ),
    "ortopedista": dict(
        kicker="ORTOPEDIA",
        l1="Controles y terapias,", l2="al día",
        accent="#B0BEC5",
        icon=('<circle cx="5" cy="9.8" r="2.3"/>'
              '<circle cx="5" cy="14.2" r="2.3"/>'
              '<circle cx="19" cy="9.8" r="2.3"/>'
              '<circle cx="19" cy="14.2" r="2.3"/>'
              '<path d="M6.8 12h10.4" stroke-width="3.4"/>'),
    ),
    "cirujano_plastico": dict(
        kicker="CIRUGÍA PLÁSTICA Y ESTÉTICA",
        l1="Valoraciones agendadas", l2="con discreción",
        accent="#BA68C8",
        icon=('<path d="M12 4c-2 3-2 6.2 0 8.8 2-2.6 2-5.8 0-8.8Z"/>'
              '<path d="M6.2 7.2c-.4 3.6 1 6.4 4.3 8"/>'
              '<path d="M17.8 7.2c.4 3.6-1 6.4-4.3 8"/>'
              '<path d="M3.8 13.2c1 4.2 4.1 6.8 8.2 6.8s7.2-2.6 8.2-6.8c-2.6-.6-5.3-.2-8.2 1.6-2.9-1.8-5.6-2.2-8.2-1.6Z"/>'),
    ),
    "automotriz": dict(
        kicker="TALLERES AUTOMOTRICES",
        l1="Cotizaciones que", l2="no se enfrían",
        accent="#9CCC65",
        icon='<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
    ),
}

FONT = "Noto Sans"


def svg_for(spec):
    a = spec["accent"]
    # chip del ícono, centro-derecha
    cx, cy = 948, 300
    icon_scale = 10.5
    icon_half = 12 * icon_scale
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0" stop-color="#0B1120"/>',
        '    <stop offset="1" stop-color="#141E38"/>',
        '  </linearGradient>',
        f'  <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">',
        f'    <stop offset="0" stop-color="{a}" stop-opacity="0.28"/>',
        f'    <stop offset="1" stop-color="{a}" stop-opacity="0"/>',
        '  </radialGradient>',
        '</defs>',
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        # retícula de puntos sutil
        '<g fill="#3A4A6B" opacity="0.35">',
    ]
    for gx in range(60, W, 76):
        for gy in range(56, H, 76):
            parts.append(f'<circle cx="{gx}" cy="{gy}" r="1.4"/>')
    parts += [
        '</g>',
        # resplandor + chip del ícono
        f'<circle cx="{cx}" cy="{cy}" r="290" fill="url(#glow)"/>',
        f'<circle cx="{cx}" cy="{cy}" r="212" fill="none" stroke="{a}" stroke-opacity="0.22" stroke-width="1.6"/>',
        f'<circle cx="{cx}" cy="{cy}" r="238" fill="none" stroke="{a}" stroke-opacity="0.10" stroke-width="1.2"/>',
        f'<circle cx="{cx}" cy="{cy}" r="168" fill="#18233F" stroke="{a}" stroke-opacity="0.55" stroke-width="2"/>',
        # puntos orbitales
        f'<circle cx="{cx - 212}" cy="{cy}" r="5" fill="{a}"/>',
        f'<circle cx="{cx + 150}" cy="{cy - 150}" r="3.6" fill="{a}" opacity="0.7"/>',
        f'<circle cx="{cx + 96}" cy="{cy + 213}" r="4.4" fill="{a}" opacity="0.5"/>',
        # ícono
        f'<g transform="translate({cx - icon_half},{cy - icon_half}) scale({icon_scale})" '
        f'color="{a}" fill="none" stroke="currentColor" stroke-width="1.6" '
        'stroke-linecap="round" stroke-linejoin="round">',
        spec["icon"],
        '</g>',
        # wordmark
        f'<text x="70" y="102" font-family="{FONT}" font-size="40" font-weight="700" '
        f'letter-spacing="7" fill="#F4F7FB">VINDAM<tspan fill="{a}">.</tspan></text>',
        # kicker
        f'<rect x="70" y="216" width="46" height="6" rx="3" fill="{a}"/>',
        f'<text x="132" y="227" font-family="{FONT}" font-size="21" font-weight="700" '
        f'letter-spacing="4" fill="{a}">{spec["kicker"]}</text>',
        # titular
        f'<text x="70" y="316" font-family="{FONT}" font-size="58" font-weight="700" '
        f'fill="#F4F7FB">{spec["l1"]}</text>',
        f'<text x="70" y="388" font-family="{FONT}" font-size="58" font-weight="700" '
        f'fill="#F4F7FB">{spec["l2"]}</text>',
        # sublínea
        f'<text x="70" y="446" font-family="{FONT}" font-size="24" '
        'fill="#A6B2C8">Su WhatsApp trabaja solo, usted atiende su negocio.</text>',
        # pie
        f'<text x="70" y="566" font-family="{FONT}" font-size="22" font-weight="700" '
        f'fill="#8FA0B8">Automatización e IA para su empresa  ·  <tspan fill="{a}">vindam.com</tspan></text>',
        '</svg>',
    ]
    return "\n".join(parts)


def main():
    ok = 0
    for slug, spec in NICHOS.items():
        svg_path = os.path.join(HERE, f"{slug}.svg")
        png_path = os.path.join(HERE, f"{slug}.png")
        with open(svg_path, "w", encoding="utf-8") as fh:
            fh.write(svg_for(spec))
        r = subprocess.run(
            ["inkscape", svg_path, "--export-filename=" + png_path,
             f"--export-width={W}", f"--export-height={H}"],
            capture_output=True, text=True)
        if r.returncode != 0 or not os.path.exists(png_path):
            print(f"FAIL {slug}: {r.stderr.strip()[:300]}", file=sys.stderr)
        else:
            ok += 1
            print(f"ok  {slug}.png")
    print(f"{ok}/{len(NICHOS)} imágenes generadas en {HERE}")
    return 0 if ok == len(NICHOS) else 1


if __name__ == "__main__":
    sys.exit(main())

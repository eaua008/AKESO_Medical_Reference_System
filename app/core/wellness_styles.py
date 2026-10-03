"""Stylesheet rules for the Wellness Calculators.

Appended to the application stylesheet by Theme.stylesheet(), like
emergency_styles.py.

Each calculator has an accent colour for its result card. Accents get a
darker shade in light mode, because amber or teal on white is hard to read.
"""

ACCENTS = {
    #            dark mode   light mode
    "bmi":       ("#38BDF8", "#0369A1"),
    "hydration": ("#2DD4BF", "#0F766E"),
    "sleep":     ("#818CF8", "#4338CA"),
    "energy":    ("#FBBF24", "#B45309"),
    "converter": ("#34D399", "#047857"),
}
AMBER = ("#FBBF24", "#B45309")


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def wellness_rules(p: dict, heading_font: str) -> str:
    from app.core.theme import Theme

    dark = Theme.mode() == "dark"
    pick = 0 if dark else 1
    amber = AMBER[pick]

    accent_rules = []
    for name, shades in ACCENTS.items():
        colour = shades[pick]
        accent_rules.append(f"""
        #wlResult[accent="{name}"] {{
            background-color: {_rgba(colour, 0.08 if dark else 0.06)};
            border: 1px solid {_rgba(colour, 0.45)};
            border-radius: 14px;
        }}
        #wlResult[accent="{name}"] #wlKicker,
        #wlResult[accent="{name}"] #wlBigNumber {{
            color: {colour};
        }}""")

    return "".join(accent_rules) + f"""
        /* ------------------------------------------- wellness calculators */
        #wlTabRow {{
            border-bottom: 1px solid {p['BORDER']};
        }}
        #wlTab {{
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            padding: 10px 14px;
            font-size: 13px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #wlTab:hover {{
            color: {p['TEXT']};
        }}
        #wlTab:checked {{
            color: {p['BADGE_TEXT']};
            border-bottom: 2px solid {p['PRIMARY']};
        }}

        #wlPanel {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #wlPanelHeading {{
            font-family: {heading_font};
            font-size: 14px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}
        #wlFieldLabel {{
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
        }}
        #wlHint {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}

        #wlSpin, #wlCombo, #wlConvInput {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 7px;
            padding: 6px 10px;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #wlSpin:focus, #wlCombo:focus, #wlConvInput:focus {{
            border: 1px solid {p['PRIMARY']};
        }}
        #wlConvInput {{
            font-family: {heading_font};
            font-size: 18px;
            font-weight: 700;
            padding: 8px 12px;
        }}
        #wlCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            selection-background-color: {p['PRIMARY_SOFT']};
            selection-color: {p['TEXT']};
            color: {p['TEXT']};
        }}

        #wlSlider::groove:horizontal {{
            height: 6px;
            background: {p['BORDER']};
            border-radius: 3px;
        }}
        #wlSlider::sub-page:horizontal {{
            background: {p['PRIMARY']};
            border-radius: 3px;
        }}
        #wlSlider::handle:horizontal {{
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
            background: #FFFFFF;
            border: 2px solid {p['PRIMARY']};
        }}

        #wlSegment, #wlConvChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 7px;
            padding: 7px 14px;
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #wlSegment:hover, #wlConvChip:hover {{
            color: {p['TEXT']};
        }}
        #wlSegment:checked, #wlConvChip:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}

        #wlKicker, #wlKickerMuted {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
        }}
        #wlKickerMuted {{
            color: {p['TEXT_MUTED']};
        }}
        #wlBigNumber {{
            font-family: {heading_font};
            font-size: 40px;
            font-weight: 800;
        }}
        #wlMidNumber {{
            font-family: {heading_font};
            font-size: 26px;
            font-weight: 800;
            color: {p['TEXT']};
        }}
        #wlBigUnit {{
            font-size: 13px;
            color: {p['TEXT_MUTED']};
            padding-bottom: 7px;
        }}
        #wlStrong {{
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #wlBody {{
            font-size: 12px;
            color: {p['TEXT']};
        }}
        #wlNote {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #wlSource {{
            font-size: 11px;
            font-style: italic;
            color: {p['TEXT_MUTED']};
        }}
        #wlDivider {{
            background-color: {p['BORDER']};
        }}

        #wlBadge {{
            border-radius: 7px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 800;
        }}
        #wlBadge[tone="good"] {{
            background-color: {_rgba('#34D399' if dark else '#16A34A', 0.14)};
            border: 1px solid {p['SUCCESS']};
            color: {p['SUCCESS']};
        }}
        #wlBadge[tone="warn"] {{
            background-color: {_rgba(amber, 0.14)};
            border: 1px solid {amber};
            color: {amber};
        }}
        #wlBadge[tone="bad"] {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']};
            color: {p['DANGER']};
        }}
        #wlBadge[tone="info"] {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            color: {p['BADGE_TEXT']};
        }}

        #wlInputBox {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #wlSwap {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            border-radius: 12px;
            font-size: 20px;
            font-weight: 700;
            color: {p['BADGE_TEXT']};
        }}
        #wlSwap:hover {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
        }}
        #wlCopy {{
            background: transparent;
            border: 1px solid {p['BORDER']};
            border-radius: 6px;
            padding: 3px 10px;
            font-size: 11px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #wlCopy:hover {{
            color: {p['TEXT']};
        }}
    """
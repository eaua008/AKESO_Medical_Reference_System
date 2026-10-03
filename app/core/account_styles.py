"""Stylesheet rules for the Account module (object names start with "ac").

Appended to the application stylesheet by Theme.stylesheet(), like the
other *_styles.py files.
"""


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def account_rules(p: dict, heading_font: str) -> str:
    from app.core.theme import Theme

    dark = Theme.mode() == "dark"
    amber = "#FBBF24" if dark else "#B45309"
    good = p["SUCCESS"]
    danger = p["DANGER"]
    return f"""
        /* ----------------------------------------------------- account */
        #acTitle {{
            font-family: {heading_font};
            font-size: 22px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #acSubtitle, #acMuted {{
            color: {p['TEXT_MUTED']};
            font-size: 13px;
        }}
        #acSmall {{
            color: {p['TEXT_MUTED']};
            font-size: 12px;
        }}
        #acHero, #acCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #acDangerCard {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {_rgba(danger, 0.45)};
            border-radius: 16px;
        }}
        #acName {{
            font-family: {heading_font};
            font-size: 20px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #acCardTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 600;
            color: {p['TEXT']};
        }}
        #acDangerTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 600;
            color: {danger};
        }}
        #acFieldLabel {{
            color: {p['TEXT_MUTED']};
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.6px;
        }}
        #acValue {{
            color: {p['TEXT']};
            font-size: 13px;
        }}
        #acError {{
            color: {danger};
            font-size: 12px;
        }}
        #acOk {{
            color: {good};
            font-size: 12px;
        }}

        /* tabs */
        #acTabRow {{
            border-bottom: 1px solid {p['BORDER']};
        }}
        #acTab {{
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            padding: 10px 14px;
            font-size: 13px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #acTab:hover {{ color: {p['TEXT']}; }}
        #acTab:checked {{
            color: {p['BADGE_TEXT']};
            border-bottom: 2px solid {p['PRIMARY']};
        }}

        /* pills */
        #acPill, #acPillGood, #acPillWarn, #acPillDanger {{
            border-radius: 10px;
            padding: 3px 10px;
            font-size: 11px;
            font-weight: 700;
        }}
        #acPill {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            color: {p['BADGE_TEXT']};
        }}
        #acPillGood {{
            background-color: {_rgba(good, 0.12)};
            border: 1px solid {_rgba(good, 0.4)};
            color: {good};
        }}
        #acPillWarn {{
            background-color: {_rgba(amber, 0.12)};
            border: 1px solid {_rgba(amber, 0.4)};
            color: {amber};
        }}
        #acPillDanger {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {_rgba(danger, 0.4)};
            color: {danger};
        }}

        /* banners */
        #acBanner {{
            border-radius: 12px;
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
        }}
        #acBanner[tone="danger"] {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {_rgba(danger, 0.45)};
        }}
        #acBanner[tone="warn"] {{
            background-color: {_rgba(amber, 0.10)};
            border: 1px solid {_rgba(amber, 0.45)};
        }}
        #acBanner[tone="good"] {{
            background-color: {_rgba(good, 0.10)};
            border: 1px solid {_rgba(good, 0.45)};
        }}
        #acBannerText {{
            color: {p['TEXT']};
            font-size: 13px;
        }}

        /* buttons */
        #acPrimary {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-weight: 600;
            font-size: 13px;
        }}
        #acPrimary:hover {{ background-color: {p['PRIMARY_HOVER']}; }}
        #acPrimary:disabled {{
            background-color: {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #acGhost {{
            background-color: transparent;
            color: {p['TEXT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 7px 14px;
            font-size: 13px;
            font-weight: 600;
        }}
        #acGhost:hover {{
            border-color: {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #acGhost:disabled {{ color: {p['TEXT_MUTED']}; }}
        #acDanger {{
            background-color: transparent;
            color: {danger};
            border: 1px solid {_rgba(danger, 0.55)};
            border-radius: 8px;
            padding: 7px 14px;
            font-size: 13px;
            font-weight: 600;
        }}
        #acDanger:hover {{ background-color: {p['DANGER_SOFT']}; }}
        #acDanger:disabled {{
            color: {p['TEXT_MUTED']};
            border-color: {p['BORDER']};
        }}
        #acLink {{
            background: transparent;
            border: none;
            color: {p['BADGE_TEXT']};
            font-size: 13px;
            font-weight: 600;
            padding: 2px 0;
            text-align: left;
        }}
        #acLink:hover {{ text-decoration: underline; }}

        /* inputs */
        #acInput {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 8px 10px;
            color: {p['TEXT']};
            font-size: 13px;
            selection-background-color: {p['PRIMARY']};
        }}
        #acInput:focus {{ border-color: {p['PRIMARY']}; }}
        #acInput:disabled {{ color: {p['TEXT_MUTED']}; }}
        QComboBox#acInput {{ padding: 6px 10px; }}
        #acCode {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
            padding: 10px;
            color: {p['TEXT']};
            font-size: 22px;
            font-weight: 700;
            letter-spacing: 8px;
        }}
        #acCode:focus {{ border-color: {p['PRIMARY']}; }}
        #acSecret {{
            background-color: {p['SURFACE_ALT']};
            border: 1px dashed {p['BORDER']};
            border-radius: 8px;
            padding: 8px;
            font-family: Consolas, 'Courier New', monospace;
            font-size: 13px;
            color: {p['TEXT']};
        }}

        /* interest chips */
        #acChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
            padding: 5px 12px;
            color: {p['TEXT_MUTED']};
            font-size: 12px;
            font-weight: 600;
        }}
        #acChip:hover {{ border-color: {p['PRIMARY']}; }}
        #acChip:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}

        /* rows in lists (devices, log, checklist) */
        #acRow {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #acRowTitle {{
            color: {p['TEXT']};
            font-size: 13px;
            font-weight: 600;
        }}
        #acDivider {{
            background-color: {p['BORDER']};
            border: none;
        }}

        /* stat tiles */
        #acStat {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #acStatNumber {{
            font-family: {heading_font};
            font-size: 24px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #acStatLabel {{
            color: {p['TEXT_MUTED']};
            font-size: 12px;
        }}

        /* dialogs */
        #acDialog {{
            background-color: {p['SURFACE']};
        }}
        #acLegal {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
            color: {p['TEXT']};
            font-size: 13px;
            padding: 6px;
        }}
    """

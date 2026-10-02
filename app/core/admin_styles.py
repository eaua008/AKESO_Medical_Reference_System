"""Stylesheet rules for the Admin Control Panel (object names start with
"ad"). Inputs, buttons, stat tiles and dialogs reuse the Account module's
"ac" rules; these add the page header, the tables and the editors."""


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def admin_amber() -> str:
    """The admin accent (amber), matching the Admin pages' badges."""
    from app.core.theme import Theme
    return "#FACC15" if Theme.mode() == "dark" else "#A16207"


def admin_rules(p: dict, heading_font: str) -> str:
    from app.core.theme import Theme

    dark = Theme.mode() == "dark"
    amber = "#FACC15" if dark else "#A16207"
    teal = "#2DD4BF" if dark else "#0F766E"
    blue = "#38BDF8" if dark else "#0369A1"
    good = p["SUCCESS"]
    danger = p["DANGER"]
    mono = "'Cascadia Mono', 'Consolas', 'DejaVu Sans Mono', monospace"
    return f"""
        /* ------------------------------------------- sidebar: ADMIN section */
        #navSectionHeader[tone="admin"] {{ color: {amber}; }}
        #navButtonAdmin {{
            background-color: transparent;
            border: none;
            border-radius: 7px;
            color: {amber};
            font-size: 12px;
            font-weight: 600;
            text-align: left;
            padding-left: 9px;
        }}
        #navButtonAdmin:hover {{ background-color: {_rgba(amber, 0.10)}; }}
        #navButtonAdmin:checked {{
            background-color: {_rgba(amber, 0.16)};
            font-weight: 700;
        }}
        #navButtonAdmin[collapsed="true"] {{ padding-left: 0px; text-align: center; }}

        /* ------------------------------------------------- admin control panel */
        #adModuleBadge {{
            border-radius: 5px;
            padding: 3px 8px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            color: {p['BADGE_TEXT']};
        }}
        #adModuleBadge[tone="good"] {{
            background-color: {_rgba(good, 0.12)};
            border: 1px solid {_rgba(good, 0.45)};
            color: {good};
        }}
        #adCrumb {{ color: {p['TEXT_MUTED']}; font-size: 12px; font-weight: 600; }}
        #adTitle {{
            font-family: {heading_font};
            font-size: 28px;
            font-weight: 800;
            color: {p['TEXT']};
        }}
        #adDesc {{ color: {p['TEXT_MUTED']}; font-size: 13px; }}
        #adRule {{ background-color: {p['BORDER']}; border: none; }}

        #adPrivacy {{
            background-color: {_rgba(amber, 0.08)};
            border: 1px solid {_rgba(amber, 0.45)};
            border-radius: 12px;
        }}
        #adPrivacyTitle {{ color: {p['TEXT']}; font-size: 13px; font-weight: 700; }}
        #adPrivacyTag {{
            background-color: {_rgba(amber, 0.15)};
            border: 1px solid {_rgba(amber, 0.5)};
            border-radius: 4px;
            padding: 1px 6px;
            color: {amber};
            font-family: {mono};
            font-size: 10px;
            font-weight: 700;
        }}
        #adPrivacyText {{ color: {amber}; font-size: 12px; }}

        #adStat {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #adStatCaption {{ font-size: 11px; font-weight: 800; letter-spacing: 1px;
                          color: {p['TEXT_MUTED']}; }}
        #adStatCaption[tone="good"] {{ color: {good}; }}
        #adStatCaption[tone="danger"] {{ color: {danger}; }}
        #adStatCaption[tone="amber"] {{ color: {amber}; }}
        #adStatCaption[tone="teal"] {{ color: {teal}; }}
        #adStatCaption[tone="blue"] {{ color: {blue}; }}
        #adStatNumber {{ font-family: {heading_font}; font-size: 24px; font-weight: 800;
                         color: {p['TEXT']}; }}
        #adStatNumber[tone="good"] {{ color: {good}; }}
        #adStatNumber[tone="danger"] {{ color: {danger}; }}
        #adStatNumber[tone="amber"] {{ color: {amber}; }}
        #adStatNumber[tone="teal"] {{ color: {teal}; }}
        #adStatNumber[tone="blue"] {{ color: {blue}; }}

        #adFilterBar {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #adFilterLabel {{ color: {p['TEXT_MUTED']}; font-size: 12px; }}

        /* section switcher (Diseases / Symptoms / Medicines / Audit Trail) */
        #adTabs {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #adTab {{
            background: transparent;
            border: none;
            border-radius: 9px;
            padding: 7px 12px;
            color: {p['TEXT_MUTED']};
            font-size: 12px;
            font-weight: 700;
            text-align: left;
        }}
        #adTab:hover {{ color: {p['TEXT']}; }}
        #adTab:checked {{ background-color: {p['PRIMARY_SOFT']}; color: {p['BADGE_TEXT']}; }}
        #adCount {{
            border-radius: 7px;
            padding: 1px 6px;
            font-size: 10px;
            font-weight: 800;
            background-color: {p['SURFACE_ALT']};
            color: {p['TEXT_MUTED']};
        }}
        #adCount[tone="primary"] {{ background-color: {p['BADGE_BG']}; color: {p['BADGE_TEXT']}; }}
        #adCount[tone="danger"] {{ background-color: {p['DANGER_SOFT']}; color: {danger}; }}
        #adCount[tone="good"] {{ background-color: {_rgba(good, 0.14)}; color: {good}; }}
        #adCount[tone="amber"] {{ background-color: {_rgba(amber, 0.16)}; color: {amber}; }}

        /* tables */
        #adTable {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
            gridline-color: transparent;
            color: {p['TEXT']};
            font-size: 12px;
            selection-background-color: transparent;
        }}
        #adTable::item {{
            border-bottom: 1px solid {p['BORDER']};
            padding: 0;
        }}
        #adTable::item:hover {{ background-color: {p['SURFACE_ALT']}; }}
        #adTable QHeaderView {{ background-color: transparent; border: none; }}
        #adTable QHeaderView::section {{
            background-color: {p['SURFACE_ALT']};
            color: {p['TEXT_MUTED']};
            border: none;
            border-bottom: 1px solid {p['BORDER']};
            padding: 10px 12px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
        }}
        #adCell {{ background: transparent; }}
        #adCellTitle {{ color: {p['TEXT']}; font-size: 13px; font-weight: 700; }}
        #adCellSub {{ color: {p['TEXT_MUTED']}; font-size: 11px; font-style: italic; }}
        #adCellMuted {{ color: {p['TEXT_MUTED']}; font-size: 11px; }}
        #adCellText {{ color: {p['TEXT']}; font-size: 12px; }}
        #adMono {{ color: {p['TEXT']}; font-family: {mono}; font-size: 11px; }}
        #adEmpty {{ color: {p['TEXT_MUTED']}; font-size: 13px; padding: 30px; }}
        #adAvatar {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
            border-radius: 15px;
            font-weight: 800;
            font-size: 12px;
        }}
        #adChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 6px;
            padding: 3px 8px;
            color: {p['TEXT']};
            font-size: 11px;
            font-weight: 600;
        }}
        #adPill {{
            border-radius: 5px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: 800;
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            color: {p['BADGE_TEXT']};
        }}
        #adPill[tone="amber"] {{ background-color: {_rgba(amber, 0.14)};
                                 border: 1px solid {_rgba(amber, 0.55)}; color: {amber}; }}
        #adPill[tone="teal"] {{ background-color: {_rgba(teal, 0.12)};
                                border: 1px solid {_rgba(teal, 0.5)}; color: {teal}; }}
        #adPill[tone="blue"] {{ background-color: {_rgba(blue, 0.12)};
                                border: 1px solid {_rgba(blue, 0.5)}; color: {blue}; }}
        #adPill[tone="good"] {{ background-color: {_rgba(good, 0.12)};
                                border: 1px solid {_rgba(good, 0.45)}; color: {good}; }}
        #adPill[tone="danger"] {{ background-color: {p['DANGER_SOFT']};
                                  border: 1px solid {_rgba(danger, 0.5)}; color: {danger}; }}
        #adPill[tone="muted"] {{ background-color: {p['SURFACE_ALT']};
                                 border: 1px solid {p['BORDER']}; color: {p['TEXT_MUTED']}; }}
        #adSubCaption {{ color: {p['TEXT_MUTED']}; font-family: {mono}; font-size: 9px;
                         letter-spacing: 1px; }}
        #adIconButton {{
            background: transparent;
            border: none;
            border-radius: 6px;
            padding: 4px;
        }}
        #adIconButton:hover {{ background-color: {p['SURFACE_ALT']}; }}
        #adIconButton:disabled {{ background: transparent; }}

        /* role picker */
        #adRoleCard {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #adRoleCard:hover {{ border-color: {p['PRIMARY']}; }}
        #adRoleCard[selected="true"][role="admin"] {{
            background-color: {_rgba(amber, 0.08)}; border: 1px solid {amber}; }}
        #adRoleCard[selected="true"][role="educator"] {{
            background-color: {_rgba(teal, 0.08)}; border: 1px solid {teal}; }}
        #adRoleCard[selected="true"][role="student"] {{
            background-color: {_rgba(blue, 0.08)}; border: 1px solid {blue}; }}
        #adRoleName {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #adRoleName[role="admin"] {{ color: {amber}; }}
        #adRoleName[role="educator"] {{ color: {teal}; }}
        #adRoleName[role="student"] {{ color: {blue}; }}

        /* editors (full-page sheet) */
        #adEditor {{ background-color: {p['BG']}; }}
        #adEditorFoot {{
            background-color: {p['SURFACE']};
            border-top: 1px solid {p['BORDER']};
        }}
        #adSection {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #adSectionTitle {{
            font-family: {heading_font};
            font-size: 14px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #adRows {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            gridline-color: {p['BORDER']};
            color: {p['TEXT']};
            font-size: 12px;
        }}
        #adRows QHeaderView::section {{
            background-color: {p['SURFACE']};
            color: {p['TEXT_MUTED']};
            border: none;
            border-bottom: 1px solid {p['BORDER']};
            padding: 6px 8px;
            font-size: 10px;
            font-weight: 800;
        }}
    """

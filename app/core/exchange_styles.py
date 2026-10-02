"""Stylesheet rules for Clinical Exchange and Notifications (object names
start with "ex"). Most of the look reuses the Account module's "ac" rules
(cards, pills, buttons, inputs); these add what the board needs."""


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def exchange_rules(p: dict, heading_font: str) -> str:
    from app.core.theme import Theme

    dark = Theme.mode() == "dark"
    amber = "#FBBF24" if dark else "#B45309"
    good = p["SUCCESS"]
    return f"""
        /* ----------------------------------------------- clinical exchange */
        QRadioButton {{
            background-color: transparent;
            color: {p['TEXT']};
            font-size: 13px;
            spacing: 8px;
        }}
        /* Styling QRadioButton drops the native circle, so draw it here. */
        QRadioButton::indicator {{
            width: 16px;
            height: 16px;
            border-radius: 9px;
            border: 1px solid {p['BORDER']};
            background-color: {p['SURFACE_ALT']};
        }}
        QRadioButton::indicator:hover {{
            border: 1px solid {p['PRIMARY']};
        }}
        QRadioButton::indicator:checked {{
            border: 1px solid {p['PRIMARY']};
            background-color: qradialgradient(cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5,
                stop:0 {p['PRIMARY']}, stop:0.5 {p['PRIMARY']},
                stop:0.6 {p['SURFACE_ALT']}, stop:1 {p['SURFACE_ALT']});
        }}
        QRadioButton:disabled {{
            color: {p['TEXT_MUTED']};
        }}

        /* full-page sheet (app/ui/components/page_sheet.py) */
        #pageSheet {{
            background-color: {p['BG']};
            border-left: 1px solid {p['BORDER']};
        }}
        #pageSheetClose {{
            background-color: #D32F2F;
            border: none;
            border-radius: 0px;
            border-top-left-radius: 4px;
            border-bottom-left-radius: 4px;
        }}
        #pageSheetClose:hover {{ background-color: #B71C1C; }}
        #pageSheetClose:pressed {{ background-color: #8E1414; }}
        #exComposer {{
            background-color: {p['BG']};
        }}
        #exComposerFoot {{
            background-color: {p['SURFACE']};
            border-top: 1px solid {p['BORDER']};
        }}
        #exPostCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #exPostCard:hover {{
            border-color: {p['PRIMARY']};
        }}
        #exPostTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 600;
            color: {p['TEXT']};
        }}
        #exDetailTitle {{
            font-family: {heading_font};
            font-size: 21px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #exBody {{
            color: {p['TEXT']};
            font-size: 14px;
        }}
        #exQuestion {{
            background-color: {p['PRIMARY_SOFT']};
            border-left: 3px solid {p['PRIMARY']};
            border-radius: 6px;
            padding: 10px 12px;
            color: {p['TEXT']};
            font-size: 14px;
            font-weight: 600;
        }}
        #exStat {{
            color: {p['TEXT_MUTED']};
            font-size: 12px;
            font-weight: 600;
        }}
        #exAuthorLink {{
            background: transparent;
            border: none;
            color: {p['TEXT']};
            font-size: 13px;
            font-weight: 600;
            padding: 0;
            text-align: left;
        }}
        #exAuthorLink:hover {{ color: {p['BADGE_TEXT']}; text-decoration: underline; }}
        #exTag {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
            padding: 2px 9px;
            color: {p['TEXT_MUTED']};
            font-size: 11px;
            font-weight: 600;
        }}
        #exTag:hover {{ border-color: {p['PRIMARY']}; color: {p['BADGE_TEXT']}; }}
        #exVote {{
            background-color: transparent;
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 4px 10px;
            color: {p['TEXT_MUTED']};
            font-size: 12px;
            font-weight: 700;
        }}
        #exVote:hover {{ border-color: {p['PRIMARY']}; }}
        #exVote:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border-color: {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #exAction {{
            background: transparent;
            border: none;
            color: {p['TEXT_MUTED']};
            font-size: 12px;
            font-weight: 600;
            padding: 3px 6px;
        }}
        #exAction:hover {{ color: {p['BADGE_TEXT']}; }}
        #exReply {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #exReply[best="true"] {{
            border: 1px solid {_rgba(good, 0.6)};
            background-color: {_rgba(good, 0.05)};
        }}
        #exChildReply {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #exPollRow {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #exPollRow[mine="true"] {{
            border: 1px solid {p['PRIMARY']};
        }}
        #exPollRow[answer="true"] {{
            border: 1px solid {good};
            background-color: {_rgba(good, 0.08)};
        }}
        #exPollBar {{
            background-color: {p['BORDER']};
            border: none;
            border-radius: 3px;
        }}
        #exPollBar::chunk {{
            background-color: {p['PRIMARY']};
            border-radius: 3px;
        }}
        #exPollBar[answer="true"]::chunk {{ background-color: {good}; }}
        #exVitals {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #exVitalValue {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #exVitalValue[flag="true"] {{ color: {amber}; }}
        #exNotif {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #exNotif[unread="true"] {{
            border: 1px solid {p['BADGE_BORDER']};
            background-color: {p['BADGE_BG']};
        }}
        #exNotif:hover {{ border-color: {p['PRIMARY']}; }}
        #exBadge {{
            background-color: {p['DANGER']};
            color: #FFFFFF;
            border-radius: 8px;
            font-size: 10px;
            font-weight: 800;
            padding: 0 4px;
        }}
    """

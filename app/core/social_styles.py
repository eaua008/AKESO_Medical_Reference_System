"""Stylesheet rules for Friends, shared notes and Study Groups (object names
start with "sc"). Most of the look reuses the Account module's "ac" rules
(cards, pills, buttons, inputs, tabs); these add the chat and list rows.
Colours come only from the theme palette, so every theme and both modes
work."""


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    if len(h) != 6:
        return hex_colour
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def social_rules(p: dict, heading_font: str) -> str:
    return f"""
        /* ------------------------------------------ friends, sharing, groups */
        #scRow {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #scRow:hover {{ border-color: {p['PRIMARY']}; }}
        #scRowTitle {{
            font-size: 14px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #scHandle {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #scUnread {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
            border-radius: 9px;
            padding: 1px 7px;
            font-size: 11px;
            font-weight: 700;
        }}
        #scSection {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: {p['TEXT_MUTED']};
        }}
        #scEmpty {{
            background-color: {p['SURFACE']};
            border: 1px dashed {p['BORDER']};
            border-radius: 12px;
        }}
        #scEmptyTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #scReadOnlyBanner {{
            background-color: {_rgba(p['PRIMARY'], 0.10)};
            border: 1px solid {_rgba(p['PRIMARY'], 0.35)};
            border-radius: 10px;
        }}
        #scReadOnlyText {{ color: {p['TEXT']}; font-size: 13px; font-weight: 600; }}
        #scReader {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
            padding: 14px;
            color: {p['TEXT']};
            font-size: 14px;
        }}
        #scHandleBox {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 10px;
            font-weight: 700;
            color: {p['TEXT']};
        }}

        /* chat */
        #scChat {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #scBubble {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #scBubbleMine {{
            background-color: {_rgba(p['PRIMARY'], 0.14)};
            border: 1px solid {_rgba(p['PRIMARY'], 0.40)};
            border-radius: 12px;
        }}
        #scBubbleHidden {{
            background-color: transparent;
            border: 1px dashed {p['BORDER']};
            border-radius: 12px;
        }}
        #scBubbleName {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #scBubbleText {{ font-size: 13px; color: {p['TEXT']}; }}
        #scBubbleTime {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #scNewLine {{ background-color: {p['PRIMARY']}; border: none; }}
        #scNewTag {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
            border-radius: 9px;
            padding: 2px 12px;
            font-size: 11px;
            font-weight: 800;
        }}
        #scPicture {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            color: {p['TEXT_MUTED']};
            padding: 2px;
        }}
        #scMention {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #scMentionRow {{
            background: transparent;
            border: none;
            border-radius: 7px;
            padding: 7px 10px;
            text-align: left;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #scMentionRow:hover, #scMentionRow[current="true"] {{
            background-color: {p['PRIMARY_SOFT']};
        }}
        #scComposer {{
            background-color: {p['SURFACE']};
            border-top: 1px solid {p['BORDER']};
        }}
    """

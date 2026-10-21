"""Stylesheet rules for Study Hub (object names start with "st"). Cards,
pills, chips, inputs and buttons reuse the Account module's "ac" rules;
these add deck tiles, the review card and the rating buttons. Colours come
only from the theme palette, so every theme and both modes work."""


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    if len(h) != 6:
        return hex_colour
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def study_rules(p: dict, heading_font: str) -> str:
    good, bad = p["SUCCESS"], p["DANGER"]
    amber = "#F59E0B"
    return f"""
        /* ------------------------------------------------------- Study Hub */
        #stTab {{
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            color: {p['TEXT_MUTED']};
            font-size: 14px;
            font-weight: 600;
            padding: 8px 4px;
        }}
        #stTab:hover {{ color: {p['TEXT']}; }}
        #stTab:checked {{ color: {p['TEXT']}; border-bottom-color: {p['PRIMARY']}; }}
        #stHero {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #stHeroNumber {{
            font-family: {heading_font};
            font-size: 34px;
            font-weight: 800;
            color: {p['TEXT']};
        }}
        #stHeroCaption {{ font-size: 13px; color: {p['TEXT_MUTED']}; }}
        #stDeck, #stRow {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #stDeck:hover, #stRow:hover {{ border-color: {p['PRIMARY']}; }}
        #stDeckTitle {{
            font-size: 15px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #stCount {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #stCountDue {{ font-size: 12px; font-weight: 700; color: {p['PRIMARY']}; }}
        #stBadge {{
            border-radius: 9px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 700;
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #stBadge[origin="official"] {{
            background-color: {p['PRIMARY_SOFT']};
            border-color: {p['BADGE_BORDER']};
            color: {p['BADGE_TEXT']};
        }}
        #stBadge[origin="auto"] {{
            background-color: {_rgba(good, 0.12)};
            border-color: {_rgba(good, 0.4)};
            color: {good};
        }}
        #stBadge[origin="shared"] {{
            background-color: {_rgba(amber, 0.12)};
            border-color: {_rgba(amber, 0.4)};
            color: {amber};
        }}
        #stReviewCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 18px;
        }}
        #stFront {{
            font-family: {heading_font};
            font-size: 20px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #stBack {{ font-size: 16px; color: {p['TEXT']}; }}
        #stRule {{ background-color: {p['BORDER']}; }}
        #stSection {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            color: {p['TEXT_MUTED']};
            padding-top: 4px;
        }}
        #stAnswer {{
            font-family: {heading_font};
            font-size: 19px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #stWhy {{ font-size: 15px; color: {p['TEXT']}; }}
        #stTyped {{
            font-size: 15px;
            color: {p['TEXT']};
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 10px;
        }}
        #stHintText {{ font-size: 14px; font-style: italic; color: {p['PRIMARY']}; }}
        #stBadge[level="basic"] {{ color: {good}; border-color: {_rgba(good, 0.4)}; }}
        #stBadge[level="clinical"] {{ color: {amber}; border-color: {_rgba(amber, 0.4)}; }}
        #stBadge[level="advanced"] {{ color: {bad}; border-color: {_rgba(bad, 0.4)}; }}
        #stChoice {{
            text-align: left;
            padding: 10px 14px;
            border-radius: 10px;
            border: 1px solid {p['BORDER']};
            background-color: {p['SURFACE_RAISED']};
            color: {p['TEXT']};
            font-size: 14px;
        }}
        #stChoice:hover {{ border-color: {p['PRIMARY']}; }}
        #stChoice[result="right"] {{ border: 2px solid {good}; background-color: {_rgba(good, 0.12)}; }}
        #stChoice[result="wrong"] {{ border: 2px solid {bad}; background-color: {_rgba(bad, 0.12)}; }}
        #stRationale {{ font-size: 12px; color: {p['TEXT_MUTED']}; padding-left: 4px; }}
        #stRate {{
            border-radius: 10px;
            padding: 8px 10px;
            font-size: 14px;
            font-weight: 700;
            border: 1px solid {p['BORDER']};
            background-color: {p['SURFACE_RAISED']};
            color: {p['TEXT']};
        }}
        #stRate[rating="1"] {{ border-color: {_rgba(bad, 0.6)}; }}
        #stRate[rating="2"] {{ border-color: {_rgba(amber, 0.6)}; }}
        #stRate[rating="3"] {{ border-color: {_rgba(good, 0.6)}; }}
        #stRate[rating="4"] {{ border-color: {p['BADGE_BORDER']}; }}
        #stRate:hover {{ background-color: {p['PRIMARY_SOFT']}; }}
        #stRate:checked {{ background-color: {p['PRIMARY_SOFT']}; border: 2px solid {p['PRIMARY']}; }}
        #stHint {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #stProgress {{
            background-color: {p['SURFACE_RAISED']};
            border: none;
            border-radius: 3px;
        }}
        #stProgress::chunk {{ background-color: {p['PRIMARY']}; border-radius: 3px; }}
        #stDisclaimer {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #stSync {{
            border-radius: 9px;
            padding: 2px 9px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #stSync[tone="good"] {{ color: {good}; border-color: {_rgba(good, 0.4)}; }}
        #stSync[tone="warn"] {{ color: {amber}; border-color: {_rgba(amber, 0.4)}; }}
        #stSync[tone="bad"] {{ color: {bad}; border-color: {_rgba(bad, 0.4)}; }}
        #stStreak {{
            background-color: {_rgba(amber, 0.10)};
            border: 1px solid {_rgba(amber, 0.35)};
            border-radius: 14px;
        }}
        #stSubject {{
            text-align: left;
            padding: 10px 12px;
            border-radius: 10px;
            border: 1px solid {p['BORDER']};
            background-color: {p['SURFACE_RAISED']};
            color: {p['TEXT']};
            font-size: 13px;
            font-weight: 600;
        }}
        #stSubject:hover {{ background-color: {p['PRIMARY_SOFT']}; }}
        #stSubject:disabled {{ color: {p['TEXT_MUTED']}; }}
        #stEditorChoice {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
    """

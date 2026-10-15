"""Stylesheet rules for Health Articles (object names start with "ha").

The list is a directory: a toolbar card, then one section per topic with a
dot, an uppercase name and an entry count, and the articles stacked in one
rounded group. A row lights up on hover with a left accent bar.
"""


def article_rules(p: dict, heading_font: str) -> str:
    from app.core.theme import Theme

    # Everything follows the colour theme (Settings > Appearance).
    dark = Theme.mode() == "dark"
    accent = p["ACCENT_2"]                              # topic label / dot
    hover_title = p["BADGE_TEXT"]
    group_bg = p["SURFACE"]
    row_alt = p["SURFACE_RAISED"] if dark else p["SURFACE_ALT"]
    row_hover = p["PRIMARY_SOFT"]
    toolbar_bg = p["SURFACE"]
    field_bg = p["SURFACE_RAISED"] if dark else p["SURFACE_ALT"]
    border = p["BORDER"]
    hero_a = p["PRIMARY_SOFT"]
    hero_b = p["SURFACE"]
    article_bg = p["SURFACE"]
    body_text = p["TEXT"]
    return f"""
        /* ------------------------------------------------- health articles */
        #haTitle {{
            background: transparent;
            color: {p['TEXT']};
            font-family: {heading_font};
            font-size: 22px;
            font-weight: 700;
        }}
        #haSubtitle {{ background: transparent; color: {p['TEXT_MUTED']}; font-size: 12px; }}
        #haCountPill {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            color: {p['TEXT']};
            border-radius: 11px;
            padding: 3px 12px;
            font-size: 11px;
            font-weight: 600;
        }}
        #haToolbar {{
            background-color: {toolbar_bg};
            border: 1px solid {border};
            border-radius: 14px;
        }}
        #haToolbar QWidget {{ background: transparent; }}
        QLineEdit#haSearch, QComboBox#haTopic {{
            background-color: {field_bg};
            border: 1px solid {border};
            border-radius: 9px;
            color: {p['TEXT']};
            padding: 8px 12px;
            font-size: 13px;
        }}
        QLineEdit#haSearch {{ padding-left: 34px; }}
        QLineEdit#haSearch:focus, QComboBox#haTopic:focus {{ border-color: {p['PRIMARY']}; }}
        #haSegment {{
            background-color: {field_bg};
            border: 1px solid {border};
            border-radius: 9px;
        }}
        QPushButton#haSegBtn {{
            background: transparent;
            border: none;
            border-radius: 7px;
            color: {p['TEXT_MUTED']};
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 600;
        }}
        QPushButton#haSegBtn:hover {{ color: {p['TEXT']}; }}
        QPushButton#haSegBtn:checked {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['BADGE_TEXT']};
        }}

        #haDot {{ background-color: {accent}; border-radius: 4px; }}
        #haSection {{
            background: transparent;
            color: {p['TEXT']};
            font-family: {heading_font};
            font-size: 13px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        #haSectionCount {{ background: transparent; color: {p['TEXT_MUTED']}; font-size: 10px; font-weight: 600; }}
        #haDivider {{ background-color: {border}; border: none; }}

        #haGroup {{
            background-color: {group_bg};
            border: 1px solid {border};
            border-radius: 14px;
        }}
        #haRow {{
            background-color: transparent;
            border: none;
            border-left: 3px solid transparent;
        }}
        #haRow[alt="true"] {{ background-color: {row_alt}; }}
        #haRow[hover="true"] {{
            background-color: {row_hover};
            border-left: 3px solid {accent};
        }}
        #haRow[pos="first"] {{ border-top-left-radius: 13px; border-top-right-radius: 13px; }}
        #haRow[pos="last"] {{ border-bottom-left-radius: 13px; border-bottom-right-radius: 13px; }}
        #haRow[pos="only"] {{ border-radius: 13px; }}
        #haRowTopic {{
            background: transparent;
            color: {accent};
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.6px;
        }}
        #haRowMeta {{ background: transparent; color: {p['TEXT_MUTED']}; font-size: 10px; }}
        #haRowTitle {{
            background: transparent;
            color: {p['TEXT']};
            font-family: {heading_font};
            font-size: 16px;
            font-weight: 700;
        }}
        #haRow[hover="true"] #haRowTitle {{ color: {hover_title}; }}
        QPushButton#haStar {{ background: transparent; border: none; border-radius: 6px; }}
        QPushButton#haStar:hover {{ background-color: {p['PRIMARY_SOFT']}; }}

        /* reader: hero, article text, source links in the rail */
        #haHero {{
            background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 {hero_a}, stop:1 {hero_b});
            border: 1px solid {border};
            border-left: 4px solid {accent};
            border-radius: 16px;
        }}
        #haHero QWidget {{ background: transparent; }}
        #haHeroChip {{
            background-color: {p['PRIMARY_SOFT']};
            color: {accent};
            border-radius: 10px;
            padding: 3px 10px;
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 0.6px;
        }}
        #haHeroTitle {{
            background: transparent;
            color: {p['TEXT']};
            font-family: {heading_font};
            font-size: 30px;
            font-weight: 700;
        }}
        #haHeroLead {{ background: transparent; color: {body_text}; font-size: 15px; }}
        #haHeroMeta {{ background: transparent; color: {p['TEXT_MUTED']}; font-size: 12px; }}
        #haArticle {{
            background-color: {article_bg};
            border: 1px solid {border};
            border-radius: 16px;
        }}
        #haH2 {{
            background: transparent;
            color: {p['TEXT']};
            font-family: {heading_font};
            font-size: 20px;
            font-weight: 700;
        }}
        #haH2Bar {{ background-color: {accent}; border-radius: 1px; }}
        #haP {{ background: transparent; color: {body_text}; font-size: 15px; }}
        #haBullet {{ background-color: {accent}; border-radius: 3px; }}
        #haLinkRow {{
            background-color: {field_bg};
            border: 1px solid {border};
            border-left: 3px solid transparent;
            border-radius: 10px;
        }}
        #haLinkRow[hover="true"] {{ border-left: 3px solid {accent}; background-color: {row_hover}; }}
        #haLinkRow QWidget {{ background: transparent; }}
        #haLinkSource {{ background: transparent; color: {accent}; font-size: 9px; font-weight: 700; letter-spacing: 0.6px; }}
        #haLinkTitle {{ background: transparent; color: {p['TEXT']}; font-size: 13px; font-weight: 600; }}
        #haLinkRow[hover="true"] #haLinkTitle {{ color: {hover_title}; }}
        #haLinkDomain {{ background: transparent; color: {p['TEXT_MUTED']}; font-size: 11px; }}
        #haEmpty {{ background: transparent; color: {p['TEXT_MUTED']}; font-size: 13px; }}
    """

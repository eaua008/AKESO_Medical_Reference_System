"""Stylesheet rules for the Study Notebook.

Appended to the application stylesheet by Theme.stylesheet(), like the
other *_styles.py files. Every id starts with "nb" so nothing here can
collide with another module's rules.
"""

# folder colour -> (dark mode, light mode)
FOLDER_HEX = {
    "purple": ("#A29BFE", "#6C5CE7"),
    "amber": ("#FBBF24", "#B45309"),
    "green": ("#34D399", "#15803D"),
    "blue": ("#60A5FA", "#2563EB"),
    "rose": ("#FB7185", "#E11D48"),
    "slate": ("#94A3B8", "#64748B"),
}


def folder_hex(color: str) -> str:
    from app.core.theme import Theme

    pair = FOLDER_HEX.get(color, FOLDER_HEX["slate"])
    return pair[0 if Theme.mode() == "dark" else 1]


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def notebook_rules(p: dict, heading_font: str) -> str:
    from app.core.theme import Theme

    dark = Theme.mode() == "dark"
    amber = "#FBBF24" if dark else "#B45309"
    strip_bg = p["BG"] if dark else p["SURFACE_ALT"]
    chip_text = "#111118" if dark else "#FFFFFF"

    folder_rules = []
    for name, pair in FOLDER_HEX.items():
        hexc = pair[0 if dark else 1]
        folder_rules.append(f"""
        #nbTab[folder="{name}"] {{ border-top: 2px solid {hexc}; }}
        #nbFolderChip[color="{name}"] {{ background-color: {hexc}; }}
        #nbFolderChip[color="{name}"][open="false"] {{
            background-color: {_rgba(hexc, 0.18)};
            border: 1px solid {hexc};
        }}
        #nbFolderChip[color="{name}"][open="false"] QLabel {{ color: {hexc}; }}
        #nbColorDot[color="{name}"] {{ background-color: {hexc}; }}
        """)

    return f"""
        /* --------------------------------------------------- study notebook */
        #nbPage {{ background-color: {p['BG']}; }}

        /* bars */
        #nbItemBar, #nbStrip {{
            background-color: {strip_bg};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #nbWsBar {{
            background-color: {p['SURFACE']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #nbCrumb {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #nbCrumbStrong {{
            font-family: {heading_font};
            font-size: 13px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #nbSaved {{ font-size: 11px; font-weight: 600; color: {p['SUCCESS']}; }}
        #nbSmallMuted {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}

        /* tabs */
        #nbStripRow {{ background-color: transparent; }}
        #nbTab {{
            background-color: {p['SURFACE_ALT'] if not dark else p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-bottom: none;
            border-top-left-radius: 8px;
            border-top-right-radius: 8px;
        }}
        #nbTab:hover {{ background-color: {p['SURFACE_RAISED']}; }}
        #nbTab[active="true"] {{
            background-color: {p['SURFACE']};
            border-top: 2px solid {p['PRIMARY']};
        }}
        #nbTabTitle {{ font-size: 12px; font-weight: 600; color: {p['TEXT_MUTED']}; }}
        #nbTab[active="true"] #nbTabTitle {{ color: {p['TEXT']}; }}
        #nbTabClose {{
            background-color: transparent;
            border: none;
            border-radius: 4px;
        }}
        #nbTabClose:hover {{ background-color: {p['DANGER_SOFT']}; }}

        /* folders */
        #nbFolderChip {{
            border-radius: 10px;
            border: 1px solid transparent;
        }}
        #nbFolderChip QLabel {{
            color: {chip_text};
            font-size: 11px;
            font-weight: 700;
        }}
        {''.join(folder_rules)}

        /* small square icon buttons */
        #nbIconButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 7px;
        }}
        #nbIconButton:hover {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
        }}
        #nbIconButton:disabled {{ background-color: transparent; }}
        #nbToggle {{
            background-color: transparent;
            border: 1px solid {p['BORDER']};
            border-radius: 7px;
        }}
        #nbToggle:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
        }}
        #nbButton {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 5px 12px;
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
        }}
        #nbButton:hover {{ border: 1px solid {p['PRIMARY']}; }}

        /* columns */
        #nbColumn {{
            background-color: {p['SURFACE']};
            border: none;
        }}
        #nbSplitter::handle {{
            background-color: {p['BORDER']};
        }}
        #nbSplitter::handle:hover {{ background-color: {p['PRIMARY']}; }}
        #nbRail {{
            background-color: {strip_bg};
            border: none;
        }}
        #nbRail:hover {{ background-color: {p['SURFACE_RAISED']}; }}
        #nbRailText {{ font-size: 11px; font-weight: 700; color: {p['TEXT_MUTED']}; }}
        #nbDropMarker {{ background-color: {p['PRIMARY']}; border-radius: 1px; }}

        /* placeholder pages (until steps 5 to 7 fill them) */
        #nbPlaceholder {{
            background-color: {p['SURFACE_ALT']};
            border: 1px dashed {p['BORDER']};
            border-radius: 14px;
        }}
        #nbPlaceholderTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 700;
        }}
        #nbPlaceholderText {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #nbEmpty {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}

        /* popups: folder editor and the all-tabs list */
        #nbPopup {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #nbPopupTitle {{ font-size: 12px; font-weight: 700; }}
        #nbInput {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 9px;
            font-size: 12px;
            color: {p['TEXT']};
        }}
        #nbInput:focus {{ border: 1px solid {p['PRIMARY']}; }}
        #nbColorDot {{
            border: 2px solid transparent;
            border-radius: 9px;
        }}
        #nbColorDot[selected="true"] {{ border: 2px solid {p['TEXT']}; }}
        #nbTabList {{
            background-color: transparent;
            border: none;
            font-size: 12px;
            outline: none;
        }}
        #nbTabList::item {{
            padding: 4px 4px;
            border-radius: 6px;
            color: {p['TEXT']};
        }}
        #nbTabList::item:selected, #nbTabList::item:hover {{
            background-color: {p['PRIMARY_SOFT']};
        }}

        /* ------------------------------------------------ level 1: home */
        #nbHomeHeader {{
            background-color: {p['BG']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #nbIconTile {{
            background-color: {p['PRIMARY']};
            border-radius: 11px;
        }}
        #nbTitle {{
            font-family: {heading_font};
            font-size: 22px;
            font-weight: 800;
        }}
        #nbSubtitle {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #nbPrimary {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 7px 14px;
            font-size: 12px;
            font-weight: 700;
        }}
        #nbPrimary:hover {{ background-color: {p['PRIMARY_HOVER']}; }}
        #nbLinkButton {{
            background-color: transparent;
            border: none;
            color: {p['PRIMARY_TEXT_ON_NAV']};
            font-size: 11px;
            font-weight: 700;
        }}
        #nbLinkButton:hover {{ text-decoration: underline; }}

        #nbLibRail {{
            background-color: {strip_bg};
            border-right: 1px solid {p['BORDER']};
        }}
        #nbRailCap {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 1px;
            color: {p['TEXT_MUTED']};
        }}
        #nbRailHint {{ font-size: 11px; color: {p['TEXT_MUTED']}; padding: 2px 6px; }}
        #nbRailRow {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 8px;
        }}
        #nbRailRow:hover {{ background-color: {p['SURFACE_RAISED']}; }}
        #nbRailRow[on="true"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {_rgba(p['PRIMARY'], 0.55)};
        }}
        #nbRailText {{ font-size: 13px; color: {p['TEXT']}; }}
        #nbRailText[on="true"] {{ color: {p['PRIMARY_TEXT_ON_NAV']}; font-weight: 700; }}
        #nbCount {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
            padding: 0 6px;
            font-size: 10px;
            font-weight: 700;
            color: {p['TEXT_MUTED']};
        }}
        #nbTagChip {{
            background-color: transparent;
            border: 1px solid {p['BORDER']};
            border-radius: 11px;
        }}
        #nbTagChip:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #nbTagChip[on="true"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
        }}
        #nbTagText {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #nbTagText[on="true"] {{ color: {p['PRIMARY_TEXT_ON_NAV']}; font-weight: 700; }}

        #nbSearchField {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #nbSearchInput {{
            background-color: transparent;
            border: none;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #nbCombo {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 12px;
            color: {p['TEXT']};
        }}
        #nbCombo:focus {{ border: 1px solid {p['PRIMARY']}; }}
        #nbCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            selection-background-color: {p['PRIMARY_SOFT']};
            color: {p['TEXT']};
            outline: none;
        }}

        #nbCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #nbCard:hover {{ border: 1px solid {_rgba(p['PRIMARY'], 0.6)}; }}
        #nbCard[selected="true"] {{
            border: 1px solid {p['PRIMARY']};
            background-color: {_rgba(p['PRIMARY'], 0.07)};
        }}
        #nbCardTitle {{
            font-family: {heading_font};
            font-size: 14px;
            font-weight: 700;
        }}
        #nbCardPreview {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #nbCardSubject {{
            font-size: 11px;
            font-weight: 700;
            color: {p['PRIMARY_TEXT_ON_NAV']};
        }}
        #nbCardSubject[empty="true"] {{ color: {p['TEXT_MUTED']}; font-weight: 600; }}
        #nbCardMeta {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #nbKindTile {{ border-radius: 8px; }}
        #nbKindTile[tone="primary"] {{ background-color: {_rgba(p['PRIMARY'], 0.16)}; }}
        #nbKindTile[tone="success"] {{ background-color: {_rgba(p['SUCCESS'], 0.14)}; }}
        #nbKindTile[tone="amber"] {{ background-color: {_rgba(amber, 0.16)}; }}
        #nbError {{ font-size: 12px; font-weight: 600; color: {p['DANGER']}; }}

        /* ------------------------------------- level 2: the slide panel */
        #nbSlidePanel {{
            background-color: {p['SURFACE']};
            border-left: 1px solid {p['PRIMARY']};
        }}
        #nbPanelBody {{ background-color: {p['SURFACE']}; }}
        #nbPanelHead {{
            background-color: {p['SURFACE']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #nbKindBadge {{
            border-radius: 6px;
            padding: 3px 2px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}
        #nbKindBadge[tone="primary"] {{
            background-color: {_rgba(p['PRIMARY'], 0.16)};
            color: {p['PRIMARY_TEXT_ON_NAV']};
        }}
        #nbKindBadge[tone="success"] {{
            background-color: {_rgba(p['SUCCESS'], 0.14)};
            color: {p['SUCCESS']};
        }}
        #nbKindBadge[tone="amber"] {{
            background-color: {_rgba(amber, 0.16)};
            color: {amber};
        }}
        #nbTitleEdit {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 7px;
            padding: 3px 6px;
            font-family: {heading_font};
            font-size: 17px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #nbTitleEdit:hover {{ border: 1px solid {p['BORDER']}; }}
        #nbTitleEdit:focus {{ border: 1px solid {p['PRIMARY']}; background-color: {p['SURFACE_ALT']}; }}
        #nbFieldLabel {{
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT_MUTED']};
        }}
        #nbSection {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #nbSectionTitle {{
            font-family: {heading_font};
            font-size: 13px;
            font-weight: 700;
        }}
        #nbLockLabel {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #nbChip {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 11px;
            padding: 3px 10px;
            font-size: 12px;
        }}
        #nbVerdict {{
            border-radius: 6px;
            padding: 4px 4px;
            font-size: 11px;
            font-weight: 800;
        }}
        #nbVerdict[tone="success"] {{ background-color: {_rgba(p['SUCCESS'], 0.14)}; color: {p['SUCCESS']}; }}
        #nbVerdict[tone="primary"] {{ background-color: {_rgba(p['PRIMARY'], 0.16)}; color: {p['PRIMARY_TEXT_ON_NAV']}; }}
        #nbVerdict[tone="amber"] {{ background-color: {_rgba(amber, 0.16)}; color: {amber}; }}
        #nbVerdict[tone="danger"] {{ background-color: {p['DANGER_SOFT']}; color: {p['DANGER']}; }}
        #nbBody {{ font-size: 13px; color: {p['TEXT']}; }}
        #nbBodyStrong {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #nbNotesView {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #nbNoteBox {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {_rgba(p['PRIMARY'], 0.35)};
            border-radius: 10px;
        }}

        /* ------------------------------------------ step 5: notes editor */
        #nbToolbar {{
            background-color: {p['SURFACE']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #nbToolButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 6px;
        }}
        #nbToolButton:hover {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
        }}
        #nbToolButton:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {_rgba(p['PRIMARY'], 0.6)};
        }}
        #nbToolGap {{ background-color: {p['BORDER']}; }}
        #nbToolCombo {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 12px;
            color: {p['TEXT']};
            min-height: 20px;
        }}
        #nbToolCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            selection-background-color: {p['PRIMARY_SOFT']};
            color: {p['TEXT']};
        }}
        #nbTableBar {{
            background-color: {_rgba(p['PRIMARY'], 0.07)};
            border-bottom: 1px solid {_rgba(p['PRIMARY'], 0.4)};
        }}
        #nbTableButton {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 6px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 600;
            color: {p['TEXT']};
        }}
        #nbTableButton:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #nbTableButton[danger="true"] {{ color: {p['DANGER']}; }}
        #nbPaperHost {{ background-color: {p['BG']}; }}
        #nbEditor {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
            color: {p['TEXT']};
            font-size: 14px;
            selection-background-color: {_rgba(p['PRIMARY'], 0.45)};
        }}
        #nbEditor:focus {{ border: 1px solid {_rgba(p['PRIMARY'], 0.6)}; }}
        #nbSwatch {{
            border: 1px solid {p['BORDER']};
            border-radius: 6px;
            background-color: {p['SURFACE']};
        }}

        /* --------------------------------------- step 6: reference column */
        #nbFilterChip {{
            background-color: transparent;
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
            padding: 4px 11px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT_MUTED']};
        }}
        #nbFilterChip:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #nbFilterChip[on="true"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            color: {p['PRIMARY_TEXT_ON_NAV']};
        }}
        #nbPinChip, #nbLinkChip {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {_rgba(p['PRIMARY'], 0.45)};
            border-radius: 11px;
            padding: 3px 10px;
            font-size: 12px;
            font-weight: 600;
            color: {p['PRIMARY_TEXT_ON_NAV']};
            text-align: left;
        }}
        #nbPinChip:hover, #nbLinkChip:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #nbRefList {{
            background-color: transparent;
            border: none;
            outline: none;
            font-size: 12px;
        }}
        #nbRefList::item {{
            border-radius: 8px;
            padding: 4px 6px;
            color: {p['TEXT']};
        }}
        #nbRefList::item:hover {{ background-color: {p['SURFACE_RAISED']}; }}
        #nbRefList::item:selected {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['TEXT']};
        }}
        #nbMonoTitle {{
            font-family: {heading_font};
            font-size: 16px;
            font-weight: 800;
        }}
        #nbRefSection {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #nbSectionToggle {{
            background-color: transparent;
            border: none;
            text-align: left;
            font-size: 13px;
            font-weight: 700;
            color: {p['TEXT']};
            padding: 2px 0;
        }}
        #nbInsertButton {{
            background-color: transparent;
            border: 1px dashed {_rgba(p['PRIMARY'], 0.7)};
            border-radius: 7px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 700;
            color: {p['PRIMARY_TEXT_ON_NAV']};
        }}
        #nbInsertButton:hover {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
        }}
        #nbRefText {{ font-size: 13px; color: {p['TEXT']}; }}

        /* ------------------------------------------ step 7: case column */
        #nbQuote {{ font-size: 13px; font-style: italic; color: {p['TEXT']}; }}
        #nbMono {{
            font-family: Consolas, "Cascadia Mono", monospace;
            font-size: 13px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #nbVitalTile {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
        }}
        #nbVitalTile[flag="true"] {{ border: 1px solid {amber}; }}
        #nbFlagText {{ font-size: 10px; font-weight: 700; color: {amber}; }}
        #nbCellGood {{ font-size: 12px; font-weight: 700; color: {p['SUCCESS']}; }}
        #nbCellBad {{ font-size: 12px; font-weight: 700; color: {p['DANGER']}; }}
        #nbCellMuted {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #nbMatchCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
        }}
        #nbMatchBar {{
            background-color: {p['BORDER']};
            border: none;
            border-radius: 2px;
        }}
        #nbMatchBar::chunk {{ background-color: {p['PRIMARY']}; border-radius: 2px; }}
        #nbChipGood {{
            background-color: {_rgba(p['SUCCESS'], 0.12)};
            border: 1px solid {_rgba(p['SUCCESS'], 0.45)};
            border-radius: 11px;
            padding: 2px 9px;
            font-size: 11px;
            color: {p['SUCCESS']};
        }}
        #nbChipBad {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {_rgba(p['DANGER'], 0.45)};
            border-radius: 11px;
            padding: 2px 9px;
            font-size: 11px;
            color: {p['DANGER']};
        }}
        #nbHidden {{
            font-size: 14px;
            color: {p['BORDER']};
            letter-spacing: 1px;
        }}

        /* quick view: checker runs attached to a note */
        #nbLinkCard {{
            background-color: {p['SURFACE_ALT']};
            border: 1px dashed {p['BORDER']};
            border-radius: 12px;
        }}
        #nbLinkCard[attached="true"] {{
            border: 1px solid {_rgba(p['PRIMARY'], 0.45)};
        }}
        #nbLinkState {{ font-size: 11px; font-weight: 700; color: {p['TEXT_MUTED']}; }}
        #nbLinkState[attached="true"] {{ color: {p['SUCCESS']}; }}

        QMenu#nbMenu {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
            padding: 5px;
            font-size: 12px;
        }}
        QMenu#nbMenu::item {{
            padding: 6px 22px 6px 10px;
            border-radius: 6px;
            color: {p['TEXT']};
            background-color: transparent;
        }}
        QMenu#nbMenu::item:selected {{ background-color: {p['PRIMARY_SOFT']}; }}
        QMenu#nbMenu::item:disabled {{ color: {p['TEXT_MUTED']}; }}
        QMenu#nbMenu::separator {{
            height: 1px;
            background-color: {p['BORDER']};
            margin: 4px 6px;
        }}
    """

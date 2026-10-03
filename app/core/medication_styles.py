"""Stylesheet rules for Medication & Drug Safety.

Appended to the application stylesheet by Theme.stylesheet(), like the
other *_styles.py files. Every id starts with "md" so nothing here can
collide with another module's rules.

Tones used across the page:
    primary   on track, selected filters, main buttons
    amber     missed dose, full-course-critical, stewardship warning
    danger    abandoned, abandon link
    success   safe profile
"""

AMBER = ("#FBBF24", "#B45309")        # dark mode, light mode


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def medication_rules(p: dict, heading_font: str) -> str:
    from app.core.theme import Theme

    dark = Theme.mode() == "dark"
    amber = AMBER[0 if dark else 1]
    success = p["SUCCESS"]
    danger = p["DANGER"]

    return f"""
        /* ------------------------------------------ medication & safety */
        #mdHeaderCard, #mdPanel, #mdCard, #mdStat {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #mdCard[state="abandoned"] {{
            border: 1px solid {_rgba(danger, 0.45)};
        }}
        #mdStat[tone="success"] {{
            background-color: {_rgba(success, 0.06)};
            border: 1px solid {_rgba(success, 0.45)};
        }}
        #mdIconTile {{
            background-color: {p['PRIMARY']};
            border-radius: 10px;
        }}
        #mdTitle {{
            font-family: {heading_font};
            font-size: 22px;
            font-weight: 800;
        }}
        #mdSubtitle, #mdMuted {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #mdSmallMuted {{
            font-size: 11px;
            color: {p['TEXT_MUTED']};
        }}

        /* buttons */
        #mdPrimary {{
            background-color: {p['PRIMARY']};
            border: none;
            border-radius: 8px;
            padding: 9px 16px;
            font-size: 12px;
            font-weight: 700;
            color: #FFFFFF;
        }}
        #mdPrimary:hover {{ background-color: {p['PRIMARY_HOVER']}; }}
        #mdPrimary:disabled {{
            background-color: {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #mdPrimaryWide {{
            background-color: {p['PRIMARY']};
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 13px;
            font-weight: 700;
            color: #FFFFFF;
        }}
        #mdPrimaryWide:hover {{ background-color: {p['PRIMARY_HOVER']}; }}
        #mdSecondary {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 9px 16px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #mdSecondary:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdDangerLink {{
            background: transparent;
            border: none;
            font-size: 12px;
            font-weight: 700;
            color: {danger};
            padding: 4px 2px;
        }}
        #mdDangerLink:hover {{ text-decoration: underline; }}

        /* stat cards */
        #mdStatLabel {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #mdStatValue {{
            font-family: {heading_font};
            font-size: 24px;
            font-weight: 800;
        }}
        #mdStat[tone="success"] #mdStatValue {{ color: {success}; }}

        /* page tabs */
        #mdTabRow {{ border-bottom: 1px solid {p['BORDER']}; }}
        #mdTab {{
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            padding: 10px 14px;
            font-size: 13px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #mdTab:hover {{ color: {p['TEXT']}; }}
        #mdTab:checked {{
            color: {p['BADGE_TEXT']};
            border-bottom: 2px solid {p['PRIMARY']};
        }}

        /* left filter column */
        #mdPanelHeading {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT']};
        }}
        #mdFilter {{
            background: transparent;
            border: 1px solid transparent;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
            text-align: left;
        }}
        #mdFilter:hover {{ background-color: {p['SURFACE_RAISED']}; }}
        #mdFilter:checked {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
        }}
        #mdFilter[soft="true"]:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #mdFilterText {{
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
        }}
        #mdFilterText[on="true"] {{ color: #FFFFFF; }}
        #mdFilterText[on="true"][soft="true"] {{ color: {p['BADGE_TEXT']}; }}
        #mdCount {{
            background-color: {p['SURFACE_RAISED']};
            border-radius: 8px;
            padding: 1px 7px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT_MUTED']};
        }}
        #mdTabCount {{
            background-color: {p['SURFACE_RAISED']};
            border-radius: 8px;
            padding: 1px 7px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #mdPreset {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
            text-align: left;
        }}
        #mdPreset:hover {{ border: 1px solid {p['PRIMARY']}; }}

        /* inputs, shared by the page and the dialogs */
        #mdInput, #mdCombo, #mdSpin, #mdText {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 7px 10px;
            font-size: 12px;
            color: {p['TEXT']};
        }}
        #mdInput:focus, #mdCombo:focus, #mdSpin:focus, #mdText:focus {{
            border: 1px solid {p['PRIMARY']};
        }}
        #mdCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            selection-background-color: {p['PRIMARY_SOFT']};
            color: {p['TEXT']};
            outline: none;
        }}
        #mdSuggest {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['PRIMARY']};
            border-radius: 8px;
            padding: 4px;
            font-size: 12px;
            color: {p['TEXT']};
            outline: none;
        }}
        #mdSuggest::item {{ padding: 7px 8px; border-radius: 6px; }}
        #mdSuggest::item:selected {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['TEXT']};
        }}
        #mdLinked {{
            font-size: 11px;
            font-weight: 600;
            color: {success};
        }}
        #mdUnlinked {{
            font-size: 11px;
            color: {p['TEXT_MUTED']};
        }}

        /* course cards */
        #mdCardTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 800;
        }}
        #mdBadge {{
            border-radius: 8px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 700;
        }}
        #mdBadge[tone="primary"] {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #mdBadge[tone="amber"] {{
            background-color: {_rgba(amber, 0.12)};
            border: 1px solid {amber};
            color: {amber};
        }}
        #mdBadge[tone="danger"] {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {danger};
            color: {danger};
        }}
        #mdBadge[tone="success"] {{
            background-color: {_rgba(success, 0.12)};
            border: 1px solid {success};
            color: {success};
        }}
        #mdChip {{
            background-color: {_rgba(amber, 0.12)};
            border: 1px solid {amber};
            border-radius: 5px;
            padding: 2px 7px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.4px;
            color: {amber};
        }}
        #mdCountdown {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdRemaining {{
            font-family: {heading_font};
            font-size: 14px;
            font-weight: 800;
        }}
        #mdProgress {{
            background-color: {p['BORDER']};
            border: none;
            border-radius: 4px;
            max-height: 8px;
            min-height: 8px;
        }}
        #mdProgress::chunk {{
            background-color: {p['PRIMARY']};
            border-radius: 4px;
        }}
        #mdProgress[tone="danger"]::chunk {{ background-color: {danger}; }}
        #mdProgress[tone="success"]::chunk {{ background-color: {success}; }}
        #mdWarnBox {{
            background-color: {_rgba(amber, 0.08)};
            border: 1px solid {_rgba(amber, 0.6)};
            border-radius: 10px;
        }}
        #mdWarnTitle {{ font-size: 12px; font-weight: 800; color: {amber}; }}
        #mdDangerBox {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {_rgba(danger, 0.6)};
            border-radius: 10px;
        }}
        #mdDangerTitle {{ font-size: 12px; font-weight: 800; color: {danger}; }}
        #mdBoxBody {{ font-size: 11px; color: {p['TEXT']}; }}
        #mdMetaKey {{ font-size: 11px; font-weight: 700; color: {p['TEXT']}; }}
        #mdMetaValue {{ font-size: 11px; color: {p['PRIMARY_TEXT_ON_NAV']}; }}
        #mdDivider {{ background-color: {p['BORDER']}; }}
        #mdEmptyTitle {{
            font-family: {heading_font};
            font-size: 16px;
            font-weight: 800;
        }}

        /* dialogs */
        #mdDialogCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #mdDialogTitle {{
            font-family: {heading_font};
            font-size: 16px;
            font-weight: 800;
        }}
        #mdFieldLabel {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #mdClose {{
            background: transparent;
            border: none;
            font-size: 16px;
            color: {p['TEXT_MUTED']};
            padding: 2px 6px;
        }}
        #mdClose:hover {{ color: {p['TEXT']}; }}
        #mdPresetChip {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 6px;
            padding: 5px 9px;
            font-size: 11px;
            font-weight: 700;
            color: {p['BADGE_TEXT']};
        }}
        #mdPresetChip:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdCheckRow {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        /* log intake + details panel */
        #mdSegment {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 8px 6px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #mdSegment:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdSegment:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #mdGhost {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 9px 12px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #mdGhost:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdSecondarySmall {{
            background-color: transparent;
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #mdSecondarySmall:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdIconTileAmber {{
            background-color: {_rgba(amber, 0.12)};
            border: 1px solid {amber};
            border-radius: 10px;
        }}
        #mdIconTileSoft {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            border-radius: 10px;
        }}
        #mdDialogTabRow, #mdDialogFooter {{ background: transparent; }}
        #mdDialogTabRow {{
            border-top: 1px solid {p['BORDER']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #mdDialogFooter {{ border-top: 1px solid {p['BORDER']}; }}
        #mdTileLabel {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #mdTileValue {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #mdStatTile {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdStatTile[tone="success"] {{
            background-color: {_rgba(success, 0.07)};
            border: 1px solid {_rgba(success, 0.5)};
        }}
        #mdStatTile[tone="amber"] {{
            background-color: {_rgba(amber, 0.07)};
            border: 1px solid {_rgba(amber, 0.5)};
        }}
        #mdStatTile[tone="primary"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
        }}
        #mdStatTileValue {{
            font-family: {heading_font};
            font-size: 20px;
            font-weight: 800;
            color: {p['TEXT']};
        }}
        #mdStatTile[tone="success"] #mdStatTileValue {{ color: {success}; }}
        #mdStatTile[tone="amber"] #mdStatTileValue {{ color: {amber}; }}
        #mdStatTile[tone="primary"] #mdStatTileValue {{ color: {p['BADGE_TEXT']}; }}
        #mdNextDose {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 10px;
        }}
        #mdTable {{
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdTableHead {{
            background-color: {p['SURFACE_RAISED']};
            padding: 10px 12px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #mdTableCell {{ border-bottom: 1px solid {p['BORDER']}; }}
        #mdDoseChip {{
            background-color: {p['SURFACE_RAISED']};
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #mdNote {{ font-size: 11px; font-style: italic; color: {p['TEXT']}; }}
        #mdNoteEmpty {{ font-size: 11px; font-style: italic; color: {p['TEXT_MUTED']}; }}
        /* ------------------------------------------ safety check tab */
        #mdStepNumber {{
            background-color: {p['PRIMARY_SOFT']};
            border-radius: 11px;
            font-size: 11px;
            font-weight: 800;
            color: {p['BADGE_TEXT']};
        }}
        #mdStepTitle {{
            font-family: {heading_font};
            font-size: 14px;
            font-weight: 800;
        }}
        #mdStepHint {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #mdActiveBadge {{
            background-color: {p['PRIMARY_SOFT']};
            border-radius: 8px;
            padding: 2px 9px;
            font-size: 11px;
            font-weight: 800;
            color: {p['BADGE_TEXT']};
        }}
        #mdSearchField {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdSearchInput {{
            background: transparent;
            border: none;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #mdSmallAccent {{ font-size: 11px; color: {p['PRIMARY_TEXT_ON_NAV']}; }}
        #mdSmallBody {{ font-size: 11px; color: {p['TEXT']}; }}
        #mdChipButton {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
        }}
        #mdChipButton:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdChipButton[on="true"] {{
            background-color: {p['PRIMARY']};
            border: 1px solid {p['PRIMARY']};
        }}
        #mdChipText {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #mdChipText[on="true"] {{ color: #FFFFFF; }}
        #mdChipTag {{
            background-color: {p['SURFACE_ALT']};
            border-radius: 4px;
            padding: 1px 5px;
            font-size: 9px;
            font-weight: 800;
            color: {p['TEXT_MUTED']};
        }}
        #mdConditionToggle {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
            text-align: left;
        }}
        #mdConditionToggle:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdConditionToggle[on="true"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
        }}
        #mdToggleTitle {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #mdToggleSub {{ font-size: 10px; color: {p['TEXT_MUTED']}; }}
        #mdToggleSubAccent {{ font-size: 10px; color: {p['PRIMARY_TEXT_ON_NAV']}; }}
        #mdRegimenRow {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdIconButton {{
            background: transparent;
            border: none;
            border-radius: 6px;
            padding: 5px;
        }}
        #mdIconButton:hover {{ background-color: {p['DANGER_SOFT']}; }}
        #mdLinkButton {{
            background: transparent;
            border: none;
            font-size: 12px;
            font-weight: 700;
            color: {p['PRIMARY_TEXT_ON_NAV']};
            padding: 4px 2px;
        }}
        #mdLinkButton:hover {{ text-decoration: underline; }}
        #mdLogHeader {{ background: transparent; border: none; }}
        #mdVerdict {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #mdVerdict[tone="success"] {{
            background-color: {_rgba(success, 0.06)};
            border: 1px solid {_rgba(success, 0.55)};
        }}
        #mdVerdict[tone="amber"] {{
            background-color: {_rgba(amber, 0.06)};
            border: 1px solid {_rgba(amber, 0.6)};
        }}
        #mdVerdict[tone="danger"] {{
            background-color: {_rgba(danger, 0.07)};
            border: 1px solid {_rgba(danger, 0.6)};
        }}
        #mdVerdict[tone="primary"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
        }}
        #mdVerdictTile {{ border-radius: 12px; background-color: {p['PRIMARY']}; }}
        #mdVerdictTile[tone="success"] {{ background-color: {success}; }}
        #mdVerdictTile[tone="amber"] {{ background-color: {amber}; }}
        #mdVerdictTile[tone="danger"] {{ background-color: {danger}; }}
        #mdVerdictName {{
            font-family: {heading_font};
            font-size: 20px;
            font-weight: 800;
        }}
        #mdSectionTitle {{
            font-family: {heading_font};
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0.6px;
        }}
        #mdSubSection {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
            padding-top: 4px;
        }}
        #mdFinding {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #mdFinding[tone="amber"] {{ border: 1px solid {_rgba(amber, 0.55)}; }}
        #mdFinding[tone="danger"] {{ border: 1px solid {_rgba(danger, 0.55)}; }}
        #mdFindingTitle {{ font-size: 13px; font-weight: 800; color: {p['TEXT']}; }}
        #mdFindingAccent {{
            font-size: 13px;
            font-weight: 800;
            color: {p['PRIMARY_TEXT_ON_NAV']};
        }}
        #mdBadge[tone="muted"] {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #mdBadgeFrame {{ border-radius: 8px; }}
        #mdBadgeFrame[tone="success"] {{
            background-color: {_rgba(success, 0.12)}; border: 1px solid {success};
        }}
        #mdBadgeFrame[tone="amber"] {{
            background-color: {_rgba(amber, 0.12)}; border: 1px solid {amber};
        }}
        #mdBadgeFrame[tone="danger"] {{
            background-color: {p['DANGER_SOFT']}; border: 1px solid {danger};
        }}
        #mdBadgeFrame[tone="primary"] {{
            background-color: {p['BADGE_BG']}; border: 1px solid {p['PRIMARY']};
        }}
        #mdBadgeText {{ font-size: 11px; font-weight: 700; }}
        #mdBadgeText[tone="success"] {{ color: {success}; }}
        #mdBadgeText[tone="amber"] {{ color: {amber}; }}
        #mdBadgeText[tone="danger"] {{ color: {danger}; }}
        #mdBadgeText[tone="primary"] {{ color: {p['BADGE_TEXT']}; }}
        #mdError {{ font-size: 12px; font-weight: 600; color: {danger}; }}
    """


def tone_color(tone: str) -> str:
    """The hex colour for a tone in the current theme, for painted icons."""
    from app.core.theme import Theme

    dark = Theme.mode() == "dark"
    return {
        "success": Theme.token("SUCCESS"),
        "danger": Theme.token("DANGER"),
        "amber": AMBER[0 if dark else 1],
        "primary": Theme.token("PRIMARY_TEXT_ON_NAV"),
        "text": Theme.token("TEXT"),
        "white": "#FFFFFF",
    }.get(tone, Theme.token("TEXT_MUTED"))

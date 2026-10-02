"""Stylesheet rules for the Drug Interaction Checker.

Appended to the application stylesheet by Theme.stylesheet(), like the
other *_styles.py files. Every id starts with "ix" so nothing here can
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


def interaction_rules(p: dict, heading_font: str) -> str:
    from app.core.theme import Theme

    dark = Theme.mode() == "dark"
    amber = AMBER[0 if dark else 1]
    success = p["SUCCESS"]
    danger = p["DANGER"]

    return f"""
        /* ------------------------------------------ medication & safety */
        #ixHeaderCard, #ixPanel, #ixCard, #ixStat {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #ixCard[state="abandoned"] {{
            border: 1px solid {_rgba(danger, 0.45)};
        }}
        #ixStat[tone="success"] {{
            background-color: {_rgba(success, 0.06)};
            border: 1px solid {_rgba(success, 0.45)};
        }}
        #ixIconTile {{
            background-color: {p['PRIMARY']};
            border-radius: 10px;
        }}
        #ixTitle {{
            font-family: {heading_font};
            font-size: 22px;
            font-weight: 800;
        }}
        #ixSubtitle, #ixMuted {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #ixSmallMuted {{
            font-size: 11px;
            color: {p['TEXT_MUTED']};
        }}

        /* buttons */
        #ixPrimary {{
            background-color: {p['PRIMARY']};
            border: none;
            border-radius: 8px;
            padding: 9px 16px;
            font-size: 12px;
            font-weight: 700;
            color: #FFFFFF;
        }}
        #ixPrimary:hover {{ background-color: {p['PRIMARY_HOVER']}; }}
        #ixPrimary:disabled {{
            background-color: {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #ixPrimaryWide {{
            background-color: {p['PRIMARY']};
            border: none;
            border-radius: 10px;
            padding: 12px;
            font-size: 13px;
            font-weight: 700;
            color: #FFFFFF;
        }}
        #ixPrimaryWide:hover {{ background-color: {p['PRIMARY_HOVER']}; }}
        #ixSecondary {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 9px 16px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #ixSecondary:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixDangerLink {{
            background: transparent;
            border: none;
            font-size: 12px;
            font-weight: 700;
            color: {danger};
            padding: 4px 2px;
        }}
        #ixDangerLink:hover {{ text-decoration: underline; }}

        /* stat cards */
        #ixStatLabel {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #ixStatValue {{
            font-family: {heading_font};
            font-size: 24px;
            font-weight: 800;
        }}
        #ixStat[tone="success"] #ixStatValue {{ color: {success}; }}

        /* page tabs */
        #ixTabRow {{ border-bottom: 1px solid {p['BORDER']}; }}
        #ixTab {{
            background: transparent;
            border: none;
            border-bottom: 2px solid transparent;
            padding: 10px 14px;
            font-size: 13px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #ixTab:hover {{ color: {p['TEXT']}; }}
        #ixTab:checked {{
            color: {p['BADGE_TEXT']};
            border-bottom: 2px solid {p['PRIMARY']};
        }}

        /* left filter column */
        #ixPanelHeading {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT']};
        }}
        #ixFilter {{
            background: transparent;
            border: 1px solid transparent;
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
            text-align: left;
        }}
        #ixFilter:hover {{ background-color: {p['SURFACE_RAISED']}; }}
        #ixFilter:checked {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
        }}
        #ixFilter[soft="true"]:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #ixFilterText {{
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
        }}
        #ixFilterText[on="true"] {{ color: #FFFFFF; }}
        #ixFilterText[on="true"][soft="true"] {{ color: {p['BADGE_TEXT']}; }}
        #ixCount {{
            background-color: {p['SURFACE_RAISED']};
            border-radius: 8px;
            padding: 1px 7px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT_MUTED']};
        }}
        #ixTabCount {{
            background-color: {p['SURFACE_RAISED']};
            border-radius: 8px;
            padding: 1px 7px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #ixPreset {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 8px 10px;
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
            text-align: left;
        }}
        #ixPreset:hover {{ border: 1px solid {p['PRIMARY']}; }}

        /* inputs, shared by the page and the dialogs */
        #ixInput, #ixCombo, #ixSpin, #ixText {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 7px 10px;
            font-size: 12px;
            color: {p['TEXT']};
        }}
        #ixInput:focus, #ixCombo:focus, #ixSpin:focus, #ixText:focus {{
            border: 1px solid {p['PRIMARY']};
        }}
        #ixCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            selection-background-color: {p['PRIMARY_SOFT']};
            color: {p['TEXT']};
            outline: none;
        }}
        #ixSuggest {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['PRIMARY']};
            border-radius: 8px;
            padding: 4px;
            font-size: 12px;
            color: {p['TEXT']};
            outline: none;
        }}
        #ixSuggest::item {{ padding: 7px 8px; border-radius: 6px; }}
        #ixSuggest::item:selected {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['TEXT']};
        }}
        #ixLinked {{
            font-size: 11px;
            font-weight: 600;
            color: {success};
        }}
        #ixUnlinked {{
            font-size: 11px;
            color: {p['TEXT_MUTED']};
        }}

        /* course cards */
        #ixCardTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 800;
        }}
        #ixBadge {{
            border-radius: 8px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 700;
        }}
        #ixBadge[tone="primary"] {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #ixBadge[tone="amber"] {{
            background-color: {_rgba(amber, 0.12)};
            border: 1px solid {amber};
            color: {amber};
        }}
        #ixBadge[tone="danger"] {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {danger};
            color: {danger};
        }}
        #ixBadge[tone="success"] {{
            background-color: {_rgba(success, 0.12)};
            border: 1px solid {success};
            color: {success};
        }}
        #ixChip {{
            background-color: {_rgba(amber, 0.12)};
            border: 1px solid {amber};
            border-radius: 5px;
            padding: 2px 7px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.4px;
            color: {amber};
        }}
        #ixCountdown {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #ixRemaining {{
            font-family: {heading_font};
            font-size: 14px;
            font-weight: 800;
        }}
        #ixProgress {{
            background-color: {p['BORDER']};
            border: none;
            border-radius: 4px;
            max-height: 8px;
            min-height: 8px;
        }}
        #ixProgress::chunk {{
            background-color: {p['PRIMARY']};
            border-radius: 4px;
        }}
        #ixProgress[tone="danger"]::chunk {{ background-color: {danger}; }}
        #ixProgress[tone="success"]::chunk {{ background-color: {success}; }}
        #ixWarnBox {{
            background-color: {_rgba(amber, 0.08)};
            border: 1px solid {_rgba(amber, 0.6)};
            border-radius: 10px;
        }}
        #ixWarnTitle {{ font-size: 12px; font-weight: 800; color: {amber}; }}
        #ixDangerBox {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {_rgba(danger, 0.6)};
            border-radius: 10px;
        }}
        #ixDangerTitle {{ font-size: 12px; font-weight: 800; color: {danger}; }}
        #ixBoxBody {{ font-size: 11px; color: {p['TEXT']}; }}
        #ixMetaKey {{ font-size: 11px; font-weight: 700; color: {p['TEXT']}; }}
        #ixMetaValue {{ font-size: 11px; color: {p['PRIMARY_TEXT_ON_NAV']}; }}
        #ixDivider {{ background-color: {p['BORDER']}; }}
        #ixEmptyTitle {{
            font-family: {heading_font};
            font-size: 16px;
            font-weight: 800;
        }}

        /* dialogs */
        #ixDialogCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #ixDialogTitle {{
            font-family: {heading_font};
            font-size: 16px;
            font-weight: 800;
        }}
        #ixFieldLabel {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #ixClose {{
            background: transparent;
            border: none;
            font-size: 16px;
            color: {p['TEXT_MUTED']};
            padding: 2px 6px;
        }}
        #ixClose:hover {{ color: {p['TEXT']}; }}
        #ixPresetChip {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 6px;
            padding: 5px 9px;
            font-size: 11px;
            font-weight: 700;
            color: {p['BADGE_TEXT']};
        }}
        #ixPresetChip:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixCheckRow {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        /* log intake + details panel */
        #ixSegment {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 8px 6px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #ixSegment:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixSegment:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #ixGhost {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 9px 12px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #ixGhost:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixSecondarySmall {{
            background-color: transparent;
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #ixSecondarySmall:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixIconTileAmber {{
            background-color: {_rgba(amber, 0.12)};
            border: 1px solid {amber};
            border-radius: 10px;
        }}
        #ixIconTileSoft {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            border-radius: 10px;
        }}
        #ixDialogTabRow, #ixDialogFooter {{ background: transparent; }}
        #ixDialogTabRow {{
            border-top: 1px solid {p['BORDER']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #ixDialogFooter {{ border-top: 1px solid {p['BORDER']}; }}
        #ixTileLabel {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #ixTileValue {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #ixStatTile {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #ixStatTile[tone="success"] {{
            background-color: {_rgba(success, 0.07)};
            border: 1px solid {_rgba(success, 0.5)};
        }}
        #ixStatTile[tone="amber"] {{
            background-color: {_rgba(amber, 0.07)};
            border: 1px solid {_rgba(amber, 0.5)};
        }}
        #ixStatTile[tone="primary"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
        }}
        #ixStatTileValue {{
            font-family: {heading_font};
            font-size: 20px;
            font-weight: 800;
            color: {p['TEXT']};
        }}
        #ixStatTile[tone="success"] #ixStatTileValue {{ color: {success}; }}
        #ixStatTile[tone="amber"] #ixStatTileValue {{ color: {amber}; }}
        #ixStatTile[tone="primary"] #ixStatTileValue {{ color: {p['BADGE_TEXT']}; }}
        #ixNextDose {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 10px;
        }}
        #ixTable {{
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #ixTableHead {{
            background-color: {p['SURFACE_RAISED']};
            padding: 10px 12px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #ixTableCell {{ border-bottom: 1px solid {p['BORDER']}; }}
        #ixDoseChip {{
            background-color: {p['SURFACE_RAISED']};
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #ixNote {{ font-size: 11px; font-style: italic; color: {p['TEXT']}; }}
        #ixNoteEmpty {{ font-size: 11px; font-style: italic; color: {p['TEXT_MUTED']}; }}
        /* ------------------------------------------ safety check tab */
        #ixStepNumber {{
            background-color: {p['PRIMARY_SOFT']};
            border-radius: 11px;
            font-size: 11px;
            font-weight: 800;
            color: {p['BADGE_TEXT']};
        }}
        #ixStepTitle {{
            font-family: {heading_font};
            font-size: 14px;
            font-weight: 800;
        }}
        #ixStepHint {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #ixActiveBadge {{
            background-color: {p['PRIMARY_SOFT']};
            border-radius: 8px;
            padding: 2px 9px;
            font-size: 11px;
            font-weight: 800;
            color: {p['BADGE_TEXT']};
        }}
        #ixSearchField {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #ixSearchInput {{
            background: transparent;
            border: none;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #ixSmallAccent {{ font-size: 11px; color: {p['PRIMARY_TEXT_ON_NAV']}; }}
        #ixSmallBody {{ font-size: 11px; color: {p['TEXT']}; }}
        #ixChipButton {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
        }}
        #ixChipButton:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixChipButton[on="true"] {{
            background-color: {p['PRIMARY']};
            border: 1px solid {p['PRIMARY']};
        }}
        #ixChipText {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #ixChipText[on="true"] {{ color: #FFFFFF; }}
        #ixChipTag {{
            background-color: {p['SURFACE_ALT']};
            border-radius: 4px;
            padding: 1px 5px;
            font-size: 9px;
            font-weight: 800;
            color: {p['TEXT_MUTED']};
        }}
        #ixConditionToggle {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
            text-align: left;
        }}
        #ixConditionToggle:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixConditionToggle[on="true"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
        }}
        #ixToggleTitle {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #ixToggleSub {{ font-size: 10px; color: {p['TEXT_MUTED']}; }}
        #ixToggleSubAccent {{ font-size: 10px; color: {p['PRIMARY_TEXT_ON_NAV']}; }}
        #ixRegimenRow {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #ixIconButton {{
            background: transparent;
            border: none;
            border-radius: 6px;
            padding: 5px;
        }}
        #ixIconButton:hover {{ background-color: {p['DANGER_SOFT']}; }}
        #ixLinkButton {{
            background: transparent;
            border: none;
            font-size: 12px;
            font-weight: 700;
            color: {p['PRIMARY_TEXT_ON_NAV']};
            padding: 4px 2px;
        }}
        #ixLinkButton:hover {{ text-decoration: underline; }}
        #ixLogHeader {{ background: transparent; border: none; }}
        #ixVerdict {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #ixVerdict[tone="success"] {{
            background-color: {_rgba(success, 0.06)};
            border: 1px solid {_rgba(success, 0.55)};
        }}
        #ixVerdict[tone="amber"] {{
            background-color: {_rgba(amber, 0.06)};
            border: 1px solid {_rgba(amber, 0.6)};
        }}
        #ixVerdict[tone="danger"] {{
            background-color: {_rgba(danger, 0.07)};
            border: 1px solid {_rgba(danger, 0.6)};
        }}
        #ixVerdict[tone="primary"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
        }}
        #ixVerdictTile {{ border-radius: 12px; background-color: {p['PRIMARY']}; }}
        #ixVerdictTile[tone="success"] {{ background-color: {success}; }}
        #ixVerdictTile[tone="amber"] {{ background-color: {amber}; }}
        #ixVerdictTile[tone="danger"] {{ background-color: {danger}; }}
        #ixVerdictName {{
            font-family: {heading_font};
            font-size: 20px;
            font-weight: 800;
        }}
        #ixSectionTitle {{
            font-family: {heading_font};
            font-size: 13px;
            font-weight: 800;
            letter-spacing: 0.6px;
        }}
        #ixSubSection {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
            padding-top: 4px;
        }}
        #ixFinding {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #ixFinding[tone="amber"] {{ border: 1px solid {_rgba(amber, 0.55)}; }}
        #ixFinding[tone="danger"] {{ border: 1px solid {_rgba(danger, 0.55)}; }}
        #ixFindingTitle {{ font-size: 13px; font-weight: 800; color: {p['TEXT']}; }}
        #ixFindingAccent {{
            font-size: 13px;
            font-weight: 800;
            color: {p['PRIMARY_TEXT_ON_NAV']};
        }}
        #ixBadge[tone="muted"] {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #ixBadgeFrame {{ border-radius: 8px; }}
        #ixBadgeFrame[tone="success"] {{
            background-color: {_rgba(success, 0.12)}; border: 1px solid {success};
        }}
        #ixBadgeFrame[tone="amber"] {{
            background-color: {_rgba(amber, 0.12)}; border: 1px solid {amber};
        }}
        #ixBadgeFrame[tone="danger"] {{
            background-color: {p['DANGER_SOFT']}; border: 1px solid {danger};
        }}
        #ixBadgeFrame[tone="primary"] {{
            background-color: {p['BADGE_BG']}; border: 1px solid {p['PRIMARY']};
        }}
        #ixBadgeText {{ font-size: 11px; font-weight: 700; }}
        #ixBadgeText[tone="success"] {{ color: {success}; }}
        #ixBadgeText[tone="amber"] {{ color: {amber}; }}
        #ixBadgeText[tone="danger"] {{ color: {danger}; }}
        #ixBadgeText[tone="primary"] {{ color: {p['BADGE_TEXT']}; }}
        /* ------------------------------------ interaction checker extras */
        #ixRefBadge {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 5px;
            padding: 2px 8px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['BADGE_TEXT']};
        }}
        #ixStatTile {{ border-radius: 10px; }}
        #ixStatTile[tone="primary"] {{
            background-color: {p['PRIMARY_SOFT']}; border: 1px solid {p['BADGE_BORDER']};
        }}
        #ixStatTile[tone="success"] {{
            background-color: {_rgba(success, 0.10)}; border: 1px solid {_rgba(success, 0.4)};
        }}
        #ixStatTile[tone="amber"] {{
            background-color: {_rgba(amber, 0.10)}; border: 1px solid {_rgba(amber, 0.4)};
        }}
        #ixBigNumber {{
            font-family: {heading_font};
            font-size: 22px;
            font-weight: 800;
        }}
        #ixSectionPanel {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #ixSectionPanel[tone="danger"] {{
            background-color: {_rgba(danger, 0.05)};
            border: 1px solid {_rgba(danger, 0.5)};
        }}
        #ixInnerCard {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #ixInnerCard[tone="amber"] {{ border: 1px solid {_rgba(amber, 0.55)}; }}
        #ixInnerCard[tone="danger"] {{ border: 1px solid {_rgba(danger, 0.55)}; }}
        #ixGuidance {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
        }}
        #ixGuidance[tone="amber"] {{
            background-color: {_rgba(amber, 0.07)}; border: 1px solid {_rgba(amber, 0.5)};
        }}
        #ixGuidance[tone="danger"] {{
            background-color: {_rgba(danger, 0.07)}; border: 1px solid {_rgba(danger, 0.5)};
        }}
        #ixGuidanceKey {{ font-size: 11px; font-weight: 800; color: {p['BADGE_TEXT']}; }}
        #ixGuidanceKey[tone="amber"] {{ color: {amber}; }}
        #ixGuidanceKey[tone="danger"] {{ color: {danger}; }}
        #ixDrugChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 5px;
            padding: 2px 7px;
            font-family: Consolas, monospace;
            font-size: 10px;
            color: {p['BADGE_TEXT']};
        }}
        #ixTag {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 5px;
            padding: 2px 7px;
            font-size: 10px;
            color: {p['BADGE_TEXT']};
        }}
        #ixFilterChip {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 7px;
            padding: 4px 10px;
            font-size: 11px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #ixFilterChip:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixFilterChip:checked {{
            background-color: {p['PRIMARY']};
            border: 1px solid {p['PRIMARY']};
            color: #FFFFFF;
        }}
        #ixFilterChip[tone="danger"] {{ color: {danger}; }}
        #ixFilterChip[tone="amber"] {{ color: {amber}; }}
        #ixFilterChip[tone="success"] {{ color: {success}; }}
        #ixFilterChip[tone]:checked {{ color: #FFFFFF; }}
        #ixCaseTitle {{
            font-family: {heading_font};
            font-size: 14px;
            font-weight: 800;
        }}
        #ixDrugTitle {{
            font-family: {heading_font};
            font-size: 24px;
            font-weight: 800;
        }}
        #ixNoteBox {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 8px;
        }}
        #ixNoteText {{ font-size: 11px; font-weight: 700; color: {p['BADGE_TEXT']}; }}
        #ixCheckInCase {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 11px;
            font-weight: 700;
            color: {p['BADGE_TEXT']};
        }}
        #ixCheckInCase:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixSuggestList {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
            outline: none;
            font-size: 12px;
            color: {p['TEXT']};
        }}
        #ixSuggestList::item {{ padding: 8px 10px; border-radius: 6px; }}
        #ixSuggestList::item:selected, #ixSuggestList::item:hover {{
            background-color: {p['PRIMARY_SOFT']};
        }}
        #ixVerdictTileSoft {{
            border-radius: 12px;
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
        }}
        #ixVerdictTileSoft[tone="success"] {{
            background-color: {_rgba(success, 0.12)}; border: 1px solid {_rgba(success, 0.5)};
        }}
        #ixVerdictTileSoft[tone="amber"] {{
            background-color: {_rgba(amber, 0.12)}; border: 1px solid {_rgba(amber, 0.5)};
        }}
        #ixVerdictTileSoft[tone="danger"] {{
            background-color: {_rgba(danger, 0.12)}; border: 1px solid {_rgba(danger, 0.5)};
        }}
        #ixIconButtonPlain {{ background: transparent; border: none; padding: 4px; }}
        #ixIconBox {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 7px;
        }}
        #ixIconBox:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ixError {{ font-size: 12px; font-weight: 600; color: {danger}; }}
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

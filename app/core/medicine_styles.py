"""Stylesheet rules for the Medicine Reference (object names start "md").

Appended to the application stylesheet by Theme.stylesheet(), like
emergency_styles.py and wellness_styles.py.

Tier colours come from the reference build and are the same in both themes,
because a weight of 10 should read as critical either way.
"""

CATEGORY = {"otc": "#10B981", "rx": "#6366F1", "controlled": "#F59E0B"}
DANGER_RED = "#F43F5E"
AMBER = "#F59E0B"
GOOD = "#10B981"


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def medicine_rules(p: dict, heading_font: str) -> str:
    category_rules = "".join(f"""
        #mdCategoryBadge[category="{key}"] {{
            background-color: {_rgba(colour, 0.15)};
            border: 1px solid {_rgba(colour, 0.55)};
            color: {colour};
        }}""" for key, colour in CATEGORY.items())

    return category_rules + f"""
        /* --------------------------------------------- symptom encyclopedia */
        #mdScopeNote {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 10px;
        }}
        #mdScopeTitle {{ font-size: 12px; font-weight: 800; color: {p['BADGE_TEXT']}; }}
        #mdScopeText {{ font-size: 12px; color: {p['TEXT']}; }}

        #mdToggle {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdToggleButton {{
            background: transparent;
            border: none;
            border-radius: 7px;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT_MUTED']};
        }}
        #mdToggleButton:checked {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['BADGE_TEXT']};
        }}

        #mdFilterBar {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #mdCombo {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #mdCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            color: {p['TEXT']};
            selection-background-color: {p['PRIMARY_SOFT']};
            selection-color: {p['TEXT']};
        }}
        #mdStatus {{ font-size: 13px; color: {p['TEXT_MUTED']}; padding: 24px; }}

        /* ------------------------------------------------------- cards */
        #mdCard, #mdRow {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #mdCard:hover, #mdRow:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdSystemChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.4px;
            color: {p['TEXT_MUTED']};
        }}
        #mdTierBadge, #mdWeightPill {{
            border-radius: 8px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.3px;
        }}
        #mdCardTitle {{
            font-family: {heading_font};
            font-size: 17px;
            font-weight: 800;
        }}
        #mdCardSci {{ font-size: 12px; font-style: italic; color: {p['BADGE_TEXT']}; }}
        #mdCardBody {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #mdCardDivider {{ background-color: {p['BORDER']}; }}
        #mdSectionLabel {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #mdChip, #mdRelatedChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 7px;
            padding: 3px 9px;
            font-size: 11px;
            color: {p['TEXT']};
        }}
        #mdRelatedChip {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            color: {p['BADGE_TEXT']};
            font-weight: 600;
        }}
        #mdChipMore {{ font-size: 11px; color: {p['TEXT_MUTED']}; padding: 3px 4px; }}
        #mdFlagCount {{
            background-color: {p['DANGER_SOFT']};
            border-radius: 6px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 700;
            color: {p['DANGER']};
        }}
        #mdLink {{ font-size: 12px; font-weight: 700; color: {p['BADGE_TEXT']}; }}

        /* --------------------------------------- 7-part entry list rows */
        #mdRowIndex {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 800;
            color: {p['TEXT_MUTED']};
        }}
        #mdRowTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 800;
        }}
        #mdPartLabel {{
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 0.4px;
            color: {p['TEXT_MUTED']};
        }}
        #mdPartValue {{ font-size: 12px; color: {p['TEXT']}; }}

        /* ------------------------------------------------------ detail */
        #mdBackButton, #mdGhostAction, #mdBookmark {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
            padding: 7px 14px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #mdBackButton:hover, #mdGhostAction:hover, #mdBookmark:hover {{
            border: 1px solid {p['PRIMARY']};
        }}
        #mdBookmark:checked {{ color: {p['BADGE_TEXT']}; border: 1px solid {p['PRIMARY']}; }}
        #mdPrimaryAction {{
            background-color: {p['PRIMARY']};
            border: none;
            border-radius: 9px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 700;
            color: #FFFFFF;
        }}
        #mdPrimaryAction:hover {{ background-color: {p['PRIMARY_HOVER']}; }}

        #mdRailBox {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #mdRailLink {{
            background: transparent;
            border: none;
            border-radius: 8px;
            padding: 8px 10px;
            text-align: left;
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #mdRailLink:hover {{ background-color: {p['PRIMARY_SOFT']}; color: {p['TEXT']}; }}
        #mdRailLink:checked {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
            font-weight: 700;
        }}
        #mdRailJump {{
            background: transparent;
            border: none;
            padding: 8px 10px;
            text-align: left;
            font-size: 12px;
            font-weight: 700;
            color: {p['BADGE_TEXT']};
        }}
        #mdProgress {{ font-size: 11px; font-weight: 800; color: {p['BADGE_TEXT']}; }}
        #mdCrossLinks {{ font-size: 10px; font-weight: 800; color: {p['BADGE_TEXT']}; }}
        #mdGlanceKey {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #mdGlanceValue {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}

        #mdSection, #mdCorrelation {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #mdCorrelation {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
        }}
        #mdCorrelationText {{ font-size: 13px; color: {p['TEXT']}; }}
        #mdRedSection {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']};
            border-radius: 14px;
        }}
        #mdHeading, #mdRedHeading {{
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.6px;
        }}
        #mdRedHeading {{ color: {p['DANGER']}; }}
        #mdBodyLarge {{ font-size: 14px; color: {p['TEXT']}; }}
        #mdBody {{ font-size: 12px; color: {p['TEXT']}; }}
        #mdStrong {{ font-size: 12px; font-weight: 800; color: {p['TEXT']}; }}
        #mdMuted {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #mdEmptyCentre {{ font-size: 12px; color: {p['TEXT_MUTED']}; padding: 14px; }}

        #mdWeightBox, #mdFactBox, #mdCauseBox, #mdRef {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdWeightValue {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #mdWeightBar {{
            background-color: {p['BORDER']};
            border: none;
            border-radius: 4px;
        }}
        #mdFactValue {{ font-size: 14px; font-weight: 700; color: {p['TEXT']}; }}
        #mdFactAccent {{ font-size: 14px; font-weight: 700; color: {p['BADGE_TEXT']}; }}
        #mdBullet {{ font-size: 11px; color: {p['BADGE_TEXT']}; }}
        #mdItem {{ font-size: 12px; color: {p['TEXT']}; }}

        #mdConditionCard {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdConditionCard:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #mdConditionName {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #mdConditionMeta {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #mdChevron {{ font-size: 16px; color: {p['TEXT_MUTED']}; }}

        #mdFlagBox {{
            background-color: {p['SURFACE']};
            border: 1px solid {_rgba(DANGER_RED, 0.4)};
            border-radius: 10px;
        }}
        #mdFlagIntro {{ font-size: 11px; font-weight: 700; color: {p['DANGER']}; }}
        #mdFlagItem {{ font-size: 12px; color: {p['TEXT']}; }}

        #mdRefPrimary {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            border-radius: 10px;
        }}
        #mdRefTier, #mdRefTierPrimary {{
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}
        #mdRefTierPrimary {{ background-color: {p['PRIMARY']}; color: #FFFFFF; }}
        #mdRefTier {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #mdRefSource {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #mdRefCitation {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
            /* ----------------------------------------- medicine reference only */
        #mdCardClass, #mdUses, #mdBody {{ font-size: 12px; color: {p['TEXT']}; }}
        #mdCardGeneric {{ font-size: 12px; font-style: italic; color: {p['TEXT_MUTED']}; }}
        #mdBrandBox {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdBrandPh, #mdBrandIntl {{ font-size: 12px; color: {p['BADGE_TEXT']}; }}
        #mdCopyLink {{
            background: transparent;
            border: none;
            padding: 0px;
            font-size: 12px;
            color: {p['TEXT_MUTED']};
            text-align: left;
        }}
        #mdCopyLink:hover {{ color: {p['TEXT']}; }}
        #mdNotice {{
            background-color: {_rgba(AMBER, 0.10)};
            border: 1px solid {_rgba(AMBER, 0.45)};
            border-radius: 10px;
        }}
        #mdNoticeText {{ font-size: 11px; color: {AMBER}; }}
        #mdDosageBox {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdDosageText {{
            font-family: "Consolas", "Courier New", monospace;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #mdGoodTile, #mdWarnTile, #mdBadTile {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #mdGoodTile {{ border: 1px solid {_rgba(GOOD, 0.45)}; }}
        #mdWarnTile {{ border: 1px solid {_rgba(AMBER, 0.45)}; }}
        #mdBadTile  {{ border: 1px solid {_rgba(DANGER_RED, 0.45)}; }}
        #mdGoodTileMarker {{ font-size: 12px; font-weight: 800; color: {GOOD}; }}
        #mdWarnTileMarker {{ font-size: 11px; color: {AMBER}; }}
        #mdBadTileMarker  {{ font-size: 12px; font-weight: 800; color: {DANGER_RED}; }}
        #mdBlackBoxBadge {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']};
            border-radius: 8px;
            padding: 3px 9px;
            font-size: 10px;
            font-weight: 800;
            color: {p['DANGER']};
        }}
        #mdBlackBoxText {{ font-size: 13px; font-weight: 600; color: {p['DANGER']}; }}
        #mdGlanceDanger {{ font-size: 12px; font-weight: 800; color: {p['DANGER']}; }}
        #mdCategoryBadge {{
            border-radius: 8px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.3px;
        }}
    """
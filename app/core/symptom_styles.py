"""Stylesheet rules for the Symptom Encyclopedia (object names start "sy").

Appended to the application stylesheet by Theme.stylesheet(), like
emergency_styles.py and wellness_styles.py.

Tier colours come from the reference build and are the same in both themes,
because a weight of 10 should read as critical either way.
"""

TIERS = {
    "critical": "#F43F5E",
    "high": "#F59E0B",
    "moderate": "#6366F1",
    "mild": "#10B981",
}
SEVERITY = {"severe": "#F43F5E", "moderate": "#F59E0B", "mild": "#10B981"}


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def symptom_rules(p: dict, heading_font: str) -> str:
    tier_rules = "".join(f"""
        #syTierBadge[tier="{key}"], #syWeightPill[tier="{key}"] {{
            background-color: {_rgba(colour, 0.15)};
            border: 1px solid {_rgba(colour, 0.55)};
            color: {colour};
        }}
        #syWeightBar[tier="{key}"]::chunk {{
            background-color: {colour};
            border-radius: 4px;
        }}""" for key, colour in TIERS.items())

    severity_rules = "".join(f"""
        #syConditionMeta[severity="{key}"] {{ color: {colour}; }}"""
                             for key, colour in SEVERITY.items())

    return tier_rules + severity_rules + f"""
        /* --------------------------------------------- symptom encyclopedia */
        #syScopeNote {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 10px;
        }}
        #syScopeTitle {{ font-size: 12px; font-weight: 800; color: {p['BADGE_TEXT']}; }}
        #syScopeText {{ font-size: 12px; color: {p['TEXT']}; }}

        #syToggle {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #syToggleButton {{
            background: transparent;
            border: none;
            border-radius: 7px;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT_MUTED']};
        }}
        #syToggleButton:checked {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['BADGE_TEXT']};
        }}

        #syFilterBar {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #syCombo {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #syCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            color: {p['TEXT']};
            selection-background-color: {p['PRIMARY_SOFT']};
            selection-color: {p['TEXT']};
        }}
        #syStatus {{ font-size: 13px; color: {p['TEXT_MUTED']}; padding: 24px; }}

        /* ------------------------------------------------------- cards */
        #syCard, #syRow {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 16px;
        }}
        #syCard:hover, #syRow:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #sySystemChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.4px;
            color: {p['TEXT_MUTED']};
        }}
        #syTierBadge, #syWeightPill {{
            border-radius: 8px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.3px;
        }}
        #syCardTitle {{
            font-family: {heading_font};
            font-size: 17px;
            font-weight: 800;
        }}
        #syCardSci {{ font-size: 12px; font-style: italic; color: {p['BADGE_TEXT']}; }}
        #syCardBody {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #syCardDivider {{ background-color: {p['BORDER']}; }}
        #sySectionLabel {{
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #syChip, #syRelatedChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 7px;
            padding: 3px 9px;
            font-size: 11px;
            color: {p['TEXT']};
        }}
        #syRelatedChip {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            color: {p['BADGE_TEXT']};
            font-weight: 600;
        }}
        #syChipMore {{ font-size: 11px; color: {p['TEXT_MUTED']}; padding: 3px 4px; }}
        #syFlagCount {{
            background-color: {p['DANGER_SOFT']};
            border-radius: 6px;
            padding: 3px 9px;
            font-size: 11px;
            font-weight: 700;
            color: {p['DANGER']};
        }}
        #syLink {{ font-size: 12px; font-weight: 700; color: {p['BADGE_TEXT']}; }}

        /* --------------------------------------- 7-part entry list rows */
        #syRowIndex {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 800;
            color: {p['TEXT_MUTED']};
        }}
        #syRowTitle {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 800;
        }}
        #syPartLabel {{
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 0.4px;
            color: {p['TEXT_MUTED']};
        }}
        #syPartValue {{ font-size: 12px; color: {p['TEXT']}; }}

        /* ------------------------------------------------------ detail */
        #syBackButton, #syGhostAction, #syBookmark {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
            padding: 7px 14px;
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #syBackButton:hover, #syGhostAction:hover, #syBookmark:hover {{
            border: 1px solid {p['PRIMARY']};
        }}
        #syBookmark:checked {{ color: {p['BADGE_TEXT']}; border: 1px solid {p['PRIMARY']}; }}
        #syPrimaryAction {{
            background-color: {p['PRIMARY']};
            border: none;
            border-radius: 9px;
            padding: 8px 16px;
            font-size: 12px;
            font-weight: 700;
            color: #FFFFFF;
        }}
        #syPrimaryAction:hover {{ background-color: {p['PRIMARY_HOVER']}; }}

        #syRailBox {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #syRailLink {{
            background: transparent;
            border: none;
            border-radius: 8px;
            padding: 8px 10px;
            text-align: left;
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #syRailLink:hover {{ background-color: {p['PRIMARY_SOFT']}; color: {p['TEXT']}; }}
        #syRailLink:checked {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
            font-weight: 700;
        }}
        #syRailJump {{
            background: transparent;
            border: none;
            padding: 8px 10px;
            text-align: left;
            font-size: 12px;
            font-weight: 700;
            color: {p['BADGE_TEXT']};
        }}
        #syProgress {{ font-size: 11px; font-weight: 800; color: {p['BADGE_TEXT']}; }}
        #syCrossLinks {{ font-size: 10px; font-weight: 800; color: {p['BADGE_TEXT']}; }}
        #syGlanceKey {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #syGlanceValue {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}

        #sySection, #syCorrelation {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #syCorrelation {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
        }}
        #syCorrelationText {{ font-size: 13px; color: {p['TEXT']}; }}
        #syRedSection {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']};
            border-radius: 14px;
        }}
        #syHeading, #syRedHeading {{
            font-size: 12px;
            font-weight: 800;
            letter-spacing: 0.6px;
        }}
        #syRedHeading {{ color: {p['DANGER']}; }}
        #syBodyLarge {{ font-size: 14px; color: {p['TEXT']}; }}
        #syBody {{ font-size: 12px; color: {p['TEXT']}; }}
        #syStrong {{ font-size: 12px; font-weight: 800; color: {p['TEXT']}; }}
        #syMuted {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #syEmptyCentre {{ font-size: 12px; color: {p['TEXT_MUTED']}; padding: 14px; }}

        #syWeightBox, #syFactBox, #syCauseBox, #syRef {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #syWeightValue {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #syWeightBar {{
            background-color: {p['BORDER']};
            border: none;
            border-radius: 4px;
        }}
        #syFactValue {{ font-size: 14px; font-weight: 700; color: {p['TEXT']}; }}
        #syFactAccent {{ font-size: 14px; font-weight: 700; color: {p['BADGE_TEXT']}; }}
        #syBullet {{ font-size: 11px; color: {p['BADGE_TEXT']}; }}
        #syItem {{ font-size: 12px; color: {p['TEXT']}; }}

        #syConditionCard {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #syConditionCard:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #syConditionName {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #syConditionMeta {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #syChevron {{ font-size: 16px; color: {p['TEXT_MUTED']}; }}

        #syFlagBox {{
            background-color: {p['SURFACE']};
            border: 1px solid {_rgba(TIERS['critical'], 0.4)};
            border-radius: 10px;
        }}
        #syFlagIntro {{ font-size: 11px; font-weight: 700; color: {p['DANGER']}; }}
        #syFlagItem {{ font-size: 12px; color: {p['TEXT']}; }}

        #syRefPrimary {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            border-radius: 10px;
        }}
        #syRefTier, #syRefTierPrimary {{
            border-radius: 6px;
            padding: 3px 8px;
            font-size: 9px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}
        #syRefTierPrimary {{ background-color: {p['PRIMARY']}; color: #FFFFFF; }}
        #syRefTier {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #syRefSource {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #syRefCitation {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
    """
"""Stylesheet rules for the Emergency Guide.

Kept out of theme.py so that file doesn't keep growing, but still appended to
the ONE application stylesheet (see the last line of Theme.stylesheet()).

That matters: WrapChip measures its own size when it is created, using the
application stylesheet. Rules set on the view with setStyleSheet() would
arrive too late and every chip would be measured without its padding.

The hero card stays red in both themes. It's the one thing on this page that
must never blend in.
"""

HERO_RED = "#E11D48"
AMBER = "#F59E0B"
AMBER_SOFT = "rgba(245, 158, 11, 0.12)"


def emergency_rules(p: dict, heading_font: str) -> str:
    return f"""
        /* ---------------------------------------------- emergency guide */
        #emHero {{
            background-color: {HERO_RED};
            border-radius: 16px;
        }}
        #emHero QLabel {{
            color: #FFFFFF;
        }}
        #emHeroKicker {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
        }}
        #emHeroNumber {{
            font-family: {heading_font};
            font-size: 60px;
            font-weight: 800;
        }}
        #emHeroText, #emHeroTip {{
            font-size: 13px;
        }}
        #emHeroTips {{
            background-color: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.25);
            border-radius: 12px;
        }}

        #emSectionHeading {{
            font-family: {heading_font};
            font-size: 16px;
            font-weight: 700;
        }}

        #emHotlineCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #emHotlineName {{
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #emHotlineNumber {{
            font-family: {heading_font};
            font-size: 22px;
            font-weight: 800;
            color: {p['DANGER']};
        }}
        #emHotlineAlt {{
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT']};
        }}
        #emHotlineDesc {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #emLocalNote {{
            font-size: 12px;
            font-style: italic;
            color: {p['TEXT_MUTED']};
        }}

        #emProtocolCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #emProtocolCard[focused="true"] {{
            border: 2px solid {p['PRIMARY']};
        }}
        #emProtocolTitle {{
            font-family: {heading_font};
            font-size: 17px;
            font-weight: 700;
        }}
        #emLocalName {{
            font-size: 13px;
            font-style: italic;
            color: {p['TEXT_MUTED']};
        }}
        #emBadgeCritical, #emBadgeUrgent, #emBadgeSameDay {{
            border-radius: 7px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 800;
            letter-spacing: 0.5px;
        }}
        #emBadgeCritical {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']};
            color: {p['DANGER']};
        }}
        #emBadgeUrgent {{
            background-color: {AMBER_SOFT};
            border: 1px solid {AMBER};
            color: {AMBER};
        }}
        #emBadgeSameDay {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            color: {p['BADGE_TEXT']};
        }}
        #emSectionLabel {{
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
            padding-top: 4px;
        }}
        #emWarningChip {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']};
            border-radius: 7px;
            padding: 4px 10px;
            font-size: 12px;
            color: {p['DANGER']};
        }}
        #emAvoidChip {{
            background-color: {p['SURFACE_ALT']};
            border: 1px dashed {p['ICON_MUTED']};
            border-radius: 7px;
            padding: 4px 10px;
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #emStepNumber {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['BADGE_TEXT']};
            border-radius: 12px;
            font-size: 12px;
            font-weight: 700;
        }}
        #emStepText {{
            font-size: 13px;
            padding-top: 3px;
        }}
        #emCallBox {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']};
            border-radius: 10px;
        }}
        #emCallTitle {{
            font-size: 11px;
            font-weight: 800;
            letter-spacing: 0.6px;
            color: {p['DANGER']};
        }}
        #emCallText {{
            font-size: 13px;
        }}
        #emSource {{
            font-size: 11px;
            font-style: italic;
            color: {p['TEXT_MUTED']};
        }}
        #emEmpty {{
            font-size: 13px;
            color: {p['TEXT_MUTED']};
            padding: 24px;
        }}
        #emDisclaimer {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #emDisclaimerText {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
    """
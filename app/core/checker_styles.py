"""Stylesheet rules for the Symptom Correlation Engine (names start "cc").

Appended to the application stylesheet by Theme.stylesheet(), like the other
module sheets.

Triage and urgency colours are fixed rather than themed: an emergency has to
read as an emergency in light mode too.
"""

DANGER_RED = "#F43F5E"
AMBER = "#F59E0B"
GOOD = "#10B981"
INFO = "#38BDF8"

URGENCY = {
    "emergency": DANGER_RED,
    "seek_urgent_care": AMBER,
    "see_doctor_soon": INFO,
    "self_care": GOOD,
    "none": "#9CA3AF",
}
LEVELS = {"high": GOOD, "mid": AMBER, "low": DANGER_RED}
TRIAGE = {"bad": DANGER_RED, "warn": AMBER, "info": INFO, "good": GOOD}


def _rgba(hex_colour: str, alpha: float) -> str:
    h = hex_colour.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r}, {g}, {b}, {alpha})"


def checker_rules(p: dict, heading_font: str) -> str:
    urgency_rules = "".join(f"""
        #ccUrgencyPill[urgency="{key}"] {{
            background-color: {_rgba(colour, 0.14)};
            border: 1px solid {_rgba(colour, 0.5)};
            color: {colour};
        }}""" for key, colour in URGENCY.items())

    level_rules = "".join(f"""
        #ccSpecBadge[level="{key}"], #ccIntensityValue[level="{key}"] {{
            color: {colour};
        }}""" for key, colour in LEVELS.items())

    triage_rules = "".join(f"""
        #ccCard[triage="{key}"], #ccRedCard[triage="{key}"] {{
            border: 1px solid {colour};
            background-color: {_rgba(colour, 0.07)};
        }}""" for key, colour in TRIAGE.items())

    return urgency_rules + level_rules + triage_rules + f"""
        /* ------------------------------------- symptom correlation engine */
        #ccCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #ccRedCard {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']};
            border-radius: 14px;
        }}
        #ccInnerBox, #ccSymptomTile {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #ccHeading, #ccRedHeading {{
            font-size: 12px; font-weight: 800; letter-spacing: 0.6px;
        }}
        #ccRedHeading {{ color: {p['DANGER']}; }}
        #ccSectionTitle {{
            font-family: {heading_font};
            font-size: 14px; font-weight: 800; letter-spacing: 0.5px;
            color: {p['BADGE_TEXT']};
        }}
        #ccLabel, #ccFieldLabel {{
            font-size: 10px; font-weight: 800; letter-spacing: 0.6px;
            color: {p['TEXT_MUTED']};
        }}
        #ccBody {{ font-size: 13px; color: {p['TEXT']}; }}
        #ccRedBody {{ font-size: 12px; color: {p['DANGER']}; }}
        #ccMuted {{ font-size: 12px; color: {p['TEXT_MUTED']}; }}
        #ccBooster {{ font-size: 12px; color: {AMBER}; }}
        #ccGood {{ font-size: 12px; font-weight: 700; color: {GOOD}; }}
        #ccWarn {{ font-size: 12px; font-weight: 700; color: {AMBER}; }}
        #ccBad  {{ font-size: 12px; color: {DANGER_RED}; }}

        #ccEngineBadge {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 7px; padding: 3px 9px;
            font-size: 10px; font-weight: 800; color: {p['BADGE_TEXT']};
        }}
        #ccDisclaimer {{
            background-color: {_rgba(AMBER, 0.10)};
            border: 1px solid {_rgba(AMBER, 0.45)};
            border-radius: 10px;
        }}
        #ccDisclaimerTitle {{ font-size: 12px; font-weight: 800; color: {AMBER}; }}
        #ccDisclaimerText {{ font-size: 12px; color: {p['TEXT']}; }}

        /* symptom picker */
        #ccSymptomRow {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
        }}
        #ccSymptomRow:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ccSymptomRow[selected="true"] {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
        }}
        #ccSymptomName {{ font-size: 13px; font-weight: 700; color: {p['TEXT']}; }}
        #ccSymptomMeta {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}

        /* per-symptom parameters */
        #ccParamCard {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #ccParamTitle {{ font-size: 13px; font-weight: 800; color: {p['TEXT']}; }}
        #ccIntensityValue {{ font-size: 12px; font-weight: 800; }}
        #ccScaleButton {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 7px;
            font-size: 12px; font-weight: 700; color: {p['TEXT_MUTED']};
        }}
        #ccScaleButton:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ccScaleButton:checked {{
            background-color: {AMBER}; border: 1px solid {AMBER}; color: #1A1A24;
        }}
        #ccRemove {{
            background: transparent; border: none;
            font-size: 11px; font-weight: 700; color: {p['DANGER']};
        }}

        /* inputs */
        #ccCombo, #ccSpin {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 6px 10px;
            font-size: 13px;
            color: {p['TEXT']};
        }}
        #ccCombo:focus, #ccSpin:focus {{ border: 1px solid {p['PRIMARY']}; }}
        #ccCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            color: {p['TEXT']};
            selection-background-color: {p['PRIMARY_SOFT']};
        }}
        #ccCheck {{ font-size: 12px; color: {p['TEXT']}; }}

        #ccPrimaryButton {{
            background-color: {p['PRIMARY']};
            border: none; border-radius: 9px; padding: 9px 18px;
            font-size: 13px; font-weight: 700; color: #FFFFFF;
        }}
        #ccPrimaryButton:hover {{ background-color: {p['PRIMARY_HOVER']}; }}
        #ccGhostButton {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px; padding: 7px 14px;
            font-size: 12px; font-weight: 700; color: {p['TEXT']};
        }}
        #ccGhostButton:hover {{ border: 1px solid {p['PRIMARY']}; }}

        /* specificity meter */
        #ccSpecBadge {{ font-size: 12px; font-weight: 800; }}
        #ccSpecBar, #ccScoreBar {{
            background-color: {p['BORDER']}; border: none; border-radius: 3px;
        }}
        #ccSpecBar::chunk, #ccScoreBar::chunk {{
            background-color: {p['PRIMARY']}; border-radius: 3px;
        }}

        /* differential */
        #ccMatchCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #ccMatchCard[top="true"] {{ border: 1px solid {p['PRIMARY']}; }}
        #ccMatchCard:hover {{ border: 1px solid {p['PRIMARY']}; }}
        #ccRank {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px; padding: 3px 8px;
            font-size: 11px; font-weight: 800; color: {p['TEXT_MUTED']};
        }}
        #ccMatchTag {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 7px; padding: 3px 9px;
            font-size: 9px; font-weight: 800; color: {p['BADGE_TEXT']};
        }}
        #ccUrgencyPill {{
            border-radius: 7px; padding: 3px 9px;
            font-size: 10px; font-weight: 800;
        }}
        #ccMatchName {{
            font-family: {heading_font}; font-size: 16px; font-weight: 800;
        }}
        #ccMatchSci {{ font-size: 11px; font-style: italic; color: {p['TEXT_MUTED']}; }}
        #ccScore {{
            font-family: {heading_font}; font-size: 22px; font-weight: 800;
            color: {p['BADGE_TEXT']};
        }}
        #ccTileName {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #ccTileMeta {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #ccHallmark {{
            background-color: {_rgba(AMBER, 0.15)};
            border: 1px solid {_rgba(AMBER, 0.5)};
            border-radius: 6px; padding: 2px 7px;
            font-size: 9px; font-weight: 800; color: {AMBER};
        }}
        #ccChip, #ccChipWarn {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 6px; padding: 3px 8px;
            font-size: 11px; color: {p['TEXT_MUTED']};
        }}
        #ccChipWarn {{ border: 1px solid {_rgba(DANGER_RED, 0.5)}; color: {DANGER_RED}; }}

        /* triage banner */
        #ccTriageTitle {{
            font-family: {heading_font}; font-size: 18px; font-weight: 800;
            color: {p['TEXT']};
        }}
        #ccTriageTag {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 7px; padding: 3px 9px;
            font-size: 10px; font-weight: 800; color: {p['TEXT']};
        }}

        /* matrix */
        #ccMatrixName {{ font-size: 12px; font-weight: 700; color: {p['TEXT']}; }}
        #ccMatrixScore {{
            font-family: {heading_font}; font-size: 13px; font-weight: 800;
            color: {p['BADGE_TEXT']};
        }}
            /* ---------------------------------------- reworked layout pieces */
        #ccCardNote, #ccCrossQuery {{
            font-size: 10px; font-weight: 700; color: {p['BADGE_TEXT']};
        }}
        #ccDot {{ font-size: 10px; color: {p['BADGE_TEXT']}; }}
        #ccStrong {{ font-size: 12px; font-weight: 800; color: {p['TEXT']}; }}

        /* intensity slider vs pain scale */
        #ccIntensityBox {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
        }}
        #ccPainBox {{
            background-color: {_rgba(AMBER, 0.06)};
            border: 1px solid {_rgba(AMBER, 0.45)};
            border-radius: 9px;
        }}
        #ccPainLabel {{ font-size: 10px; font-weight: 800; color: {AMBER}; }}
        #ccPainBadge {{
            background-color: {_rgba(AMBER, 0.15)};
            border: 1px solid {_rgba(AMBER, 0.5)};
            border-radius: 7px; padding: 3px 9px;
            font-size: 10px; font-weight: 800; color: {AMBER};
        }}
        #ccPresentation {{ font-size: 11px; color: {p['TEXT_MUTED']}; }}
        #ccSlider::groove:horizontal {{
            height: 6px; background: {p['BORDER']}; border-radius: 3px;
        }}
        #ccSlider::sub-page:horizontal {{
            background: {p['PRIMARY']}; border-radius: 3px;
        }}
        #ccSlider::handle:horizontal {{
            width: 16px; height: 16px; margin: -5px 0; border-radius: 8px;
            background: #FFFFFF; border: 2px solid {p['PRIMARY']};
        }}

        /* associated symptom checklist */
        #ccSuggestCard {{
            background-color: {p['BADGE_BG']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 12px;
        }}
        #ccSuggestTitle {{ font-size: 12px; font-weight: 800; color: {p['TEXT']}; }}
        #ccSuggestSub {{ font-size: 11px; color: {p['BADGE_TEXT']}; }}
        #ccSuggestChip {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px; padding: 6px 12px;
            font-size: 11px; font-weight: 600; color: {p['TEXT']};
        }}
        #ccSuggestChip:hover {{
            border: 1px solid {p['PRIMARY']}; color: {p['BADGE_TEXT']};
        }}

        /* vitals */
        #ccUnitButton {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 6px;
            font-size: 10px; font-weight: 700; color: {p['TEXT_MUTED']};
        }}
        #ccUnitButton:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['PRIMARY']};
            color: {p['BADGE_TEXT']};
        }}
        #ccVitalStatus {{
            border-radius: 7px; padding: 4px 8px;
            font-size: 10px; font-weight: 700;
        }}
        #ccVitalStatus[tone="bad"] {{
            background-color: {p['DANGER_SOFT']};
            border: 1px solid {p['DANGER']}; color: {p['DANGER']};
        }}
        #ccVitalStatus[tone="warn"] {{
            background-color: {_rgba(AMBER, 0.12)};
            border: 1px solid {_rgba(AMBER, 0.5)}; color: {AMBER};
        }}
        #ccVitalStatus[tone="good"] {{
            background-color: {_rgba(GOOD, 0.10)};
            border: 1px solid {_rgba(GOOD, 0.4)}; color: {GOOD};
        }}

        /* family history */
        #ccFamilyRow {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
        }}
        #ccFamilyName {{ font-size: 11px; font-weight: 700; color: {p['TEXT']}; }}
        #ccFamilyMeta {{
            font-family: "Consolas", monospace;
            font-size: 10px; color: {p['BADGE_TEXT']};
        }}

        /* journal strip */
        #ccJournalStrip {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 10px;
        }}
        #ccJournalTitle {{ font-size: 12px; font-weight: 800; color: {p['BADGE_TEXT']}; }}
        #ccLinkButton {{
            background: transparent; border: none;
            font-size: 12px; font-weight: 700; color: {p['BADGE_TEXT']};
        }}
        #ccSavedBadge {{
            background-color: {_rgba(GOOD, 0.14)};
            border: 1px solid {_rgba(GOOD, 0.5)};
            border-radius: 8px; padding: 6px 12px;
            font-size: 11px; font-weight: 800; color: {GOOD};
        }}

        /* matrix: every row a fixed height so the pinned left/right parts
           line up with the scrolling middle */
        #ccMxCell {{
            background: transparent;
            border-bottom: 1px solid {p['BORDER']};
        }}
        #ccMxHead {{ background: transparent; border-bottom: 1px solid {p['BORDER']}; }}
        #ccMxPinLeft {{ border-right: 1px solid {p['BORDER']}; background: transparent; }}
        #ccMxPinRight {{ border-left: 1px solid {p['BORDER']}; background: transparent; }}
        #ccMxScroll, #ccMxScroll > QWidget > QWidget {{ background: transparent; border: none; }}
        #ccMxSlot {{ background: transparent; }}

        /* matrix cells */
        #ccPillGood, #ccPillBad {{
            border-radius: 7px; padding: 3px 9px;
            font-size: 10px; font-weight: 700;
        }}
        #ccPillGood {{
            background-color: {_rgba(GOOD, 0.12)};
            border: 1px solid {_rgba(GOOD, 0.45)}; color: {GOOD};
        }}
        #ccPillBad {{
            background-color: {_rgba(DANGER_RED, 0.12)};
            border: 1px solid {_rgba(DANGER_RED, 0.45)}; color: {DANGER_RED};
        }}
        #ccChevron {{
            background: transparent; border: none;
            font-size: 11px; color: {p['TEXT_MUTED']};
        }}
        #ccChevron:hover {{ color: {p['BADGE_TEXT']}; }}
        #ccScorePercent {{
            font-size: 12px; font-weight: 700; color: {p['BADGE_TEXT']};
            padding-bottom: 3px;
        }}
        #ccBoosterBox {{
            background-color: {_rgba(AMBER, 0.08)};
            border: 1px solid {_rgba(AMBER, 0.4)};
            border-radius: 8px;
        }}
        #ccBoosterLabel {{ font-size: 10px; font-weight: 800; color: {AMBER}; }}
        #ccChipAccent {{
            background-color: {_rgba(AMBER, 0.12)};
            border: 1px solid {_rgba(AMBER, 0.45)};
            border-radius: 6px; padding: 3px 8px;
            font-size: 11px; color: {AMBER};
        }}
    """
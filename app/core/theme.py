class Theme:
    """Design tokens for the Akeso UI.

    Two jobs: hand out raw colour values to widget code that draws its own
    pixmaps (via token()), and build the application stylesheet string.
    """

    _mode = "dark"

    _DARK = {
        "BG": "#0D0D13",
        "SURFACE": "#14141C",
        "SURFACE_ALT": "#0D0D13",
        "SURFACE_RAISED": "#1A1A24",
        "BORDER": "#2A2A38",
        "PRIMARY": "#6C5CE7",
        "PRIMARY_HOVER": "#7D6DFA",
        "PRIMARY_SOFT": "rgba(108, 92, 231, 0.16)",
        "PRIMARY_TEXT_ON_NAV": "#A29BFE",
        "TEXT": "#F3F4F6",
        "TEXT_MUTED": "#9CA3AF",
        "ICON_MUTED": "#6B7280",
        "DANGER": "#FB7185",
        "DANGER_SOFT": "rgba(251, 113, 133, 0.12)",
        "SUCCESS": "#34D399",
        "BADGE_BG": "rgba(108, 92, 231, 0.15)",
        "BADGE_BORDER": "rgba(108, 92, 231, 0.3)",
        "BADGE_TEXT": "#A29BFE",
    }

    _LIGHT = {
        "BG": "#F7F7FA",
        "SURFACE": "#FFFFFF",
        "SURFACE_ALT": "#F0F0F4",
        "SURFACE_RAISED": "#FFFFFF",
        "BORDER": "#E1E1E8",
        "PRIMARY": "#6C5CE7",
        "PRIMARY_HOVER": "#5C4BD1",
        "PRIMARY_SOFT": "rgba(108, 92, 231, 0.10)",
        "PRIMARY_TEXT_ON_NAV": "#5C4BD1",
        "TEXT": "#17171F",
        "TEXT_MUTED": "#6B6B78",
        "ICON_MUTED": "#8A8A98",
        "DANGER": "#DC2626",
        "DANGER_SOFT": "rgba(220, 38, 38, 0.08)",
        "SUCCESS": "#16A34A",
        "BADGE_BG": "#EDEAFF",
        "BADGE_BORDER": "#D6CFFF",
        "BADGE_TEXT": "#6C5CE7",
    }

    FONT = "DM Sans"
    HEADING_FONT = "Poppins"
    FALLBACK_FONT = "Segoe UI"

    # ------------------------------------------------------------ mode API

    @classmethod
    def mode(cls) -> str:
        return cls._mode

    @classmethod
    def set_mode(cls, mode: str) -> None:
        if mode not in ("dark", "light"):
            raise ValueError("mode must be 'dark' or 'light'")
        cls._mode = mode

    @classmethod
    def toggle_mode(cls) -> None:
        cls.set_mode("light" if cls._mode == "dark" else "dark")

    @classmethod
    def _palette(cls) -> dict:
        return cls._DARK if cls._mode == "dark" else cls._LIGHT

    @classmethod
    def token(cls, name: str) -> str:
        """Look up one colour by name.

        Icons are drawn with QPainter, not styled by CSS, so that code needs
        the raw value rather than a stylesheet rule.
        """
        return cls._palette()[name]

    # -------------------------------------------------------------- output

    @classmethod
    def stylesheet(cls) -> str:
        p = cls._palette()
        body_font = f"'{cls.FONT}', '{cls.FALLBACK_FONT}', sans-serif"
        heading_font = f"'{cls.HEADING_FONT}', '{cls.FALLBACK_FONT}', sans-serif"
        return f"""
        QWidget {{
            background-color: {p['BG']};
            color: {p['TEXT']};
            font-family: {body_font};
            font-size: 14px;
        }}

        /* The QWidget rule above paints EVERY widget with the page colour,
           including QLabel and plain container widgets. Inside a lighter
           card that leaves visible dark rectangles, so anything that should
           show its parent through it must be cleared explicitly.

           These selectors stay narrow deliberately: a blanket
           "#someCard QWidget" rule would beat ID selectors like #iconField
           on CSS specificity and wipe their backgrounds too. */
        QLabel, QCheckBox {{
            background-color: transparent;
        }}
        #formPanel, #panel {{
            background-color: transparent;
        }}
        QScrollArea, QScrollArea > QWidget > QWidget {{
            background-color: transparent;
            border: none;
        }}

        QToolTip {{
            background-color: {p['SURFACE_RAISED']};
            color: {p['TEXT']};
            border: 1px solid {p['BORDER']};
            border-radius: 6px;
            padding: 5px 8px;
            font-size: 12px;
        }}

        QScrollBar:vertical {{
            background: transparent;
            width: 8px;
            margin: 0;
        }}
        QScrollBar::handle:vertical {{
            background: {p['BORDER']};
            border-radius: 4px;
            min-height: 30px;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: transparent;
        }}

        /* ------------------------------------------------------- header */
        #headerFrame {{
            background-color: {p['SURFACE']};
            border-bottom: 1px solid {p['BORDER']};
        }}
        #brandLogo {{
            background-color: transparent;
        }}
        #searchField {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
        }}
        #searchInput {{
            background-color: transparent;
            border: none;
            color: {p['TEXT']};
            font-size: 13px;
        }}
        #kbdBadge {{
            color: {p['ICON_MUTED']};
            border: 1px solid {p['BORDER']};
            border-radius: 5px;
            padding: 2px 6px;
            font-size: 10px;
            font-weight: 700;
        }}
        #iconButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 9px;
        }}
        #iconButton:hover {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
        }}
        #emergencyButton {{
            background-color: {p['DANGER_SOFT']};
            color: {p['DANGER']};
            border: 1px solid {p['DANGER']};
            border-radius: 9px;
            padding: 8px 14px;
            font-size: 12px;
            font-weight: 700;
        }}
        #emergencyButton:hover {{
            background-color: {p['DANGER']};
            color: #FFFFFF;
        }}
        #profileChip {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 19px;
        }}
        #avatarCircle {{
            background-color: {p['PRIMARY']};
            color: #FFFFFF;
            border-radius: 14px;
            font-size: 13px;
            font-weight: 800;
        }}
        #profileName {{
            font-size: 12px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #profileRole {{
            font-size: 9px;
            font-weight: 700;
            letter-spacing: 0.8px;
            color: {p['TEXT_MUTED']};
        }}

        /* ------------------------------------------------------ sidebar */
        #sidebarFrame {{
            background-color: {p['SURFACE']};
            border-right: 1px solid {p['BORDER']};
        }}
        /* No padding here. Padding stacked on top of a fixed row height is
           what clipped these labels; the layout handles spacing instead. */
        #navSectionHeader {{
            color: {p['ICON_MUTED']};
            font-size: 9.5px;
            font-weight: 800;
            letter-spacing: 1.2px;
            padding: 0px;
        }}
        #navButton {{
            background-color: transparent;
            border: none;
            border-radius: 7px;
            color: {p['TEXT_MUTED']};
            font-size: 12px;
            font-weight: 600;
            text-align: left;
            padding-left: 9px;
        }}
        #navButton:hover {{
            background-color: {p['SURFACE_ALT']};
            color: {p['TEXT']};
        }}
        #navButton:checked {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['PRIMARY_TEXT_ON_NAV']};
            font-weight: 700;
        }}
        #navButtonFeatured {{
            background-color: {p['PRIMARY']};
            border: none;
            border-radius: 8px;
            color: #FFFFFF;
            font-size: 12px;
            font-weight: 700;
            text-align: left;
            padding-left: 9px;
        }}
        #navButtonFeatured:hover {{
            background-color: {p['PRIMARY_HOVER']};
        }}
        #navChevron {{
            background-color: transparent;
        }}
        #navButtonDanger {{
            background-color: transparent;
            border: none;
            border-radius: 7px;
            color: {p['DANGER']};
            font-size: 12px;
            font-weight: 600;
            text-align: left;
            padding-left: 9px;
        }}
        #navButtonDanger:hover {{
            background-color: {p['DANGER_SOFT']};
        }}
        #navButtonDanger:checked {{
            background-color: {p['DANGER_SOFT']};
            font-weight: 700;
        }}
        #navButtonAccent {{
            background-color: transparent;
            border: none;
            border-radius: 7px;
            color: {p['PRIMARY_TEXT_ON_NAV']};
            font-size: 12px;
            font-weight: 600;
            text-align: left;
            padding-left: 9px;
        }}
        #navButtonAccent:hover {{
            background-color: {p['PRIMARY_SOFT']};
        }}
        #navButtonAccent:checked {{
            background-color: {p['PRIMARY_SOFT']};
            font-weight: 700;
        }}
        #pinButton {{
            background-color: transparent;
            border: 1px solid transparent;
            border-radius: 7px;
        }}
        #pinButton:hover {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
        }}
        #pinButton:checked {{
            background-color: {p['PRIMARY_SOFT']};
            border: 1px solid {p['BADGE_BORDER']};
        }}

        /* -------------------------------------------- encyclopedia page */
        #pageTitle {{
            font-family: {heading_font};
            font-size: 26px;
            font-weight: 800;
        }}
        #pageSubtitle {{
            font-size: 12.5px;
            color: {p['TEXT_MUTED']};
        }}
        #countBadge {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
            padding: 9px 14px;
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #secondaryButton {{
            background-color: transparent;
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
            padding: 9px 16px;
            font-size: 12px;
            font-weight: 600;
        }}
        #secondaryButton:hover {{
            border: 1px solid {p['PRIMARY']};
            color: {p['PRIMARY_TEXT_ON_NAV']};
        }}

        #filterBar {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 12px;
        }}
        #filterSearch {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
            padding: 0 14px;
            color: {p['TEXT']};
            font-size: 13px;
        }}
        #filterSearch:focus {{
            border: 1px solid {p['PRIMARY']};
        }}
        #filterCombo {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 9px;
            padding: 0 12px;
            color: {p['TEXT']};
            font-size: 13px;
        }}
        #filterCombo::drop-down {{
            border: none;
            width: 22px;
        }}
        #filterCombo QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            selection-background-color: {p['PRIMARY_SOFT']};
            color: {p['TEXT']};
            outline: none;
        }}

        #conditionCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #conditionCard:hover {{
            border: 1px solid {p['PRIMARY']};
        }}
        #cardConditionName {{
            font-family: {heading_font};
            font-size: 17px;
            font-weight: 700;
            color: {p['TEXT']};
        }}
        #cardScientificName {{
            font-size: 12px;
            font-style: italic;
            color: {p['TEXT_MUTED']};
        }}
        #cardDescription {{
            font-size: 12.5px;
            color: {p['TEXT_MUTED']};
        }}
        #systemChip {{
            background-color: {p['PRIMARY_SOFT']};
            color: {p['BADGE_TEXT']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 5px;
            padding: 4px 9px;
            font-size: 9.5px;
            font-weight: 800;
            letter-spacing: 0.6px;
        }}
        #entryChip {{
            background-color: rgba(52, 211, 153, 0.12);
            color: {p['SUCCESS']};
            border: 1px solid rgba(52, 211, 153, 0.35);
            border-radius: 5px;
            padding: 4px 9px;
            font-size: 9.5px;
            font-weight: 700;
        }}
        #bookmarkButton {{
            background-color: transparent;
            border: none;
            border-radius: 6px;
        }}
        #bookmarkButton:hover {{
            background-color: {p['SURFACE_ALT']};
        }}
        #inspectLink {{
            background-color: transparent;
            border: none;
            color: {p['TEXT_MUTED']};
            font-size: 12px;
            font-weight: 600;
            padding: 4px;
        }}
        #inspectLink:hover {{
            color: {p['PRIMARY_TEXT_ON_NAV']};
        }}

        /* Urgency pills. Unknown is deliberately grey and plainly labelled
           rather than colour-coded, so an unassessed condition never looks
           like a triage decision. */
        #urgencyPillSelfCare {{
            background-color: rgba(52, 211, 153, 0.12);
            color: {p['SUCCESS']};
            border: 1px solid rgba(52, 211, 153, 0.4);
            border-radius: 6px;
            padding: 5px 11px;
            font-size: 10px;
            font-weight: 800;
        }}
        #urgencyPillSoon {{
            background-color: rgba(108, 92, 231, 0.12);
            color: {p['BADGE_TEXT']};
            border: 1px solid {p['BADGE_BORDER']};
            border-radius: 6px;
            padding: 5px 11px;
            font-size: 10px;
            font-weight: 800;
        }}
        #urgencyPillUrgent {{
            background-color: rgba(251, 146, 60, 0.12);
            color: #FB923C;
            border: 1px solid rgba(251, 146, 60, 0.4);
            border-radius: 6px;
            padding: 5px 11px;
            font-size: 10px;
            font-weight: 800;
        }}
        #urgencyPillEmergency {{
            background-color: {p['DANGER_SOFT']};
            color: {p['DANGER']};
            border: 1px solid {p['DANGER']};
            border-radius: 6px;
            padding: 5px 11px;
            font-size: 10px;
            font-weight: 800;
        }}
        #urgencyPillUnknown {{
            background-color: transparent;
            color: {p['ICON_MUTED']};
            border: 1px dashed {p['BORDER']};
            border-radius: 6px;
            padding: 5px 11px;
            font-size: 10px;
            font-weight: 700;
        }}

        #severityChipMild, #severityChipModerate,
        #severityChipSevere, #severityChipCritical {{
            border-radius: 5px;
            padding: 4px 10px;
            font-size: 9.5px;
            font-weight: 800;
        }}
        #severityChipMild {{
            background-color: rgba(52, 211, 153, 0.12);
            color: {p['SUCCESS']};
        }}
        #severityChipModerate {{
            background-color: rgba(56, 189, 248, 0.12);
            color: #38BDF8;
        }}
        #severityChipSevere {{
            background-color: rgba(251, 146, 60, 0.12);
            color: #FB923C;
        }}
        #severityChipCritical {{
            background-color: {p['DANGER_SOFT']};
            color: {p['DANGER']};
        }}

        /* --------------------------------------------------- auth screen */
        #authCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 14px;
        }}
        #logoBox {{
            background-color: {p['PRIMARY']};
            border-radius: 10px;
            font-size: 20px;
            color: white;
        }}
        #cardTitle {{
            font-family: {heading_font};
            font-size: 21px;
            font-weight: 700;
        }}
        #cardSubtitle {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #fieldLabel {{
            font-size: 12px;
            font-weight: 600;
        }}
        #linkLabel {{
            color: {p['BADGE_TEXT']};
            font-size: 11px;
            font-weight: 600;
        }}
        #statusLabel {{
            color: {p['DANGER']};
            font-size: 11px;
        }}
        #heroTitle {{
            font-family: {heading_font};
            font-size: 38px;
            font-weight: 800;
        }}
        #heroBody {{
            font-size: 14px;
            color: {p['TEXT_MUTED']};
        }}
        #featureCard {{
            background-color: {p['SURFACE']};
            border: 1px solid {p['BORDER']};
            border-radius: 10px;
        }}
        #featureTitle {{
            font-size: 13px;
            font-weight: 700;
            color: {p['BADGE_TEXT']};
        }}
        #featureBody {{
            font-size: 11px;
            color: {p['TEXT_MUTED']};
        }}
        #separator {{
            background-color: {p['BORDER']};
        }}
        #statNumber {{
            font-family: {heading_font};
            font-size: 15px;
            font-weight: 800;
        }}
        #statLabel {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        #iconField {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 7px;
        }}
        #fieldIcon {{
            color: {p['ICON_MUTED']};
            font-size: 13px;
        }}
        #iconFieldEdit {{
            background-color: transparent;
            border: none;
            padding: 9px 0;
            color: {p['TEXT']};
            font-size: 13px;
        }}
        #eyeToggle {{
            background-color: transparent;
            border: none;
            color: {p['ICON_MUTED']};
            font-size: 11px;
            font-weight: 600;
        }}
        #eyeToggle:hover {{
            color: {p['TEXT']};
        }}
        #reqCheckOff {{ color: {p['BORDER']}; font-size: 11px; }}
        #reqCheckOn  {{ color: {p['SUCCESS']}; font-size: 11px; }}
        #reqLabelOff {{ color: {p['TEXT_MUTED']}; font-size: 11px; }}
        #reqLabelOn  {{ color: {p['SUCCESS']}; font-size: 11px; font-weight: 700; }}
        #matchBad    {{ color: {p['DANGER']}; font-size: 10px; font-weight: 700; }}

        QCheckBox {{
            font-size: 12px;
            color: {p['TEXT_MUTED']};
        }}
        QCheckBox::indicator {{
            width: 14px;
            height: 14px;
            border-radius: 3px;
            border: 1px solid {p['BORDER']};
            background-color: {p['SURFACE_ALT']};
        }}
        QCheckBox::indicator:checked {{
            background-color: {p['PRIMARY']};
            border: 1px solid {p['PRIMARY']};
        }}

        #primaryButton {{
            background-color: {p['PRIMARY']};
            border: none;
            border-radius: 7px;
            padding: 11px;
            font-family: {heading_font};
            font-size: 13px;
            font-weight: 700;
            color: white;
        }}
        #primaryButton:hover {{
            background-color: {p['PRIMARY_HOVER']};
        }}
        #primaryButton:disabled {{
            background-color: {p['BORDER']};
            color: {p['TEXT_MUTED']};
        }}
        #tabBar {{
            background-color: {p['SURFACE_ALT']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
        }}
        #tabButton {{
            background-color: transparent;
            border: none;
            border-radius: 6px;
            padding: 8px;
            font-size: 12px;
            font-weight: 600;
            color: {p['TEXT_MUTED']};
        }}
        #tabButton:checked {{
            background-color: {p['PRIMARY']};
            color: white;
        }}
        """
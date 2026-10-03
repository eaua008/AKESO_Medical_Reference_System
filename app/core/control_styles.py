"""App-wide look for dropdowns (QComboBox) and number boxes (QSpinBox).

Without these rules Qt falls back to the operating system's arrow button,
which is what made the dropdowns look like an old Windows app. Each
module's own rules (#ccCombo, #ixCombo...) still set the box itself; these
only restyle the arrow part and the list that opens, so every dropdown in
Akeso matches.
"""

from app.core import lucide


def control_rules(p: dict) -> str:
    muted = p["TEXT_MUTED"]
    down = lucide.file("chevron-down", 16, muted)
    up = lucide.file("chevron-up", 16, muted)
    down_on = lucide.file("chevron-down", 16, p["PRIMARY_TEXT_ON_NAV"])
    up_on = lucide.file("chevron-up", 16, p["PRIMARY_TEXT_ON_NAV"])
    return f"""
        /* ------------------------------------------- dropdowns (all modules) */
        QComboBox {{
            combobox-popup: 0;
        }}
        QComboBox:hover {{
            border-color: {p['PRIMARY']};
        }}
        QComboBox::drop-down {{
            subcontrol-origin: padding;
            subcontrol-position: center right;
            width: 26px;
            border: none;
            background: transparent;
        }}
        QComboBox::down-arrow {{
            image: url("{down}");
            width: 13px;
            height: 13px;
        }}
        QComboBox::down-arrow:hover, QComboBox::down-arrow:on {{
            image: url("{down_on}");
        }}
        QComboBox QAbstractItemView {{
            background-color: {p['SURFACE_RAISED']};
            border: 1px solid {p['BORDER']};
            border-radius: 8px;
            padding: 4px;
            color: {p['TEXT']};
            selection-background-color: {p['PRIMARY_SOFT']};
            selection-color: {p['TEXT']};
            outline: none;
        }}

        /* ------------------------------------------ number boxes (spinners) */
        QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {{
            subcontrol-origin: border;
            width: 22px;
            border: none;
            background: transparent;
        }}
        QAbstractSpinBox::up-button {{ subcontrol-position: top right; }}
        QAbstractSpinBox::down-button {{ subcontrol-position: bottom right; }}
        QAbstractSpinBox::up-button:hover, QAbstractSpinBox::down-button:hover {{
            background-color: {p['PRIMARY_SOFT']};
            border-radius: 4px;
        }}
        QAbstractSpinBox::up-arrow {{
            image: url("{up}");
            width: 11px;
            height: 11px;
        }}
        QAbstractSpinBox::down-arrow {{
            image: url("{down}");
            width: 11px;
            height: 11px;
        }}
        QAbstractSpinBox::up-arrow:hover {{ image: url("{up_on}"); }}
        QAbstractSpinBox::down-arrow:hover {{ image: url("{down_on}"); }}
    """

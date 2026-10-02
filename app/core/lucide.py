"""Modern outline icons (Lucide), rendered crisply at any size and colour.

Lucide (lucide.dev, ISC licence) is the icon set the React design uses:
24x24 grid, 2px round strokes. Each icon below is its SVG path data; this
module fills in the colour and renders it with Qt's SVG renderer at 2x, so
edges stay sharp on high-DPI screens.

    lucide.pixmap("shield-check", 18, "#34D399")   for a QLabel
    lucide.icon("trash-2", 16, "#9CA3AF")          for a QPushButton

Icons are baked in one colour, so a theme switch has to redraw them. Pages
that use them rebuild on refresh_theme(), like the rest of the app.
"""

from functools import lru_cache

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

_SCALE = 2

_SHIELD = ('<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 '
           '1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 '
           '1 0 0 1 1 1z"/>')
_CIRCLE = '<circle cx="12" cy="12" r="10"/>'
_BOOKMARK = '<path d="m19 21-7-4-7 4V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2v16z"/>'

PATHS = {
    "circle": _CIRCLE,
    # --- clinical exchange
    "message-circle": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "thumbs-up": ('<path d="M7 10v12"/><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 '
                  '0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 '
                  '2a3.13 3.13 0 0 1 3 3.88Z"/>'),
    "flag": ('<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/>'
             '<line x1="4" x2="4" y1="22" y2="15"/>'),
    "reply": '<polyline points="9 17 4 12 9 7"/><path d="M20 18v-2a4 4 0 0 0-4-4H4"/>',
    "share-2": ('<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/>'
                '<line x1="8.59" x2="15.42" y1="13.51" y2="17.49"/><line x1="15.41" x2="8.59" y1="6.51" y2="10.49"/>'),
    "bell": ('<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>'),
    "users": ('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
              '<path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'),
    "user-check": ('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
                   '<polyline points="16 11 18 13 22 9"/>'),
    "archive": ('<rect width="20" height="5" x="2" y="3" rx="1"/>'
                '<path d="M4 8v11a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8"/><path d="M10 12h4"/>'),
    "user-x": ('<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>'
               '<line x1="17" x2="22" y1="8" y2="13"/><line x1="22" x2="17" y1="8" y2="13"/>'),
    "chart-bar": ('<path d="M3 3v18h18"/><path d="M7 16h8"/><path d="M7 11h12"/><path d="M7 6h3"/>'),
    # --- account module
    "key-round": ('<path d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 '
                  '0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 '
                  '6.5 0 1 0-4-4z"/><circle cx="16.5" cy="7.5" r=".5"/>'),
    "monitor": ('<rect width="20" height="14" x="2" y="3" rx="2"/>'
                '<line x1="8" x2="16" y1="21" y2="21"/><line x1="12" x2="12" y1="17" y2="21"/>'),
    "smartphone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    "download": ('<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>'
                 '<polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/>'),
    "trash-2": ('<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>'
                '<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>'
                '<line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/>'),
    "log-out": ('<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>'
                '<polyline points="16 17 21 12 16 7"/><line x1="21" x2="9" y1="12" y2="12"/>'),
    "graduation-cap": ('<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 '
                       '9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/>'
                       '<path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>'),
    "camera": ('<path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 '
               '0 0 0-2-2h-3l-2.5-3z"/><circle cx="12" cy="13" r="3"/>'),
    "badge-check": ('<path d="M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 '
                    '4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 '
                    '0 0 1 0-6.76Z"/><path d="m9 12 2 2 4-4"/>'),
    "at-sign": '<circle cx="12" cy="12" r="4"/><path d="M16 8v5a3 3 0 0 0 6 0v-1a10 10 0 1 0-4 8"/>',
    "flame": ('<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 '
              '2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 '
              '1-3a2.5 2.5 0 0 0 2.5 2.5z"/>'),
    "mail": ('<rect width="20" height="16" x="2" y="4" rx="2"/>'
             '<path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/>'),
    "refresh-cw": ('<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/>'
                   '<path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/>'
                   '<path d="M8 16H3v5"/>'),
    "copy": ('<rect width="14" height="14" x="8" y="8" rx="2" ry="2"/>'
             '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/>'),
    "play": '<polygon points="6 3 20 12 6 21 6 3"/>',
    "database": ('<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/>'
                 '<path d="M3 12A9 3 0 0 0 21 12"/>'),
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "plus": '<path d="M5 12h14"/><path d="M12 5v14"/>',
    "clock": _CIRCLE + '<polyline points="12 6 12 12 16 14"/>',
    "history": ('<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>'
                '<path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>'),
    "triangle-alert": ('<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 '
                       '2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>'),
    "circle-alert": _CIRCLE + '<path d="M12 8v4"/><path d="M12 16h.01"/>',
    "octagon-alert": ('<path d="M12 16h.01"/><path d="M12 8v4"/><path d="M15.312 2a2 2 0 0 1 '
                      '1.414.586l4.688 4.688A2 2 0 0 1 22 8.688v6.624a2 2 0 0 1-.586 '
                      '1.414l-4.688 4.688a2 2 0 0 1-1.414.586H8.688a2 2 0 0 1-1.414-.586l'
                      '-4.688-4.688A2 2 0 0 1 2 15.312V8.688a2 2 0 0 1 .586-1.414l4.688'
                      '-4.688A2 2 0 0 1 8.688 2z"/>'),
    "info": _CIRCLE + '<path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "circle-check": _CIRCLE + '<path d="m9 12 2 2 4-4"/>',
    "circle-x": _CIRCLE + '<path d="m15 9-6 6"/><path d="m9 9 6 6"/>',
    "circle-help": _CIRCLE + ('<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>'
                              '<path d="M12 17h.01"/>'),
    "eye": ('<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 '
            '.696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>'),
    "pencil": ('<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l'
               '-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z"/>'
               '<path d="m15 5 4 4"/>'),
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "shield": _SHIELD,
    "shield-check": _SHIELD + '<path d="m9 12 2 2 4-4"/>',
    "shield-alert": _SHIELD + '<path d="M12 8v4"/><path d="M12 16h.01"/>',
    "file-text": ('<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
                  '<path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/>'
                  '<path d="M16 13H8"/><path d="M16 17H8"/>'),
    "trash-2": ('<path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/>'
                '<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/>'
                '<line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/>'),
    "heart-pulse": ('<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 '
                    '.5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 '
                    '5.5l7 7Z"/><path d="M3.22 12H9.5l.5-1 2 4.5 2-7 1.5 3.5h5.27"/>'),
    "activity": '<path d="M22 12h-4l-3 9L9 3l-3 9H2"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "bookmark": _BOOKMARK,
    "bookmark-plus": _BOOKMARK + ('<line x1="12" x2="12" y1="7" y2="13"/>'
                                  '<line x1="15" x2="9" y1="10" y2="10"/>'),
    "external-link": ('<path d="M15 3h6v6"/><path d="M10 14 21 3"/>'
                      '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>'),
    "calendar": ('<path d="M8 2v4"/><path d="M16 2v4"/>'
                 '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>'),
    "trending-up": ('<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>'
                    '<polyline points="16 7 22 7 22 13"/>'),
    "pill": ('<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/>'
             '<path d="m8.5 8.5 7 7"/>'),
    "chevron-down": '<path d="m6 9 6 6 6-6"/>',
    "chevron-up": '<path d="m18 15-6-6-6 6"/>',
    "sparkles": ('<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L'
                 '8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 '
                 '2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 '
                 '0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>'),
    "funnel": '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
    "tag": ('<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 '
            '.586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 '
            '0-3.42z"/><circle cx="7.5" cy="7.5" r="1"/>'),
    "arrow-left-right": ('<path d="M8 3 4 7l4 4"/><path d="M4 7h16"/>'
                         '<path d="m16 21 4-4-4-4"/><path d="M20 17H4"/>'),
    "rotate-ccw": ('<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/>'
                   '<path d="M3 3v5h5"/>'),
    "layers": ('<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 '
               '2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/>'
               '<path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/>'
               '<path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>'),
    # notes editor
    "undo-2": '<path d="M9 14 4 9l5-5"/><path d="M4 9h10.5a5.5 5.5 0 0 1 5.5 5.5a5.5 5.5 0 0 1-5.5 5.5H11"/>',
    "redo-2": '<path d="m15 14 5-5-5-5"/><path d="M20 9H9.5A5.5 5.5 0 0 0 4 14.5A5.5 5.5 0 0 0 9.5 20H13"/>',
    "bold": '<path d="M6 12h9a4 4 0 0 1 0 8H7a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h7a4 4 0 0 1 0 8"/>',
    "italic": ('<line x1="19" x2="10" y1="4" y2="4"/><line x1="14" x2="5" y1="20" y2="20"/>'
               '<line x1="15" x2="9" y1="4" y2="20"/>'),
    "underline": '<path d="M6 4v6a6 6 0 0 0 12 0V4"/><line x1="4" x2="20" y1="20" y2="20"/>',
    "strikethrough": ('<path d="M16 4H9a3 3 0 0 0-2.83 4"/><path d="M14 12a4 4 0 0 1 0 8H6"/>'
                      '<line x1="4" x2="20" y1="12" y2="12"/>'),
    "baseline": '<path d="M4 20h16"/><path d="m6 16 6-12 6 12"/><path d="M8 12h8"/>',
    "highlighter": ('<path d="m9 11-6 6v3h9l3-3"/>'
                    '<path d="m22 12-4.6 4.6a2 2 0 0 1-2.8 0l-5.2-5.2a2 2 0 0 1 0-2.8L14 4"/>'),
    "align-left": '<path d="M15 12H3"/><path d="M17 18H3"/><path d="M21 6H3"/>',
    "align-center": '<path d="M17 12H7"/><path d="M19 18H5"/><path d="M21 6H3"/>',
    "align-right": '<path d="M21 12H9"/><path d="M21 18H7"/><path d="M21 6H3"/>',
    "list-ordered": ('<path d="M10 12h11"/><path d="M10 18h11"/><path d="M10 6h11"/><path d="M4 10h2"/>'
                     '<path d="M4 6h1v4"/><path d="M6 18H4c0-1 2-2 2-3s-1-1.5-2-1"/>'),
    "list-checks": ('<path d="m3 17 2 2 4-4"/><path d="m3 7 2 2 4-4"/><path d="M13 6h8"/>'
                    '<path d="M13 12h8"/><path d="M13 18h8"/>'),
    "indent-increase": ('<polyline points="3 8 7 12 3 16"/><line x1="21" x2="11" y1="12" y2="12"/>'
                        '<line x1="21" x2="11" y1="6" y2="6"/><line x1="21" x2="11" y1="18" y2="18"/>'),
    "indent-decrease": ('<polyline points="7 8 3 12 7 16"/><line x1="21" x2="11" y1="12" y2="12"/>'
                        '<line x1="21" x2="11" y1="6" y2="6"/><line x1="21" x2="11" y1="18" y2="18"/>'),
    "table": ('<path d="M12 3v18"/><rect width="18" height="18" x="3" y="3" rx="2"/>'
              '<path d="M3 9h18"/><path d="M3 15h18"/>'),
    "minus": '<path d="M5 12h14"/>',
    "image": ('<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/>'
              '<path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>'),
    "code": '<polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/>',
    "remove-formatting": ('<path d="M4 7V4h16v3"/><path d="M5 20h6"/><path d="M13 4 8 20"/>'
                          '<path d="m15 15 5 5"/><path d="m20 15-5 5"/>'),
    "text-quote": ('<path d="M17 6H3"/><path d="M21 12H8"/><path d="M21 18H8"/>'
                   '<path d="M3 12v6"/>'),
    "arrow-down-to-line": '<path d="M12 17V3"/><path d="m6 11 6 6 6-6"/><path d="M19 21H5"/>',
    "eye-off": ('<path d="M10.733 5.076a10.744 10.744 0 0 1 11.205 6.575 1 1 0 0 1 0 .696 10.747 '
                '10.747 0 0 1-1.444 2.49"/><path d="M14.084 14.158a3 3 0 0 1-4.242-4.242"/>'
                '<path d="M17.479 17.499a10.75 10.75 0 0 1-15.417-5.151 1 1 0 0 1 0-.696 10.75 '
                '10.75 0 0 1 4.446-5.143"/><path d="m2 2 20 20"/>'),
    "target": ('<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/>'
               '<circle cx="12" cy="12" r="2"/>'),
    # Study Notebook
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "layout-grid": ('<rect width="7" height="7" x="3" y="3" rx="1"/>'
                    '<rect width="7" height="7" x="14" y="3" rx="1"/>'
                    '<rect width="7" height="7" x="14" y="14" rx="1"/>'
                    '<rect width="7" height="7" x="3" y="14" rx="1"/>'),
    "chevron-left": '<path d="m15 18-6-6 6-6"/>',
    "chevron-right": '<path d="m9 18 6-6-6-6"/>',
    "chevrons-left": '<path d="m11 17-5-5 5-5"/><path d="m18 17-5-5 5-5"/>',
    "chevrons-right": '<path d="m6 17 5-5-5-5"/><path d="m13 17 5-5-5-5"/>',
    "arrow-left": '<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>',
    "folder": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    "folder-plus": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/><path d="M12 10v6"/><path d="M9 13h6"/>',
    "list": ('<path d="M3 12h.01"/><path d="M3 18h.01"/><path d="M3 6h.01"/>'
             '<path d="M8 12h13"/><path d="M8 18h13"/><path d="M8 6h13"/>'),
    "ellipsis": ('<circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/>'
                 '<circle cx="5" cy="12" r="1"/>'),
    "notebook-pen": ('<path d="M13.4 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-7.4"/>'
                     '<path d="M2 6h4"/><path d="M2 10h4"/><path d="M2 14h4"/><path d="M2 18h4"/>'
                     '<path d="M21.378 5.626a1 1 0 1 0-3.004-3.004l-5.01 5.012a2 2 0 0 0-.506.854'
                     'l-.837 2.87a.5.5 0 0 0 .62.62l2.87-.837a2 2 0 0 0 .854-.506z"/>'),
    "stethoscope": ('<path d="M11 2v2"/><path d="M5 2v2"/>'
                    '<path d="M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1"/>'
                    '<path d="M8 15a6 6 0 0 0 12 0v-3"/><circle cx="20" cy="10" r="2"/>'),
    "book-open": ('<path d="M12 7v14"/><path d="M3 18a1 1 0 0 1-1-1V4a1 1 0 0 1 1-1h5a4 4 0 0 1 '
                  '4 4 4 4 0 0 1 4-4h5a1 1 0 0 1 1 1v13a1 1 0 0 1-1 1h-6a3 3 0 0 0-3 3 3 3 0 0 '
                  '0-3-3z"/>'),
    "panel-left": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/>',
    "panel-right": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M15 3v18"/>',
    "maximize-2": ('<polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/>'
                   '<line x1="21" x2="14" y1="3" y2="10"/><line x1="3" x2="10" y1="21" y2="14"/>'),
    "minimize-2": ('<polyline points="4 14 10 14 10 20"/><polyline points="20 10 14 10 14 4"/>'
                   '<line x1="14" x2="21" y1="10" y2="3"/><line x1="3" x2="10" y1="21" y2="14"/>'),
    "pin": ('<path d="M12 17v5"/><path d="M9 10.76a2 2 0 0 1-1.11 1.79l-1.78.9A2 2 0 0 0 5 15.24'
            'V16a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 '
            '10.76V7a1 1 0 0 1 1-1 2 2 0 0 0 0-4H8a2 2 0 0 0 0 4 1 1 0 0 1 1 1z"/>'),
}


@lru_cache(maxsize=512)
def pixmap(name: str, size: int = 16, color: str = "#9CA3AF", stroke: float = 2.0) -> QPixmap:
    """The icon as a pixmap. Unknown names draw nothing rather than crash."""
    body = PATHS.get(name, "")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" '
           f'stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
           f'stroke-linejoin="round">{body}</svg>')
    image = QPixmap(size * _SCALE, size * _SCALE)
    image.fill(Qt.GlobalColor.transparent)
    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    painter = QPainter(image)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter, QRectF(0, 0, size * _SCALE, size * _SCALE))
    painter.end()
    image.setDevicePixelRatio(_SCALE)
    return image


def icon(name: str, size: int = 16, color: str = "#9CA3AF") -> QIcon:
    return QIcon(pixmap(name, size, color))


def file(name: str, size: int = 16, color: str = "#9CA3AF") -> str:
    """The icon saved as a PNG, for stylesheets. Qt stylesheets can only
    load images from a path (no inline SVG), e.g. the dropdown chevrons."""
    import tempfile
    from pathlib import Path

    folder = Path(tempfile.gettempdir()) / "akeso_icons"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{name}_{size}_{color.lstrip('#')}.png"
    if not path.exists():
        pixmap(name, size, color).save(str(path))
    return str(path).replace("\\", "/")

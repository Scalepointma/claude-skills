"""
ScalePoint M&A PDF Helper Module — Re-export Wrapper
=====================================================
All drawing functions for ScalePoint-branded PDFs (CIMs, teasers,
proposals, brochures, one-pagers, closing binders).

Usage:
    import sys
    sys.path.insert(0, '<path-to-skill>/scripts')
    from scalepoint_pdf import *

    from reportlab.pdfgen import canvas
    c = canvas.Canvas("output.pdf", pagesize=letter)
    assets = discover_assets()
    draw_front_cover(c, title="Crown Holdings LOI",
                     logo_stacked_path=assets.get("logo-stacked"))
    c.showPage()
    draw_page_setup(c, doc_title="Crown Holdings",
                    page_num=2, icon_path=assets.get("icon-fullcolor"))
    # ... content calls ...
    c.save()
"""

from scalepoint_base import *
from scalepoint_page import *
from scalepoint_cards import *
from scalepoint_elements import *
from scalepoint_covers import *
from scalepoint_layouts import *

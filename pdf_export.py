from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, Preformatted, HRFlowable
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from io import BytesIO
from datetime import datetime

PRIMARY   = colors.HexColor("#0284c7")
SUCCESS   = colors.HexColor("#16a34a")
ERROR     = colors.HexColor("#dc2626")
WARNING   = colors.HexColor("#ea580c")
BG_LIGHT  = colors.HexColor("#f8fafc")
BORDER    = colors.HexColor("#e2e8f0")
TEXT      = colors.HexColor("#0f172a")
TEXT_MUTED= colors.HexColor("#475569")

def generate_pdf_report(data: dict) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    story  = []

    # Title
    title_style = ParagraphStyle(
        "Title", parent=styles["Heading1"],
        fontSize=22, textColor=PRIMARY,
        spaceAfter=4, alignment=TA_CENTER
    )
    sub_style = ParagraphStyle(
        "Sub", parent=styles["Normal"],
        fontSize=10, textColor=TEXT_MUTED,
        alignment=TA_CENTER, spaceAfter=20
    )
    story.append(Paragraph("AI Code Optimization Report", title_style))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')} · Language: {data.get('language','N/A').upper()}",
        sub_style
    ))
    story.append(HRFlowable(width="100%", thickness=1, color=BORDER))
    story.append(Spacer(1, 0.4*cm))

    # Metrics Table
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=13, textColor=TEXT, spaceAfter=8)
    story.append(Paragraph("Metrics Overview", h2))

    metrics = data.get("metrics", {})
    issues  = data.get("analysis", {})

    metrics_data = [
        ["Metric", "Before", "After", "Change"],
        ["Lines of Code",
         str(metrics.get("original_lines", "—")),
         str(metrics.get("optimized_lines", "—")),
         f"{metrics.get('lines_delta', 0):+d} lines"],
        ["Complexity",
         metrics.get("original_complexity", "—"),
         metrics.get("optimized_complexity", "—"),
         "Reduced" if metrics.get("original_complexity","") > metrics.get("optimized_complexity","") else "Same"],
        ["Character Count",
         str(metrics.get("original_chars", "—")),
         str(metrics.get("optimized_chars", "—")),
         f"{metrics.get('chars_reduction', 0)}% smaller"],
        ["Quality Score",
         str(issues.get("score_before", "—")),
         str(issues.get("score", "—")),
         "Improved" if issues.get("score", 0) > issues.get("score_before", 0) else "—"],
    ]

    tbl = Table(metrics_data, colWidths=[5*cm, 3*cm, 3*cm, 4*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), PRIMARY),
        ("TEXTCOLOR",  (0,0), (-1,0), colors.white),
        ("FONTNAME",   (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 9),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [BG_LIGHT, colors.white]),
        ("GRID",       (0,0), (-1,-1), 0.5, BORDER),
        ("ALIGN",      (0,0), (-1,-1), "LEFT"),
        ("LEFTPADDING",(0,0), (-1,-1), 8),
        ("RIGHTPADDING",(0,0),(-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.5*cm))

    # Issues
    issue_list = data.get("analysis", {}).get("issues", [])
    if issue_list:
        story.append(Paragraph(f"Issues Found ({len(issue_list)})", h2))
        sev_colors = {"error": ERROR, "warning": WARNING, "info": PRIMARY}
        for iss in issue_list:
            sev   = iss.get("severity","info")
            color = sev_colors.get(sev, PRIMARY)
            row_data = [[
                Paragraph(f'<font color="{color.hexval()}">[{sev.upper()}]</font> <b>{iss.get("title","")}</b> — Line {iss.get("line","?")}', styles["Normal"]),
            ],[
                Paragraph(f'{iss.get("description","")} <i>Fix: {iss.get("fix","")}</i>', styles["Normal"]),
            ]]
            t = Table(row_data, colWidths=[15*cm])
            t.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), BG_LIGHT),
                ("LEFTPADDING",(0,0),(-1,-1), 8),
                ("BOTTOMPADDING",(0,0),(-1,-1), 4),
                ("TOPPADDING",(0,0),(-1,-1), 4),
                ("LINEAFTER", (0,0), (-1,-1), 0, colors.white),
                ("LINEBEFORE",(0,0),(0,-1), 3, color),
            ]))
            story.append(t)
            story.append(Spacer(1, 0.15*cm))
        story.append(Spacer(1, 0.3*cm))

    # Optimized code
    story.append(Paragraph("Optimized Code", h2))
    code_style = ParagraphStyle(
        "Code", parent=styles["Code"],
        fontSize=8, fontName="Courier",
        backColor=colors.HexColor("#f1f5f9"),
        leftIndent=8, rightIndent=8,
        spaceBefore=4, spaceAfter=4,
    )
    opt_code = data.get("optimized_code", "")
    story.append(Preformatted(opt_code[:3000], code_style))

    doc.build(story)
    return buffer.getvalue()
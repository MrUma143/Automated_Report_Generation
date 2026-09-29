import csv
from collections import Counter
from pathlib import Path
from statistics import mean
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


def read_data(file_path):
    """Read records from a CSV file."""
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def analyze_data(records):
    """Calculate summary statistics from the input records."""
    scores = [float(row["Score"]) for row in records]
    return {
        "total_records": len(records),
        "average_score": mean(scores) if scores else 0,
        "highest_score": max(scores) if scores else 0,
        "lowest_score": min(scores) if scores else 0,
        "status_counts": Counter(row["Status"] for row in records),
        "course_counts": Counter(row["Course"] for row in records),
    }


def styled_table(data, header_color):
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_color)),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F2F6F8")]),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))
    return table


def create_pdf(records, analysis, output_path):
    """Generate a formatted PDF report using ReportLab."""
    document = SimpleDocTemplate(
        str(output_path), pagesize=A4,
        rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"],
        alignment=TA_CENTER, fontSize=20, spaceAfter=12
    )
    heading_style = ParagraphStyle(
        "Heading", parent=styles["Heading2"],
        fontSize=13, spaceBefore=10, spaceAfter=7
    )

    story = [
        Paragraph("Automated Data Analysis Report", title_style),
        Paragraph(
            "This report was generated automatically from a CSV data file.",
            styles["Normal"]
        ),
        Spacer(1, 10),
        Paragraph("1. Summary", heading_style)
    ]

    summary = [
        ["Metric", "Value"],
        ["Total Records", str(analysis["total_records"])],
        ["Average Score", f'{analysis["average_score"]:.2f}'],
        ["Highest Score", f'{analysis["highest_score"]:.2f}'],
        ["Lowest Score", f'{analysis["lowest_score"]:.2f}'],
    ]
    story.append(styled_table(summary, "#1F4E78"))

    story.append(Paragraph("2. Status Analysis", heading_style))
    status_data = [["Status", "Count"]]
    status_data += [[status, str(count)]
                    for status, count in analysis["status_counts"].items()]
    story.append(styled_table(status_data, "#548235"))

    story.append(Paragraph("3. Course Distribution", heading_style))
    course_data = [["Course", "Participants"]]
    course_data += [[course, str(count)]
                    for course, count in analysis["course_counts"].items()]
    story.append(styled_table(course_data, "#7030A0"))

    story += [PageBreak(), Paragraph("4. Detailed Records", heading_style)]

    detail = [["ID", "Name", "Course", "Status", "Score"]]
    detail += [[r["ID"], r["Name"], r["Course"], r["Status"], r["Score"]]
               for r in records]

    detail_table = Table(
        detail,
        colWidths=[15 * mm, 28 * mm, 48 * mm, 32 * mm, 20 * mm],
        repeatRows=1
    )
    detail_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F3F6F8")]),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(detail_table)
    story += [
        Spacer(1, 12),
        Paragraph(
            "Generated automatically with Python and ReportLab.",
            styles["Italic"]
        )
    ]

    document.build(story)


def main():
    input_file = Path("data.csv")
    output_file = Path("sample_report.pdf")

    if not input_file.exists():
        raise FileNotFoundError(
            "data.csv was not found. Place the CSV file in the project folder."
        )

    records = read_data(input_file)
    if not records:
        raise ValueError("The input CSV file is empty.")

    analysis = analyze_data(records)
    create_pdf(records, analysis, output_file)
    print(f"Report generated successfully: {output_file.resolve()}")


if __name__ == "__main__":
    main()

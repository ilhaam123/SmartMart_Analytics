from datetime import datetime
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)


class ReportGenerator:
    """
    Responsible for generating and exporting SmartMart sales reports.
    """

    def generate_report(
        self,
        dataframe,
        analysis_results,
        validation_results=None
    ):
        """
        Combines dataset information, validation results
        and sales analysis into a structured report.
        """

        report = {
            "report_title": "SmartMart Sales Analysis Report",
            "generated_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "total_records": len(dataframe),
            "total_sales": analysis_results["total_sales"],
            "total_transactions": analysis_results[
                "total_transactions"
            ],
            "best_selling_products": (
                analysis_results["best_selling_products"]
                .to_dict()
            ),
            "sales_by_region": (
                analysis_results["sales_by_region"]
                .to_dict()
            ),
            "sales_by_category": (
                analysis_results["sales_by_category"]
                .to_dict()
            ),
            "data_quality": validation_results or {}
        }

        return report

    def display_report(self, report):
        """
        Displays the generated report in a readable format.
        """

        print("\n" + "=" * 50)
        print(report["report_title"])
        print("=" * 50)

        print("Generated At:", report["generated_at"])
        print("Total Records:", report["total_records"])
        print("Total Sales:", report["total_sales"])
        print("Total Transactions:", report["total_transactions"])

        print("\nBest-Selling Products:")
        for product, quantity in report[
            "best_selling_products"
        ].items():
            print(f"{product}: {quantity}")

        print("\nSales by Region:")
        for region, amount in report["sales_by_region"].items():
            print(f"{region}: {amount}")

        print("\nSales by Category:")
        for category, amount in report["sales_by_category"].items():
            print(f"{category}: {amount}")

        print("\nData Quality Overview:")
        for item, value in report["data_quality"].items():
            print(f"{item}: {value}")

        print("=" * 50)

    def export_report_to_excel(self, report, file_path):
        """
        Exports the generated sales report into an Excel workbook.
        """

        summary_data = {
            "Report Information": [
                "Report Title",
                "Generated At",
                "Total Records",
                "Total Net Sales (Rs.)",
                "Total Transactions"
            ],
            "Value": [
                report["report_title"],
                report["generated_at"],
                report["total_records"],
                report["total_sales"],
                report["total_transactions"]
            ]
        }

        best_selling_data = pd.DataFrame(
            list(report["best_selling_products"].items()),
            columns=["Product Name", "Quantity Sold"]
        )

        regional_sales_data = pd.DataFrame(
            list(report["sales_by_region"].items()),
            columns=["Region", "Total Sales (Rs.)"]
        )

        category_sales_data = pd.DataFrame(
            list(report["sales_by_category"].items()),
            columns=["Product Category", "Total Sales (Rs.)"]
        )

        with pd.ExcelWriter(file_path, engine="openpyxl") as writer:

            pd.DataFrame(summary_data).to_excel(
                writer,
                sheet_name="Summary",
                index=False
            )

            best_selling_data.to_excel(
                writer,
                sheet_name="Best Selling Products",
                index=False
            )

            regional_sales_data.to_excel(
                writer,
                sheet_name="Sales by Region",
                index=False
            )

            category_sales_data.to_excel(
                writer,
                sheet_name="Sales by Category",
                index=False
            )

            quality_data = pd.DataFrame(
                list(report["data_quality"].items()),
                columns=["Data Quality Metric", "Count"]
            )

            quality_data.to_excel(
                writer,
                sheet_name="Data Quality",
                index=False
            )

        return file_path

    def export_report_to_pdf(self, report, file_path):
        """
        Exports the generated report into a formatted PDF document.
        """

        document = SimpleDocTemplate(
            file_path,
            pagesize=A4,
            rightMargin=20 * mm,
            leftMargin=20 * mm,
            topMargin=20 * mm,
            bottomMargin=20 * mm
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontSize=20,
            textColor=colors.HexColor("#1F3A5F"),
            alignment=TA_CENTER,
            spaceAfter=15
        )

        heading_style = ParagraphStyle(
            "SectionHeading",
            parent=styles["Heading2"],
            fontSize=13,
            textColor=colors.HexColor("#1F3A5F"),
            spaceBefore=12,
            spaceAfter=8
        )

        normal_style = styles["Normal"]

        elements = []

        # Report title
        elements.append(
            Paragraph(report["report_title"], title_style)
        )

        elements.append(
            Paragraph(
                f"Generated At: {report['generated_at']}",
                normal_style
            )
        )

        elements.append(Spacer(1, 12))

        # Sales overview
        elements.append(
            Paragraph("1. Sales Overview", heading_style)
        )

        summary_data = [
            ["Metric", "Value"],
            ["Processed Records", f"{report['total_records']:,}"],
            [
                "Total Net Sales (Rs.)",
                f"{report['total_sales']:,.2f}"
            ],
            [
                "Total Transactions",
                f"{report['total_transactions']:,}"
            ]
        ]

        elements.append(
            self.create_pdf_table(summary_data)
        )

        # Data quality overview
        elements.append(
            Paragraph("2. Data Quality Overview", heading_style)
        )

        quality_data = [
            ["Data Quality Metric", "Count"]
        ]

        for metric, value in report["data_quality"].items():
            quality_data.append([
                metric.replace("_", " ").title(),
                f"{value:,}"
            ])

        if len(quality_data) == 1:
            quality_data.append(["No data available", "-"])

        elements.append(
            self.create_pdf_table(quality_data)
        )

        # Best-selling products
        elements.append(
            Paragraph("3. Best-Selling Products", heading_style)
        )

        product_data = [
            ["Product Name", "Quantity Sold"]
        ]

        for product, quantity in report[
            "best_selling_products"
        ].items():
            product_data.append([str(product), f"{quantity:,}"])

        elements.append(
            self.create_pdf_table(product_data)
        )

        # Sales by region
        elements.append(
            Paragraph("4. Sales by Region", heading_style)
        )

        region_data = [
            ["Region", "Total Net Sales (Rs.)"]
        ]

        for region, amount in report["sales_by_region"].items():
            region_data.append([
                str(region),
                f"{amount:,.2f}"
            ])

        elements.append(
            self.create_pdf_table(region_data)
        )

        # Sales by category
        elements.append(
            Paragraph("5. Sales by Product Category", heading_style)
        )

        category_data = [
            ["Product Category", "Total Net Sales (Rs.)"]
        ]

        for category, amount in report["sales_by_category"].items():
            category_data.append([
                str(category),
                f"{amount:,.2f}"
            ])

        elements.append(
            self.create_pdf_table(category_data)
        )

        document.build(elements)

        return file_path

    def create_pdf_table(self, data):
        """
        Creates a consistently formatted table for the PDF report.
        """

        table = Table(
            data,
            repeatRows=1,
            hAlign="LEFT"
        )

        table.setStyle(
            TableStyle([
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F3A5F")
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "FONTNAME",
                    (0, 1),
                    (-1, -1),
                    "Helvetica"
                ),
                (
                    "FONTSIZE",
                    (0, 0),
                    (-1, -1),
                    9
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#D9DEE7")
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F4F6F9")
                    ]
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "RIGHT"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    7
                )
            ])
        )

        return table

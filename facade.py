from data_reader import ExcelDataReader
from data_validator import DataValidator
from data_processor import DataProcessor
from sales_analyzer import SalesAnalyzer
from report_generator import ReportGenerator


class SmartMartFacade:
    """
    Coordinates the main operations of the SmartMart application.
    """

    def __init__(self):
        self.data_reader = ExcelDataReader()
        self.data_validator = DataValidator()
        self.data_processor = DataProcessor()
        self.sales_analyzer = SalesAnalyzer()
        self.report_generator = ReportGenerator()

    def process_dataset(self, file_path):
        """
        Reads, validates, processes and analyses the dataset.
        Generates a report containing sales and data quality results.
        """

        dataframe = self.data_reader.read_data(file_path)

        validation_results = self.data_validator.validate_data(
            dataframe
        )

        processed_data = self.data_processor.process_data(
            dataframe
        )

        analysis_results = {
            "total_sales": self.sales_analyzer.get_total_sales(
                processed_data
            ),
            "total_transactions": (
                self.sales_analyzer.get_total_transactions(
                    processed_data
                )
            ),
            "best_selling_products": (
                self.sales_analyzer.get_best_selling_products(
                    processed_data
                )
            ),
            "sales_by_region": (
                self.sales_analyzer.get_sales_by_region(
                    processed_data
                )
            ),
            "sales_by_category": (
                self.sales_analyzer.get_sales_by_category(
                    processed_data
                )
            )
        }

        report = self.report_generator.generate_report(
            processed_data,
            analysis_results,
            validation_results
        )

        return {
            "validation_results": validation_results,
            "processed_data": processed_data,
            "analysis_results": analysis_results,
            "report": report
        }



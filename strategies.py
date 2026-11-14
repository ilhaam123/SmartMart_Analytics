from abc import ABC, abstractmethod


class SalesAnalysisStrategy(ABC):
    """
    Abstract base class for sales analysis strategies.
    """

    @abstractmethod
    def analyze(self, dataframe):
        pass


class TotalSalesStrategy(SalesAnalysisStrategy):
    """
    Calculates total sales revenue.
    """

    def analyze(self, dataframe):
        return round(dataframe["total_amount"].sum(), 2)


class BestSellingProductStrategy(SalesAnalysisStrategy):
    """
    Identifies the best-selling products.
    """

    def analyze(self, dataframe):
        return (
            dataframe.groupby("product_name")["quantity"]
            .sum()
            .sort_values(ascending=False)
            .head(5)
        )


class RegionalSalesStrategy(SalesAnalysisStrategy):
    """
    Calculates sales revenue by region.
    """

    def analyze(self, dataframe):
        return (
            dataframe.groupby("region")["total_amount"]
            .sum()
            .sort_values(ascending=False)
        )


class StrategyContext:
    """
    Executes the selected sales analysis strategy.
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        """
        Changes the current analysis strategy.
        """

        self.strategy = strategy

    def perform_analysis(self, dataframe):
        """
        Executes the selected strategy.
        """

        return self.strategy.analyze(dataframe)

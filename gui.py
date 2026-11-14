import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from facade import SmartMartFacade
from peak_sales_analyzer import PeakSalesAnalyzer
from customer_analyzer import CustomerAnalyzer
from seasonal_analyzer import SeasonalAnalyzer
from store_analyzer import StoreAnalyzer
from inventory_analyzer import InventoryAnalyzer

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import LinearSegmentedColormap


class SmartMartGUI:
    """Main graphical user interface for SmartMart Analytics."""

    def __init__(self, root):
        self.root = root
        self.root.title("SmartMart Retail Analytics System")
        self.root.state("zoomed")
        self.root.minsize(950, 650)

        self.background_color = "#F4F6F9"
        self.primary_color = "#1F3A5F"

        self.selected_file = None
        self.processing_results = None

        self.facade = SmartMartFacade()
        self.peak_sales_analyzer = PeakSalesAnalyzer()
        self.customer_analyzer = CustomerAnalyzer()
        self.seasonal_analyzer = SeasonalAnalyzer()
        self.store_analyzer = StoreAnalyzer()
        self.inventory_analyzer = InventoryAnalyzer()

        self.root.configure(bg=self.background_color)

        self.create_header()
        self.create_main_content()
        self.create_status_bar()

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------

    def create_header(self):
        header = tk.Frame(
            self.root,
            bg=self.primary_color,
            height=80
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="SmartMart Analytics",
            font=("Arial", 22, "bold"),
            fg="white",
            bg=self.primary_color
        ).pack(side="left", padx=25, pady=20)

        tk.Label(
            header,
            text="Retail Data Analysis System",
            font=("Arial", 11),
            fg="white",
            bg=self.primary_color
        ).pack(side="right", padx=25)

    # --------------------------------------------------
    # MAIN CONTENT AND TABS
    # --------------------------------------------------

    def create_main_content(self):
        main_container = tk.Frame(
            self.root,
            bg=self.background_color
        )
        main_container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=12
        )

        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)

        self.overview_tab = tk.Frame(
            self.notebook, bg=self.background_color
        )
        self.peak_sales_tab = tk.Frame(
            self.notebook, bg=self.background_color
        )
        self.customers_tab = tk.Frame(
            self.notebook, bg=self.background_color
        )
        self.seasonal_tab = tk.Frame(
            self.notebook, bg=self.background_color
        )
        self.stores_tab = tk.Frame(
            self.notebook, bg=self.background_color
        )
        self.inventory_tab = tk.Frame(
            self.notebook, bg=self.background_color
        )

        self.notebook.add(self.overview_tab, text="Overview")
        self.notebook.add(self.peak_sales_tab, text="Peak Sales")
        self.notebook.add(self.customers_tab, text="Customers")
        self.notebook.add(
            self.seasonal_tab, text="Seasonal & Promotions"
        )
        self.notebook.add(
            self.stores_tab, text="Stores & Regions"
        )
        self.notebook.add(
            self.inventory_tab, text="Inventory & Stock"
        )

        self.create_overview_tab()
        self.create_peak_sales_tab()
        self.create_customers_tab()
        self.create_seasonal_tab()
        self.create_stores_tab()
        self.create_inventory_tab()

    # --------------------------------------------------
    # SCROLLABLE FRAME
    # --------------------------------------------------

    def create_scrollable_frame(self, parent):
        container = tk.Frame(
            parent,
            bg=self.background_color
        )
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            container,
            bg=self.background_color,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=canvas.yview
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        frame = tk.Frame(
            canvas,
            bg=self.background_color
        )

        window_id = canvas.create_window(
            (0, 0),
            window=frame,
            anchor="nw"
        )

        frame.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                window_id,
                width=event.width
            )
        )

        canvas.bind_all(
            "<MouseWheel>",
            lambda event: canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

        return frame

    # --------------------------------------------------
    # COMMON CHART CREATION
    # --------------------------------------------------

    def create_chart(
        self, parent, figure, axis,
        title, x_label, y_label
    ):
        axis.set_title(title, fontsize=13, fontweight="bold")
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)

        axis.text(
            0.5, 0.5,
            "Process a dataset to view the chart",
            ha="center", va="center",
            transform=axis.transAxes
        )

        figure.subplots_adjust(
            left=0.22, right=0.96,
            top=0.85, bottom=0.20
        )

        chart_canvas = FigureCanvasTkAgg(
            figure, master=parent
        )
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

        return chart_canvas

    def reset_chart(
        self, axis, canvas, figure,
        title, x_label, y_label
    ):
        axis.clear()
        axis.set_title(title)
        axis.set_xlabel(x_label)
        axis.set_ylabel(y_label)

        axis.text(
            0.5, 0.5,
            "Process a dataset to view the chart",
            ha="center", va="center",
            transform=axis.transAxes
        )

        figure.subplots_adjust(
            left=0.22, right=0.96,
            top=0.85, bottom=0.20
        )
        canvas.draw()

    def update_bar_chart(
        self, axis, canvas, figure,
        chart_data, title, x_label, y_label
    ):
        axis.clear()

        if chart_data.empty:
            axis.text(
                0.5, 0.5, "No data available",
                ha="center", va="center",
                transform=axis.transAxes
            )
        else:
            sorted_data = chart_data.sort_values(
                ascending=True
            )

            axis.barh(
                sorted_data.index.astype(str),
                sorted_data.values
            )

            axis.set_title(
                title, fontsize=13, fontweight="bold"
            )
            axis.set_xlabel(x_label)
            axis.set_ylabel(y_label)
            axis.grid(
                axis="x", linestyle="--", alpha=0.4
            )
            axis.set_axisbelow(True)

        figure.subplots_adjust(
            left=0.22, right=0.96,
            top=0.85, bottom=0.20
        )
        canvas.draw()

    # --------------------------------------------------
    # OVERVIEW TAB
    # --------------------------------------------------

    def create_overview_tab(self):
        main_frame = self.create_scrollable_frame(
            self.overview_tab
        )

        tk.Label(
            main_frame,
            text="Welcome to SmartMart Analytics",
            font=("Arial", 20, "bold"),
            bg=self.background_color,
            fg=self.primary_color
        ).pack(anchor="w", padx=25, pady=(20, 15))

        upload_frame = ttk.LabelFrame(
            main_frame,
            text="Dataset Selection",
            padding=15
        )
        upload_frame.pack(
            fill="x", padx=25, pady=(0, 15)
        )

        ttk.Button(
            upload_frame,
            text="Browse Dataset",
            command=self.browse_dataset
        ).pack(anchor="w")

        self.file_label = tk.Label(
            upload_frame,
            text="No dataset selected",
            font=("Arial", 10),
            bg="white",
            fg="#777777",
            anchor="w",
            padx=10,
            pady=8
        )
        self.file_label.pack(fill="x", pady=8)

        self.process_button = ttk.Button(
            upload_frame,
            text="Process Dataset",
            command=self.process_dataset
        )
        self.process_button.pack(anchor="w", pady=(0, 8))

        export_frame = tk.Frame(upload_frame)
        export_frame.pack(anchor="w")

        self.export_button = ttk.Button(
            export_frame,
            text="Export Excel Report",
            command=self.export_excel_report,
            state="disabled"
        )
        self.export_button.pack(side="left", padx=(0, 8))

        self.pdf_export_button = ttk.Button(
            export_frame,
            text="Export PDF Report",
            command=self.export_pdf_report,
            state="disabled"
        )
        self.pdf_export_button.pack(side="left")

        # Sales overview cards

        sales_frame = ttk.LabelFrame(
            main_frame,
            text="Sales Overview",
            padding=10
        )
        sales_frame.pack(
            fill="x", padx=25, pady=(0, 12)
        )

        self.sales_labels = {}

        sales_items = [
            ("processed_records", "Processed Records"),
            ("total_sales", "Total Net Sales (Rs.)"),
            ("total_transactions", "Total Transactions")
        ]

        for key, title in sales_items:
            card = tk.Frame(
                sales_frame,
                bg="white",
                padx=15,
                pady=12,
                highlightbackground="#D9DEE7",
                highlightthickness=1
            )
            card.pack(
                side="left", fill="both",
                expand=True, padx=5
            )

            tk.Label(
                card, text=title,
                bg="white", fg="#555555",
                font=("Arial", 10)
            ).pack()

            value_label = tk.Label(
                card, text="0",
                bg="white", fg=self.primary_color,
                font=("Arial", 17, "bold")
            )
            value_label.pack(pady=5)
            self.sales_labels[key] = value_label

        # Data quality cards

        quality_frame = ttk.LabelFrame(
            main_frame,
            text="Data Quality Overview",
            padding=10
        )
        quality_frame.pack(
            fill="x", padx=25, pady=(0, 12)
        )

        self.quality_labels = {}

        quality_items = [
            ("missing_values", "Missing Values"),
            ("duplicate_records", "Duplicate Records"),
            ("suspicious_sale_prices", "Suspicious Sale Prices"),
            ("missing_discounts", "Missing Discounts"),
            ("mismatched_sale_amounts", "Mismatched Sale Amounts"),
            ("return_transactions", "Return Transactions")
        ]

        for index, (key, title) in enumerate(quality_items):
            row = index // 3
            column = index % 3

            card = tk.Frame(
                quality_frame,
                bg="white",
                padx=10,
                pady=12,
                highlightbackground="#D9DEE7",
                highlightthickness=1
            )
            card.grid(
                row=row, column=column,
                sticky="nsew", padx=5, pady=5
            )

            tk.Label(
                card, text=title,
                bg="white", fg="#555555",
                font=("Arial", 9)
            ).pack()

            value_label = tk.Label(
                card, text="0",
                bg="white", fg=self.primary_color,
                font=("Arial", 16, "bold")
            )
            value_label.pack(pady=5)
            self.quality_labels[key] = value_label

        for column in range(3):
            quality_frame.columnconfigure(column, weight=1)

        for row in range(2):
            quality_frame.rowconfigure(row, weight=1)

        # Overview charts

        chart_definitions = [
            (
                "Top 5 Best-Selling Products",
                "product_figure", "product_ax", "product_canvas",
                "Total Quantity Sold", "Product Name"
            ),
            (
                "Sales by Region",
                "region_figure", "region_ax", "region_canvas",
                "Total Net Sales (Rs.)", "Region"
            ),
            (
                "Sales by Product Category",
                "category_figure", "category_ax", "category_canvas",
                "Total Net Sales (Rs.)", "Product Category"
            )
        ]

        for title, fig_name, ax_name, canvas_name, xlabel, ylabel in chart_definitions:
            frame = ttk.LabelFrame(
                main_frame, text=title, padding=10
            )
            frame.pack(
                fill="x", padx=25, pady=(0, 12)
            )

            figure = Figure(figsize=(9, 3.5), dpi=100)
            axis = figure.add_subplot(111)

            canvas = self.create_chart(
                frame, figure, axis,
                title, xlabel, ylabel
            )

            setattr(self, fig_name, figure)
            setattr(self, ax_name, axis)
            setattr(self, canvas_name, canvas)

    # --------------------------------------------------
    # PEAK SALES TAB
    # --------------------------------------------------

    def create_peak_sales_tab(self):
        main_frame = self.create_scrollable_frame(
            self.peak_sales_tab
        )

        tk.Label(
            main_frame,
            text="Peak Sales Analysis",
            font=("Arial", 20, "bold"),
            bg=self.background_color,
            fg=self.primary_color
        ).pack(anchor="w", padx=25, pady=(20, 5))

        tk.Label(
            main_frame,
            text=(
                "Analyse shopping activity by weekday and hour "
                "and search individual customer transactions."
            ),
            font=("Arial", 10),
            bg=self.background_color,
            fg="#555555"
        ).pack(anchor="w", padx=25, pady=(0, 15))

        heatmap_frame = ttk.LabelFrame(
            main_frame,
            text="Sales Transactions by Weekday and Hour",
            padding=12
        )
        heatmap_frame.pack(
            fill="x", padx=25, pady=(0, 15)
        )

        self.heatmap_figure = Figure(
            figsize=(11, 4.5), dpi=100
        )
        self.heatmap_ax = self.heatmap_figure.add_subplot(111)

        self.heatmap_canvas = FigureCanvasTkAgg(
            self.heatmap_figure,
            master=heatmap_frame
        )
        self.heatmap_canvas.get_tk_widget().pack(
            fill="both", expand=True
        )

        self.reset_heatmap()

        customer_frame = ttk.LabelFrame(
            main_frame,
            text="Customer Lookup",
            padding=15
        )
        customer_frame.pack(
            fill="x", padx=25, pady=(0, 15)
        )

        search_frame = tk.Frame(
            customer_frame,
            bg=self.background_color
        )
        search_frame.pack(fill="x", pady=5)

        tk.Label(
            search_frame,
            text="Enter Customer ID:",
            font=("Arial", 10, "bold"),
            bg=self.background_color
        ).pack(side="left", padx=(0, 10))

        self.customer_search_entry = ttk.Entry(
            search_frame, width=30,
            font=("Arial", 10)
        )
        self.customer_search_entry.pack(
            side="left", padx=(0, 10)
        )

        ttk.Button(
            search_frame,
            text="Search Customer",
            command=self.search_customer
        ).pack(side="left")

        self.customer_search_entry.bind(
            "<Return>",
            lambda event: self.search_customer()
        )

        summary_frame = ttk.LabelFrame(
            customer_frame,
            text="Customer Summary",
            padding=10
        )
        summary_frame.pack(fill="x", pady=10)

        self.customer_summary_labels = {}

        summary_items = [
            ("transactions", "Total Transactions"),
            ("amount", "Total Sale Amount (Rs.)"),
            ("quantity", "Total Quantity Purchased")
        ]

        for key, title in summary_items:
            card = tk.Frame(
                summary_frame,
                bg="white",
                padx=12, pady=10,
                highlightbackground="#D9DEE7",
                highlightthickness=1
            )
            card.pack(
                side="left", fill="both",
                expand=True, padx=5
            )

            tk.Label(
                card, text=title,
                bg="white", fg="#555555",
                font=("Arial", 9)
            ).pack()

            value_label = tk.Label(
                card, text="0",
                bg="white", fg=self.primary_color,
                font=("Arial", 15, "bold")
            )
            value_label.pack(pady=5)
            self.customer_summary_labels[key] = value_label

        table_frame = ttk.LabelFrame(
            customer_frame,
            text="Customer Transaction History",
            padding=10
        )
        table_frame.pack(
            fill="both", expand=True, pady=10
        )

        columns = (
            "transaction_id", "date", "product",
            "quantity", "amount"
        )

        self.customer_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=10
        )

        headings = {
            "transaction_id": "Transaction ID",
            "date": "Transaction Date",
            "product": "Product",
            "quantity": "Quantity",
            "amount": "Total Amount (Rs.)"
        }

        widths = {
            "transaction_id": 130,
            "date": 170,
            "product": 220,
            "quantity": 90,
            "amount": 150
        }

        for column in columns:
            self.customer_tree.heading(
                column, text=headings[column]
            )
            self.customer_tree.column(
                column, width=widths[column],
                anchor="center"
            )

        self.customer_tree.column("product", anchor="w")
        self.customer_tree.column("amount", anchor="e")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.customer_tree.yview
        )
        self.customer_tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.customer_tree.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

    def reset_heatmap(self):
        self.heatmap_ax.clear()

        self.heatmap_ax.set_title(
            "Peak Shopping Activity",
            fontsize=13, fontweight="bold"
        )
        self.heatmap_ax.text(
            0.5, 0.5,
            "Process a dataset to view the heatmap",
            ha="center", va="center",
            transform=self.heatmap_ax.transAxes
        )
        self.heatmap_canvas.draw()

    def update_peak_sales_heatmap(self, heatmap_data):
        self.heatmap_ax.clear()

        colour_map = LinearSegmentedColormap.from_list(
            "smartmart_blue",
            ["#F4F8FC", "#9CC4E4", "#1F3A5F"]
        )

        image = self.heatmap_ax.imshow(
            heatmap_data.values,
            aspect="auto",
            cmap=colour_map,
            interpolation="nearest"
        )

        weekdays = heatmap_data.index.tolist()

        self.heatmap_ax.set_yticks(range(len(weekdays)))
        self.heatmap_ax.set_yticklabels(weekdays)

        self.heatmap_ax.set_xticks(range(24))
        self.heatmap_ax.set_xticklabels(
            [f"{hour:02d}:00" for hour in range(24)],
            rotation=45, ha="right"
        )

        self.heatmap_ax.set_xlabel("Hour of Day")
        self.heatmap_ax.set_ylabel("Weekday")
        self.heatmap_ax.set_title(
            "Sale Transaction Count by Weekday and Hour",
            fontsize=13, fontweight="bold"
        )

        if hasattr(self, "heatmap_colorbar"):
            self.heatmap_colorbar.remove()

        self.heatmap_colorbar = self.heatmap_figure.colorbar(
            image,
            ax=self.heatmap_ax,
            label="Number of Transactions"
        )

        self.heatmap_figure.tight_layout()
        self.heatmap_canvas.draw()

    # --------------------------------------------------
    # CUSTOMERS TAB
    # --------------------------------------------------

    def create_customers_tab(self):
        main_frame = self.create_scrollable_frame(
            self.customers_tab
        )

        tk.Label(
            main_frame,
            text="Customer Analysis",
            font=("Arial", 20, "bold"),
            bg=self.background_color,
            fg=self.primary_color
        ).pack(anchor="w", padx=25, pady=(20, 5))

        tk.Label(
            main_frame,
            text=(
                "Analyse customer purchasing frequency, behaviour, "
                "age groups and geographical distribution."
            ),
            font=("Arial", 10),
            bg=self.background_color,
            fg="#555555"
        ).pack(anchor="w", padx=25, pady=(0, 15))

        chart_definitions = [
            (
                "Customer Frequency Share",
                "frequency_figure", "frequency_ax", "frequency_canvas",
                "Customer Category", "Number of Customers"
            ),
            (
                "K-means Customer Clustering",
                "clustering_figure", "clustering_ax", "clustering_canvas",
                "Average Basket Value (Rs.)", "Purchase Frequency"
            ),
            (
                "Customer Age Group Analysis",
                "age_figure", "age_ax", "age_canvas",
                "Age Group", "Number of Customers"
            ),
            (
                "Top 10 Customer Cities by Sales",
                "city_figure", "city_ax", "city_canvas",
                "Total Sales (Rs.)", "Customer City"
            )
        ]

        for title, fig_name, ax_name, canvas_name, xlabel, ylabel in chart_definitions:
            frame = ttk.LabelFrame(
                main_frame, text=title, padding=10
            )
            frame.pack(
                fill="x", padx=25, pady=(0, 12)
            )

            figure = Figure(figsize=(9, 3.8), dpi=100)
            axis = figure.add_subplot(111)

            canvas = self.create_chart(
                frame, figure, axis,
                title, xlabel, ylabel
            )

            setattr(self, fig_name, figure)
            setattr(self, ax_name, axis)
            setattr(self, canvas_name, canvas)

    def search_customer(self):
        if self.processing_results is None:
            messagebox.showwarning(
                "Dataset Not Processed",
                "Please process the dataset before searching for customers."
            )
            return

        customer_id = self.customer_search_entry.get().strip()

        if not customer_id:
            messagebox.showwarning(
                "Missing Customer ID",
                "Please enter a customer ID."
            )
            return

        dataframe = self.processing_results["processed_data"]

        customer_data = self.peak_sales_analyzer.search_customer(
            dataframe, customer_id
        )

        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)

        if customer_data.empty:
            for label in self.customer_summary_labels.values():
                label.config(text="0")

            messagebox.showinfo(
                "Customer Not Found",
                f"No transactions found for Customer ID: {customer_id}"
            )
            return

        sale_data = customer_data[
            customer_data["transaction_type"] == "Sale"
        ]

        total_transactions = len(customer_data)
        total_amount = sale_data["total_amount"].sum()
        total_quantity = sale_data["quantity"].sum()

        self.customer_summary_labels["transactions"].config(
            text=f"{total_transactions:,}"
        )
        self.customer_summary_labels["amount"].config(
            text=f"{total_amount:,.2f}"
        )
        self.customer_summary_labels["quantity"].config(
            text=f"{total_quantity:,.0f}"
        )

        for _, row in customer_data.iterrows():
            quantity = row.get("quantity", 0)
            amount = row.get("total_amount", 0)

            try:
                quantity = f"{float(quantity):,.0f}"
            except (ValueError, TypeError):
                quantity = str(quantity)

            try:
                amount = f"{float(amount):,.2f}"
            except (ValueError, TypeError):
                amount = str(amount)

            self.customer_tree.insert(
                "",
                "end",
                values=(
                    row.get("transaction_id", ""),
                    row.get("transaction_datetime", ""),
                    row.get("product_name", ""),
                    quantity,
                    amount
                )
            )

        self.update_status(
            f"Customer {customer_id} search completed"
        )

    def update_customer_charts(self, dataframe):
        # Customer frequency

        frequency_data = (
            self.customer_analyzer.get_customer_frequency(dataframe)
        )

        self.frequency_ax.clear()

        if frequency_data.sum() == 0:
            self.frequency_ax.text(
                0.5, 0.5, "No customer data available",
                ha="center", va="center",
                transform=self.frequency_ax.transAxes
            )
        else:
            self.frequency_ax.bar(
                frequency_data.index,
                frequency_data.values
            )
            self.frequency_ax.set_title(
                "Customer Purchase Frequency",
                fontsize=13, fontweight="bold"
            )
            self.frequency_ax.set_xlabel("Customer Category")
            self.frequency_ax.set_ylabel("Number of Customers")
            self.frequency_ax.grid(
                axis="y", linestyle="--", alpha=0.4
            )
            self.frequency_ax.set_axisbelow(True)

        self.frequency_figure.tight_layout()
        self.frequency_canvas.draw()

        # Customer clustering

        cluster_data = (
            self.customer_analyzer.get_customer_clusters(dataframe)
        )

        self.clustering_ax.clear()

        if cluster_data.empty:
            self.clustering_ax.text(
                0.5, 0.5,
                "Not enough customer data for clustering",
                ha="center", va="center",
                transform=self.clustering_ax.transAxes
            )
        else:
            for cluster_id in sorted(
                cluster_data["cluster"].unique()
            ):
                cluster = cluster_data[
                    cluster_data["cluster"] == cluster_id
                ]

                self.clustering_ax.scatter(
                    cluster["average_basket_value"],
                    cluster["purchase_frequency"],
                    label=f"Cluster {cluster_id + 1}",
                    alpha=0.7
                )

            self.clustering_ax.set_title(
                "K-means Customer Segmentation",
                fontsize=13, fontweight="bold"
            )
            self.clustering_ax.set_xlabel(
                "Average Basket Value (Rs.)"
            )
            self.clustering_ax.set_ylabel("Purchase Frequency")
            self.clustering_ax.set_yscale("log")
            self.clustering_ax.legend()
            self.clustering_ax.grid(
                linestyle="--", alpha=0.4
            )

        self.clustering_figure.tight_layout()
        self.clustering_canvas.draw()

        # Age groups

        age_data = (
            self.customer_analyzer.get_customer_age_groups(dataframe)
        )

        self.age_ax.clear()

        if age_data.empty:
            self.age_ax.text(
                0.5, 0.5, "No age data available",
                ha="center", va="center",
                transform=self.age_ax.transAxes
            )
        else:
            self.age_ax.bar(
                age_data["age_group"].astype(str),
                age_data["customers"]
            )
            self.age_ax.set_title(
                "Customers by Age Group",
                fontsize=13, fontweight="bold"
            )
            self.age_ax.set_xlabel("Age Group")
            self.age_ax.set_ylabel("Number of Customers")
            self.age_ax.grid(
                axis="y", linestyle="--", alpha=0.4
            )
            self.age_ax.set_axisbelow(True)

        self.age_figure.tight_layout()
        self.age_canvas.draw()

        # Customer cities

        city_data = (
            self.customer_analyzer.get_top_customer_cities(
                dataframe, limit=10
            )
        )

        self.city_ax.clear()

        if city_data.empty:
            self.city_ax.text(
                0.5, 0.5, "No city data available",
                ha="center", va="center",
                transform=self.city_ax.transAxes
            )
        else:
            sorted_cities = city_data.sort_values(
                "total_sales", ascending=True
            )

            self.city_ax.barh(
                sorted_cities["customer_city"].astype(str),
                sorted_cities["total_sales"]
            )
            self.city_ax.set_title(
                "Top 10 Customer Cities by Sales",
                fontsize=13, fontweight="bold"
            )
            self.city_ax.set_xlabel("Total Sales (Rs.)")
            self.city_ax.set_ylabel("Customer City")
            self.city_ax.grid(
                axis="x", linestyle="--", alpha=0.4
            )
            self.city_ax.set_axisbelow(True)

        self.city_figure.tight_layout()
        self.city_canvas.draw()

    # --------------------------------------------------
    # SEASONAL & PROMOTIONS TAB
    # --------------------------------------------------

    def create_seasonal_tab(self):
        main_frame = self.create_scrollable_frame(
            self.seasonal_tab
        )

        tk.Label(
            main_frame,
            text="Seasonal & Promotions Analysis",
            font=("Arial", 20, "bold"),
            bg=self.background_color,
            fg=self.primary_color
        ).pack(anchor="w", padx=25, pady=(20, 5))

        tk.Label(
            main_frame,
            text=(
                "Explore daily and monthly sales trends, "
                "promotion performance and public holiday sales."
            ),
            font=("Arial", 10),
            bg=self.background_color,
            fg="#555555"
        ).pack(anchor="w", padx=25, pady=(0, 15))

        chart_definitions = [
            (
                "Daily Sales Trend",
                "daily_figure", "daily_ax", "daily_canvas",
                "Date", "Net Sales (Rs.)"
            ),
            (
                "Monthly Sales Trend",
                "monthly_figure", "monthly_ax", "monthly_canvas",
                "Month", "Net Sales (Rs.)"
            ),
            (
                "Promotion Performance",
                "promotion_figure", "promotion_ax", "promotion_canvas",
                "Total Sales (Rs.)", "Promotion"
            )
        ]

        for title, fig_name, ax_name, canvas_name, xlabel, ylabel in chart_definitions:
            frame = ttk.LabelFrame(
                main_frame, text=title, padding=10
            )
            frame.pack(
                fill="x", padx=25, pady=(0, 12)
            )

            figure = Figure(figsize=(10, 4), dpi=100)
            axis = figure.add_subplot(111)

            canvas = self.create_chart(
                frame, figure, axis,
                title, xlabel, ylabel
            )

            setattr(self, fig_name, figure)
            setattr(self, ax_name, axis)
            setattr(self, canvas_name, canvas)

        holiday_frame = ttk.LabelFrame(
            main_frame,
            text="Public Holiday Analysis",
            padding=15
        )
        holiday_frame.pack(
            fill="x", padx=25, pady=(0, 12)
        )

        tk.Label(
            holiday_frame,
            text=(
                "Enter public holiday dates within the dataset date range. "
                "Use YYYY-MM-DD format and separate dates with commas."
            ),
            bg=self.background_color,
            fg="#555555",
            wraplength=850,
            justify="left"
        ).pack(anchor="w", pady=(0, 8))

        self.holiday_entry = ttk.Entry(
            holiday_frame, font=("Arial", 10)
        )
        self.holiday_entry.pack(fill="x", pady=(0, 8))

        ttk.Button(
            holiday_frame,
            text="Analyse Holiday Sales",
            command=self.update_holiday_chart
        ).pack(anchor="w")

        self.holiday_figure = Figure(
            figsize=(10, 3.5), dpi=100
        )
        self.holiday_ax = self.holiday_figure.add_subplot(111)

        self.holiday_canvas = self.create_chart(
            holiday_frame,
            self.holiday_figure,
            self.holiday_ax,
            "Public Holiday vs Normal Day Sales",
            "Day Type",
            "Total Sales (Rs.)"
        )

    def update_seasonal_charts(self, dataframe):
        # Daily sales

        daily_data = (
            self.seasonal_analyzer.get_daily_sales_trend(dataframe)
        )

        self.daily_ax.clear()

        if daily_data.empty:
            self.daily_ax.text(
                0.5, 0.5, "No daily sales data available",
                ha="center", va="center",
                transform=self.daily_ax.transAxes
            )
        else:
            self.daily_ax.plot(
                daily_data["date"].astype(str),
                daily_data["net_sales"],
                marker="o", linewidth=1
            )
            self.daily_ax.set_title(
                "Daily Net Sales Trend",
                fontsize=13, fontweight="bold"
            )
            self.daily_ax.set_xlabel("Date")
            self.daily_ax.set_ylabel("Net Sales (Rs.)")
            self.daily_ax.tick_params(
                axis="x", rotation=45
            )
            self.daily_ax.grid(
                linestyle="--", alpha=0.4
            )

        self.daily_figure.tight_layout()
        self.daily_canvas.draw()

        # Monthly sales

        monthly_data = (
            self.seasonal_analyzer.get_monthly_sales_trend(dataframe)
        )

        self.monthly_ax.clear()

        if monthly_data.empty:
            self.monthly_ax.text(
                0.5, 0.5, "No monthly sales data available",
                ha="center", va="center",
                transform=self.monthly_ax.transAxes
            )
        else:
            self.monthly_ax.plot(
                monthly_data["month"],
                monthly_data["net_sales"],
                marker="o", linewidth=2
            )
            self.monthly_ax.set_title(
                "Monthly Net Sales Trend",
                fontsize=13, fontweight="bold"
            )
            self.monthly_ax.set_xlabel("Month")
            self.monthly_ax.set_ylabel("Net Sales (Rs.)")
            self.monthly_ax.tick_params(
                axis="x", rotation=45
            )
            self.monthly_ax.grid(
                linestyle="--", alpha=0.4
            )

        self.monthly_figure.tight_layout()
        self.monthly_canvas.draw()

        # Promotions

        promotion_data = (
            self.seasonal_analyzer.get_promotion_sales(dataframe)
        )

        self.promotion_ax.clear()

        if promotion_data.empty:
            self.promotion_ax.text(
                0.5, 0.5, "No promotion data available",
                ha="center", va="center",
                transform=self.promotion_ax.transAxes
            )
        else:
            sorted_promotions = promotion_data.sort_values(
                "total_sales", ascending=True
            )

            self.promotion_ax.barh(
                sorted_promotions["promotion_name"].astype(str),
                sorted_promotions["total_sales"]
            )
            self.promotion_ax.set_title(
                "Sales by Promotion",
                fontsize=13, fontweight="bold"
            )
            self.promotion_ax.set_xlabel("Total Sales (Rs.)")
            self.promotion_ax.set_ylabel("Promotion")
            self.promotion_ax.grid(
                axis="x", linestyle="--", alpha=0.4
            )
            self.promotion_ax.set_axisbelow(True)

        self.promotion_figure.tight_layout()
        self.promotion_canvas.draw()

    def update_holiday_chart(self):
        if self.processing_results is None:
            messagebox.showwarning(
                "Dataset Not Processed",
                "Please process the dataset first."
            )
            return

        entered_dates = self.holiday_entry.get().strip()

        if not entered_dates:
            messagebox.showwarning(
                "Missing Dates",
                "Please enter at least one public holiday date."
            )
            return

        holiday_dates = [
            date.strip()
            for date in entered_dates.split(",")
            if date.strip()
        ]

        try:
            from datetime import datetime

            for date in holiday_dates:
                datetime.strptime(date, "%Y-%m-%d")

            dataframe = self.processing_results["processed_data"]

            holiday_data = (
                self.seasonal_analyzer.get_holiday_sales(
                    dataframe, holiday_dates
                )
            )

            self.holiday_ax.clear()

            if holiday_data.empty:
                self.holiday_ax.text(
                    0.5, 0.5,
                    "No holiday comparison data available",
                    ha="center", va="center",
                    transform=self.holiday_ax.transAxes
                )
            else:
                self.holiday_ax.bar(
                    holiday_data["day_type"],
                    holiday_data["total_sales"]
                )
                self.holiday_ax.set_title(
                    "Public Holiday vs Normal Day Sales",
                    fontsize=13, fontweight="bold"
                )
                self.holiday_ax.set_xlabel("Day Type")
                self.holiday_ax.set_ylabel("Total Sales (Rs.)")
                self.holiday_ax.grid(
                    axis="y", linestyle="--", alpha=0.4
                )
                self.holiday_ax.set_axisbelow(True)

            self.holiday_figure.tight_layout()
            self.holiday_canvas.draw()

            self.update_status(
                "Public holiday analysis completed"
            )

        except ValueError:
            messagebox.showerror(
                "Invalid Date",
                "Please enter dates using YYYY-MM-DD format.\n"
                "Example: 2025-12-25"
            )

        except Exception as error:
            messagebox.showerror(
                "Holiday Analysis Error",
                f"Unable to analyse holiday sales:\n{error}"
            )

    # --------------------------------------------------
    # STORES & REGIONS TAB
    # --------------------------------------------------

    def create_stores_tab(self):
        main_frame = self.create_scrollable_frame(
            self.stores_tab
        )

        tk.Label(
            main_frame,
            text="Stores & Regions Analysis",
            font=("Arial", 20, "bold"),
            bg=self.background_color,
            fg=self.primary_color
        ).pack(anchor="w", padx=25, pady=(20, 5))

        tk.Label(
            main_frame,
            text=(
                "Compare store performance, sales volume, "
                "regional results and store-level performance indicators."
            ),
            font=("Arial", 10),
            bg=self.background_color,
            fg="#555555"
        ).pack(anchor="w", padx=25, pady=(0, 15))

        # Store performance table

        performance_frame = ttk.LabelFrame(
            main_frame,
            text="Store Performance Rankings",
            padding=10
        )
        performance_frame.pack(
            fill="x", padx=25, pady=(0, 12)
        )

        performance_columns = (
            "rank", "store_id", "store_city", "region",
            "total_sales", "total_transactions",
            "total_quantity_sold"
        )

        self.store_performance_tree = ttk.Treeview(
            performance_frame,
            columns=performance_columns,
            show="headings",
            height=8
        )

        performance_headings = {
            "rank": "Rank",
            "store_id": "Store ID",
            "store_city": "City",
            "region": "Region",
            "total_sales": "Total Sales (Rs.)",
            "total_transactions": "Transactions",
            "total_quantity_sold": "Quantity Sold"
        }

        for column in performance_columns:
            self.store_performance_tree.heading(
                column, text=performance_headings[column]
            )
            self.store_performance_tree.column(
                column, width=125, anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            performance_frame,
            orient="vertical",
            command=self.store_performance_tree.yview
        )
        self.store_performance_tree.configure(
            yscrollcommand=scrollbar.set
        )
        self.store_performance_tree.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

        # Store volume chart

        volume_frame = ttk.LabelFrame(
            main_frame,
            text="Sales Volume by Store",
            padding=10
        )
        volume_frame.pack(
            fill="x", padx=25, pady=(0, 12)
        )

        self.store_volume_figure = Figure(
            figsize=(10, 4), dpi=100
        )
        self.store_volume_ax = (
            self.store_volume_figure.add_subplot(111)
        )
        self.store_volume_canvas = self.create_chart(
            volume_frame,
            self.store_volume_figure,
            self.store_volume_ax,
            "Sales Volume by Store",
            "Total Quantity Sold",
            "Store ID"
        )

        # Regional performance chart

        regional_frame = ttk.LabelFrame(
            main_frame,
            text="Regional Performance Comparison",
            padding=10
        )
        regional_frame.pack(
            fill="x", padx=25, pady=(0, 12)
        )

        self.regional_figure = Figure(
            figsize=(10, 4), dpi=100
        )
        self.regional_ax = (
            self.regional_figure.add_subplot(111)
        )
        self.regional_canvas = self.create_chart(
            regional_frame,
            self.regional_figure,
            self.regional_ax,
            "Sales Performance by Region",
            "Total Sales (Rs.)",
            "Region"
        )

        # Store efficiency table

        efficiency_frame = ttk.LabelFrame(
            main_frame,
            text="Store Efficiency Indicators",
            padding=10
        )
        efficiency_frame.pack(
            fill="x", padx=25, pady=(0, 20)
        )

        efficiency_columns = (
            "store_id", "store_city", "total_sales",
            "total_transactions", "average_transaction_value",
            "average_stock_on_hand", "sales_per_transaction"
        )

        self.store_efficiency_tree = ttk.Treeview(
            efficiency_frame,
            columns=efficiency_columns,
            show="headings",
            height=8
        )

        efficiency_headings = {
            "store_id": "Store ID",
            "store_city": "City",
            "total_sales": "Total Sales (Rs.)",
            "total_transactions": "Transactions",
            "average_transaction_value": "Average Basket (Rs.)",
            "average_stock_on_hand": "Average Stock",
            "sales_per_transaction": "Sales per Transaction"
        }

        for column in efficiency_columns:
            self.store_efficiency_tree.heading(
                column, text=efficiency_headings[column]
            )
            self.store_efficiency_tree.column(
                column, width=150, anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            efficiency_frame,
            orient="vertical",
            command=self.store_efficiency_tree.yview
        )
        self.store_efficiency_tree.configure(
            yscrollcommand=scrollbar.set
        )
        self.store_efficiency_tree.pack(
            side="left", fill="both", expand=True
        )
        scrollbar.pack(side="right", fill="y")

    def update_store_charts(self, dataframe):
        # Store performance ranking

        performance_data = (
            self.store_analyzer.get_store_performance(dataframe)
        )

        for item in self.store_performance_tree.get_children():
            self.store_performance_tree.delete(item)

        for _, row in performance_data.iterrows():
            self.store_performance_tree.insert(
                "",
                "end",
                values=(
                    row["rank"],
                    row["store_id"],
                    row["store_city"],
                    row["region"],
                    f'{row["total_sales"]:,.2f}',
                    f'{row["total_transactions"]:,}',
                    f'{row["total_quantity_sold"]:,.0f}'
                )
            )

        # Sales volume chart

        volume_data = (
            self.store_analyzer.get_sales_volume_by_store(dataframe)
        )

        self.store_volume_ax.clear()

        if volume_data.empty:
            self.store_volume_ax.text(
                0.5, 0.5, "No store sales data available",
                ha="center", va="center",
                transform=self.store_volume_ax.transAxes
            )
        else:
            sorted_volume = volume_data.sort_values(
                "total_quantity_sold", ascending=True
            )
            self.store_volume_ax.barh(
                sorted_volume["store_id"].astype(str),
                sorted_volume["total_quantity_sold"]
            )
            self.store_volume_ax.set_title(
                "Sales Volume by Store",
                fontsize=13, fontweight="bold"
            )
            self.store_volume_ax.set_xlabel("Total Quantity Sold")
            self.store_volume_ax.set_ylabel("Store ID")
            self.store_volume_ax.grid(
                axis="x", linestyle="--", alpha=0.4
            )
            self.store_volume_ax.set_axisbelow(True)

        self.store_volume_figure.tight_layout()
        self.store_volume_canvas.draw()

        # Regional performance

        regional_data = (
            self.store_analyzer.get_regional_performance(dataframe)
        )

        self.regional_ax.clear()

        if regional_data.empty:
            self.regional_ax.text(
                0.5, 0.5, "No regional sales data available",
                ha="center", va="center",
                transform=self.regional_ax.transAxes
            )
        else:
            sorted_regions = regional_data.sort_values(
                "total_sales", ascending=True
            )
            self.regional_ax.barh(
                sorted_regions["region"].astype(str),
                sorted_regions["total_sales"]
            )
            self.regional_ax.set_title(
                "Sales Performance by Region",
                fontsize=13, fontweight="bold"
            )
            self.regional_ax.set_xlabel("Total Sales (Rs.)")
            self.regional_ax.set_ylabel("Region")
            self.regional_ax.grid(
                axis="x", linestyle="--", alpha=0.4
            )
            self.regional_ax.set_axisbelow(True)

        self.regional_figure.tight_layout()
        self.regional_canvas.draw()

        # Store efficiency table

        efficiency_data = (
            self.store_analyzer.get_store_efficiency(dataframe)
        )

        for item in self.store_efficiency_tree.get_children():
            self.store_efficiency_tree.delete(item)

        for _, row in efficiency_data.iterrows():
            self.store_efficiency_tree.insert(
                "",
                "end",
                values=(
                    row["store_id"],
                    row["store_city"],
                    f'{row["total_sales"]:,.2f}',
                    f'{row["total_transactions"]:,}',
                    f'{row["average_transaction_value"]:,.2f}',
                    f'{row["average_stock_on_hand"]:,.2f}',
                    f'{row["sales_per_transaction"]:,.2f}'
                )
            )

    # --------------------------------------------------
    # INVENTORY & STOCK ANALYSIS TAB
    # --------------------------------------------------

    def create_inventory_tab(self):
        main_frame = self.create_scrollable_frame(
            self.inventory_tab
        )

        tk.Label(
            main_frame,
            text="Inventory & Stock Analysis",
            font=("Arial", 20, "bold"),
            bg=self.background_color,
            fg=self.primary_color
        ).pack(anchor="w", padx=25, pady=(20, 5))

        tk.Label(
            main_frame,
            text=(
                "Monitor the latest stock levels, identify products "
                "requiring reordering and compare inventory across stores "
                "and product categories."
            ),
            font=("Arial", 10),
            bg=self.background_color,
            fg="#555555",
            wraplength=1000,
            justify="left"
        ).pack(anchor="w", padx=25, pady=(0, 15))

        # Inventory summary cards

        summary_frame = ttk.LabelFrame(
            main_frame,
            text="Inventory Summary",
            padding=10
        )
        summary_frame.pack(
            fill="x", padx=25, pady=(0, 12)
        )

        self.inventory_summary_labels = {}

        summary_items = [
            ("total_products", "Total Products"),
            ("total_product_store_combinations", "Product-Store Records"),
            ("healthy_stock", "Healthy Stock"),
            ("reorder_required", "Reorder Required"),
            ("out_of_stock", "Out of Stock"),
            ("total_stock_units", "Total Stock Units")
        ]

        for index, (key, title) in enumerate(summary_items):
            row = index // 3
            column = index % 3

            card = tk.Frame(
                summary_frame,
                bg="white",
                padx=12,
                pady=12,
                highlightbackground="#D9DEE7",
                highlightthickness=1
            )
            card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=5,
                pady=5
            )

            tk.Label(
                card,
                text=title,
                bg="white",
                fg="#555555",
                font=("Arial", 9)
            ).pack()

            value_label = tk.Label(
                card,
                text="0",
                bg="white",
                fg=self.primary_color,
                font=("Arial", 17, "bold")
            )
            value_label.pack(pady=5)

            self.inventory_summary_labels[key] = value_label

        for column in range(3):
            summary_frame.columnconfigure(column, weight=1)

        # Latest stock status table

        status_frame = ttk.LabelFrame(
            main_frame,
            text="Latest Stock Status by Product and Store",
            padding=10
        )
        status_frame.pack(
            fill="both", expand=True,
            padx=25, pady=(0, 12)
        )

        status_columns = (
            "store_id",
            "product_name",
            "stock_on_hand",
            "reorder_level",
            "stock_status",
            "transaction_datetime"
        )

        self.inventory_status_tree = ttk.Treeview(
            status_frame,
            columns=status_columns,
            show="headings",
            height=10
        )

        status_headings = {
            "store_id": "Store ID",
            "product_name": "Product Name",
            "stock_on_hand": "Stock on Hand",
            "reorder_level": "Reorder Level",
            "stock_status": "Stock Status",
            "transaction_datetime": "Last Updated"
        }

        status_widths = {
            "store_id": 100,
            "product_name": 220,
            "stock_on_hand": 120,
            "reorder_level": 120,
            "stock_status": 150,
            "transaction_datetime": 180
        }

        for column in status_columns:
            self.inventory_status_tree.heading(
                column, text=status_headings[column]
            )
            self.inventory_status_tree.column(
                column,
                width=status_widths[column],
                anchor="center"
            )

        self.inventory_status_tree.column(
            "product_name", anchor="w"
        )

        self.inventory_status_tree.tag_configure(
            "healthy", foreground="#287A3D"
        )
        self.inventory_status_tree.tag_configure(
            "reorder", foreground="#B7791F"
        )
        self.inventory_status_tree.tag_configure(
            "out", foreground="#C0392B"
        )

        status_scrollbar = ttk.Scrollbar(
            status_frame,
            orient="vertical",
            command=self.inventory_status_tree.yview
        )
        self.inventory_status_tree.configure(
            yscrollcommand=status_scrollbar.set
        )

        self.inventory_status_tree.pack(
            side="left", fill="both", expand=True
        )
        status_scrollbar.pack(side="right", fill="y")

        # Low-stock products table

        low_stock_frame = ttk.LabelFrame(
            main_frame,
            text="Products Requiring Reorder",
            padding=10
        )
        low_stock_frame.pack(
            fill="both", expand=True,
            padx=25, pady=(0, 12)
        )

        low_stock_columns = (
            "store_id", "product_name",
            "stock_on_hand", "reorder_level"
        )

        self.low_stock_tree = ttk.Treeview(
            low_stock_frame,
            columns=low_stock_columns,
            show="headings",
            height=7
        )

        low_stock_headings = {
            "store_id": "Store ID",
            "product_name": "Product Name",
            "stock_on_hand": "Current Stock",
            "reorder_level": "Reorder Level"
        }

        for column in low_stock_columns:
            self.low_stock_tree.heading(
                column, text=low_stock_headings[column]
            )
            self.low_stock_tree.column(
                column, width=160, anchor="center"
            )

        self.low_stock_tree.column(
            "product_name", anchor="w"
        )

        low_scrollbar = ttk.Scrollbar(
            low_stock_frame,
            orient="vertical",
            command=self.low_stock_tree.yview
        )
        self.low_stock_tree.configure(
            yscrollcommand=low_scrollbar.set
        )
        self.low_stock_tree.pack(
            side="left", fill="both", expand=True
        )
        low_scrollbar.pack(side="right", fill="y")

        # Out-of-stock products table

        out_stock_frame = ttk.LabelFrame(
            main_frame,
            text="Out-of-Stock Products",
            padding=10
        )
        out_stock_frame.pack(
            fill="both", expand=True,
            padx=25, pady=(0, 12)
        )

        out_columns = (
            "store_id", "product_name",
            "stock_on_hand", "reorder_level"
        )

        self.out_stock_tree = ttk.Treeview(
            out_stock_frame,
            columns=out_columns,
            show="headings",
            height=6
        )

        for column in out_columns:
            self.out_stock_tree.heading(
                column, text=low_stock_headings[column]
            )
            self.out_stock_tree.column(
                column, width=160, anchor="center"
            )

        self.out_stock_tree.column(
            "product_name", anchor="w"
        )

        out_scrollbar = ttk.Scrollbar(
            out_stock_frame,
            orient="vertical",
            command=self.out_stock_tree.yview
        )
        self.out_stock_tree.configure(
            yscrollcommand=out_scrollbar.set
        )
        self.out_stock_tree.pack(
            side="left", fill="both", expand=True
        )
        out_scrollbar.pack(side="right", fill="y")

        # Stock by store chart

        store_stock_frame = ttk.LabelFrame(
            main_frame,
            text="Stock Distribution by Store",
            padding=10
        )
        store_stock_frame.pack(
            fill="x", padx=25, pady=(0, 12)
        )

        self.inventory_store_figure = Figure(
            figsize=(10, 4), dpi=100
        )
        self.inventory_store_ax = (
            self.inventory_store_figure.add_subplot(111)
        )

        self.inventory_store_canvas = self.create_chart(
            store_stock_frame,
            self.inventory_store_figure,
            self.inventory_store_ax,
            "Total Stock Units by Store",
            "Total Stock Units",
            "Store ID"
        )

        # Stock by category chart

        category_stock_frame = ttk.LabelFrame(
            main_frame,
            text="Stock Distribution by Product Category",
            padding=10
        )
        category_stock_frame.pack(
            fill="x", padx=25, pady=(0, 20)
        )

        self.inventory_category_figure = Figure(
            figsize=(10, 4), dpi=100
        )
        self.inventory_category_ax = (
            self.inventory_category_figure.add_subplot(111)
        )

        self.inventory_category_canvas = self.create_chart(
            category_stock_frame,
            self.inventory_category_figure,
            self.inventory_category_ax,
            "Total Stock Units by Product Category",
            "Total Stock Units",
            "Product Category"
        )

    # --------------------------------------------------
    # INVENTORY UPDATE METHODS
    # --------------------------------------------------

    def update_inventory_analysis(self, dataframe):
        """Update all inventory tables, summary cards and charts."""

        # Calculate inventory summary

        summary = (
            self.inventory_analyzer.get_inventory_summary(dataframe)
        )

        for key, label in self.inventory_summary_labels.items():
            value = summary.get(key, 0)

            if key == "total_stock_units":
                label.config(text=f"{value:,.0f}")
            else:
                label.config(text=f"{value:,}")

        # Latest stock status

        stock_data = (
            self.inventory_analyzer.get_stock_status(dataframe)
        )

        for item in self.inventory_status_tree.get_children():
            self.inventory_status_tree.delete(item)

        for _, row in stock_data.iterrows():
            status = row["stock_status"]

            if status == "Healthy":
                tag = "healthy"
            elif status == "Reorder Required":
                tag = "reorder"
            else:
                tag = "out"

            self.inventory_status_tree.insert(
                "",
                "end",
                values=(
                    row["store_id"],
                    row["product_name"],
                    f'{row["stock_on_hand"]:,.0f}',
                    f'{row["reorder_level"]:,.0f}',
                    status,
                    row["transaction_datetime"]
                ),
                tags=(tag,)
            )

        # Products requiring reorder

        low_stock_data = (
            self.inventory_analyzer.get_low_stock_products(dataframe)
        )

        for item in self.low_stock_tree.get_children():
            self.low_stock_tree.delete(item)

        for _, row in low_stock_data.iterrows():
            self.low_stock_tree.insert(
                "",
                "end",
                values=(
                    row["store_id"],
                    row["product_name"],
                    f'{row["stock_on_hand"]:,.0f}',
                    f'{row["reorder_level"]:,.0f}'
                )
            )

        # Out-of-stock products

        out_stock_data = (
            self.inventory_analyzer.get_out_of_stock_products(
                dataframe
            )
        )

        for item in self.out_stock_tree.get_children():
            self.out_stock_tree.delete(item)

        for _, row in out_stock_data.iterrows():
            self.out_stock_tree.insert(
                "",
                "end",
                values=(
                    row["store_id"],
                    row["product_name"],
                    f'{row["stock_on_hand"]:,.0f}',
                    f'{row["reorder_level"]:,.0f}'
                )
            )

        # Stock by store chart

        store_stock_data = (
            self.inventory_analyzer.get_stock_by_store(dataframe)
        )

        self.inventory_store_ax.clear()

        if store_stock_data.empty:
            self.inventory_store_ax.text(
                0.5, 0.5,
                "No inventory data available",
                ha="center", va="center",
                transform=self.inventory_store_ax.transAxes
            )
        else:
            sorted_store_data = store_stock_data.sort_values(
                "total_stock_units", ascending=True
            )

            self.inventory_store_ax.barh(
                sorted_store_data["store_id"].astype(str),
                sorted_store_data["total_stock_units"]
            )

            self.inventory_store_ax.set_title(
                "Total Stock Units by Store",
                fontsize=13, fontweight="bold"
            )
            self.inventory_store_ax.set_xlabel(
                "Total Stock Units"
            )
            self.inventory_store_ax.set_ylabel("Store ID")
            self.inventory_store_ax.grid(
                axis="x", linestyle="--", alpha=0.4
            )
            self.inventory_store_ax.set_axisbelow(True)

        self.inventory_store_figure.tight_layout()
        self.inventory_store_canvas.draw()

        # Stock by category chart

        category_stock_data = (
            self.inventory_analyzer.get_stock_by_category(dataframe)
        )

        self.inventory_category_ax.clear()

        if category_stock_data.empty:
            self.inventory_category_ax.text(
                0.5, 0.5,
                "No category inventory data available",
                ha="center", va="center",
                transform=self.inventory_category_ax.transAxes
            )
        else:
            sorted_category_data = (
                category_stock_data.sort_values(
                    "total_stock_units", ascending=True
                )
            )

            self.inventory_category_ax.barh(
                sorted_category_data["product_category"].astype(str),
                sorted_category_data["total_stock_units"]
            )

            self.inventory_category_ax.set_title(
                "Total Stock Units by Product Category",
                fontsize=13, fontweight="bold"
            )
            self.inventory_category_ax.set_xlabel(
                "Total Stock Units"
            )
            self.inventory_category_ax.set_ylabel(
                "Product Category"
            )
            self.inventory_category_ax.grid(
                axis="x", linestyle="--", alpha=0.4
            )
            self.inventory_category_ax.set_axisbelow(True)

        self.inventory_category_figure.tight_layout()
        self.inventory_category_canvas.draw()

    # --------------------------------------------------
    # DATASET SELECTION
    # --------------------------------------------------

    def browse_dataset(self):
        file_path = filedialog.askopenfilename(
            title="Select SmartMart Dataset",
            filetypes=[
                ("Excel Files", "*.xlsx"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        if not file_path.lower().endswith(".xlsx"):
            messagebox.showerror(
                "Invalid File",
                "Please select an Excel (.xlsx) file."
            )
            return

        self.selected_file = file_path
        self.processing_results = None

        self.export_button.config(state="disabled")
        self.pdf_export_button.config(state="disabled")

        self.file_label.config(
            text=f"Selected Dataset: {file_path}",
            fg=self.primary_color
        )

        # Reset overview cards

        for label in self.sales_labels.values():
            label.config(text="0")

        for label in self.quality_labels.values():
            label.config(text="0")

        # Reset overview charts

        self.reset_chart(
            self.product_ax, self.product_canvas,
            self.product_figure,
            "Top 5 Best-Selling Products",
            "Total Quantity Sold", "Product Name"
        )

        self.reset_chart(
            self.region_ax, self.region_canvas,
            self.region_figure,
            "Sales by Region",
            "Total Net Sales (Rs.)", "Region"
        )

        self.reset_chart(
            self.category_ax, self.category_canvas,
            self.category_figure,
            "Sales by Product Category",
            "Total Net Sales (Rs.)", "Product Category"
        )

        # Reset peak sales

        self.reset_heatmap()
        self.customer_search_entry.delete(0, tk.END)

        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)

        for label in self.customer_summary_labels.values():
            label.config(text="0")

        # Reset customer charts

        self.reset_chart(
            self.frequency_ax, self.frequency_canvas,
            self.frequency_figure,
            "Customer Purchase Frequency",
            "Customer Category", "Number of Customers"
        )

        self.reset_chart(
            self.clustering_ax, self.clustering_canvas,
            self.clustering_figure,
            "Customer Segmentation",
            "Average Basket Value (Rs.)", "Purchase Frequency"
        )
        self.clustering_ax.set_yscale("linear")

        self.reset_chart(
            self.age_ax, self.age_canvas,
            self.age_figure,
            "Customers by Age Group",
            "Age Group", "Number of Customers"
        )

        self.reset_chart(
            self.city_ax, self.city_canvas,
            self.city_figure,
            "Top 10 Customer Cities",
            "Total Sales (Rs.)", "Customer City"
        )

        # Reset seasonal charts

        self.reset_chart(
            self.daily_ax, self.daily_canvas,
            self.daily_figure,
            "Daily Net Sales Trend",
            "Date", "Net Sales (Rs.)"
        )

        self.reset_chart(
            self.monthly_ax, self.monthly_canvas,
            self.monthly_figure,
            "Monthly Net Sales Trend",
            "Month", "Net Sales (Rs.)"
        )

        self.reset_chart(
            self.promotion_ax, self.promotion_canvas,
            self.promotion_figure,
            "Sales by Promotion",
            "Total Sales (Rs.)", "Promotion"
        )

        self.reset_chart(
            self.holiday_ax, self.holiday_canvas,
            self.holiday_figure,
            "Public Holiday vs Normal Day Sales",
            "Day Type", "Total Sales (Rs.)"
        )

        self.holiday_entry.delete(0, tk.END)

        # Reset store tables

        for item in self.store_performance_tree.get_children():
            self.store_performance_tree.delete(item)

        for item in self.store_efficiency_tree.get_children():
            self.store_efficiency_tree.delete(item)

        self.reset_chart(
            self.store_volume_ax, self.store_volume_canvas,
            self.store_volume_figure,
            "Sales Volume by Store",
            "Total Quantity Sold", "Store ID"
        )

        self.reset_chart(
            self.regional_ax, self.regional_canvas,
            self.regional_figure,
            "Sales Performance by Region",
            "Total Sales (Rs.)", "Region"
        )

        # Reset inventory summary cards

        for label in self.inventory_summary_labels.values():
            label.config(text="0")

        # Reset inventory tables

        for tree in (
            self.inventory_status_tree,
            self.low_stock_tree,
            self.out_stock_tree
        ):
            for item in tree.get_children():
                tree.delete(item)

        # Reset inventory charts

        self.reset_chart(
            self.inventory_store_ax,
            self.inventory_store_canvas,
            self.inventory_store_figure,
            "Total Stock Units by Store",
            "Total Stock Units", "Store ID"
        )

        self.reset_chart(
            self.inventory_category_ax,
            self.inventory_category_canvas,
            self.inventory_category_figure,
            "Total Stock Units by Product Category",
            "Total Stock Units", "Product Category"
        )

        self.update_status("Dataset selected successfully")

    # --------------------------------------------------
    # DATASET PROCESSING
    # --------------------------------------------------

    def process_dataset(self):
        if not self.selected_file:
            messagebox.showwarning(
                "No Dataset",
                "Please select an Excel dataset first."
            )
            return

        try:
            self.process_button.config(state="disabled")
            self.export_button.config(state="disabled")
            self.pdf_export_button.config(state="disabled")

            self.update_status("Processing dataset...")
            self.root.update_idletasks()

            self.processing_results = (
                self.facade.process_dataset(self.selected_file)
            )

            results = self.processing_results

            analysis = results["analysis_results"]
            validation = results["validation_results"]
            processed_data = results["processed_data"]

            # Sales overview

            self.sales_labels["processed_records"].config(
                text=f"{len(processed_data):,}"
            )

            self.sales_labels["total_sales"].config(
                text=f"{analysis['total_sales']:,.2f}"
            )

            self.sales_labels["total_transactions"].config(
                text=f"{analysis['total_transactions']:,}"
            )

            # Data quality overview

            for key, label in self.quality_labels.items():
                label.config(
                    text=f"{validation.get(key, 0):,}"
                )

            # Overview charts

            self.update_best_selling_chart(
                analysis["best_selling_products"]
            )
            self.update_sales_by_region_chart(
                analysis["sales_by_region"]
            )
            self.update_sales_by_category_chart(
                analysis["sales_by_category"]
            )

            # Peak sales

            heatmap_data = (
                self.peak_sales_analyzer.get_peak_sales_heatmap(
                    processed_data
                )
            )
            self.update_peak_sales_heatmap(heatmap_data)

            # Customer analysis

            self.update_customer_charts(processed_data)

            # Seasonal analysis

            self.update_seasonal_charts(processed_data)

            # Store analysis

            self.update_store_charts(processed_data)

            # Inventory analysis

            self.update_inventory_analysis(processed_data)

            self.export_button.config(state="normal")
            self.pdf_export_button.config(state="normal")

            self.update_status(
                "Dataset processing completed"
            )

            messagebox.showinfo(
                "Processing Complete",
                "The dataset has been processed successfully!"
            )

        except Exception as error:
            self.processing_results = None

            messagebox.showerror(
                "Processing Error",
                f"An error occurred:\n{error}"
            )

            self.update_status("Processing failed")

        finally:
            self.process_button.config(state="normal")

    # --------------------------------------------------
    # OVERVIEW CHART UPDATE METHODS
    # --------------------------------------------------

    def update_best_selling_chart(self, best_selling_products):
        self.update_bar_chart(
            self.product_ax,
            self.product_canvas,
            self.product_figure,
            best_selling_products,
            "Top 5 Best-Selling Products",
            "Total Quantity Sold",
            "Product Name"
        )

    def update_sales_by_region_chart(self, sales_by_region):
        self.update_bar_chart(
            self.region_ax,
            self.region_canvas,
            self.region_figure,
            sales_by_region,
            "Sales by Region",
            "Total Net Sales (Rs.)",
            "Region"
        )

    def update_sales_by_category_chart(self, sales_by_category):
        self.update_bar_chart(
            self.category_ax,
            self.category_canvas,
            self.category_figure,
            sales_by_category,
            "Sales by Product Category",
            "Total Net Sales (Rs.)",
            "Product Category"
        )

    # --------------------------------------------------
    # EXCEL EXPORT
    # --------------------------------------------------

    def export_excel_report(self):
        if not self.processing_results:
            messagebox.showwarning(
                "No Report Available",
                "Please process a dataset before exporting a report."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Save SmartMart Excel Report",
            defaultextension=".xlsx",
            initialfile="SmartMart_Sales_Report.xlsx",
            filetypes=[("Excel Workbook", "*.xlsx")]
        )

        if not file_path:
            return

        try:
            report = self.processing_results["report"]

            self.facade.report_generator.export_report_to_excel(
                report, file_path
            )

            self.update_status(
                "Excel report exported successfully"
            )

            messagebox.showinfo(
                "Export Successful",
                f"Excel report saved successfully!\n\n{file_path}"
            )

        except Exception as error:
            messagebox.showerror(
                "Export Error",
                f"Unable to export the Excel report:\n{error}"
            )
            self.update_status("Excel report export failed")

    # --------------------------------------------------
    # PDF EXPORT
    # --------------------------------------------------

    def export_pdf_report(self):
        if not self.processing_results:
            messagebox.showwarning(
                "No Report Available",
                "Please process a dataset before exporting a report."
            )
            return

        file_path = filedialog.asksaveasfilename(
            title="Save SmartMart PDF Report",
            defaultextension=".pdf",
            initialfile="SmartMart_Sales_Report.pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not file_path:
            return

        try:
            report = self.processing_results["report"]

            self.facade.report_generator.export_report_to_pdf(
                report, file_path
            )

            self.update_status(
                "PDF report exported successfully"
            )

            messagebox.showinfo(
                "Export Successful",
                f"PDF report saved successfully!\n\n{file_path}"
            )

        except Exception as error:
            messagebox.showerror(
                "Export Error",
                f"Unable to export the PDF report:\n{error}"
            )
            self.update_status("PDF report export failed")

    # --------------------------------------------------
    # STATUS BAR
    # --------------------------------------------------

    def create_status_bar(self):
        self.status_label = tk.Label(
            self.root,
            text="Ready | SmartMart Analytics System",
            font=("Arial", 9),
            bg="#E1E5EA",
            fg="#333333",
            anchor="w",
            padx=15,
            pady=8
        )
        self.status_label.pack(
            side="bottom", fill="x"
        )

    def update_status(self, message):
        self.status_label.config(
            text=f"Status: {message}"
        )


# --------------------------------------------------
# APPLICATION ENTRY POINT
# --------------------------------------------------

def main():
    root = tk.Tk()
    app = SmartMartGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
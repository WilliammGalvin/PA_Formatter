import math

class LineItem:
    def __init__(
            self,
            sub_id: str,
            job_id: str,
            file_name: str,
            exact_count: int,
            fuzzy_count: int,
            new_count: int,
            total_count: int,
            is_rush: bool,
    ):
        self.sub_id = sub_id
        self.job_id = job_id
        self.file_name = file_name
        self.exact_count = exact_count
        self.fuzzy_count = fuzzy_count
        self.new_count = new_count
        self.total_count = total_count
        self.is_rush = is_rush
        self._validate_total()


    def _validate_total(self) -> None:
        total = self.exact_count + self.fuzzy_count + self.new_count

        if total != self.total_count:
            raise ValueError("Column total count doesn't match with added total count.")


    def extend(
            self,
            exact_count: int,
            fuzzy_count: int,
            new_count: int,
            total_count: int
    ) -> None:
        self.exact_count += exact_count
        self.fuzzy_count += fuzzy_count
        self.new_count += new_count
        self.total_count += total_count
        self._validate_total()


    @staticmethod
    def get_price_rates() -> dict:
        exact_rate = 0.08
        fuzzy_rate = 0.16
        new_rate = 0.25

        return {
            "exact_rate": exact_rate,
            "fuzzy_rate": fuzzy_rate,
            "new_rate": new_rate,
        }


    def _get_expanded_counts(self) -> dict:
        expand_rate = 1.25

        exact_count_expanded = math.ceil(self.exact_count * expand_rate)
        fuzzy_count_expanded = math.ceil(self.fuzzy_count * expand_rate)
        new_count_expanded = math.ceil(self.new_count * expand_rate)
        total_count_expanded = math.ceil(self.total_count * expand_rate)

        return {
            "exact_count_expanded": exact_count_expanded,
            "fuzzy_count_expanded": fuzzy_count_expanded,
            "new_count_expanded": new_count_expanded,
            "total_count_expanded": total_count_expanded,
        }


    def _get_total_expanded_price(self) -> float:
        rates = LineItem.get_price_rates()
        expanded_counts = self._get_expanded_counts()

        exact_expanded_price = rates["exact_rate"] * expanded_counts["exact_count_expanded"]
        fuzzy_expanded_price = rates["fuzzy_rate"] * expanded_counts["fuzzy_count_expanded"]
        new_expanded_price = rates["new_rate"] * expanded_counts["new_count_expanded"]
        total_expanded_price = exact_expanded_price + fuzzy_expanded_price + new_expanded_price

        return total_expanded_price


    @staticmethod
    def get_excel_cols() -> list:
        return [
            "Sub ID",
            "Job ID",
            "File Name",
            "Exact Count",
            "Fuzzy Count",
            "New Count",
            "Total Count",
            "Expanded Total",
            "Rush",
        ]


    def format_for_excel(self) -> dict:
        expanded_counts = self._get_expanded_counts()

        entry = {
            "Sub ID": self.sub_id,
            "Job ID": self.job_id,
            "File Name": self.file_name,
            "Exact Count": self.exact_count,
            "Fuzzy Count": self.fuzzy_count,
            "New Count": self.new_count,
            "Total Count": self.total_count,
            "Expanded Total": expanded_counts["total_count_expanded"],
            "Rush": self.is_rush,
        }

        return entry


    def _add_lp_detail(
            self,
            service_group_1: str,
            service_group_2: str,
            service: str,
            unit_of_measurement: str,
            quantity: str,
            rate: str,
    ) -> dict:
        return {
            "Mark New Line Item": "",
            "Item Description": self.sub_id,
            "Source": "en-CA",
            "Target": "fr-CA",
            "Hide Unit Costs": 0,
            "Hide Details": 0,
            "Service Group 1": service_group_1,
            "Service Group 2": service_group_2,
            "Service Group 3": "",
            "Service": service,
            "UofM": unit_of_measurement,
            "Quantity": quantity,
            "Rate": rate,
            "CommentsForInvoice": self.file_name,
            "Technology Product": "TransPort",
        }


    @staticmethod
    def get_csv_cols() -> list:
        return [
            "Mark New Line Item",
            "Item Description",
            "Source",
            "Target",
            "Hide Unit Costs",
            "Hide Details",
            "Service Group 1",
            "Service Group 2",
            "Service Group 3",
            "Service",
            "UofM",
            "Quantity",
            "Rate",
            "CommentsForInvoice",
            "Technology Product",
        ]


    def format_for_csv(self) -> list[dict]:
        entries = []
        is_min_job = False

        expanded_counts = self._get_expanded_counts()
        rates = LineItem.get_price_rates()
        total_price = self._get_total_expanded_price()

        if expanded_counts["total_count_expanded"] <= 500:
            is_min_job = True
            total_price = 125
        elif expanded_counts["total_count_expanded"] <= 700:
            is_min_job = True
            total_price = 175

        if self.is_rush:
            entries.append(self._add_lp_detail(
                "Handling & Delivery",
                "",
                "Supplément urgence / Rush Fee",
                "fixed",
                str(total_price),
                "0.5",
            ))

        if is_min_job:
            entries.append(self._add_lp_detail(
                "Language Services",
                "Translation",
                "Traduction / Translation",
                "fixed",
                str(total_price),
                "1"
            ))

            return entries

        entries.append(self._add_lp_detail(
            "Language Services",
            "Translation",
            "TM - Exact Match",
            "word",
            str(expanded_counts["exact_count_expanded"]),
            str(rates["exact_rate"]),
        ))

        entries.append(self._add_lp_detail(
            "Language Services",
            "Translation",
            "TM - Fuzzy Match",
            "word",
            str(expanded_counts["fuzzy_count_expanded"]),
            str(rates["fuzzy_rate"]),
        ))

        entries.append(self._add_lp_detail(
            "Language Services",
            "Translation",
            "Traduction / Translation",
            "word",
            str(expanded_counts["new_count_expanded"]),
            str(rates["new_rate"]),
        ))

        entries.append(self._add_lp_detail(
            "Language Services",
            "Translation",
            "File Preparation",
            "hour",
            "0",
            "75"
        ))

        return entries
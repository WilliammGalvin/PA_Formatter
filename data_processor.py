import pandas as pd
from line_item import LineItem
import os

def _read_entries(frame: pd.DataFrame) -> dict:
    entries = {}
    for i, row in frame.iterrows():
        if i == 0:  # Skip header
            continue

        # Extract data from row
        data = row.tolist()

        try:
            sub_id = data[0]
            job_id = data[1]
            file_name = data[6]

            hundred_percent_count = data[13]
            rep_count = data[14]
            context_count = data[18]
            exact_count = hundred_percent_count + rep_count + context_count

            range_fuzzy_count = data[16]
            fuzzy_reps_count = data[17]
            fuzzy_count = range_fuzzy_count + fuzzy_reps_count

            new_count = data[15]
            total_count = data[19]

            is_rush = True if data[25].upper() == "YES" else False
        except IndexError:
            raise ValueError("Incorrect file format.")

        # Create entry
        lp = LineItem(
            sub_id=sub_id,
            job_id=job_id,
            file_name=file_name,
            exact_count=exact_count,
            fuzzy_count=fuzzy_count,
            new_count=new_count,
            total_count=total_count,
            is_rush=is_rush
        )

        # If entry with same sub_id is already added, merge entries
        if sub_id in entries:
            existing = entries[sub_id]
            lp.extend(
                exact_count=existing.exact_count,
                fuzzy_count=existing.fuzzy_count,
                new_count=existing.new_count,
                total_count=existing.total_count,
            )
        else:
            entries[sub_id] = lp

    return entries


def process_data(path: str, out_dir: str) -> None:
    err = None

    excel_path = os.path.join(out_dir, "output.xlsx")
    csv_path = os.path.join(out_dir, "pa_output.csv")

    try:
        # Extract data
        df = pd.read_excel(path)
        data_entries = _read_entries(df)

        # Create Excel file from entries
        excel_entries = [entry.format_for_excel() for entry in data_entries.values()]
        output_excel_df = pd.DataFrame(excel_entries)[LineItem.get_excel_cols()]
        output_excel_df.to_excel(excel_path, index=False)
        print("Generated output excel file.")

        # Convert to CSV format for PA
        csv_entries = []
        for item in data_entries.values():
            csv_entries.extend(item.format_for_csv())

        output_csv_df = pd.DataFrame(csv_entries)[LineItem.get_csv_cols()]
        output_csv_df.to_csv(csv_path, index=False)
        print("Generated output csv file.")
    except ValueError as e:
        err = e

    if err:
        raise err
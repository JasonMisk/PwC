import pandas as pd
import csv
import os
import re

def find_targets_with_headers_df(file_path, targets):
    """
    Reads a CSV file line by line, locates each target row in the first column,
    backtracks to the last 'Description' entry (before the first target) to identify
    the header row, and returns a pandas DataFrame with one row per target.
    """
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    first_cols = [row[0] if row else '' for row in rows]
    target_indices = [i for i, val in enumerate(first_cols) if val in targets]
    if not target_indices:
        raise ValueError(f"None of the targets {targets} found in {file_path}")

    first_target_idx = min(target_indices)
    header_indices = [
        i for i, v in enumerate(first_cols[:first_target_idx + 1])
        if v == 'Description'
    ]
    if not header_indices:
        raise ValueError(f"No 'Description' row found before the first target in {file_path}")
    header_idx = header_indices[-1]
    header_row = rows[header_idx]

    dfs = []
    for idx in target_indices:
        target_row = rows[idx]
        mapping = {
            header_row[i]: (target_row[i] if i < len(target_row) else None)
            for i in range(len(header_row))
        }
        dfs.append(pd.DataFrame([mapping]))
    return pd.concat(dfs, ignore_index=True)


def aggregate_totals_to_csv(data_dir, targets, output_csv='aggregated_totals.csv'):
    """
    Walk subdirs named BA900_YYYY-MM-DD_zipcsv, extract each target row from TOTAL.csv,
    append a 'date' column (from the folder name), concatenate results,
    pivot so each target is its own column (with the 'TOTAL ASSETS (Col 1 plus col 3)' value),
    compute NPL = impairments ÷ loans, and write out to CSV.
    """
    dfs = []
    pattern = re.compile(r'^BA900_(\d{4}-\d{2}-\d{2})_zipcsv$')

    for entry in os.listdir(data_dir):
        match = pattern.match(entry)
        if not match:
            continue
        date_str = match.group(1)
        total_csv = os.path.join(data_dir, entry, 'TOTAL.csv')
        if os.path.isfile(total_csv):
            df = find_targets_with_headers_df(total_csv, targets)
            df['date'] = pd.to_datetime(date_str)
            dfs.append(df)

    if dfs:
        combined = pd.concat(dfs, ignore_index=True)
        # pivot into columns per target
        pivoted = (
            combined
            .set_index(['date', 'Description'])['TOTAL ASSETS (Col 1 plus col 3)']
            .unstack('Description')
        )
        # ensure numeric
        pivoted = pivoted.apply(pd.to_numeric)
        # compute NPL ratio
        imp_col, loan_col = targets
        pivoted['NPL'] = pivoted[imp_col] / pivoted[loan_col]
    else:
        # empty DataFrame with the three columns
        pivoted = pd.DataFrame(columns=targets + ['NPL'])

    pivoted.to_csv(output_csv)
    return pivoted


if __name__ == "__main__":
    import argparse

    TARGETS = [
        'Less: credit impairments in respect of loans and advances',
        'Overdrafts, loans and advances: private sector (total of items 181, 187 and 188)'
    ]

    parser = argparse.ArgumentParser(
        description="Aggregate two rows from multiple TOTAL.csv files and compute NPL ratio."
    )
    parser.add_argument(
        'data_dir',
        help="Directory containing BA900_YYYY-MM-DD_zipcsv subfolders"
    )
    parser.add_argument(
        '--output', '-o',
        default='aggregated_totals.csv',
        help="Output CSV filename"
    )
    args = parser.parse_args()

    df = aggregate_totals_to_csv(
        data_dir=args.data_dir,
        targets=TARGETS,
        output_csv=args.output
    )
    print(f"Aggregated {len(df)} dates and saved to {args.output}")

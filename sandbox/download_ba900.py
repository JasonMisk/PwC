#!/usr/bin/env python3
"""
download_ba900_to_csv.py

Download aggregated BA900 'TOTAL' data from the South African Reserve Bank API
for a specified period range, convert the XML responses into a CSV file, and save.

Dependencies:
  - requests
  - python-dateutil
  - pandas
"""

import argparse
import time
import requests
from dateutil.parser import isoparse
import xml.etree.ElementTree as ET
import pandas as pd

API_BASE = "https://custom.resbank.co.za/SarbWebApi/SarbData/IFData"
STATUS_FORCELIST = {429, 500, 502, 503, 504}


def retry_get(url: str, max_retries: int = 5, backoff_factor: float = 1.0) -> requests.Response:
    """
    Perform GET with exponential backoff on specified status codes.
    """
    for attempt in range(max_retries):
        response = requests.get(url, timeout=10)
        if response.status_code in STATUS_FORCELIST:
            delay = backoff_factor * (2 ** attempt)
            time.sleep(delay)
            continue
        response.raise_for_status()
        return response
    # last attempt
    response.raise_for_status()
    return response


def fetch_periods() -> list[str]:
    """
    Retrieve all available BA900 periods.
    """
    url = f"{API_BASE}/GetPeriods/BA900"
    resp = retry_get(url)
    return resp.json()


def parse_xml_to_dict(xml_data: str) -> dict:
    """
    Parse XML string into a flat dict of {tag_name: text}.
    """
    root = ET.fromstring(xml_data)
    record = {}
    for elem in root.iter():
        if len(list(elem)) == 0:  # leaf node
            tag = elem.tag.split("}")[-1]  # strip namespace if present
            record[tag] = elem.text
    return record


def download_and_convert(
        start_period: str,
        end_period: str,
        output_csv: str,
        max_retries: int,
        backoff_factor: float,
) -> None:
    """
    Loop through BA900 periods, fetch TOTAL XML data, convert to dicts,
    and assemble into a single CSV.
    """
    start_dt = isoparse(start_period)
    end_dt = isoparse(end_period)
    all_periods = fetch_periods()
    valid_periods = sorted(
        p for p in all_periods if start_dt <= isoparse(p) <= end_dt
    )

    records = []
    for period in valid_periods:
        url = f"{API_BASE}/GetInstitutionData/BA900/{period}/TOTAL"
        resp = retry_get(url, max_retries=max_retries, backoff_factor=backoff_factor)

        # **Key fix**: extract the raw XML string from the JSON wrapper
        xml_data = resp.json().get("XMLData", "")
        if not xml_data:
            print(f"⚠ No XMLData for period {period}, skipping.")
            continue

        record = parse_xml_to_dict(xml_data)
        record["Period"] = period
        records.append(record)
        print(f"✔ Processed period {period}")

    df = pd.DataFrame(records)
    df.sort_values("Period", inplace=True)
    df.to_csv(output_csv, index=False)
    print(f"\nSaved CSV to {output_csv}")


def main():
    parser = argparse.ArgumentParser(
        description="Download BA900 TOTAL XML data and convert to a single CSV"
    )
    parser.add_argument(
        "--start-period", required=True, help="Start period (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-period", required=True, help="End period (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--output-csv",
        default="data/raw/ba900_total.csv",
        help="Path for the combined output CSV",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=5,
        help="Max retry attempts on transient failures",
    )
    parser.add_argument(
        "--backoff-factor",
        type=float,
        default=1.0,
        help="Backoff factor (seconds) for exponential delay",
    )
    args = parser.parse_args()

    download_and_convert(
        args.start_period,
        args.end_period,
        args.output_csv,
        args.max_retries,
        args.backoff_factor,
    )


if __name__ == "__main__":
    main()

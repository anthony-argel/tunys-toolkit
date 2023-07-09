import csv
import requests
import os
from urllib.parse import urlparse
from tqdm import tqdm


def download_by_csv_column(csv_path, column, save_path):
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        rows = list(reader)
        total_rows = len(rows)

        for row in tqdm(rows, total=total_rows):
            url = row[column]
            if url[0] == "/":
                url = "http:" + url

            a = urlparse(url)
            file_name = os.path.basename(a.path)

            full_save_path = os.path.join(save_path, file_name)

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(full_save_path, "wb") as f:
                    f.write(response.content)

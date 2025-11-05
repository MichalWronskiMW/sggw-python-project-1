import time
import csv
import requests
from datetime import datetime


# ===== Ćwiczenie IV - dekorator
def log_time(func):
    """Dekorator logujący czas działania funkcji."""
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Start: {func.__name__} ({datetime.now().strftime('%H:%M:%S')})")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Koniec: {func.__name__} ({datetime.now().strftime('%H:%M:%S')})")
        print(f"Czas: {end - start:.2f}s\n")
        return result
    return wrapper


# ===== Ćwiczenie I – pobieranie pliku + uzupełnienie o nowe wyjątki =====
def download_csv(url: str, filename: str = "latest.csv") -> str:
    """Pobiera plik CSV z podanego URL i zapisuje lokalnie."""
    try:
        resp = requests.get(url)
        if resp.status_code == 404:
            raise NotFoundError(url)
        elif resp.status_code == 403:
            raise AccessDeniedError(url)
        resp.raise_for_status()

        with open(filename, "w", encoding="utf-8") as f:
            f.write(resp.text)

        print(f"Zapisano plik: {filename}")
        return filename

    except (requests.RequestException, DownloadError) as e:
        print(f"[ERROR] {e}")
        return ""


# ===== Ćwiczenie II – wyjątki =====
class DownloadError(Exception):
    """Bazowy wyjątek dla błędów pobierania pliku."""
    def __init__(self, url: str):
        super().__init__(f"Błąd pobierania pliku: {url}")
        self.url = url

class NotFoundError(DownloadError):
    """Plik nie znaleziony (HTTP 404)."""
    def __init__(self, url: str):
        super().__init__(url)
        self.args = (f"Plik nie znaleziony (HTTP 404): {url}",)

class AccessDeniedError(DownloadError):
    """Brak dostępu do pliku (HTTP 403)."""
    def __init__(self, url: str):
        super().__init__(url)
        self.args = (f"Brak dostępu do pliku (HTTP 403): {url}",)


# ===== Ćwiczenie III i IV – ETL z dekoratorem =====
class ETL:
    def __init__(self, input_file: str):
        self.input_file = input_file

    def read_rows(self):
        """Generator wczytujący plik CSV linijka po linijce, pomijając nagłówek."""
        with open(self.input_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                yield row

    def process(self):
        """Generator przetwarzający każdą linijkę: suma, średnia, brakujące wartości."""
        for row in self.read_rows():
            if not row or not row[0].strip():
                continue  

            idx = int(row[0])
            values = row[1:]
            missing = [i + 1 for i, v in enumerate(values) if v.strip() in ("", "-")]
            nums = [float(v) for v in values if v.strip() not in ("", "-")]
            total = sum(nums)
            avg = total / len(nums) if nums else 0
            yield idx, total, avg, missing

    @log_time
    def save(self, values_file="values.csv", missing_file="missing_values.csv"):
        """Zapis wyników do dwóch plików CSV."""
        with open(values_file, "w", newline="", encoding="utf-8") as f_val, \
             open(missing_file, "w", newline="", encoding="utf-8") as f_miss:

            w_val = csv.writer(f_val)
            w_miss = csv.writer(f_miss)

            w_val.writerow(["id", "sum", "avg"])
            w_miss.writerow(["id", "missing_indices"])

            for idx, total, avg, missing in self.process():
                w_val.writerow([idx, total, avg])
                w_miss.writerow([idx, ",".join(map(str, missing))])


# ===== Uruchomienie programu =====
if __name__ == "__main__":
    url = "https://oleksandr-fedoruk.com/wp-content/uploads/2025/10/sample.csv"
    #url = "https://mock.httpstatus.io/403"
    #url = "https://mock.httpstatus.io/404"

    filename = download_csv(url, "latest.csv")
    if filename:
        ETL(filename).save()

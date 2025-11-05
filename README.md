# Projekt: Prosty proces ETL w Pythonie (SGGW – Programowanie w Pythonie)

## Opis

Projekt realizuje zadania z ćwiczeń I–IV:

1. **Pobieranie pliku CSV z Internetu** (z wykorzystaniem biblioteki `requests`)
2. **Obsługa wyjątków** dla błędów HTTP (403, 404)
3. **Transformacja danych CSV** przy użyciu klasy `ETL`
4. **Zastosowanie dekoratora** do logowania czasu działania funkcji

W wyniku działania programu powstają dwa pliki:

* `values.csv` – zawiera numer porządkowy, sumę i średnią wartości w wierszu
* `missing_values.csv` – zawiera numer porządkowy oraz indeksy kolumn z brakującymi danymi (`"-"`)

---

## Struktura projektu

```
.
├── src/
│   └── my-app/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── __init__.py
├── pyproject.toml
├── poetry.lock
├── README.md
└── .gitignore
```

---

## Wymagania

* Python 3.11+
* Poetry (do zarządzania środowiskiem i zależnościami)
* Zainstalowana biblioteka `requests` (automatycznie przez Poetry)

---

## Działanie programu

* Domyślnie program pobiera plik CSV z adresu:

  ```
  https://oleksandr-fedoruk.com/wp-content/uploads/2025/10/sample.csv
  ```
* Jeśli serwer zwróci błąd 403 lub 404 — zostanie rzucony odpowiedni wyjątek (`AccessDeniedError` lub `NotFoundError`).
* Program przetwarza dane, tworząc dwa pliki wynikowe:

  * `values.csv`
  * `missing_values.csv`

Wszystkie wartości (również pojedyncze) są ujmowane w cudzysłowie dla spójności.

---

## Autor

**Michał Wroński**
Projekt wykonany w ramach przedmiotu *Programowanie w Pythonie* (SGGW, 2025).

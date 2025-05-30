# ING Zadanie Rekrutacyjne

Zadanie sprawdzające funkcjonalność akceptacji ciastek na stronie ing.pl

## Wymagania

- Python 3.11 lub nowszy
- pip (instalator pakietów Python)

# Instalacja

```bash
pip install pytest pytest-playwright
python -m playwright install --with-deps
```

## Uruchomienie Testu

Uruchomienie testu lokalnie:
```bash
python test_cookies.py
```
Test uruchamia się w trzech przeglądarkach:
- Chromium
- Firefox
- WebKit

## Zakres Testów

Test sprawdza następujące funkcjonalności:
1. Przejście na stronę ing.pl
2. Kliknięcie przycisku "Dostosuj" w menu ciasteczek
3. Wyrażenie zgody na ciasteczka analityczne
4. Zaakceptowanie wybranych preferencji
5. Weryfikację poprawności zapisanych ciasteczek w przeglądarce

## Obsługa Błędów

W przypadku wystąpienia błędu podczas testu:
- Zostanie wykonany zrzut ekranu
- Plik ze zrzutem zostanie zapisany jako `cookie_error_{nazwa_przeglądarki_w_której_wystąpił_błąd}.png`
- Szczegółowy komunikat błędu zostanie wyświetlony w konsoli

## CI

Projekt zawiera skonfigurowany pipeline GitHub Actions, który:
- Uruchamia testy automatycznie przy każdym push i pull request
- Zapisuje zrzuty ekranu jako artefakty w przypadku błędów

Z uwagi na miejsce uruchomienia testów przez serwis GitHub zabezpieczenia strony ing.pl wymagają rozwiązania hCaptcha

## Autor

Łukasz Oleksiuk

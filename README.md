## Konfiguracja DVC (Data Version Control)

Ten projekt wykorzystuje **DVC** (Data Version Control) do zarządzania dużymi plikami danych i modelami, które nie są przechowywane bezpośrednio w repozytorium Git. Dane te są hostowane na **Google Drive** z wykorzystaniem **konta usługi (Service Account)**.

Aby pobrać i pracować z danymi projektu, wykonaj poniższe kroki:

### 1. Wymagania wstępne

Upewnij się, że masz zainstalowane następujące oprogramowanie:

* **Python 3.9+**.

* **DVC (Data Version Control)**: Jeśli jeszcze nie masz, zainstaluj w swoim środowisku wirtualnym:

    ```bash
    pip install dvc
    ```

* **Wtyczka DVC dla Google Drive**: Niezbędna do integracji z Google Drive. Zainstaluj w środowisku wirtualnym:

    ```bash
    pip install "dvc[gdrive]"
    ```

    lub

    ```bash
    pip install dvc-gdrive
    ```

### 2. Plik klucza konta usługi Google Drive

Do pobierania danych z Google Drive wymagany jest **plik JSON z kluczem konta usługi**. Otrzymasz ten plik od właściciela projektu lub administratora.

**Ważne:**
* **Przechowuj ten plik w bezpiecznym miejscu** na swoim komputerze.
* **Nigdy nie dodawaj go do repozytorium Git ani DVC!** Jest to plik poufny.

### 3. Automatyczna konfiguracja DVC

Przygotowaliśmy uniwersalny skrypt, który skonfiguruje DVC w Twoim lokalnym repozytorium, używając podanego pliku klucza.

1.  **Aktywuj swoje środowisko wirtualne**:
    * **Linux/macOS:**
        ```bash
        source venv/bin/activate
        ```
    * **Windows (Command Prompt):**
        ```bash
        .\venv\Scripts\activate
        ```
    * **Windows (PowerShell):**
        ```bash
        .\venv\Scripts\Activate.ps1
        ```

2.  **Uruchom skrypt konfiguracyjny**:
    Po aktywacji środowiska, wykonaj następującą komendę w katalogu głównym projektu, podając pełną ścieżkę do swojego pliku JSON z kluczem konta usługi:

    ```bash
    python setup_dvc.py /sciezka/do/TWOJEGO_KLUCZA_KONTA_USLUGI.json
    ```
    * **Przykład na Linux/macOS:**
        ```bash
        python setup_dvc.py /home/uzytkownik/moje_klucze/gdrive_service_account.json
        ```
    * **Przykład na Windows:**
        ```bash
        python setup_dvc.py C:\Users\TwojaNazwa\Dokumenty\moje_klucze\gdrive_service_account.json
        ```

    Skrypt automatycznie ustawi lokalne parametry DVC, które umożliwią dostęp do Google Drive.

### 4. Pobieranie danych DVC

Po pomyślnej konfiguracji, możesz pobrać wszystkie dane DVC z Google Drive za pomocą prostej komendy:

```bash
dvc pull


# Konfiguracja DVC dla Projektu Kedro

Witaj w projekcie! Używamy Data Version Control (DVC) do zarządzania dużymi plikami danych i modelami, które nie są przechowywane bezpośrednio w repozytorium Git. Naszym zdalnym magazynem DVC jest Google Drive.

Poniżej znajdziesz instrukcje, jak skonfigurować DVC na swoim komputerze, aby móc pracować z danymi projektu.

## 1. Wymagania wstępne

Zanim zaczniesz, upewnij się, że masz zainstalowane:

1. **Git:** [Instrukcja instalacji Git](https://git-scm.com/book/pl/v2/Pierwsze-kroki-Instalacja-Gita)
2. **Python:** Wersja zgodna z projektem Kedro (np. 3.9+).
3. **DVC oraz wsparcie dla Google Drive:**  
   Otwórz terminal/konsolę i w swoim środowisku wirtualnym projektu (jeśli używasz) uruchom:  
   ```bash
   pip install "dvc[gdrive]"
   ```
4. **Środowisko Projektu Kedro:** Upewnij się, że masz skonfigurowane środowisko wirtualne dla tego projektu Kedro i zainstalowane wszystkie zależności z `requirements.txt` (lub zgodnie z instrukcją konfiguracji projektu Kedro).

## 2. Klonowanie repozytorium projektu

Jeśli jeszcze tego nie zrobiłeś, sklonuj główne repozytorium projektu:

```bash
git clone <adres_URL_repozytorium_git>
cd <nazwa_katalogu_projektu>
```

## 3. Konfiguracja DVC z Google Drive (Metoda: Konto Usługi - Zalecana)

Ta metoda wykorzystuje dedykowane Konto Usługi Google do autoryzacji DVC. Jest to preferowane podejście, aby uniknąć problemów z indywidualną konfiguracją OAuth 2.0.

### Krok 3.1: Uzyskaj plik klucza Konta Usługi

Do autoryzacji DVC będziesz potrzebować specjalnego pliku klucza JSON dla Konta Usługi (np. `service-account-key.json`).  
Skontaktuj się z administratorem projektu (Przemek), aby otrzymać ten plik.  
**WAŻNE:** Ten plik zawiera poufne dane uwierzytelniające. **NIGDY** nie dodawaj go do repozytorium Git! Przechowuj go w bezpiecznym miejscu na swoim komputerze (np. poza katalogiem repozytorium lub w ścieżce ignorowanej przez Git, jeśli tak ustalono w zespole).

### Krok 3.2: Skonfiguruj DVC lokalnie

Po otrzymaniu pliku klucza JSON i zapisaniu go na swoim komputerze, musisz wskazać DVC, gdzie ten plik się znajduje. Główna konfiguracja zdalnego magazynu (`mygdrive`) jest już w projekcie (w `.dvc/config`). Ty musisz tylko dodać lokalną konfigurację ścieżki do klucza.

W terminalu, w głównym katalogu projektu, uruchom:

```bash
dvc remote modify --local mygdrive gdrive_service_account_json_file_path /pełna/ścieżka/do/twojego/service-account-key.json
```

Zastąp `/pełna/ścieżka/do/twojego/service-account-key.json` rzeczywistą, pełną ścieżką do miejsca, gdzie zapisałeś otrzymany plik klucza JSON.  
Użycie flagi `--local` sprawi, że ta konfiguracja zostanie zapisana w pliku `.dvc/config.local`, który jest ignorowany przez Git i pozostanie tylko na Twoim komputerze.  
Konfiguracja `gdrive_use_service_account true` dla zdalnego magazynu `mygdrive` powinna już być ustawiona w głównym pliku `.dvc/config` przez administratora.

### Krok 3.3: Pobierz dane projektu

Teraz możesz pobrać najnowsze wersje danych i modeli zarządzanych przez DVC:

```bash
dvc pull -r mygdrive
```

Powinieneś zobaczyć postęp pobierania plików. Jeśli DVC zgłosi, że wszystko jest aktualne, oznacza to, że nie ma nowszych danych na zdalnym magazynie lub masz już najnowszą wersję.

### Krok 3.4: Rozwiązywanie problemów (dla metody z Kontem Usługi)

- **Błąd ('Unexpected credentials type', None, 'Expected', 'service_account'):**  
  Upewnij się, że plik JSON, którego ścieżkę podałeś w `gdrive_service_account_json_file_path`, jest na pewno kluczem Konta Usługi (powinien zawierać m.in. `"type": "service_account"`, `"private_key"`, `"client_email"`), a nie np. plikiem `client_secret.json` z konfiguracji Klienta OAuth 2.0. Poproś administratora o właściwy plik.

- **Błąd HttpError 404 ... File not found: 1OSSSo35ObNdt5Hf5kLAZTf1QXyhoFoZ4 (lub podobny z ID folderu używanego przez DVC):**  
  Ten błąd oznacza, że DVC (używając Konta Usługi) nie może znaleźć folderu na Google Drive o podanym ID (`1OSSSo35ObNdt5Hf5kLAZTf1QXyhoFoZ4`) lub nie ma do niego dostępu.  
  - Skontaktuj się z administratorem (Przemek), aby potwierdzić, że ID folderu zdalnego magazynu DVC jest poprawne.  
  - Administrator musi również upewnić się, że Konto Usługi (którego `client_email` znajduje się w Twoim pliku klucza JSON) zostało udostępnione do folderu Google Drive (`1OSSSo35ObNdt5Hf5kLAZTf1QXyhoFoZ4`) z uprawnieniami "Edytor" (Editor).

## 4. Alternatywna konfiguracja DVC z Google Drive (Metoda: OAuth 2.0)

Użyj tej metody tylko jeśli została jawnie wskazana przez administratora projektu i problemy z konfiguracją Klienta OAuth "ASI DVC" (lub podobnego, używanego przez zespół) zostały rozwiązane (m.in. kwestia trybu testowania aplikacji OAuth i poprawności autoryzowanych URI przekierowania).

W tej metodzie każdy użytkownik autoryzuje DVC indywidualnie poprzez swoje konto Google.

### Wymagania wstępne i klonowanie repozytorium
Jak w punktach 1 i 2 powyżej.

### Pierwsza interakcja z DVC wymagająca dostępu do remotu
Gdy po raz pierwszy uruchomisz komendę taką jak:

```bash
dvc pull -r mygdrive
```

lub

```bash
dvc push -r mygdrive
```

DVC automatycznie otworzy Twoją domyślną przeglądarkę internetową.

### Autoryzacja w przeglądarce
1. Zaloguj się na swoje konto Google (to, któremu udostępniono folder projektu na Google Drive).  
2. Pojawi się ekran zgody OAuth proszący o zezwolenie aplikacji (np. "ASI DVC" lub innej skonfigurowanej przez zespół) na dostęp do Twojego Dysku Google. Udziel tej zgody.  
3. Po pomyślnej autoryzacji przeglądarka może wyświetlić komunikat o sukcesie, a DVC w terminalu powinno kontynuować operację.

### Pobierz dane projektu

```bash
dvc pull -r mygdrive
```

### Rozwiązywanie problemów (dla metody OAuth 2.0)

- **Błąd "Aplikacja [...] nie przeszła procesu weryfikacji... dostępna tylko dla testerów...":**  
  Skontaktuj się z administratorem (Przemek). Musi on dodać Twój adres e-mail Google do listy "Użytkowników testowych" dla aplikacji OAuth używanej przez zespół w Google Cloud Console.

- **Błąd `invalid_clientUnauthorized`:**  
  Ten błąd wskazuje na problem z konfiguracją samego Klienta OAuth 2.0 w Google Cloud Console (prawdopodobnie brakujące lub niepoprawne "Autoryzowane identyfikatory URI przekierowania" jak `http://localhost:8080/`). Problem ten musi naprawić administrator w Google Cloud Console.

- **Inne błędy autoryzacji:**  
  Spróbuj wyczyścić zapisane poświadczenia DVC dla Google Drive, aby wymusić ponowną autoryzację. Tokeny są zwykle przechowywane w `~/.cache/pydrive2fs/` (Linux/macOS) lub `%LOCALAPPDATA%\pydrive2fs\` (Windows). Usuń odpowiedni plik/folder powiązany z używanym `client_id` i spróbuj ponownie.

## 5. Podstawowy cykl pracy z DVC

### Pobieranie najnowszych danych

```bash
dvc pull -r mygdrive
```

### Dodawanie nowych lub zmodyfikowanych plików danych/modeli do śledzenia przez DVC

```bash
dvc add sciezka/do/twoich/danych_lub_modelu
```

Np.:

```bash
dvc add data/01_raw/nowe_dane.csv
dvc add models/model.pkl
```

### Commitowanie zmian do Gita
Pamiętaj, aby dodać do Gita pliki `.dvc` (utworzone lub zmodyfikowane przez `dvc add`) oraz ewentualne zmiany w `.dvcignore`:

```bash
git add sciezka/do/twoich/danych_lub_modelu.dvc .dvcignore
git commit -m "Opis zmian w danych/modelu"
```

### Wysyłanie danych na zdalny magazyn

```bash
dvc push -r mygdrive
```

## 6. Wsparcie

W razie problemów z konfiguracją DVC lub jego działaniem, skontaktuj się z Przemkiem (wstaw tutaj e-mail Przemka lub inny preferowany kontakt).

import os
import subprocess
import sys


def run_command(command, check_success=True):
    """Pomocnicza funkcja do uruchamiania komend i sprawdzania sukcesu."""
    print(f"Wykonuję komendę: {' '.join(command)}")
    try:
        result = subprocess.run(
            command, check=True, capture_output=True, text=True, shell=False
        )
        print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Błąd podczas wykonywania komendy: {e}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        if check_success:
            sys.exit(1)
        return False
    except FileNotFoundError:
        print(f"Błąd: Komenda '{command[0]}' nie została znaleziona.")
        print("Upewnij się, że DVC jest zainstalowane i dostępne w PATH.")
        if check_success:
            sys.exit(1)
        return False


def setup_dvc_gdrive(json_key_path):
    normalized_path = os.path.abspath(os.path.normpath(json_key_path))

    print("Konfigurowanie DVC dla zdalnego 'mygdrive' z użyciem konta usługi...")
    print(f"Ścieżka do klucza JSON: {normalized_path}")

    # Komenda 1
    cmd1 = [
        "dvc",
        "remote",
        "modify",
        "mygdrive",
        "gdrive_use_service_account",
        "true",
        "--local",
    ]
    if not run_command(cmd1):
        print("Wystąpił błąd podczas pierwszej komendy DVC.")
        return

    # Komenda 2
    cmd2 = [
        "dvc",
        "remote",
        "modify",
        "mygdrive",
        "--local",
        "gdrive_service_account_json_file_path",
        normalized_path,
    ]
    if not run_command(cmd2):
        print("Wystąpił błąd podczas drugiej komendy DVC.")
        return

    print("DVC zostało pomyślnie skonfigurowane.")
    print("Możesz teraz uruchomić 'dvc pull', aby pobrać dane.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Błąd: Nie podano ścieżki do pliku JSON z kluczem konta usługi Google Drive."
        )
        print(
            "Użycie: python setup_dvc.py /sciezka/do/TWOJEGO_KLUCZA_KONTA_USLUGI.json"
        )
        sys.exit(1)

    json_key_path_arg = sys.argv[1]

    if not os.path.isfile(json_key_path_arg):
        print(f"Błąd: Podany plik JSON nie istnieje: {json_key_path_arg}")
        print("Upewnij się, że ścieżka jest poprawna.")
        sys.exit(1)

    setup_dvc_gdrive(json_key_path_arg)

# --- Etap 1: "Builder" - Przygotowanie zależności ---
# Ten etap służy do zbudowania "kół" (wheels) z zależnościami, co przyspiesza instalację
# i pozwala na mniejszy obraz finalny, ponieważ nie zostawiamy w nim pamięci podręcznej pip.
FROM python:3.11-slim AS builder

# Deklarujemy argument, który będzie przekazany z workflow. Nie jest tu używany, ale
# dobra praktyka to deklarowanie go w każdym etapie, w którym jest potrzebny.
ARG LATEST_MODEL_DIR

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Kopiujemy tylko plik z wymaganiami. Ścieżka jest względna do kontekstu budowania (głównego katalogu repo).
COPY asi-project/requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- Etap 2: Finalny obraz aplikacji ---
# Zaczynamy od nowa z czystym obrazem, aby był jak najmniejszy.
FROM python:3.11-slim

# Ponownie deklarujemy argument, aby był dostępny w tym etapie.
# To jest kluczowe dla dynamicznego kopiowania modelu.
ARG LATEST_MODEL_DIR

WORKDIR /app

# Tworzenie użytkownika bez uprawnień roota - dobra praktyka bezpieczeństwa
RUN useradd --create-home appuser
# Dalsze komendy będą domyślnie uruchamiane jako ten użytkownik
USER appuser

# Kopiujemy gotowe "koła" (wheels) i listę wymagań z etapu "builder"
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# --- Kopiowanie plików aplikacji ---
# Wszystkie ścieżki źródłowe są względne do kontekstu budowania (głównego katalogu repo).
# Ścieżki docelowe są względne do WORKDIR (/app) w kontenerze.
COPY asi-project/streamlit_app/ ./streamlit_app/
COPY asi-project/src/ ./src/
COPY asi-project/conf/ ./conf/

# Kopiujemy TYLKO najnowszy folder z modelem, używając przekazanego argumentu.
# To jest serce optymalizacji, którą wdrożyliśmy w workflow.
COPY asi-project/AutogluonModels/${LATEST_MODEL_DIR} ./AutogluonModels/

# Instalujemy zależności z przygotowanych "kół"
RUN pip install --no-cache /wheels/*

# Ustawiamy port, na którym nasłuchuje aplikacja Streamlit
EXPOSE 8501

# Zmieniamy właściciela wszystkich plików na naszego użytkownika bez uprawnień roota.
# Musimy na chwilę wrócić na 'root', żeby móc użyć 'chown'.
USER root
RUN chown -R appuser:appuser /app
# I od razu wracamy do bezpiecznego użytkownika 'appuser'.
USER appuser

# Komenda uruchamiająca aplikację
CMD ["/home/appuser/.local/bin/streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
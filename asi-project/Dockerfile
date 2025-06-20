# --- Etap 1: "Builder" - Przygotowanie wszystkich zależności ---
    FROM python:3.11-slim AS builder

    ARG LATEST_MODEL_DIR
    ENV PYTHONUNBUFFERED=1
    WORKDIR /app
    
    COPY asi-project/requirements.txt ./
    
    # ZMIANA: Usunęliśmy flagę --no-deps.
    # Teraz pip wheel pobierze i zbuduje "koła" dla pakietów z requirements.txt ORAZ dla wszystkich ich zależności.
    RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt
    
    
    # --- Etap 2: Finalny obraz aplikacji ---
    FROM python:3.11-slim
    
    ARG LATEST_MODEL_DIR
    WORKDIR /app
    
    RUN useradd --create-home appuser
    USER appuser
    
    # Kopiujemy gotowe "koła" i listę wymagań z etapu "builder"
    COPY --from=builder /app/wheels /wheels
    COPY --from=builder /app/requirements.txt .
    
    # Kopiowanie plików aplikacji - bez zmian
    COPY asi-project/streamlit_app/ ./streamlit_app/
    COPY asi-project/src/ ./src/
    COPY asi-project/conf/ ./conf/
    COPY asi-project/AutogluonModels/${LATEST_MODEL_DIR} ./AutogluonModels/
    RUN ls -l ./AutogluonModels/
    RUN find ./AutogluonModels
    
    # ZMIANA: Używamy teraz bardziej niezawodnej metody instalacji.
    # --no-index mówi pip, aby nie łączył się z internetowym indeksem pakietów (PyPI).
    # --find-links=/wheels mówi pip, aby szukał pakietów wyłącznie w naszym lokalnym folderze /wheels.
    # Instalujemy pakiety na podstawie oryginalnego pliku requirements.txt.
    RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt
    
    EXPOSE 8501
    
    USER root
    RUN chown -R appuser:appuser /app
    USER appuser
    
    CMD ["/home/appuser/.local/bin/streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
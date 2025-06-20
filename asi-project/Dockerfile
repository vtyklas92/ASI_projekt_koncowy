FROM python:3.11-slim AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt ./
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Tworzenie użytkownika bez uprawnień roota - bezpieczeństwo
RUN useradd --create-home appuser
USER appuser

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Kopiujemy całą aplikację, w tym modele i kod źródłowy
COPY streamlit_app/app.py ./streamlit_app/app.py
COPY AutogluonModels ./AutogluonModels
COPY src ./src
COPY conf ./asi-project/conf
# Jeśli masz assets, odkomentuj poniżej:
# COPY assets ./assets/

RUN pip install --no-cache /wheels/*

EXPOSE 8501

USER root
RUN chown -R appuser:appuser /app
USER appuser

CMD ["/home/appuser/.local/bin/streamlit", "run", "streamlit_app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]
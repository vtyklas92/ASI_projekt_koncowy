FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app
COPY streamlit_app/app.py /app
ADD AutogluonModels /app/AutogluonModels

RUN pip install  --upgrade pip \
 && pip install  --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]
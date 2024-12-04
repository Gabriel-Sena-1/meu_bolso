# Dockerfile para a API FastAPI

FROM python:3.12-slim

# Instalar dependências necessárias
WORKDIR /meu_bolso-api

COPY ./requirements.txt /meu_bolso-api/requirements.txt

RUN pip install --no-cache-dir -r /meu_bolso-api/requirements.txt

# Copiar o código da API para o container
COPY . /app

# Expor a porta 8000 e rodar o aplicativo
EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

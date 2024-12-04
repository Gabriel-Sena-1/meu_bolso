FROM python:3.12

WORKDIR /app

# Copiar apenas os arquivos da API
COPY ./meu_bolso-api /app

# Instalar dependências
RUN pip install -r requirements.txt

# Expor a porta da aplicação
EXPOSE 8000

# Comando para iniciar o app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]

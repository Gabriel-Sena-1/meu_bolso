FROM python:3.11

WORKDIR /app

# Copiar os arquivos do projeto
COPY . /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta da aplicação
EXPOSE 8000

# Criar script de inicialização
RUN echo "#!/bin/sh\n\
python manage.py migrate\n\
python manage.py collectstatic --noinput\n\
gunicorn meu_bolso.wsgi:application --bind 0.0.0.0:8000" > /app/start.sh

RUN chmod +x /app/start.sh

# Comando para iniciar o app
CMD ["/app/start.sh"]
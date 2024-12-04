FROM python:3.11

WORKDIR /app

# Copiar primeiro só o requirements para aproveitar o cache do Docker
COPY ./meu_bolso-api/requirements.txt /app/

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copiar o resto dos arquivos do projeto
COPY ./meu_bolso-api /app/

# Expor a porta da aplicação
EXPOSE 8000

# Criar script de inicialização
RUN echo '#!/bin/bash\n\
python manage.py migrate\n\
python manage.py collectstatic --noinput\n\
exec gunicorn meu_bolso.wsgi:application --bind 0.0.0.0:8000' > /app/start.sh

RUN chmod +x /app/start.sh

# Comando para iniciar o app
CMD ["/bin/bash", "/app/start.sh"]
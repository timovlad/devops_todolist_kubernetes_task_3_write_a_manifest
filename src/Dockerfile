FROM  python:3.8-slim
WORKDIR /app
COPY . .
EXPOSE 8080
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations && python manage.py migrate

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
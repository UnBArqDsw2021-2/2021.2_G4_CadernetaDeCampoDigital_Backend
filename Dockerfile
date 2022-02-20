FROM python:3
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /var/www
COPY . /var/www

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.9-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 6123
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:6123", "-t", "0", "app:app"]

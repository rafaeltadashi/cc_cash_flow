FROM python:3.9

ARG TARGET_REQ

WORKDIR /app

COPY ${TARGET_REQ}.txt .
RUN pip install --no-cache-dir -r ${TARGET_REQ}.txt

COPY . .

EXPOSE 8081
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
FROM bitnami/python

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8888

CMD ["uvicorn", "vista:app", "--host","0.0.0.0", "--port", "8000", "--reload"]
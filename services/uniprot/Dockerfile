FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py datareader.py ./
COPY data/uniprot.fasta data/uniprot.fasta

EXPOSE 8000

ENTRYPOINT ["python3", "main.py"]

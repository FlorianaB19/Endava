# Imagine oficială Python
FROM python:3.12-slim

# Directorul de lucru din container
WORKDIR /app

# Copiem fișierul cu dependențe
COPY requirements.txt .

# Instalăm bibliotecile
RUN pip install --no-cache-dir -r requirements.txt

# Copiem întreg proiectul
COPY . .

# Comanda executată la pornirea containerului
CMD ["python", "main.py"]
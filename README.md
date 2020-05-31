# Projekt_statystyka

Aby uruchomić projekt w Dockerze należy:
1. W wierszu poleceń upewnić się, że znajdujemy się w katalogu projektu.
2. W wierszu poleceń wprowadzić następujące komendy:

docker build -t statystyka_projekt:latest .

docker run -p 5000:5000 statystyka_projekt:latest

3. Wpisać w pasku adresu przelądarki http://127.0.0.1:5000/

# Wedding Tables Optimizer 🎊

Nowoczesna aplikacja webowa do optymalizacji rozmieszczenia gości przy stolikach weselnych w oparciu o macierz relacji między gośćmi.

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> **Historia projektu:** Ten kod został użyty do zoptymalizowania stolików weselnych na prawdziwym weselu!
> Szczegóły w rozdziale "Guest Seating Optimization for Weddings" w [tej książce](https://www.google.pl/books/edition/Narz%C4%99dzia_analityczne_teoria_i_zastosow/M7_QEAAAQBAJ?hl=pl&gbpv=0).

<img width="474" alt="Original visualization" src="https://github.com/user-attachments/assets/67eb9ade-0301-4802-9598-8a62afc893fa" />

---

## 📋 Spis treści

- [Funkcje](#-funkcje)
- [Demo](#-demo)
- [Technologie](#-technologie)
- [Instalacja](#-instalacja)
- [Użycie](#-użycie)
- [Jak działa algorytm](#-jak-działa-algorytm)
- [API](#-api)
- [Rozwój](#-rozwój)
- [Licencja](#-licencja)

## ✨ Funkcje

### 🎯 Główne możliwości
- **Macierz relacji** - Intuicyjny edytor do definiowania relacji między gośćmi
- **Automatyczna optymalizacja** - Algorytm stochastyczny maksymalizujący satysfakcję gości
- **Wizualizacja stolików** - Przejrzysta prezentacja rozmieszczenia z oceną każdego stolika
- **Edycja manualna** - Drag & drop do ręcznego dostosowania miejsc
- **Wykres postępu** - Wizualizacja procesu optymalizacji w czasie rzeczywistym
- **Import/Export** - Zapisywanie i wczytywanie danych gości w formacie JSON

### 🎨 Interfejs
- Nowoczesny, responsywny design z TailwindCSS
- Dwie główne zakładki:
  - **Macierz Relacji** - zarządzanie gośćmi i ich relacjami
  - **Stoliki** - wizualizacja i optymalizacja rozmieszczenia
- Intuicyjna kolorystyka wskazująca jakość relacji
- Wskaźniki jakości dla każdego stolika

## 🎬 Demo

### Zakładka: Macierz Relacji
Edytor pozwala na:
- Dodawanie/usuwanie gości
- Klasyfikację gości (rodzina/znajomi)
- Definiowanie relacji między każdą parą gości
- Konfigurację parametrów optymalizacji

### Zakładka: Stoliki
Wizualizacja umożliwia:
- Uruchomienie automatycznej optymalizacji
- Podgląd wyniku dla każdego stolika
- Wykres postępu optymalizacji
- Ręczne przesuwanie gości między stolikami (drag & drop)

## 🛠 Technologie

### Backend
- **FastAPI** 0.109.0 - Nowoczesny framework API
- **NetworkX** 3.2.1 - Reprezentacja grafowa relacji
- **NumPy** 1.26.3 - Obliczenia numeryczne
- **Pandas** 2.2.0 - Manipulacja danych

### Frontend
- **React** 18.2 - Biblioteka UI
- **Vite** 5.0 - Narzędzie budowania
- **TailwindCSS** 3.4 - Stylowanie
- **Recharts** 2.10 - Wykresy
- **React DnD** 16.0 - Drag and drop
- **Axios** - Komunikacja HTTP

### DevOps
- **Docker** & **Docker Compose** - Konteneryzacja
- **Nginx** - Serwer www dla frontendu

## 📦 Instalacja

### Metoda 1: Docker (Zalecana)

1. **Klonuj repozytorium**
```bash
git clone https://github.com/tomWitkowski/Wedding-Tables-Optimizer.git
cd Wedding-Tables-Optimizer
```

2. **Uruchom z Docker Compose**
```bash
docker-compose up --build
```

3. **Otwórz przeglądarkę**
```
http://localhost
```

Backend API dostępne pod: `http://localhost:8000`

### Metoda 2: Manualna instalacja

#### Backend

```bash
cd api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend dostępny pod: `http://localhost:3000`

## 🚀 Użycie

### 1. Dodaj gości

W zakładce **Macierz Relacji**:
1. Wprowadź imię i nazwisko gościa
2. Wybierz kategorię (Rodzina/Znajomi)
3. Kliknij "Dodaj"

### 2. Zdefiniuj relacje

1. Wybierz gościa z listy
2. Dla każdego innego gościa ustaw wartość relacji:
   - **10** - Para (muszą siedzieć razem)
   - **2-9** - Dobrzy przyjaciele
   - **0.5-2** - Znajomi
   - **0** - Neutralna relacja
   - **Wartości ujemne** - Konflikt (lepiej nie sadzać razem)

### 3. Skonfiguruj parametry

- **Maks. miejsc przy stoliku** - Ile osób może usiąść przy jednym stoliku
- **Kara za mieszanie rodziny/znajomych** - Wartość ujemna (np. -3)
- **Liczba iteracji** - Więcej = lepsza optymalizacja, ale dłużej trwa

### 4. Uruchom optymalizację

Przejdź do zakładki **Stoliki** i kliknij **Uruchom Optymalizację**.

### 5. Dostosuj ręcznie (opcjonalnie)

Przeciągnij gości między stolikami, aby dostosować rozmieszczenie do swoich potrzeb.

### 6. Eksportuj dane

Zapisz konfigurację gości za pomocą przycisku **Eksportuj dane**.

## 🧮 Jak działa algorytm?

### Reprezentacja problemu
- Goście = wierzchołki grafu
- Relacje = krawędzie z wagami
- Cel: maksymalizacja średniej relacji w każdym stoliku

### Algorytm optymalizacji

Stosujemy **stochastyczne wspinanie się** (stochastic hill climbing):

1. **Inicjalizacja**: Losowe rozmieszczenie gości
2. **Iteracja** (powtarzana N razy):
   - Generowanie 100 wariantów przez wymianę 2-4 osób między stolikami
   - Generowanie 100 wariantów przez przenoszenie 1-2 osób do najmniej zapełnionego stolika
   - Ocena wszystkich 201 konfiguracji
   - Wybór najlepszej konfiguracji
3. **Wynik**: Najlepsze znalezione rozmieszczenie

### Funkcja oceny

Dla każdego stolika:
```
wynik_stolika = suma_relacji_par / liczba_gości
```

Wynik całkowity:
```
wynik = średnia(wyniki_stolików)
```

### Automatyczne kary

System automatycznie dodaje karę (domyślnie -3) za posadzenie rodziny ze znajomymi przy tym samym stoliku.

## 📡 API

### Endpoint optymalizacji

**POST** `/api/`

#### Request Body
```json
[
  {
    "person_id": 0,
    "state": "f",
    "relations": {
      "1": 10.0,
      "2": 2.0
    }
  }
]
```

#### Query Parameters
- `max_seats` (int, default: 10) - Maksymalna liczba miejsc przy stoliku
- `family_friends_not_score` (float, default: -3.0) - Kara za mieszanie grup
- `iterations` (int, default: 200) - Liczba iteracji
- `seats` (array, optional) - Początkowe rozmieszczenie

#### Response
```json
{
  "tables": [[0, 1, 2], [3, 4, 5]],
  "tables_scores": [2.5, 1.8],
  "score_history": [0.5, 0.8, 1.2, ...]
}
```

### Dokumentacja interaktywna

FastAPI automatycznie generuje dokumentację:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 💻 Rozwój

### Struktura projektu

```
Wedding-Tables-Optimizer/
├── api/                          # Backend FastAPI
│   ├── main.py                   # Endpoint API
│   ├── core.py                   # Algorytm optymalizacji
│   ├── api_models.py             # Modele Pydantic
│   ├── utils.py                  # Funkcje pomocnicze
│   ├── requirements.txt          # Zależności Python
│   └── Dockerfile                # Kontener backend
├── frontend/                     # Frontend React
│   ├── src/
│   │   ├── components/           # Komponenty React
│   │   ├── pages/                # Strony aplikacji
│   │   ├── utils/                # Funkcje pomocnicze
│   │   ├── types/                # Typy TypeScript
│   │   ├── App.jsx               # Główny komponent
│   │   └── main.jsx              # Entry point
│   ├── package.json              # Zależności Node.js
│   └── Dockerfile                # Kontener frontend
└── docker-compose.yml            # Orkiestracja kontenerów
```

### Uruchomienie w trybie deweloperskim

#### Backend z hot reload
```bash
cd api
uvicorn main:app --reload --port 8000
```

#### Frontend z hot reload
```bash
cd frontend
npm run dev
```

### Testowanie

Backend:
```bash
cd api
pytest
```

Frontend:
```bash
cd frontend
npm test
```

## 🐛 Rozwiązywanie problemów

### Problem: Backend nie startuje
- Sprawdź czy port 8000 jest wolny: `lsof -i :8000`
- Upewnij się, że wszystkie zależności są zainstalowane: `pip install -r requirements.txt`

### Problem: Frontend nie łączy się z backendem
- Sprawdź czy backend działa: `curl http://localhost:8000/`
- Zweryfikuj CORS w `api/main.py`
- Sprawdź konfigurację proxy w `frontend/vite.config.js`

### Problem: Docker nie buduje się
- Upewnij się, że Docker jest uruchomiony: `docker --version`
- Wyczyść cache: `docker-compose down -v`
- Przebuduj: `docker-compose up --build --force-recreate`

## 📝 Przykładowe dane

W katalogu `api/` znajduje się plik `example_relations_request.json` zawierający rzeczywiste dane z wesela (87 gości). Możesz go użyć jako punktu wyjścia.

## 🤝 Wkład

Zapraszamy do współpracy! Proszę:
1. Forkuj projekt
2. Stwórz branch feature (`git checkout -b feature/AmazingFeature`)
3. Commituj zmiany (`git commit -m 'Add some AmazingFeature'`)
4. Pushuj do brancha (`git push origin feature/AmazingFeature`)
5. Otwórz Pull Request

## 📄 Licencja

Projekt udostępniony na licencji MIT. Zobacz plik `LICENSE` dla szczegółów.

## 👨‍💻 Autor

**Tomasz Witkowski**

- GitHub: [@tomWitkowski](https://github.com/tomWitkowski)

## 🙏 Podziękowania

Projekt powstał jako praktyczne rozwiązanie problemu optymalizacji stolików weselnych i został opisany w książce "Narzędzia analityczne - teoria i zastosowania".

---

**Miłego organizowania wesela! 🎉**

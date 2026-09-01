# DEFA — Django backend

API de base pour DEFA — Finance Responsable.

## Démarrage local

```bash
cd backend
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows
# .venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

API : `http://127.0.0.1:8000/api/`
Admin : `http://127.0.0.1:8000/admin/`
Health : `http://127.0.0.1:8000/api/health/`

## Docker

Depuis la racine :

```bash
docker compose up --build
```

## API principale

- `GET /api/health/`
- `GET /api/me/`
- `/api/profiles/`
- `/api/addresses/`
- `/api/employment/`
- `/api/businesses/`
- `/api/references/`
- `/api/applications/`
- `POST /api/applications/{id}/submit/`
- `POST /api/applications/{id}/decision/`
- `/api/loans/`
- `/api/payments/`

Le moteur de score est indicatif. La décision de crédit doit rester contrôlée par un opérateur autorisé.

# Since API

Backend API for [Since](https://since.amirhossein.info).

## API

Production API at [api.since.amirhossein.info](https://api.since.amirhossein.info)

## Documentation

- Swagger: [api.since.amirhossein.info/docs](https://api.since.amirhossein.info/docs)
- ReDoc: [api.since.amirhossein.info/redoc](https://api.since.amirhossein.info/redoc)

## Development

### Requirements

- Python 3.14
- UV
- PostgreSQL

### Setup

```bash
git clone https://github.com/BlackIQ/since-backend
cd since-backend

uv sync
```

Copy the `.env.example` file to `.env` then set variables.

Run migrations:

```bash
alembic upgrade head
```

Start the development server:

```bash
uv run fastapi dev
```

The API will be available at [localhost:8000](http://localhost:8000)

---

[Amirhossein Mohammadi](https://amirhossein.info) - Aug 17

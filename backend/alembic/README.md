# Alembic Migrations

This directory contains database migrations managed by Alembic.

## Running Migrations

To run the migrations and bring the database up to date, execute the following command after setting the `DATABASE_URL` environment variable:

```bash
alembic upgrade head
```

# Hybrid-Learning-Hub
physical (bricks &amp; mortal) and online digital learning hub

1. alembic revision --autogenerate -m "create_main_tables"
2. alembic upgrade head - whenever you update the table
3. alembic downgrade -1 - to rollback 1 migration step
4. docker-compose exec postgres_db psql -h localhost -U postgres --dbname=postgres

- \l - list all databases
- \d+ - list all tables (relations) in the current database
- \dT+ - list all enums in the current database
- \c postgres - connect to the postgres database
- \d users - describe the users table and the associated columns

- openssl rand -hex 32
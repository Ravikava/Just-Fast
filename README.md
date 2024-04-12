
## to initiate migrations
alembic init alembic

## to generate migration file
alembic revision --autogenerate -m "Your migration message"

## to migrate
alembic upgrade head


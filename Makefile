.DEFAULT_GOAL := help


run:
	poetry run gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker -c gunicorn.conf.py

install:
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)


unistall:
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)


migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)


migrate-apply:
	alembic upgrade head

help:
	@echo "Usage: make [command]"
	@echo ""
	@echo "Command"
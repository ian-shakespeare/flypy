VENV_DIR := venv

setup: requirements.txt
	@python3 -m venv $(VENV_DIR)
	@./$(VENV_DIR)/bin/pip install -r requirements.txt

.PHONY: setup

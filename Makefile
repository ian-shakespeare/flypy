VENV_DIR := venv

setup: requirements.txt
	@python3 -m venv $(VENV_DIR)
	@./$(VENV_DIR)/bin/pip install -r requirements.txt

example:
	@./$(VENV_DIR)/bin/python ./flypy/main.py -o LAX -d NRT -D 2024-03-09

test:
	@./$(VENV_DIR)/bin/python -m unittest discover .

.PHONY: setup example test

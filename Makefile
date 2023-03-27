.PHONY: clean lint 
.DEFAULT_GOAL := help

PYTHON := .venv/bin/python
LINTER := black

# Show help
help:
	@echo "——————————————————————————————————————————————"
	@echo " Usage: make [options]"
	@echo " Options:"
	@echo "   help:      Show this help message and exit."
	@echo "   clean:     Clean up the project."
	@echo "   lint:      Prettify the source code."
	@echo "——————————————————————————————————————————————"

# Clean up
clean:
	find . -name "__pycache__" -exec rm -fr {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete

# Prettify the source code
lint:
	$(LINTER) .

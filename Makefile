.PHONY: all
all: clean-result result.png

.PHONY: .venv
.venv: .venv/touchfile
.venv/touchfile: requirements.txt
	@echo "Creating virtual environment..."
	@python3.11 -m venv .venv
	@echo "Upgrading pip..."
	@.venv/bin/pip install --upgrade pip
	@echo "Installing dependencies..."
	@.venv/bin/pip install -r requirements.txt

	@touch .venv/touchfile

result.png: .venv
	@echo "Running simulation..."
	@.venv/bin/python simulation.py && echo "Generated result.png"

clean-result:
	@if [ -f result.png ]; then \
		echo "Cleaning result.png..."; \
		rm -rf result.png; \
	fi

clean: clean-result
	@echo "Cleaning virtual environment..."
	@rm -rf .venv
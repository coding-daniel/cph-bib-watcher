.PHONY: venv run freeze clean

venv:
	@echo "📦 Creating virtual environment and installing requirements..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt || pip install requests beautifulsoup4

run:
	@echo "🚀 Running bib checker..."
	. venv/bin/activate && python3 checker.py

freeze:
	@echo "📌 Freezing installed packages to requirements.txt..."
	. venv/bin/activate && pip freeze > requirements.txt

clean:
	@echo "🧹 Removing virtual environment and cache..."
	rm -rf venv __pycache__ *.pyc

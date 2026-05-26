.PHONY: verify demo validate-data validate-ontology build-cases evaluate report test clean

PYTHON ?= python3

verify: clean demo test

demo:
	$(PYTHON) -m policy_ax.cli demo

validate-data:
	$(PYTHON) -m policy_ax.cli validate-data

validate-ontology:
	$(PYTHON) -m policy_ax.cli validate-ontology

build-cases:
	$(PYTHON) -m policy_ax.cli build-cases

evaluate:
	$(PYTHON) -m policy_ax.cli evaluate

report:
	$(PYTHON) -m policy_ax.cli report

test:
	$(PYTHON) -m unittest discover -s tests -v

clean:
	rm -f data/processed/evaluation_cases.json
	rm -f reports/sample_poc_report.md

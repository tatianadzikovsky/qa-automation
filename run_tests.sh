#!/bin/bash
# run_tests.sh
source .venv/bin/activate
python -m pytest -v -s tests --html=report.html --self-contained-html
open report.html   # 👈 auto-open report after run

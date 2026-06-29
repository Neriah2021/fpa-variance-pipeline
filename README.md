# FPA Variance and Forecasting Pipeline

An end-to-end financial planning and analysis pipeline that automates budget vs actuals monitoring, variance flagging, and executive reporting. Built with Python, dbt, BigQuery, and Streamlit.

---

## Overview

Finance teams spend significant time each month comparing planned budgets against actual spend, identifying problem areas, and producing reports for leadership. This project automates that entire workflow, from raw data ingestion through to a live dashboard and formatted Excel report, using the same tools and architecture found in modern data engineering environments.

The pipeline covers 3 years of monthly data across 6 departments and 4 cost categories for a fictional company called Meridian Corp.

---

## Architecture

Raw CSV -> BigQuery -> dbt (3 transformation layers) -> Streamlit dashboard + Excel report

---

## dbt Pipeline

Three-layer transformation following analytics engineering best practices:

- Staging: cleans and renames raw data, computes variance amount and percentage per row
- Intermediate: aggregates by department and month
- Mart: final P&L summary with automated budget status flags (Over Budget, Under Budget, On Track)

---

## Features

- Automated variance analysis that flags any department more than 10% off budget
- Interactive Streamlit dashboard with year and department filters, budget vs actuals charts, variance trend line, and flagged items table
- Multi-tab formatted Excel report generated with openpyxl, ready to share with finance leadership
- Full dbt project with source definitions, ref() patterns, and modular SQL models

---

## Tech Stack

Python, SQL, dbt, Google BigQuery, Streamlit, Plotly, openpyxl, pandas

---

## How to Run

1. Clone the repository
2. Set up a Python 3.12 virtual environment and install dependencies
3. Authenticate with Google Cloud: gcloud auth application-default login
4. Generate data: python generate_data.py
5. Run dbt pipeline: cd fpa_pipeline && dbt run
6. Run variance analysis: python variance_analysis.py
7. Launch dashboard: streamlit run app.py

---

## Project Context

Built to demonstrate how modern data engineering tools can replace manual finance workflows at scale. The monthly budget vs actuals process that finance teams run in Excel can be fully automated through a structured data pipeline, with variance detection, status flagging, and formatted reporting handled end to end without manual intervention. The architecture follows the same layered approach used by data teams at high-growth technology and finance companies, with a clear separation between ingestion, transformation, and the presentation layer.

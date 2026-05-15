# Snowflake Executive Sales Analytics Dashboard

## Project Overview
Built an end-to-end Snowflake analytics platform using Bronze/Silver/Gold architecture with automated CDC pipelines using Streams, Tasks, and MERGE operations.

Developed an interactive Streamlit dashboard powered by Snowpark SQL queries for:
- Revenue trends
- Customer analytics
- KPI monitoring
- Sales reporting

---

## Technologies Used
- Snowflake
- Snowpark
- Streamlit
- Python
- SQL
- CDC Pipelines
- Streams & Tasks

---

## Features
- Incremental data processing
- Automated Snowflake Tasks
- Interactive dashboard filters
- KPI cards
- Revenue trend analysis
- Customer analytics

---

## Dashboard Preview
<img width="1250" height="233" alt="KPI Cards" src="https://github.com/user-attachments/assets/787670fa-eca3-46f1-89e4-db0b7ce77caa" />
<img width="1340" height="458" alt="Chart 1, 2" src="https://github.com/user-attachments/assets/0020c300-c5e4-4a2e-aaaa-bfe9adca1ba8" />
<img width="1330" height="491" alt="Chart 3,4" src="https://github.com/user-attachments/assets/b43b1515-496b-4f9c-8f0c-4a338efbbae0" />
<img width="1331" height="432" alt="Chart 5" src="https://github.com/user-attachments/assets/cd71b868-2114-4e14-acfb-d3075c4481ee" />
<img width="283" height="615" alt="Sidebar" src="https://github.com/user-attachments/assets/5ca1296f-0f48-405f-8217-1d00b1c2bd25" />
<img width="399" height="650" alt="pipeline_architecture" src="https://github.com/user-attachments/assets/e40bb90d-c170-4bda-b8ac-174f4c66b65b" />







---

## Architecture

Raw Data
↓
Bronze Layer
↓
Streams + Tasks
↓
Silver Layer
↓
Gold Analytics
↓
Snowpark
↓
Streamlit Dashboard

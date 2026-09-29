# Automated Report Generation

## Objective
Read data from a CSV file, analyze it, and automatically generate a formatted PDF report using Python and ReportLab.

## Files
- `report_generator.py` — main automation script
- `data.csv` — sample input data
- `sample_report.pdf` — sample generated report
- `requirements.txt` — dependency
- `README.md` — project documentation

## Run
```bash
pip install -r requirements.txt
python report_generator.py
```

The script reads `data.csv` and creates `sample_report.pdf`.

## Analysis Included
- Total records
- Average score
- Highest score
- Lowest score
- Status distribution
- Course distribution
- Detailed records table

## Input Format
The CSV should contain:
`ID, Name, Course, Status, Score`

## Technologies
Python, CSV/file handling, statistics, collections, ReportLab, PDF automation.

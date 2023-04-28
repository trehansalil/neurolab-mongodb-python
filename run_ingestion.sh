pip install -r requirements.txt

python ingestion.py sheet_name=procedure_risk > logs/procedure_risk_ingestion.log 2>&1&
python ingestion.py sheet_name=sun_sensitivity > logs/sun_sensitivity_ingestion.log 2>&1&
python ingestion.py sheet_name=hq > logs/hq_ingestion.log 2>&1&
python ingestion.py sheet_name=retinol > logs/retinol_ingestion.log 2>&1&
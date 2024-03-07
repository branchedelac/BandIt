#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn bandit.api.app:app

run_streamlit:
	-@streamlit run user_interface/app.py

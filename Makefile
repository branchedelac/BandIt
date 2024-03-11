#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn backend.api.app:app

run_streamlit:
	-@streamlit run frontend/app.py

run_preprocecss:
	python -c 'from backend.model_training.main import preprocess; preprocess()'

run_train:
	python -c 'from backend.model_training.main import train; train()'

run_evaluate:
	python -c 'from backend.model_training.main import evaluate; evaluate()'

#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn bandit.api.app:app

run_streamlit:
	-@streamlit run user_interface/app.py

run_preprocecss:
	python -c 'from bandit.model_training.main import preprocess; preprocess()'

run_train:
	python -c 'from bandit.model_training.main import train; train()'

run_evaluate:
	python -c 'from bandit.model_training.main import evaluate; evaluate()'

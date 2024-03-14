#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn backend.api.app:app

run_streamlit:
	-@streamlit run frontend/app.py

run_preprocecss:
	python -c 'from backend.main import preprocess; preprocess()'

run_train:
	python -c 'from backend.main import train; train()'

run_evaluate:
	python -c 'from backend.main import evaluate; evaluate()'

run_predict_with_pop2piano:
	python -c 'from backend.main import predict_with_pop2piano; predict_with_pop2piano("data/Janis_Joplin_-_Piece_Of_My_Heart.mid")'

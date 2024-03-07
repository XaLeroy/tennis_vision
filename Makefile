.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn api.fast_api:app host= 0.0.0.0 port=8000

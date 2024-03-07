.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn api.fast_api:app --reload

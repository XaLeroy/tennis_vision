.DEFAULT_GOAL := default
#################### PACKAGE ACTIONS ###################
run_api:
	uvicorn fast_api:app --reload

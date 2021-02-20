PYTHON = python3

.PHONY = help, install-tools, vsopc

.DEFAULT-GOAL = help

help:
	@echo "---------------HELP---------------------------------------------------------"
	@echo "To install any software needed to build the compiler type make install-tools"
	@echo "To o build the compiler type make vsopc"
	@echo "----------------------------------------------------------------------------"


	install-tools:



	vsopc: vsopc.py
			python vsopc.py -lex $@

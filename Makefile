PYTHON = python3

.PHONY = help install-tools vsopc

.DEFAULT-GOAL = help

help:
	@echo "---------------HELP---------------------------------------------------------"
	@echo "To install any software needed to build the compiler type make install-tools"
	@echo "To build the compiler type make vsopc"
	@echo "----------------------------------------------------------------------------"


install-tools:
	sudo apt-get install --yes python3-pip
	sudo apt-get install --yes python-setuptools
	yes | sudo pip3 install llvmlite

vsopc:


PYTHON_VERSION := 3.7

CONDA_URL := https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh


.PHONY: all clean

all: python

python: venv 


clean: clean_extra
	rm -rf venv
	rm -f miniconda.sh
	rm -rf *.done
	find . -iname "*.pyc" -delete
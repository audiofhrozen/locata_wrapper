PYTHON_VERSION := 3.7

CONDA_URL := https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh


.PHONY: all clean

all: python

python: locata_wrapper.done

miniconda.sh:
	test -f miniconda.sh || wget $(CONDA_URL) -O miniconda.sh
venv: miniconda.sh
	test -d $(PWD)/venv || bash miniconda.sh -b -p $(PWD)/venv
	. venv/bin/activate && conda update -y conda
	. venv/bin/activate && conda install -y python=$(PYTHON_VERSION)
	. venv/bin/activate && conda info -a
locata_wrapper.done: venv
	. venv/bin/activate && conda install -y matplotlib
	. venv/bin/activate && pip install -e ..
	touch locata_wrapper.done

clean:
	rm -rf venv
	rm -f miniconda.sh
	rm -rf *.done
	find . -iname "*.pyc" -delete
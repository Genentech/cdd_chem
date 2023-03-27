# To deployt to smdi dev after succesfull gitlab ci build:
# this is not quite working yet. issues with conda install, need to talk to Kriszti

sudo -u smdi tcsh -l
set version=0.4.13
set version=<version from cdd_chem/__init__.py>
conda activate cdd_py3_dev
conda install -c https://repository.intranet.roche.com/artifactory/api/conda/smdd-conda-local/dev cdd_chem=$version

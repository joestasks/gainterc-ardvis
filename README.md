# gainterc-ardvis

Intercomparison - SR ARD visualisation

```code
python ./configuration_controller/app_pipeline.py configuration_controller global.yml
```

## Environment

Get and install system appropriate Miniconda:
<https://docs.conda.io/en/latest/miniconda.html>

```code
conda deactivate
conda config --set auto_activate_base false
conda update -n base -c defaults conda
conda create -n gainterc
conda activate gainterc
conda install pandas
conda install pyyaml
conda install matplotlib
```

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

## Testing

### QA Reference Data & Outputs

Reference data (input) and QAed reference outputs are located in the *test* folder. To test modified code against this reference, use the following configuration settings:

```code
IN_BASE: /home/myname/workspace/gainterc-ardvis/test/qa_ref_input/output_60_and_NBR_sites
TEST_REF_BASE: /home/myname/workspace/gainterc-ardvis/test/qa_ref_output
```

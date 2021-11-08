"""Comparison Logic



"""

import os
import sys
import importlib
import importlib.util


def compare(path_to_config, config_file):
    """Rules."""

    # This sys.path bookended chunk is common to all entry functions.
    sys.path.insert(0, './')
    app_pipeline = importlib.import_module(path_to_config + '.app_pipeline')
    subproject_name = os.path.basename(os.path.dirname(__file__))
    app_configuration, next_subproject_name, next_subproject_module, \
        next_entry = app_pipeline.entry_load_next_mod(
            app_pipeline, subproject_name, path_to_config, config_file)
    plot_plan = importlib.import_module(subproject_name + '.plot_plan')
    sequential_run = importlib.import_module(subproject_name + '.sequential_run')
    sys.path.remove('./')

    plans, ack = plot_plan.get_plans(app_configuration, subproject_name)
    sequential_run.all(plans, **ack)
    #parallel_run.all(plans)
    #cloud_run.all(plans)

    if next_subproject_name is not None:
        call_next_entry(next_subproject_module, next_entry, path_to_config, config_file)


def call_next_entry(next_subproject_module, next_entry, path_to_config, config_file):
    """Call the next entry point function in the processing pipeline."""

    run_success = eval('next_subproject_module.' + next_entry + '(path_to_config, config_file)')

    return run_success


if __name__ == "__main__":
    compare(sys.argv[1], sys.argv[2])

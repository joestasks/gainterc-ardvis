"""Application Pipeline Starting Point

    The main starting point for initiating a complete processing pipeline.

"""

import os
import pprint
import importlib.util
import json
from yaml import safe_load, load, dump, YAMLError
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

PP = pprint.PrettyPrinter(indent=4)

def get_config(path_to_config, config_file):
    """Load and return the YAML based configuration for running a pipeline."""

    app_configuration = 0
    config_path = './global.yml'
    if isinstance(path_to_config, str) and isinstance(config_file, str):
        config_path = path_to_config + '/' + config_file
    elif isinstance(path_to_config, str):
        config_path = path_to_config + '/' + config_path
    else:
        print('HELP! One or more arguments is missing.')
    with open(config_path, 'rb') as stream:
        try:
            app_configuration = load(stream, Loader=Loader)
            stream.close()
        except YAMLError as err:
            print('ERROR: ' + str(err))

    return app_configuration

def test_get_config():
    """Load and check global.yml which should always exist."""

    assert 'APP_NAME' in get_config(None, None)

def start(path_to_config, config_file):
    """Main starting point for a pipeline. Processing will continue as far as
       the configuration specifies a chain of linked subprojects via the
       NEXT_ENTRY_SUBPROJECT property."""

    app_configuration = get_config(path_to_config, config_file)
    app_source_root = app_configuration['APP_SOURCE']['ROOT']
    app_source_main = app_configuration['APP_SOURCE']['MAIN']
    main_module = app_configuration['APP_SOURCE']['SUBPROJECTS'][
        app_source_main]['MODULE']
    interface_entry = app_configuration['APP_SOURCE']['SUBPROJECTS'][
        app_source_main]['INTERFACE']['ENTRY']
    try:
        module_name = main_module
        module_file_path = app_source_root + '/' + app_source_main + '/' + main_module + '.py'
        module_spec = importlib.util.spec_from_file_location(
            module_name, module_file_path)
        module = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(module)
        eval('module.' + interface_entry + '(path_to_config, config_file)')
    except ImportError as err:
        print('ERROR: ' + str(err))

def test_start():
    """Check if module can find itself."""

    os.chdir('..')

    assert not str(start('configuration_controller', None)).startswith('ERROR')

def entry_load_next_mod(app_pipeline, subproject_name, path_to_config, config_file):
    """Helper to keep entry functions in subsequent pipeline segments cleaner."""

    app_configuration = app_pipeline.get_config(path_to_config, config_file)
    next_subproject_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][
        subproject_name]['INTERFACE']['NEXT_ENTRY_SUBPROJECT']
    next_module_name = None
    next_entry = None
    next_subproject_module = None
    if next_subproject_name is not None:
        next_module_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][
            next_subproject_name]['MODULE']
        next_entry = app_configuration['APP_SOURCE']['SUBPROJECTS'][
            next_subproject_name]['INTERFACE']['ENTRY']
        next_subproject_module = importlib.import_module(
            next_subproject_name + '.' + next_module_name)

    return (app_configuration, next_subproject_name, next_subproject_module, next_entry)

def read_data(path, format, params):
    """Wrapper to abstract data file persistence I/O."""

    return 1

def write_data(path, format, params):
    """Wrapper to abstract data file persistence I/O."""

    return 1

def read_data_df(path, format, params):
    """Wrapper to abstract data file persistence I/O."""

    return 1

def write_data_df(path, format, params):
    """Wrapper to abstract data file persistence I/O."""

    return 1

if __name__ == "__main__":
    import sys
    try:
        print('Configuration Module: ' + sys.argv[1])
        print('Configuration File: ' + sys.argv[2])
    except IndexError as err:
        print('ERROR: ' + str(err))
        print(u"***\n"
              u"First argument must be the relative path to a configuration"
              u" module with a full set of configuration files.\n"
              u"Second argument must be the main configuration file to use"
              u" (defaults to global.yml).\n"
              u"Usage:\n"
              u"python ./configuration_controller/app_pipeline.py"
              u" configuration_controller global.yml\n"
              u"***")
        sys.exit(1)
    finally:
        print('Starting Pipeline...')
        start(sys.argv[1], sys.argv[2])

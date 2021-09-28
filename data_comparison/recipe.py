"""Comparison Logic



"""

import os
import sys
import importlib
import importlib.util
from pathlib import Path
import pandas as pd
pd.options.mode.chained_assignment = None
import numpy as np
import matplotlib.pyplot as plt

def p2f(x):
    return float(x.strip('%')) / 100

def compare(path_to_config, config_file):
    """Rules."""

    # This sys.path bookended chunk is common to all entry functions.
    sys.path.insert(0, './')
    app_pipeline = importlib.import_module(path_to_config + '.app_pipeline')
    subproject_name = os.path.basename(os.path.dirname(__file__))
    app_configuration, next_subproject_name, next_subproject_module, \
        next_entry = app_pipeline.entry_load_next_mod(
            app_pipeline, subproject_name, path_to_config, config_file)
    sys.path.remove('./')

    in_a_measurements_min_valid_pixel_percentage = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'IN_A_MEASUREMENTS_MIN_VALID_PIXEL_PERCENTAGE'
    ]
    in_b_measurements_min_valid_pixel_percentage = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'IN_B_MEASUREMENTS_MIN_VALID_PIXEL_PERCENTAGE'
    ]
    in_a_indices_min_valid_pixel_percentage = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'IN_A_INDICES_MIN_VALID_PIXEL_PERCENTAGE'
    ]
    in_b_indices_min_valid_pixel_percentage = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'IN_B_INDICES_MIN_VALID_PIXEL_PERCENTAGE'
    ]
    standardised_date_format = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'STANDARDISED_DATE_FORMAT'
    ]
    ga_band_prefix_rg0 = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'GA_BAND_PREFIX_RG0'
    ]
    ga_band_prefix_rg1 = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'GA_BAND_PREFIX_RG1'
    ]
    ga_band_lam_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'GA_BAND_LAM_NAME'
    ]
    measurements_plot_type = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'MEASUREMENTS_PLOT_TYPE'
    ]
    indices_plot_type = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'INDICES_PLOT_TYPE'
    ]

    in_a_data_path = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_BASE']
    in_a_prefix = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_A_PREFIX']
    in_a_source_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_A_SOURCE_NAME']
    in_a_satellite_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_A_SATELLITE_NAME']
    in_a_product = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_A_PRODUCT']
    in_a_site = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_A_SITE']
    in_a_measurements_file = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_A_MEASUREMENTS_FILE']
    in_a_indices_file = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_A_INDICES_FILE']
    in_a_site_path = in_a_data_path + '/' + in_a_prefix + '_' + in_a_source_name + '_' + in_a_satellite_name + '/'

    in_b_data_path = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_BASE']
    in_b_prefix = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_B_PREFIX']
    in_b_source_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_B_SOURCE_NAME']
    in_b_satellite_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_B_SATELLITE_NAME']
    in_b_product = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_B_PRODUCT']
    in_b_site = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_B_SITE']
    in_b_measurements_file = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_B_MEASUREMENTS_FILE']
    in_b_indices_file = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['IN_B_INDICES_FILE']
    in_b_site_path = in_b_data_path + '/' + in_b_prefix + '_' + in_b_source_name + '_' + in_b_satellite_name + (
        lambda x: (x is not None and '_' + x) or ("")
    )(in_b_product) + '/'

    out_path = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['OUT_BASE']
    rec_max = app_configuration['APP_SOURCE']['DATA_RECORD_MAX_LIMIT']

    products = None
    if in_a_product is None:
        products = [*app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['GA_ALGORITHMS']]
    else:
        products = list((in_a_product,))
    print('Using these products:-')
    print(products)

    for product in products:
        if in_a_source_name.upper() == 'GA':
            in_a_site_path = in_a_data_path + '/' + in_a_prefix + '_' + in_a_source_name + '_' + in_a_satellite_name + '_' + product + '/'
        print('Input A sites path: ' + in_a_site_path)
        print('Input A configured site: ' + (in_a_site or '~'))
        print('Input B sites path: ' + in_b_site_path)
        print('Input B configured site: ' + (in_b_site or '~'))
        site_paths = None
        if in_a_site is None:
            site_paths = list(Path(in_a_site_path).glob('**'))
            site_paths.pop(0)
        else:
            site_paths = list((in_a_site_path + in_a_site,))
        print('Found these site paths:-')
        print(site_paths)
        sites = list(map(lambda x: os.path.basename(os.path.normpath(x)), site_paths))
        print('Processing these sites:-')
        print(sites)
        for site in sites:
            print('Working on site: ' + site)
            this_in_a_site_path = in_a_site_path + site
            this_in_b_site_path = in_b_site_path + site

            # Read in As and Bs.
            in_a_measurements_path = Path(this_in_a_site_path + '/' + in_a_measurements_file)
            in_b_measurements_path = Path(this_in_b_site_path + '/' + in_b_measurements_file)
            in_a_indices_path = Path(this_in_a_site_path + '/' + in_a_indices_file)
            in_b_indices_path = Path(this_in_b_site_path + '/' + in_b_indices_file)
            in_a_measurements_df = None
            in_b_measurements_df = None
            in_a_indices_df = None
            in_b_indices_df = None
            print('Measurements input A: ' + str(in_a_measurements_path))
            print('Measurements input B: ' + str(in_b_measurements_path))
            print('Indices input A: ' + str(in_a_indices_path))
            print('Indices input B: ' + str(in_b_indices_path))

            if in_a_measurements_path.is_file():
                print('Making DataFrame from: ' + str(in_a_measurements_path))
                in_a_measurements_df = pd.read_csv(in_a_measurements_path,
                                        nrows=(rec_max if rec_max is not None else None),
                                        sep=',',
                                        skipinitialspace=False,
                                        quotechar='|',
                                        converters={'valid_pixel_percentage': p2f})
                #print(in_a_measurements_df)
            if in_b_measurements_path.is_file():
                print('Making DataFrame from: ' + str(in_b_measurements_path))
                in_b_measurements_df = pd.read_csv(in_b_measurements_path,
                                        nrows=(rec_max if rec_max is not None else None),
                                        sep=',',
                                        skipinitialspace=False,
                                        quotechar='|',
                                        converters={'valid_pixel_percentage': p2f})
                #print(in_b_measurements_df)
            if in_a_indices_path.is_file():
                print('Making DataFrame from: ' + str(in_a_indices_path))
                in_a_indices_df = pd.read_csv(in_a_indices_path,
                                        nrows=(rec_max if rec_max is not None else None),
                                        sep=',',
                                        skipinitialspace=False,
                                        quotechar='|',
                                        converters={'valid_pixel_percentage': p2f})
                #print(in_a_indices_df)
            if in_b_indices_path.is_file():
                print('Making DataFrame from: ' + str(in_b_indices_path))
                in_b_indices_df = pd.read_csv(in_b_indices_path,
                                        nrows=(rec_max if rec_max is not None else None),
                                        sep=',',
                                        skipinitialspace=False,
                                        quotechar='|',
                                        converters={'valid_pixel_percentage': p2f})
                #print(in_b_indices_df)

            date_col = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['DATE_COL']
            band_col = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['BAND_COL']
            indices_col = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['INDICES_COL']
            ga_bands = [*app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['GA_BANDS']]
            spectral_indices = [*app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['SPECTRAL_INDICES']]

            # Generate measurements plots.
            if in_a_measurements_df is not None and in_b_measurements_df is not None:
                m_fig, m_axs = plt.subplots(len(ga_bands), 1, figsize=(12, 10), squeeze=False)
                for idx_band, band in enumerate(ga_bands):
                    prefixed_band = band
                    if in_a_source_name.upper() == 'GA':
                        if prefixed_band.startswith(('satellite', 'solar')):
                            prefixed_band = ga_band_prefix_rg1 + '_oa_' + prefixed_band
                        elif product.upper() == 'LAM':
                            prefixed_band = ga_band_prefix_rg1 + '_' + ga_band_lam_name + '_' + prefixed_band
                        else:
                            prefixed_band = ga_band_prefix_rg1 + '_' + product + '_' + prefixed_band
                    measurements = [*app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['GA_BANDS'][band]]
                    for measurement in measurements:
                        temp_a_df = in_a_measurements_df.loc[in_a_measurements_df[band_col] == prefixed_band]
                        temp_a_df.loc[
                            temp_a_df[
                                'valid_pixel_percentage'] < in_a_measurements_min_valid_pixel_percentage, [measurement]] = np.nan
                        #print(temp_a_df)
                        temp_b_df = in_b_measurements_df.loc[in_b_measurements_df[band_col] == band]
                        temp_b_df.loc[
                            temp_b_df[
                                'valid_pixel_percentage'] < in_b_measurements_min_valid_pixel_percentage, [measurement]] = np.nan
                        #print(temp_b_df)
                        ax = temp_a_df.plot(kind=measurements_plot_type, x=date_col, y=measurement, ax=m_axs[idx_band][0])
                        ax = temp_b_df.plot(kind=measurements_plot_type, x=date_col, y=measurement, ax=m_axs[idx_band][0])
                #plt.show()
                plot_target = (out_path + '/' + in_a_source_name + '_' + in_a_satellite_name + \
                    '_vs_' + \
                    in_b_source_name + '_' + in_b_satellite_name + '/' + product + '/' + site + '/').lower()
                print('Making plot output directory: ' + plot_target)
                Path(os.path.dirname(plot_target)).mkdir(parents=True, exist_ok=True)
                plot_path = (plot_target + measurement + '_' + os.path.splitext(
                    in_a_measurements_file)[0]).lower() + '.png'
                print('Writing plot image: ' + plot_path)
                plt.savefig(plot_path)

            # Generate indices plots.
            if in_a_indices_df is not None and in_b_indices_df is not None:
                in_a_indices_df[date_col] = pd.to_datetime(in_a_indices_df[date_col], format=standardised_date_format).dt.date
                in_b_indices_df[date_col] = pd.to_datetime(in_b_indices_df[date_col], format=standardised_date_format).dt.date
                i_fig, i_axs = plt.subplots(len(spectral_indices), 1, figsize=(12, 4), squeeze=False)
                for idx_spec_ind, spec_ind in enumerate(spectral_indices):
                    spec_ind_measurements = [*app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
                        'SPECTRAL_INDICES'][spec_ind]]
                    for measurement in spec_ind_measurements:
                        temp_a_df = in_a_indices_df.loc[in_a_indices_df[indices_col] == spec_ind]
                        temp_a_df.loc[
                            temp_a_df[
                                'valid_pixel_percentage'] < in_a_indices_min_valid_pixel_percentage, [measurement]] = np.nan
                        temp_a_df.loc[temp_a_df[measurement] == '--', [measurement]] = np.nan
                        #print(temp_a_df)
                        temp_b_df = in_b_indices_df.loc[in_b_indices_df[indices_col] == spec_ind]
                        temp_b_df.loc[
                            temp_b_df[
                                'valid_pixel_percentage'] < in_b_indices_min_valid_pixel_percentage, [measurement]] = np.nan
                        temp_b_df.loc[temp_b_df[measurement] == '--', [measurement]] = np.nan
                        #print(temp_b_df)
                        temp_a_df[measurement] = pd.to_numeric(temp_a_df[measurement])
                        temp_b_df[measurement] = pd.to_numeric(temp_b_df[measurement])
                        ax = temp_a_df.plot(kind=indices_plot_type, x=date_col, y=measurement, ax=i_axs[idx_spec_ind][0])
                        ax = temp_b_df.plot(kind=indices_plot_type, x=date_col, y=measurement, ax=i_axs[idx_spec_ind][0])
                #plt.show()
                plot_target = (out_path + '/' + in_a_source_name + '_' + in_a_satellite_name + \
                    '_vs_' + \
                    in_b_source_name + '_' + in_b_satellite_name + '/' + product + '/' + site + '/').lower()
                print('Making plot output directory: ' + plot_target)
                Path(os.path.dirname(plot_target)).mkdir(parents=True, exist_ok=True)
                plot_path = (plot_target + spec_ind + '_' + os.path.splitext(
                    in_a_indices_file)[0]).lower() + '.png'
                print('Writing plot image: ' + plot_path)
                plt.savefig(plot_path)

    if next_subproject_name is not None:
        call_next_entry(next_subproject_module, next_entry, path_to_config, config_file)

def call_next_entry(next_subproject_module, next_entry, path_to_config, config_file):
    """Call the next entry point function in the processing pipeline."""

    run_success = eval('next_subproject_module.' + next_entry + '(path_to_config, config_file)')

    return run_success

if __name__ == "__main__":
    compare(sys.argv[1], sys.argv[2])

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
    plot_start_date = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'PLOT_START_DATE'
    ]
    plot_start_date = np.datetime64(plot_start_date)
    plot_end_date = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'PLOT_END_DATE'
    ]
    plot_end_date = np.datetime64(plot_end_date)
    ga_band_lam_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'GA_BAND_LAM_NAME'
    ]
    ga_band_oa_name = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'GA_BAND_OA_NAME'
    ]
    measurements_plot_type = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'MEASUREMENTS_PLOT_TYPE'
    ]
    indices_plot_type = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'INDICES_PLOT_TYPE'
    ]
    measurements_plot_y_label = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'MEASUREMENTS_PLOT_Y_LABEL'
    ]
    oa_plot_y_label = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'OA_PLOT_Y_LABEL'
    ]
    plot_style = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'PLOT_STYLE'
    ]
    spectral_indices = [*app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'SPECTRAL_INDICES'
    ]]
    date_col = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'DATE_COL'
    ]
    band_col = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'BAND_COL'
    ]
    indices_col = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'INDICES_COL'
    ]
    ga_oa_mappings = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'GA_OA_MAPPINGS'
    ]
    ga_oas = [*ga_oa_mappings]
    ga_band_mappings = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA'][
        'GA_BAND_MAPPINGS'
    ]
    ga_bands = [*ga_band_mappings]

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
        product_label = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['GA_ALGORITHMS'][product]
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
                                        #parse_dates=[date_col],
                                        #index_col=[date_col],
                                        converters={'valid_pixel_percentage': p2f})
                #print(in_a_measurements_df)
            if in_b_measurements_path.is_file():
                print('Making DataFrame from: ' + str(in_b_measurements_path))
                in_b_measurements_df = pd.read_csv(in_b_measurements_path,
                                        nrows=(rec_max if rec_max is not None else None),
                                        sep=',',
                                        skipinitialspace=False,
                                        quotechar='|',
                                        #parse_dates=[date_col],
                                        #index_col=[date_col],
                                        converters={'valid_pixel_percentage': p2f})
                #print(in_b_measurements_df)
            if in_a_indices_path.is_file():
                print('Making DataFrame from: ' + str(in_a_indices_path))
                in_a_indices_df = pd.read_csv(in_a_indices_path,
                                        nrows=(rec_max if rec_max is not None else None),
                                        sep=',',
                                        skipinitialspace=False,
                                        quotechar='|',
                                        #parse_dates=[date_col],
                                        #index_col=[date_col],
                                        converters={'valid_pixel_percentage': p2f})
                #print(in_a_indices_df)
            if in_b_indices_path.is_file():
                print('Making DataFrame from: ' + str(in_b_indices_path))
                in_b_indices_df = pd.read_csv(in_b_indices_path,
                                        nrows=(rec_max if rec_max is not None else None),
                                        sep=',',
                                        skipinitialspace=False,
                                        quotechar='|',
                                        #parse_dates=[date_col],
                                        #index_col=[date_col],
                                        converters={'valid_pixel_percentage': p2f})
                #print(in_b_indices_df)

            # Generate measurements plots.
            if in_a_measurements_df is not None and in_b_measurements_df is not None:
                oa_temp_a_df = None
                oa_temp_b_df = None
                band_mutations = []
                oa_band_mutations = []
                plot_measurements = []
                oa_plot_measurements = []
                ga_oas_and_bands = ga_oas + ga_bands
                ga_band_mappings = {**ga_oa_mappings, **ga_band_mappings}
                #print(ga_oas_and_bands)
                #print(ga_band_mappings)

                for band in ga_oas_and_bands:
                    band_prefixes = [*ga_band_mappings[band]['PREFIXES']]
                    band_plot_props = [*ga_band_mappings[band]['PLOT']]
                    a_band_lookup_key = (lambda x: (x.upper() == 'ESA' and 'ESA_S2AB') or (None))(in_a_source_name)
                    a_band_lookup_key = (lambda x: (x.upper() == 'USGS' and 'USGS_LS8') or (a_band_lookup_key))(in_a_source_name)
                    b_band_lookup_key = (lambda x: (x.upper() == 'ESA' and 'ESA_S2AB') or (None))(in_b_source_name)
                    b_band_lookup_key = (lambda x: (x.upper() == 'USGS' and 'USGS_LS8') or (b_band_lookup_key))(in_b_source_name)
                    if in_a_source_name.upper() == 'GA' and band.lower().startswith(('satellite', 'solar')):
                        b_band_lookup_key = 'GA'
                    for band_prefix in band_prefixes:
                        band_suffixes = [*ga_band_mappings[band]['PREFIXES'][band_prefix]['SUFFIXES']]
                        for band_suffix in band_suffixes:
                            if b_band_lookup_key in [*ga_band_mappings[band]['PREFIXES'][band_prefix]['SUFFIXES'][band_suffix]]:
                                a_band_mut = band_prefix + product.lower() + '_' + band
                                if a_band_lookup_key in [*ga_band_mappings[band]['PREFIXES'][band_prefix]['SUFFIXES'][band_suffix]]:
                                    a_band_mut = ga_band_mappings[band]['PREFIXES'][band_prefix]['SUFFIXES'][band_suffix][a_band_lookup_key]
                                b_band_mut = ga_band_mappings[band]['PREFIXES'][band_prefix]['SUFFIXES'][band_suffix][b_band_lookup_key]
                                if in_a_source_name.upper() == 'GA' and product.upper() == 'LAM':
                                    a_band_mut = band_prefix + ga_band_lam_name + '_' + band
                                if band_suffix != 'Empty':
                                    a_band_mut = a_band_mut + band_suffix

                                if in_a_source_name.upper() == 'GA' and band.lower().startswith(('satellite', 'solar')):
                                    a_band_mut = band_prefix + ga_band_oa_name + '_' + band
                                    if len(oa_band_mutations) > 0:
                                        oa_band_mutations[0][1] = a_band_mut
                                    else:
                                        oa_band_mutations.append([a_band_mut, b_band_mut])
                                        oa_plot_measurements.append([band_plot_props[0], ga_band_mappings[band]['PLOT'][band_plot_props[0]]])
                                else:
                                    band_mutations.append([a_band_mut, b_band_mut])
                                    plot_measurements.append([band_plot_props[0], ga_band_mappings[band]['PLOT'][band_plot_props[0]]])

                #band_mutations = band_mutations + oa_band_mutations
                #plot_measurements = plot_measurements + oa_plot_measurements
                #print(oa_band_mutations)
                #print(len(oa_band_mutations))
                #print(oa_plot_measurements)
                #print(len(oa_plot_measurements))
                #print(band_mutations)
                #print(len(band_mutations))
                #print(plot_measurements)
                #print(len(plot_measurements))

                plt.style.use(plot_style)
                plot_target = (out_path + '/' + in_a_source_name + '_' + in_a_satellite_name + \
                    '_vs_' + \
                    in_b_source_name + '_' + in_b_satellite_name + '/' + product + '/' + site + '/').lower()
                print('Making plot output directory: ' + plot_target)
                Path(os.path.dirname(plot_target)).mkdir(parents=True, exist_ok=True)

                if len(oa_band_mutations) > 0 and (oa_temp_a_df is None or oa_temp_b_df is None):
                    oa_temp_a_df = in_a_measurements_df.loc[in_a_measurements_df[band_col] == oa_band_mutations[0][0]]
                    oa_temp_a_df.loc[
                        oa_temp_a_df[
                            'valid_pixel_percentage'] < in_a_measurements_min_valid_pixel_percentage, [oa_plot_measurements[0][0]]] = np.nan
                    #print(oa_temp_a_df)
                    oa_temp_b_df = in_a_measurements_df.loc[in_a_measurements_df[band_col] == oa_band_mutations[0][1]]
                    oa_temp_b_df.loc[
                        oa_temp_b_df[
                            'valid_pixel_percentage'] < in_b_measurements_min_valid_pixel_percentage, [oa_plot_measurements[0][0]]] = np.nan
                    #print(oa_temp_b_df)
                    oa_temp_a_df = oa_temp_a_df[oa_temp_a_df[oa_plot_measurements[0][0]].notna()]
                    oa_temp_b_df = oa_temp_b_df[oa_temp_b_df[oa_plot_measurements[0][0]].notna()]
                    oa_temp_a_df[oa_plot_measurements[0][0]] = pd.to_numeric(oa_temp_a_df[oa_plot_measurements[0][0]])
                    oa_temp_b_df[oa_plot_measurements[0][0]] = pd.to_numeric(oa_temp_b_df[oa_plot_measurements[0][0]])
                    oa_temp_a_df[date_col] = pd.to_datetime(oa_temp_a_df[date_col], format=standardised_date_format) #.dt.date
                    oa_temp_b_df[date_col] = pd.to_datetime(oa_temp_b_df[date_col], format=standardised_date_format) #.dt.date
                    oa_temp_a_df.to_csv(plot_target + oa_band_mutations[0][0].lower() + '_' + oa_plot_measurements[0][0].lower() + '_' + in_a_source_name.lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                    oa_temp_b_df.to_csv(plot_target + oa_band_mutations[0][1].lower() + '_' + oa_plot_measurements[0][0].lower() + '_' + in_b_source_name.lower() + '_temp.csv', index=False, sep=',', quotechar='|')

                for idx_band_ab, band_ab in enumerate(band_mutations):
                    m_fig, m_axs = plt.subplots(2, 1, figsize=(12, 10), squeeze=False)
                    temp_a_df = in_a_measurements_df.loc[in_a_measurements_df[band_col] == band_ab[0]]
                    temp_a_df.loc[
                        temp_a_df[
                            'valid_pixel_percentage'] < in_a_measurements_min_valid_pixel_percentage, [plot_measurements[idx_band_ab][0]]] = np.nan
                    #print(temp_a_df)
                    temp_b_df = in_b_measurements_df.loc[in_b_measurements_df[band_col] == band_ab[1]]
                    temp_b_df.loc[
                        temp_b_df[
                            'valid_pixel_percentage'] < in_b_measurements_min_valid_pixel_percentage, [plot_measurements[idx_band_ab][0]]] = np.nan
                    #print(temp_b_df)
                    temp_a_df = temp_a_df[temp_a_df[plot_measurements[idx_band_ab][0]].notna()]
                    temp_b_df = temp_b_df[temp_b_df[plot_measurements[idx_band_ab][0]].notna()]
                    temp_a_df[plot_measurements[idx_band_ab][0]] = pd.to_numeric(temp_a_df[plot_measurements[idx_band_ab][0]])
                    temp_b_df[plot_measurements[idx_band_ab][0]] = pd.to_numeric(temp_b_df[plot_measurements[idx_band_ab][0]])
                    temp_a_df[date_col] = pd.to_datetime(temp_a_df[date_col], format=standardised_date_format) #.dt.date
                    temp_b_df[date_col] = pd.to_datetime(temp_b_df[date_col], format=standardised_date_format) #.dt.date
                    #temp_a_df.set_index(date_col, inplace=True)
                    #temp_b_df.set_index(date_col, inplace=True)
                    #print(temp_a_df.dtypes)
                    #print(temp_a_df)
                    #print(temp_b_df.dtypes)
                    #print(temp_b_df)
                    m_axs[0][0].set(
                        xlabel=date_col,
                        ylabel=measurements_plot_y_label,
                        title=in_a_source_name + ' ' + in_a_satellite_name + \
                            ' VS ' + \
                            in_b_source_name + ' ' + in_b_satellite_name + ' for ' + product_label + ' at ' + site,
                            xlim=[plot_start_date, plot_end_date]
                    )
                    ga_product_label = ''
                    if in_a_source_name.upper() == 'GA':
                        ga_product_label = ' ' + product_label
                    temp_a_df.to_csv(plot_target + band_ab[0].lower() + '_' + plot_measurements[idx_band_ab][0].lower() + '_' + in_a_source_name.lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                    temp_b_df.to_csv(plot_target + band_ab[1].lower() + '_' + plot_measurements[idx_band_ab][0].lower() + '_' + in_b_source_name.lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                    ax = temp_a_df.plot(kind=measurements_plot_type, x=date_col, y=plot_measurements[idx_band_ab][0], label=plot_measurements[idx_band_ab][1] + ' ' + in_a_source_name + ga_product_label, ax=m_axs[0][0])
                    ax = temp_b_df.plot(kind=measurements_plot_type, x=date_col, y=plot_measurements[idx_band_ab][0], label=plot_measurements[idx_band_ab][1] + ' ' + in_b_source_name, ax=m_axs[0][0])

                    if oa_temp_a_df is not None and oa_temp_b_df is not None:
                        m_axs[1][0].set(
                            xlabel=date_col,
                            ylabel=oa_plot_y_label,
                            title=in_a_source_name + ' ' + in_a_satellite_name + \
                                ' VS ' + \
                                in_a_source_name + ' ' + in_a_satellite_name + ' for ' + product_label + ' at ' + site,
                                xlim=[plot_start_date, plot_end_date]
                        )
                        ax = oa_temp_a_df.plot(kind=measurements_plot_type, x=date_col, y=oa_plot_measurements[0][0], label=oa_plot_measurements[0][1] + ' ' + oa_band_mutations[0][0][7:], ax=m_axs[1][0], sharex=m_axs[0][0])
                        ax = oa_temp_b_df.plot(kind=measurements_plot_type, x=date_col, y=oa_plot_measurements[0][0], label=oa_plot_measurements[0][1] + ' ' + oa_band_mutations[0][1][7:], ax=m_axs[1][0], sharex=m_axs[0][0])

                    plot_path = (plot_target + band_ab[0].lower() + '_' + plot_measurements[idx_band_ab][0].lower() + '_' + os.path.splitext(
                        in_a_measurements_file)[0]).lower() + '.png'
                    print('Writing plot image: ' + plot_path)
                    m_fig.autofmt_xdate()
                    #plt.show()
                    plt.savefig(plot_path)

            # Generate indices plots.
            if in_a_indices_df is not None and in_b_indices_df is not None:
                plot_target = (out_path + '/' + in_a_source_name + '_' + in_a_satellite_name + \
                    '_vs_' + \
                    in_b_source_name + '_' + in_b_satellite_name + '/' + product + '/' + site + '/').lower()
                print('Making plot output directory: ' + plot_target)
                Path(os.path.dirname(plot_target)).mkdir(parents=True, exist_ok=True)
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

                        temp_a_df = temp_a_df[temp_a_df[measurement].notna()]
                        temp_b_df = temp_b_df[temp_b_df[measurement].notna()]
                        temp_a_df[measurement] = pd.to_numeric(temp_a_df[measurement])
                        temp_b_df[measurement] = pd.to_numeric(temp_b_df[measurement])
                        temp_a_df[date_col] = pd.to_datetime(temp_a_df[date_col], format=standardised_date_format) #.dt.date
                        temp_b_df[date_col] = pd.to_datetime(temp_b_df[date_col], format=standardised_date_format) #.dt.date
                        #temp_a_df.set_index(date_col, inplace=True)
                        #temp_b_df.set_index(date_col, inplace=True)
                        #print(temp_a_df.dtypes)
                        #print(temp_a_df)
                        #print(temp_b_df.dtypes)
                        #print(temp_b_df)
                        i_axs[idx_spec_ind][0].set(
                            xlabel=date_col,
                            ylabel=spec_ind,
                            title=in_a_source_name + ' ' + in_a_satellite_name + \
                                ' VS ' + \
                                in_b_source_name + ' ' + in_b_satellite_name + ' for ' + product + ' at ' + site,
                                xlim=[plot_start_date, plot_end_date]
                        )
                        temp_a_df.to_csv(plot_target + spec_ind.lower() + '_' + measurement.lower() + '_' + in_a_source_name.lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                        temp_b_df.to_csv(plot_target + spec_ind.lower() + '_' + measurement.lower() + '_' + in_b_source_name.lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                        measurement_label = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name]['DATA']['SPECTRAL_INDICES'][spec_ind][measurement]
                        ax = temp_a_df.plot(kind=indices_plot_type, x=date_col, y=measurement, label=measurement_label + ' ' + in_a_source_name, ax=i_axs[idx_spec_ind][0])
                        ax = temp_b_df.plot(kind=indices_plot_type, x=date_col, y=measurement, label=measurement_label + ' ' + in_b_source_name, ax=i_axs[idx_spec_ind][0])
                plot_path = (plot_target + os.path.splitext(
                    in_a_indices_file)[0]).lower() + '.png'
                print('Writing plot image: ' + plot_path)
                i_fig.autofmt_xdate()
                #plt.show()
                plt.savefig(plot_path)

    if next_subproject_name is not None:
        call_next_entry(next_subproject_module, next_entry, path_to_config, config_file)

def call_next_entry(next_subproject_module, next_entry, path_to_config, config_file):
    """Call the next entry point function in the processing pipeline."""

    run_success = eval('next_subproject_module.' + next_entry + '(path_to_config, config_file)')

    return run_success

if __name__ == "__main__":
    compare(sys.argv[1], sys.argv[2])

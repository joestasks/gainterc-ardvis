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

    acd = app_configuration['APP_SOURCE']['SUBPROJECTS'][subproject_name][
        'DATA']
    ack = {
        "acd": acd,
        "in_a_measurements_min_valid_pixel_percentage": acd['IN_A_MEASUREMENTS_MIN_VALID_PIXEL_PERCENTAGE'],
        "in_b_measurements_min_valid_pixel_percentage": acd['IN_B_MEASUREMENTS_MIN_VALID_PIXEL_PERCENTAGE'],
        "in_a_indices_min_valid_pixel_percentage": acd['IN_A_INDICES_MIN_VALID_PIXEL_PERCENTAGE'],
        "in_b_indices_min_valid_pixel_percentage": acd['IN_B_INDICES_MIN_VALID_PIXEL_PERCENTAGE'],
        "date_filtering": acd['DATE_FILTERING'],
        "standardised_date_format": acd['STANDARDISED_DATE_FORMAT'],
        "plot_start_date": np.datetime64(acd['PLOT_START_DATE']),
        "plot_end_date": np.datetime64(acd['PLOT_END_DATE']),
        "plot_style": acd['PLOT_STYLE'],
        "measurements_plot_type": acd['MEASUREMENTS_PLOT_TYPE'],
        "indices_plot_type": acd['INDICES_PLOT_TYPE'],
        "measurements_plot_y_label": acd['MEASUREMENTS_PLOT_Y_LABEL'],
        "oa_plot_y_label": acd['OA_PLOT_Y_LABEL'],
        "ga_algorithms": [*acd['GA_ALGORITHMS']],
        "ga_band_lam_name": acd['GA_BAND_LAM_NAME'],
        "ga_band_oa_name": acd['GA_BAND_OA_NAME'],
        "spectral_indices": [*acd['SPECTRAL_INDICES']],
        "date_col": acd['DATE_COL'],
        "band_col": acd['BAND_COL'],
        "indices_col": acd['INDICES_COL'],
        "ga_oa_mappings": acd['GA_OA_MAPPINGS'],
        "ga_oas": [*acd['GA_OA_MAPPINGS']],
        "ga_band_mappings": acd['GA_BAND_MAPPINGS'],
        "ga_bands": [*acd['GA_BAND_MAPPINGS']],
        "in_a_data_path": acd['IN_BASE'],
        "in_a_prefix": acd['IN_A_PREFIX'],
        "in_a_source_name": acd['IN_A_SOURCE_NAME'],
        "in_a_satellite_name": acd['IN_A_SATELLITE_NAME'],
        "in_a_product": acd['IN_A_PRODUCT'],
        "in_a_site": acd['IN_A_SITE'],
        "in_a_measurements_file": acd['IN_A_MEASUREMENTS_FILE'],
        "in_a_indices_file": acd['IN_A_INDICES_FILE'],
        "in_b_data_path": acd['IN_BASE'],
        "in_b_prefix": acd['IN_B_PREFIX'],
        "in_b_source_name": acd['IN_B_SOURCE_NAME'],
        "in_b_satellite_name": acd['IN_B_SATELLITE_NAME'],
        "in_b_product": acd['IN_B_PRODUCT'],
        "in_b_site": acd['IN_B_SITE'],
        "in_b_measurements_file": acd['IN_B_MEASUREMENTS_FILE'],
        "in_b_indices_file": acd['IN_B_INDICES_FILE'],
        "out_path": acd['OUT_BASE'],
        "rec_max": app_configuration['APP_SOURCE']['DATA_RECORD_MAX_LIMIT'],
    }

    ack['in_a_site_path'] = ack.get(
        'in_a_data_path'
    ) + '/' + ack.get(
        'in_a_prefix'
    ) + '_' + ack.get(
        'in_a_source_name'
    ) + '_' + ack.get(
        'in_a_satellite_name'
    ) + '/'
    ack['in_b_site_path'] = ack.get(
        'in_b_data_path'
    ) + '/' + ack.get(
        'in_b_prefix'
    ) + '_' + ack.get(
        'in_b_source_name'
    ) + '_' + ack.get(
        'in_b_satellite_name'
    ) + (
        lambda x: (x is not None and '_' + x) or ("")
    )(ack.get('in_b_product')) + '/'

    plt.style.use(ack.get('plot_style'))
    products = None
    if ack.get('in_a_product') is None:
        products = ack.get('ga_algorithms')
    else:
        products = list((ack.get('in_a_product'),))
    print('Using these products:-')
    print(products)

    for product in products:
        ack['product'] = product
        ack['product_label'] = acd['GA_ALGORITHMS'][product]
        if ack.get('in_a_source_name').upper() == 'GA':
            ack['in_a_site_path'] = ack.get(
                'in_a_data_path'
            ) + '/' + ack.get(
                'in_a_prefix'
            ) + '_' + ack.get(
                'in_a_source_name'
            ) + '_' + ack.get(
                'in_a_satellite_name'
            ) + '_' + product + '/'
        print('Input A sites path: ' + ack.get('in_a_site_path'))
        print('Input A configured site: ' + (ack.get('in_a_site') or '~'))
        print('Input B sites path: ' + ack.get('in_b_site_path'))
        print('Input B configured site: ' + (ack.get('in_b_site') or '~'))
        site_paths = None
        if ack.get('in_a_site') is None:
            site_paths = list(Path(ack.get('in_a_site_path')).glob('**'))
            site_paths.pop(0)
        else:
            site_paths = list((ack.get('in_a_site_path') + ack.get('in_a_site'),))
        print('Found these site paths:-')
        print(site_paths)
        sites = list(map(lambda x: os.path.basename(os.path.normpath(x)), site_paths))
        print('Processing these sites:-')
        print(sites)
        for site in sites:
            ack['site'] = site
            print('Working on site: ' + site)
            this_in_a_site_path = ack.get('in_a_site_path') + site
            this_in_b_site_path = ack.get('in_b_site_path') + site
            in_a_measurements_path = Path(this_in_a_site_path + '/' + ack.get('in_a_measurements_file'))
            in_b_measurements_path = Path(this_in_b_site_path + '/' + ack.get('in_b_measurements_file'))
            in_a_indices_path = Path(this_in_a_site_path + '/' + ack.get('in_a_indices_file'))
            in_b_indices_path = Path(this_in_b_site_path + '/' + ack.get('in_b_indices_file'))
            print('Measurements input A: ' + str(in_a_measurements_path))
            print('Measurements input B: ' + str(in_b_measurements_path))
            print('Indices input A: ' + str(in_a_indices_path))
            print('Indices input B: ' + str(in_b_indices_path))
            print('Making DataFrame from: ' + str(in_a_measurements_path))
            in_a_measurements_df = _get_df_from_csv(in_a_measurements_path, **ack)
            print('Making DataFrame from: ' + str(in_b_measurements_path))
            in_b_measurements_df = _get_df_from_csv(in_b_measurements_path, **ack)
            print('Making DataFrame from: ' + str(in_a_indices_path))
            in_a_indices_df = _get_df_from_csv(in_a_indices_path, **ack)
            print('Making DataFrame from: ' + str(in_b_indices_path))
            in_b_indices_df = _get_df_from_csv(in_b_indices_path, **ack)
            ack['plot_target'] = (ack.get(
                    'out_path'
                ) + '/' + ack.get(
                    'in_a_source_name'
                ) + '_' + ack.get(
                    'in_a_satellite_name'
                ) + '_vs_' + ack.get(
                    'in_b_source_name'
                ) + '_' + ack.get(
                    'in_b_satellite_name'
                ) + '/' + product + '/' + site + '/').lower()
            print('Making plot output directory: ' + ack.get('plot_target'))
            Path(os.path.dirname(ack.get('plot_target'))).mkdir(parents=True, exist_ok=True)

            band_mutations, oa_band_mutations, plot_measurements, oa_plot_measurements = _get_band_mutations(**ack)
            oa_temp_a_df, oa_temp_b_df = _generate_oa_dfs(in_a_measurements_df, in_b_measurements_df, oa_band_mutations, oa_plot_measurements, **ack)
            m_title, oa_title, i_title = _get_plot_titles(**ack)
            _generate_measurements_plots(in_a_measurements_df, in_b_measurements_df, band_mutations, plot_measurements, oa_temp_a_df, oa_temp_b_df, oa_band_mutations, oa_plot_measurements, **ack)
            _generate_indices_plots(in_a_indices_df, in_b_indices_df, **ack)

    if next_subproject_name is not None:
        call_next_entry(next_subproject_module, next_entry, path_to_config, config_file)


def _get_df_from_csv(file_path, **ack):
    """Read CSVs."""

    new_df = None
    if file_path.is_file():
        print('Making DataFrame from: ' + str(file_path))
        new_df = pd.read_csv(
            file_path,
            nrows=(ack.get('rec_max') if ack.get('rec_max') is not None else None),
            sep=',',
            skipinitialspace=False,
            quotechar='|',
            converters={'valid_pixel_percentage': p2f})
        #print(new_df)

    return new_df


def _get_band_mutations(**ack):
    """Work out possible comparable band mutations."""

    band_mutations = []
    oa_band_mutations = []
    plot_measurements = []
    oa_plot_measurements = []
    ga_oas_and_bands = ack.get('ga_oas') + ack.get('ga_bands')
    ga_band_mappings = {
        **(ack.get('ga_oa_mappings')),
        **(ack.get('ga_band_mappings'))}
    for band in ga_oas_and_bands:
        band_prefixes = [*ga_band_mappings[band]['PREFIXES']]
        band_plot_props = [*ga_band_mappings[band]['PLOT']]
        a_band_lookup_key = (lambda x:
            (x.upper() == 'ESA' and 'ESA_S2AB') or (None)
        )(ack.get('in_a_source_name'))
        a_band_lookup_key = (lambda x:
            (x.upper() == 'USGS' and 'USGS_LS8') or (a_band_lookup_key)
        )(ack.get('in_a_source_name'))
        b_band_lookup_key = (lambda x:
            (x.upper() == 'ESA' and 'ESA_S2AB') or (None)
        )(ack.get('in_b_source_name'))
        b_band_lookup_key = (lambda x:
            (x.upper() == 'USGS' and 'USGS_LS8') or (b_band_lookup_key)
        )(ack.get('in_b_source_name'))
        if (
            ack.get('in_a_source_name').upper() == 'GA'
        ) and (
            band.lower().startswith(('satellite', 'solar'))
        ):
            b_band_lookup_key = 'GA'
        for band_prefix in band_prefixes:
            band_suffixes = [
                *ga_band_mappings[band]['PREFIXES'][band_prefix]['SUFFIXES']]
            for band_suffix in band_suffixes:
                if b_band_lookup_key in [*ga_band_mappings[
                        band]['PREFIXES'][
                            band_prefix]['SUFFIXES'][
                                band_suffix]]:
                    a_band_mut = band_prefix + ack.get(
                        'product'
                    ).lower() + '_' + band
                    if a_band_lookup_key in [*ga_band_mappings[
                        band]['PREFIXES'][
                            band_prefix]['SUFFIXES'][
                                band_suffix]]:
                        a_band_mut = ga_band_mappings[
                            band]['PREFIXES'][
                                band_prefix]['SUFFIXES'][
                                    band_suffix][a_band_lookup_key]
                    b_band_mut = ga_band_mappings[
                        band]['PREFIXES'][
                            band_prefix]['SUFFIXES'][
                                band_suffix][b_band_lookup_key]
                    if (
                        ack.get('in_a_source_name').upper() == 'GA'
                    ) and (
                        ack.get('product').upper() == 'LAM'
                    ):
                        a_band_mut = band_prefix + ack.get(
                            'ga_band_lam_name'
                        ) + '_' + band
                    if band_suffix != 'Empty':
                        a_band_mut = a_band_mut + band_suffix

                    if (
                        ack.get('in_a_source_name').upper() == 'GA'
                    ) and (
                        band.lower().startswith(('satellite', 'solar')
                    )):
                        a_band_mut = band_prefix + ack.get(
                            'ga_band_oa_name'
                        ) + '_' + band
                        if len(oa_band_mutations) > 0:
                            oa_band_mutations[0][1] = a_band_mut
                        else:
                            oa_band_mutations.append([a_band_mut, b_band_mut])
                            oa_plot_measurements.append([
                                band_plot_props[0],
                                ga_band_mappings[
                                    band]['PLOT'][band_plot_props[0]]])
                    else:
                        band_mutations.append([a_band_mut, b_band_mut])
                        plot_measurements.append([
                            band_plot_props[0],
                            ga_band_mappings[
                                band]['PLOT'][band_plot_props[0]]])
    #print(oa_band_mutations)
    #print(len(oa_band_mutations))
    #print(oa_plot_measurements)
    #print(len(oa_plot_measurements))
    #print(band_mutations)
    #print(len(band_mutations))
    #print(plot_measurements)
    #print(len(plot_measurements))

    return (band_mutations, oa_band_mutations,
            plot_measurements, oa_plot_measurements)


def _generate_oa_dfs(in_a_measurements_df, in_b_measurements_df,
    oa_band_mutations, oa_plot_measurements, **ack):
    """(OA) measurements and write the DataFrames used to name matched data files."""

    oa_temp_a_df = None
    oa_temp_b_df = None
    if len(oa_band_mutations) > 0:

        oa_temp_a_df, oa_temp_b_df = _prepare_ab_data(
            in_a_measurements_df, in_a_measurements_df,
            ack.get('band_col'), oa_band_mutations[0][0], oa_band_mutations[0][1],
            ack.get('in_a_measurements_min_valid_pixel_percentage'),
            ack.get('in_b_measurements_min_valid_pixel_percentage'),
            oa_plot_measurements[0][0], **ack)

        oa_temp_a_df.to_csv(
            ack.get(
            'plot_target'
        ) + oa_band_mutations[0][
            0
        ].lower() + '_' + oa_plot_measurements[0][
            0
        ].lower() + '_' + ack.get(
            'in_a_source_name'
        ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')
        oa_temp_b_df.to_csv(
            ack.get(
                'plot_target'
        ) + oa_band_mutations[0][
            1
        ].lower() + '_' + oa_plot_measurements[0][
            0
        ].lower() + '_' + ack.get(
            'in_b_source_name'
        ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')

    return (oa_temp_a_df, oa_temp_b_df)


def _generate_measurements_plots(in_a_measurements_df, in_b_measurements_df,
    band_mutations, plot_measurements,
    oa_temp_a_df, oa_temp_b_df,
    oa_band_mutations, oa_plot_measurements, **ack):
    """Plot measurements and write the DataFrames used to name matched data files."""

    app_config_data = ack.get('app_config_data')

    if in_a_measurements_df is not None and in_b_measurements_df is not None:
        for idx_band_ab, band_ab in enumerate(band_mutations):
            m_fig, m_axs = plt.subplots(2, 1, figsize=(12, 10), squeeze=False)

            temp_a_df, temp_b_df = _prepare_ab_data(
                in_a_measurements_df, in_b_measurements_df,
                ack.get('band_col'), band_ab[0], band_ab[1],
                ack.get('in_a_measurements_min_valid_pixel_percentage'),
                ack.get('in_b_measurements_min_valid_pixel_percentage'),
                plot_measurements[idx_band_ab][0], **ack)

            m_axs[0][0].set(
                xlabel=ack.get('date_col'),
                ylabel=ack.get('measurements_plot_y_label'),
                title=ack.get('measurements_plot_title'),
                xlim=[ack.get('plot_start_date'), ack.get('plot_end_date')]
            )
            ga_product_label = ''
            if ack.get('in_a_source_name').upper() == 'GA':
                ga_product_label = ' ' + ack.get('product_label')
            temp_a_df.to_csv(
                ack.get(
                    'plot_target'
                ) + band_ab[0].lower() + '_' + plot_measurements[
                    idx_band_ab
                ][0].lower() + '_' + ack.get(
                    'in_a_source_name'
                ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')
            temp_b_df.to_csv(
                ack.get(
                    'plot_target'
                ) + band_ab[1].lower() + '_' + plot_measurements[
                    idx_band_ab
                ][0].lower() + '_' + ack.get(
                    'in_b_source_name'
                ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')
            ax = temp_a_df.plot(
                kind=ack.get(
                    'measurements_plot_type'
                ), x=ack.get(
                    'date_col'
                ), y=plot_measurements[idx_band_ab][0], label=plot_measurements[
                    idx_band_ab
                ][1] + ' ' + ack.get(
                    'in_a_source_name'
                ) + ga_product_label, ax=m_axs[0][0])
            ax = temp_b_df.plot(
                kind=ack.get(
                    'measurements_plot_type'
                ), x=ack.get(
                    'date_col'
                ), y=plot_measurements[idx_band_ab][0], label=plot_measurements[
                    idx_band_ab
                ][1] + ' ' + ack.get(
                    'in_b_source_name'
                ), ax=m_axs[0][0])
            if oa_temp_a_df is not None and oa_temp_b_df is not None:
                m_axs[1][0].set(
                    xlabel=ack.get('date_col'),
                    ylabel=ack.get('oa_plot_y_label'),
                    title=ack.get('oa_plot_title'),
                    xlim=[ack.get('plot_start_date'), ack.get('plot_end_date')]
                )
                ax = oa_temp_a_df.plot(
                    kind=ack.get(
                        'measurements_plot_type'
                    ), x=ack.get('date_col'), y=oa_plot_measurements[0][
                        0
                    ], label=oa_plot_measurements[0][
                        1
                    ] + ' ' + oa_band_mutations[0][
                        0
                    ][7:], ax=m_axs[1][0], sharex=m_axs[0][0])
                ax = oa_temp_b_df.plot(
                    kind=ack.get(
                        'measurements_plot_type'
                    ), x=ack.get('date_col'), y=oa_plot_measurements[0][
                        0
                    ], label=oa_plot_measurements[0][
                        1
                    ] + ' ' + oa_band_mutations[0][
                        1
                    ][7:], ax=m_axs[1][0], sharex=m_axs[0][0])
            plot_path = (ack.get(
                'plot_target'
            ) + band_ab[0].lower() + '_' + plot_measurements[
                idx_band_ab
            ][0].lower() + '_' + os.path.splitext(
                ack.get('in_a_measurements_file'))[0]).lower() + '.png'
            print('Writing plot image: ' + plot_path)
            m_fig.autofmt_xdate()
            #plt.show()
            plt.savefig(plot_path)

    return True


def _generate_indices_plots(in_a_indices_df, in_b_indices_df, **ack):
    """Plot indices and write the DataFrames used to name matched data files."""

    app_config_data = ack.get('app_config_data')

    if in_a_indices_df is not None and in_b_indices_df is not None:
        i_fig, i_axs = plt.subplots(
            len(ack.get('spectral_indices')), 1, figsize=(12, 4), squeeze=False)
        for idx_spec_ind, spec_ind in enumerate(ack.get('spectral_indices')):
            spec_ind_measurements = [*app_config_data[
                'SPECTRAL_INDICES'][spec_ind]]
            for measurement in spec_ind_measurements:

                temp_a_df, temp_b_df = _prepare_ab_data(
                    in_a_indices_df, in_b_indices_df,
                    ack.get('indices_col'), spec_ind, spec_ind,
                    ack.get('in_a_indices_min_valid_pixel_percentage'),
                    ack.get('in_b_indices_min_valid_pixel_percentage'),
                    measurement, **ack)

                i_axs[idx_spec_ind][0].set(
                    xlabel=ack.get('date_col'),
                    ylabel=spec_ind,
                    title=ack.get('indices_plot_title'),
                    xlim=[ack.get('plot_start_date'), ack.get('plot_end_date')]
                )
                measurement_label = app_config_data[
                    'SPECTRAL_INDICES'][spec_ind][measurement]
                temp_a_df.to_csv(
                    ack.get(
                        'plot_target'
                    ) + spec_ind.lower() + '_' + measurement.lower() + '_' + ack.get(
                        'in_a_source_name'
                    ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                temp_b_df.to_csv(
                    ack.get(
                        'plot_target'
                    ) + spec_ind.lower() + '_' + measurement.lower() + '_' + ack.get(
                        'in_b_source_name'
                    ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                ax = temp_a_df.plot(
                    kind=ack.get(
                        'indices_plot_type'
                    ), x=ack.get(
                        'date_col'
                    ), y=measurement, label=measurement_label + ' ' + ack.get(
                        'in_a_source_name'
                    ), ax=i_axs[idx_spec_ind][0])
                ax = temp_b_df.plot(
                    kind=ack.get(
                        'indices_plot_type'
                    ), x=ack.get(
                        'date_col'
                    ), y=measurement, label=measurement_label + ' ' + ack.get(
                        'in_b_source_name'
                    ), ax=i_axs[idx_spec_ind][0])
        plot_path = (ack.get('plot_target') + os.path.splitext(
            ack.get('in_a_indices_file'))[0]).lower() + '.png'
        print('Writing plot image: ' + plot_path)
        i_fig.autofmt_xdate()
        #plt.show()
        plt.savefig(plot_path)

    return True


def _prepare_ab_data(in_a_df, in_b_df,
    extract_col, extract_a_val, extract_b_val,
    in_a_min_valid_pixel_percentage, in_b_min_valid_pixel_percentage,
    measurement, **ack):
    """Cleanse, repair and filter (by date) data in preparation for plotting."""

    temp_a_df = in_a_df.loc[in_a_df[extract_col] == extract_a_val]
    temp_a_df.loc[
        temp_a_df[
            'valid_pixel_percentage'] < in_a_min_valid_pixel_percentage, [
                measurement]] = np.nan
    temp_a_df.loc[temp_a_df[measurement] == '--', [measurement]] = np.nan
    #print(temp_a_df)
    temp_b_df = in_b_df.loc[in_b_df[extract_col] == extract_b_val]
    temp_b_df.loc[
        temp_b_df[
            'valid_pixel_percentage'] < in_b_min_valid_pixel_percentage, [
                measurement]] = np.nan
    temp_b_df.loc[temp_b_df[measurement] == '--', [measurement]] = np.nan
    #print(temp_b_df)
    temp_a_df = temp_a_df[temp_a_df[measurement].notna()]
    temp_b_df = temp_b_df[temp_b_df[measurement].notna()]
    temp_a_df[measurement] = pd.to_numeric(temp_a_df[measurement])
    temp_b_df[measurement] = pd.to_numeric(temp_b_df[measurement])
    temp_a_df[ack.get('date_col')] = pd.to_datetime(
        temp_a_df[ack.get('date_col')],
        format=ack.get('standardised_date_format')) #.dt.date
    temp_b_df[ack.get('date_col')] = pd.to_datetime(
        temp_b_df[ack.get('date_col')],
        format=ack.get('standardised_date_format')) #.dt.date
    #print(temp_a_df.dtypes)
    #print(temp_a_df)
    #print(temp_b_df.dtypes)
    #print(temp_b_df)

    return (temp_a_df, temp_b_df)


def _apply_date_filtering(temp_a_df, temp_b_df):

    return (temp_a_df, temp_b_df)


def _get_plot_titles(**ack):
    """Make plot titles."""

    m_title = ack.get(
        'in_a_source_name'
    ) + ' ' + ack.get(
        'in_a_satellite_name'
    ) + ' VS ' + ack.get(
        'in_b_source_name'
    ) + ' ' + ack.get(
        'in_b_satellite_name'
    ) + ' for ' + ack.get(
        'product_label'
    ) + ' at ' + ack.get(
        'site'
    )
    oa_title = ack.get(
        'in_a_source_name'
    ) + ' ' + ack.get(
        'in_a_satellite_name'
    ) + ' VS ' + ack.get(
        'in_a_source_name'
    ) + ' ' + ack.get(
        'in_a_satellite_name'
    ) + ' for ' + ack.get(
        'product_label'
    ) + ' at ' + ack.get(
        'site'
    )
    i_title = m_title

    return (m_title, oa_title, i_title)


def call_next_entry(next_subproject_module, next_entry, path_to_config, config_file):
    """Call the next entry point function in the processing pipeline."""

    run_success = eval('next_subproject_module.' + next_entry + '(path_to_config, config_file)')

    return run_success


if __name__ == "__main__":
    compare(sys.argv[1], sys.argv[2])

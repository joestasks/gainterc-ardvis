"""



"""

import os
from pathlib import Path
import numpy as np


def get_plans(app_configuration, subproject_name):
    """Return a flattened list of standardised plans."""

    ack = _make_app_config_kwargs(app_configuration, subproject_name)
    plans = []

    products = get_products(**ack)
    print('Using these products:-')
    print(products)
    for product in products:
        sites = _get_sites(product, **ack)
        print('Processing these sites:-')
        print(sites)
        for site in sites:
            m_title, oa_title, i_title, esa_oa_title = _get_plot_titles(product, site, **ack)
            plan_properties = {
                "product": product,
                "site": site,
                "in_a_source_name": ack.get('in_a_source_name'),
                "in_b_source_name": ack.get('in_b_source_name'),
                "in_c_source_name": ack.get('in_c_source_name'),
                "in_a_satellite_name": ack.get('in_a_satellite_name'),
                "in_b_satellite_name": ack.get('in_b_satellite_name'),
                "in_c_satellite_name": ack.get('in_c_satellite_name'),
                "in_a_site_path": get_in_site_path('a', product, **ack),
                "in_b_site_path": get_in_site_path('b', product, **ack),
                "in_c_site_path": get_in_site_path('c', product, **ack),
                "in_a_sr_measurements_file": ack.get('in_a_measurements_file'),
                "in_b_sr_measurements_file": ack.get('in_b_measurements_file'),
                "in_a_indices_file": ack.get('in_a_indices_file'),
                "in_b_indices_file": ack.get('in_b_indices_file'),
                "in_c_indices_file": ack.get('in_c_indices_file'),
                "plot_target": get_plot_target(product, site, **ack),
                "all_sites_plot_target": get_all_sites_plot_target(product, **ack),
                "srm_title": m_title,
                "srm_oa_title": oa_title,
                "srm_esa_oa_title": esa_oa_title,
                "indices_title": i_title,
                "rec_max": ack.get('rec_max'),
                "plot_sr_measurements": ack.get('plot_sr_measurements'),
                "plot_indices": ack.get('plot_indices'),
                "ga_bands": ack.get('ga_bands'),
                "ga_band_mappings": ack.get('ga_band_mappings'),
                "ga_oas": ack.get('ga_oas'),
                "ga_oa_mappings": ack.get('ga_oa_mappings'),
                "ga_band_lam_name": ack.get('ga_band_lam_name'),
                "ga_band_oa_name": ack.get('ga_band_oa_name'),
                "plot_start_date": np.datetime64(ack.get('plot_start_date')),
                "plot_end_date": np.datetime64(ack.get('plot_end_date')),
                "in_a_measurements_min_valid_pixel_percentage": ack.get('in_a_measurements_min_valid_pixel_percentage'),
                "in_b_measurements_min_valid_pixel_percentage": ack.get('in_b_measurements_min_valid_pixel_percentage'),
                "in_c_measurements_min_valid_pixel_percentage": ack.get('in_c_measurements_min_valid_pixel_percentage'),
                "in_a_indices_min_valid_pixel_percentage": ack.get('in_a_indices_min_valid_pixel_percentage'),
                "in_b_indices_min_valid_pixel_percentage": ack.get('in_b_indices_min_valid_pixel_percentage'),
                "in_c_indices_min_valid_pixel_percentage": ack.get('in_c_indices_min_valid_pixel_percentage'),
                "sr_measurements_date_filtering": ack.get('sr_measurements_date_filtering'),
                "date_col": ack.get('date_col'),
                "band_col": ack.get('band_col'),
                "standardised_date_format": ack.get('standardised_date_format'),
                "esa_oa_mappings": ack.get('esa_oa_mappings'),
                "plot_style": ack.get('plot_style'),
                "measurements_plot_y_label": ack.get('measurements_plot_y_label'),
                "measurements_plot_type": ack.get('measurements_plot_type'),
                "oa_plot_y_label": ack.get('oa_plot_y_label'),
                "acd": ack.get('acd'),
                "indices_col": ack.get('indices_col'),
                "indices_plot_type": ack.get('indices_plot_type'),
                "in_a_data_path": ack.get('in_a_data_path'),
                "in_a_prefix": ack.get('in_a_prefix'),
                "in_a_same_sensor_date_filter_source": ack.get('in_a_same_sensor_date_filter_source'),
                "in_b_data_path": ack.get('in_b_data_path'),
                "in_b_prefix": ack.get('in_b_prefix'),
                "in_b_same_sensor_date_filter_source": ack.get('in_b_same_sensor_date_filter_source'),
                "in_c_data_path": ack.get('in_c_data_path'),
                "in_c_prefix": ack.get('in_c_prefix'),
                "in_c_same_sensor_date_filter_source": ack.get('in_c_same_sensor_date_filter_source'),
                "product_label": get_product_label(product, **ack),
                "spectral_indices": ack.get('spectral_indices'),
                "test_ref_base": ack.get('test_ref_base'),
                "test_ref_path": get_test_ref_path(product, site, **ack),
                "indices_same_sensor_date_filtering": ack.get('indices_same_sensor_date_filtering'),
                "in_a_same_sensor_date_filter_source": ack.get('in_a_same_sensor_date_filter_source'),
                "in_b_same_sensor_date_filter_source": ack.get('in_b_same_sensor_date_filter_source'),
                "in_c_same_sensor_date_filter_source": ack.get('in_c_same_sensor_date_filter_source'),
            }

            plans.append(plan_properties)

    return (plans, ack)


def _make_app_config_kwargs(app_c, subp_name):

    acd = app_c['APP_SOURCE']['SUBPROJECTS'][subp_name]['DATA']
    ack = {
        "acd": acd,
        "in_a_measurements_min_valid_pixel_percentage": acd['COMPARISON_SOURCES']['A']['MEASUREMENTS_MIN_VALID_PIXEL_PERCENTAGE'],
        "in_b_measurements_min_valid_pixel_percentage": acd['COMPARISON_SOURCES']['B']['MEASUREMENTS_MIN_VALID_PIXEL_PERCENTAGE'],
        "in_c_measurements_min_valid_pixel_percentage": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['MEASUREMENTS_MIN_VALID_PIXEL_PERCENTAGE']) or None,
        "in_a_indices_min_valid_pixel_percentage": acd['COMPARISON_SOURCES']['A']['INDICES_MIN_VALID_PIXEL_PERCENTAGE'],
        "in_b_indices_min_valid_pixel_percentage": acd['COMPARISON_SOURCES']['B']['INDICES_MIN_VALID_PIXEL_PERCENTAGE'],
        "in_c_indices_min_valid_pixel_percentage": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['INDICES_MIN_VALID_PIXEL_PERCENTAGE']) or None,
        "plot_sr_measurements": acd['PLOT_SR_MEASUREMENTS'],
        "plot_indices": acd['PLOT_INDICES'],
        "sr_measurements_date_filtering": acd['SR_MEASUREMENTS_DATE_FILTERING'],
        "indices_same_sensor_date_filtering": acd['INDICES_SAME_SENSOR_DATE_FILTERING'],
        "standardised_date_format": acd['STANDARDISED_DATE_FORMAT'],
        "plot_start_date": acd['PLOT_START_DATE'],
        "plot_end_date": acd['PLOT_END_DATE'],
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
        "esa_oa_mappings": ('ESA_OA_MAPPINGS' in [*acd] and acd['ESA_OA_MAPPINGS']) or {},
        "ga_band_mappings": acd['GA_BAND_MAPPINGS'],
        "ga_bands": [*acd['GA_BAND_MAPPINGS']],
        "in_a_data_path": acd['IN_BASE'],
        "in_a_prefix": acd['COMPARISON_SOURCES']['A']['PREFIX'],
        "in_a_source_name": acd['COMPARISON_SOURCES']['A']['SOURCE_NAME'],
        "in_a_satellite_name": acd['COMPARISON_SOURCES']['A']['SATELLITE_NAME'],
        "in_a_product": acd['COMPARISON_SOURCES']['A']['PRODUCT'],
        "in_a_site": acd['COMPARISON_SOURCES']['A']['SITE'],
        "in_a_measurements_file": acd['COMPARISON_SOURCES']['A']['MEASUREMENTS_FILE'],
        "in_a_indices_file": acd['COMPARISON_SOURCES']['A']['INDICES_FILE'],
        "in_a_same_sensor_date_filter_source": ('SAME_SENSOR_DATE_FILTER_SOURCE' in [*acd['COMPARISON_SOURCES']['A']] and acd['COMPARISON_SOURCES']['A']['SAME_SENSOR_DATE_FILTER_SOURCE']) or '',
        "in_b_data_path": acd['IN_BASE'],
        "in_b_prefix": acd['COMPARISON_SOURCES']['B']['PREFIX'],
        "in_b_source_name": acd['COMPARISON_SOURCES']['B']['SOURCE_NAME'],
        "in_b_satellite_name": acd['COMPARISON_SOURCES']['B']['SATELLITE_NAME'],
        "in_b_product": acd['COMPARISON_SOURCES']['B']['PRODUCT'],
        "in_b_site": acd['COMPARISON_SOURCES']['B']['SITE'],
        "in_b_measurements_file": acd['COMPARISON_SOURCES']['B']['MEASUREMENTS_FILE'],
        "in_b_indices_file": acd['COMPARISON_SOURCES']['B']['INDICES_FILE'],
        "in_b_same_sensor_date_filter_source": ('SAME_SENSOR_DATE_FILTER_SOURCE' in [*acd['COMPARISON_SOURCES']['B']] and acd['COMPARISON_SOURCES']['B']['SAME_SENSOR_DATE_FILTER_SOURCE']) or '',
        "in_c_data_path": acd['IN_BASE'],
        "in_c_prefix": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['PREFIX']) or '',
        "in_c_source_name": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['SOURCE_NAME']) or '',
        "in_c_satellite_name": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['SATELLITE_NAME']) or '',
        "in_c_product": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['PRODUCT']) or '',
        "in_c_site": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['SITE']) or '',
        "in_c_measurements_file": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['MEASUREMENTS_FILE']) or '',
        "in_c_indices_file": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['INDICES_FILE']) or '',
        "in_c_same_sensor_date_filter_source": ('C' in [*acd['COMPARISON_SOURCES']] and acd['COMPARISON_SOURCES']['C']['SAME_SENSOR_DATE_FILTER_SOURCE']) or '',
        "out_path": acd['OUT_BASE'],
        "rec_max": app_c['APP_SOURCE']['DATA_RECORD_MAX_LIMIT'],
        "test_ref_base": acd['TEST_REF_BASE'],
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
        lambda x: (x is not None and '_' + x) or ('')
    )(ack.get('in_b_product')) + '/'
    if ack.get('in_c_source_name'):
        ack['in_c_site_path'] = ack.get(
            'in_c_data_path'
        ) + '/' + ack.get(
            'in_c_prefix'
        ) + '_' + ack.get(
            'in_c_source_name'
        ) + '_' + ack.get(
            'in_c_satellite_name'
        ) + (
            lambda x: (len(x) > 0 and '_' + x) or ('')
        )(ack.get('in_c_product')) + '/'
    else:
        ack['in_c_site_path'] = ''

    return ack


def get_products(**ack):

    products = None
    if ack.get('in_a_product') is None:
        products = ack.get('ga_algorithms')
    else:
        products = list((ack.get('in_a_product'),))

    return products


def _get_sites(s_product, **ack):

    site_paths = None
    if ack.get('in_a_site') is None:
        site_paths = list(Path(get_in_site_path('a', s_product, **ack)).glob('**'))
        site_paths.pop(0)
    else:
        site_paths = list((get_in_site_path('a', s_product, **ack) + ack.get('in_a_site'),))
    print('Found these site paths:-')
    print(site_paths)
    sites = list(map(lambda x: os.path.basename(os.path.normpath(x)), site_paths))

    return sites


def get_product_label(s_product, **ack):

    product_label = ''
    if s_product:
        product_label = ' for ' + ack.get('acd')['GA_ALGORITHMS'][s_product]

    return product_label


def get_in_site_path(inn, s_product, **ack):

    site_path = ack.get(f"in_{inn}_site_path")
    if ack.get(f"in_{inn}_source_name").upper() == 'GA':
        site_path = ack.get(
            f"in_{inn}_data_path"
        ) + '/' + ack.get(
            f"in_{inn}_prefix"
        ) + '_' + ack.get(
            f"in_{inn}_source_name"
        ) + '_' + ack.get(
            f"in_{inn}_satellite_name"
        ) + '_' + s_product + '/'

    return site_path


def _get_plot_titles(t_product, t_site, **ack):
    """Make plot titles."""

    m_title = ack.get(
        'in_a_source_name'
    ) + ' ' + ack.get(
        'in_a_satellite_name'
    ) + ' VS ' + ack.get(
        'in_b_source_name'
    ) + ' ' + ack.get(
        'in_b_satellite_name'
    ) + get_product_label(
        t_product, **ack
    ) + ' at ' + t_site
    oa_title = ack.get(
        'in_a_source_name'
    ) + ' ' + ack.get(
        'in_a_satellite_name'
    ) + get_product_label(
        t_product, **ack
    ) + ' at ' + t_site
    i_title = m_title
    if len(ack.get(
        'in_c_source_name'
    )) > 0 and len(ack.get(
        'in_c_satellite_name'
    )) > 0:
        i_title = ack.get(
            'in_a_source_name'
        ) + ' ' + ack.get(
            'in_a_satellite_name'
        ) + ' VS ' + ack.get(
            'in_b_source_name'
        ) + ' ' + ack.get(
            'in_b_satellite_name'
        ) + ' VS ' + ack.get(
            'in_c_source_name'
        ) + ' ' + ack.get(
            'in_c_satellite_name'
        ) + ' at ' + t_site
    esa_oa_title = ack.get(
        'in_b_source_name'
    ) + ' ' + ack.get(
        'in_b_satellite_name'
    ) + ' at ' + t_site

    return (m_title, oa_title, i_title, esa_oa_title)


def get_plot_target(t_product, t_site, **ack):

    plot_target = ack.get(
            'out_path'
        ) + '/' + ack.get(
            'in_a_source_name'
        ).lower() + '_' + ack.get(
            'in_a_satellite_name'
        ).lower() + '_vs_' + ack.get(
            'in_b_source_name'
        ).lower() + '_' + ack.get(
            'in_b_satellite_name'
        ).lower() + '/' + t_product.lower() + '/' + t_site.lower() + '/'

    return plot_target


def get_test_ref_path(t_product, t_site, **ack):

    plot_target = ack.get(
            'test_ref_base'
        ) + '/' + ack.get(
            'in_a_source_name'
        ).lower() + '_' + ack.get(
            'in_a_satellite_name'
        ).lower() + '_vs_' + ack.get(
            'in_b_source_name'
        ).lower() + '_' + ack.get(
            'in_b_satellite_name'
        ).lower() + '/' + t_product.lower() + '/' + (
            (t_site is not None and t_site.lower() + '/') or ''
        )

    return plot_target


def get_all_sites_plot_target(t_product, **ack):

    all_sites_plot_target = ack.get(
            'out_path'
        ) + '/' + ack.get(
            'in_a_source_name'
        ).lower() + '_' + ack.get(
            'in_a_satellite_name'
        ).lower() + '_vs_' + ack.get(
            'in_b_source_name'
        ).lower() + '_' + ack.get(
            'in_b_satellite_name'
        ).lower() + '/' + t_product.lower() + '/'

    return all_sites_plot_target

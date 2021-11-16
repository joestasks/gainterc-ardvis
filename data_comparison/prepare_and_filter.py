"""



"""

from pathlib import Path
import pandas as pd
pd.options.mode.chained_assignment = None
from pandas._testing import assert_frame_equal
import numpy as np


def prepare_ab_data(in_a_df, in_b_df, in_c_df,
    extract_col, extract_a_val, extract_b_val, extract_c_val,
    in_a_min_valid_pixel_percentage, in_b_min_valid_pixel_percentage,
    in_c_min_valid_pixel_percentage, measurement, do_date_filtering, plan):
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
    temp_c_df = None
    if in_c_df is not None:
        temp_c_df = in_c_df.loc[in_c_df[extract_col] == extract_c_val]
        temp_c_df.loc[
            temp_c_df[
                'valid_pixel_percentage'] < in_c_min_valid_pixel_percentage, [
                    measurement]] = np.nan
        temp_c_df.loc[temp_c_df[measurement] == '--', [measurement]] = np.nan
        #print(temp_c_df)
        temp_c_df = temp_c_df[temp_c_df[measurement].notna()]
        temp_c_df[measurement] = pd.to_numeric(temp_c_df[measurement])
    temp_a_df = temp_a_df[temp_a_df[measurement].notna()]
    temp_b_df = temp_b_df[temp_b_df[measurement].notna()]
    temp_a_df[measurement] = pd.to_numeric(temp_a_df[measurement])
    temp_b_df[measurement] = pd.to_numeric(temp_b_df[measurement])

    if do_date_filtering:
        temp_a_df, temp_b_df, temp_c_df = _apply_date_filtering(
            temp_a_df, temp_b_df, temp_c_df, plan)

    temp_a_df[plan.get('date_col')] = pd.to_datetime(
        temp_a_df[plan.get('date_col')],
        format=plan.get('standardised_date_format'))
    temp_b_df[plan.get('date_col')] = pd.to_datetime(
        temp_b_df[plan.get('date_col')],
        format=plan.get('standardised_date_format'))
    if temp_c_df is not None:
        temp_c_df[plan.get('date_col')] = pd.to_datetime(
            temp_c_df[plan.get('date_col')],
            format=plan.get('standardised_date_format'))
    #print(temp_a_df.dtypes)
    #print(temp_a_df)
    #print(temp_b_df.dtypes)
    #print(temp_b_df)
    #print(temp_c_df.dtypes)
    #print(temp_c_df)

    return (temp_a_df, temp_b_df, temp_c_df)


def _apply_date_filtering(temp_a_df, temp_b_df, temp_c_df, plan):
    """Apply date filtering to match dates and ensure the same number of
       aligned data points from each data set."""

    temp_a_df[plan.get('date_col')] = pd.to_datetime(
        temp_a_df[plan.get('date_col')],
        format=plan.get('standardised_date_format')).dt.date
    temp_b_df[plan.get('date_col')] = pd.to_datetime(
        temp_b_df[plan.get('date_col')],
        format=plan.get('standardised_date_format')).dt.date
    res = pd.merge(
        temp_a_df.assign(
            grouper=pd.to_datetime(
                temp_a_df[plan.get('date_col')]
            ).dt.to_period('D')),
        temp_b_df.assign(
            grouper=pd.to_datetime(
                temp_b_df[plan.get('date_col')]
            ).dt.to_period('D')),
        how='inner', on='grouper',
        suffixes=('_' + plan.get('in_a_source_name') + plan.get('in_a_satellite_name'),
                  '_' + plan.get('in_b_source_name') + plan.get('in_b_satellite_name')))
    temp_a_df = res.loc[:, res.columns.str.endswith(
        '_' + plan.get('in_a_source_name') + plan.get('in_a_satellite_name'))]
    temp_a_df.columns = temp_a_df.columns.str.rstrip(
        '_' + plan.get('in_a_source_name') + plan.get('in_a_satellite_name'))
    temp_b_df = res.loc[:, res.columns.str.endswith(
        '_' + plan.get('in_b_source_name') + plan.get('in_b_satellite_name'))]
    temp_b_df.columns = temp_b_df.columns.str.rstrip(
        '_' + plan.get('in_b_source_name') + plan.get('in_b_satellite_name'))

    if temp_c_df is not None:
        temp_c_df[plan.get('date_col')] = pd.to_datetime(
            temp_c_df[plan.get('date_col')],
            format=plan.get('standardised_date_format')).dt.date
        res2 = pd.merge(
            temp_a_df.assign(
                grouper=pd.to_datetime(
                    temp_a_df[plan.get('date_col')]
                ).dt.to_period('D')),
            temp_c_df.assign(
                grouper=pd.to_datetime(
                    temp_c_df[plan.get('date_col')]
                ).dt.to_period('D')),
            how='inner', on='grouper',
            suffixes=('_' + plan.get('in_a_source_name') + plan.get('in_a_satellite_name'),
                      '_' + plan.get('in_c_source_name') + plan.get('in_c_satellite_name')))
        temp_a_df = res2.loc[:, res2.columns.str.endswith(
            '_' + plan.get('in_a_source_name') + plan.get('in_a_satellite_name'))]
        temp_a_df.columns = temp_a_df.columns.str.rstrip(
            '_' + plan.get('in_a_source_name') + plan.get('in_a_satellite_name'))
        temp_c_df = res2.loc[:, res2.columns.str.endswith(
            '_' + plan.get('in_c_source_name') + plan.get('in_c_satellite_name'))]
        temp_c_df.columns = temp_c_df.columns.str.rstrip(
            '_' + plan.get('in_c_source_name') + plan.get('in_c_satellite_name'))

    return (temp_a_df, temp_b_df, temp_c_df)


def get_min_max_mean(temp_a_df, temp_b_df, y_col_name, plan):

    res = pd.merge(
        temp_a_df.assign(
            grouper=pd.to_datetime(
                temp_a_df[plan.get('date_col')]
            ).dt.to_period('D')),
        temp_b_df.assign(
            grouper=pd.to_datetime(
                temp_b_df[plan.get('date_col')]
            ).dt.to_period('D')),
        how='inner', on='grouper',
        suffixes=('_' + plan.get('in_a_source_name') + plan.get('in_a_satellite_name'),
                  '_' + plan.get('in_b_source_name') + plan.get('in_b_satellite_name')))
    res['msr_diff'] = (
        res[
            y_col_name + '_' + plan.get('in_a_source_name') + plan.get('in_a_satellite_name')
        ] - res[
            y_col_name + '_' + plan.get('in_b_source_name') + plan.get('in_b_satellite_name')
        ]
    )
    msr_diff_min = res['msr_diff'].min()
    msr_diff_max = res['msr_diff'].max()
    msr_diff_mean = res['msr_diff'].mean()
    #print(msr_diff_min)
    #print(msr_diff_max)
    #print(msr_diff_mean)
    #print(res)

    return (msr_diff_min, msr_diff_max, msr_diff_mean)


def apply_indices_same_sensor_date_filtering(
    temp_a_df, temp_b_df, temp_c_df, spec_ind, measurement, ssdf_algref, generate_df, plan):

    in_a_site_path = plan.get(
        'in_a_data_path'
    ) + '/' + plan.get(
        'in_a_prefix'
    ) + '_' + plan.get(
        'in_a_same_sensor_date_filter_source'
    ) + '_' + plan.get(
        'in_a_satellite_name'
    ) + '/'
    in_b_site_path = plan.get(
        'in_b_data_path'
    ) + '/' + plan.get(
        'in_b_prefix'
    ) + '_' + plan.get(
        'in_b_same_sensor_date_filter_source'
    ) + '_' + plan.get(
        'in_b_satellite_name'
    ) + '/'
    in_c_site_path = ''
    if plan.get('in_c_source_name'):
        in_c_site_path = plan.get(
            'in_c_data_path'
        ) + '/' + plan.get(
            'in_c_prefix'
        ) + '_' + plan.get(
            'in_c_same_sensor_date_filter_source'
        ) + '_' + plan.get(
            'in_c_satellite_name'
        ) + '/'
    if plan.get('in_a_same_sensor_date_filter_source').upper() == 'GA':
        in_a_site_path = plan.get(
            'in_a_data_path'
        ) + '/' + plan.get(
            'in_a_prefix'
        ) + '_' + plan.get(
            'in_a_same_sensor_date_filter_source'
        ) + '_' + plan.get(
            'in_a_satellite_name'
        ) + '_' + ssdf_algref + '/'
    if plan.get('in_b_same_sensor_date_filter_source').upper() == 'GA':
        in_b_site_path = plan.get(
            'in_b_data_path'
        ) + '/' + plan.get(
            'in_b_prefix'
        ) + '_' + plan.get(
            'in_b_same_sensor_date_filter_source'
        ) + '_' + plan.get(
            'in_b_satellite_name'
        ) + '_' + ssdf_algref + '/'
    if plan.get('in_c_same_sensor_date_filter_source').upper() == 'GA':
        in_c_site_path = plan.get(
            'in_c_data_path'
        ) + '/' + plan.get(
            'in_c_prefix'
        ) + '_' + plan.get(
            'in_c_same_sensor_date_filter_source'
        ) + '_' + plan.get(
            'in_c_satellite_name'
        ) + '_' + ssdf_algref + '/'
    this_in_a_site_path = in_a_site_path + plan.get('site')
    this_in_b_site_path = in_b_site_path + plan.get('site')
    this_in_c_site_path = in_c_site_path + plan.get('site')
    in_a_indices_path = Path(this_in_a_site_path + '/' + plan.get('in_a_indices_file'))
    in_b_indices_path = Path(this_in_b_site_path + '/' + plan.get('in_b_indices_file'))
    in_c_indices_path = Path(this_in_c_site_path + '/' + plan.get('in_c_indices_file'))
    in_a_indices_df = generate_df.get_df_from_csv(in_a_indices_path, plan.get('rec_max'))
    in_b_indices_df = generate_df.get_df_from_csv(in_b_indices_path, plan.get('rec_max'))
    in_c_indices_df = None
    if plan.get('in_c_source_name'):
        in_c_indices_df = generate_df.get_df_from_csv(in_c_indices_path, plan.get('rec_max'))
    #print(in_a_indices_path)
    #print(in_b_indices_path)
    #print(in_c_indices_path)
    #print(in_a_indices_df, in_b_indices_df, in_c_indices_df)

    new_temp_a_df = temp_a_df
    if in_a_indices_df is not None:
        new_temp_a_df, junk_b_df, junk_c_df = prepare_ab_data(
            temp_a_df, in_a_indices_df, None,
            plan.get('indices_col'),
            spec_ind, spec_ind, None,
            plan.get('in_a_indices_min_valid_pixel_percentage'),
            plan.get('in_a_indices_min_valid_pixel_percentage'),
            None,
            measurement,
            True, plan)
    new_temp_b_df = temp_b_df
    if in_b_indices_df is not None:
        new_temp_b_df, junk_b_df, junk_c_df = prepare_ab_data(
            temp_b_df, in_b_indices_df, None,
            plan.get('indices_col'),
            spec_ind, spec_ind, None,
            plan.get('in_b_indices_min_valid_pixel_percentage'),
            plan.get('in_b_indices_min_valid_pixel_percentage'),
            None,
            measurement,
            True, plan)
    new_temp_c_df = temp_c_df
    if in_c_indices_df is not None:
        new_temp_c_df, junk_b_df, junk_c_df = prepare_ab_data(
            temp_c_df, in_c_indices_df, None,
            plan.get('indices_col'),
            spec_ind, spec_ind, None,
            plan.get('in_c_indices_min_valid_pixel_percentage'),
            plan.get('in_c_indices_min_valid_pixel_percentage'),
            None,
            measurement,
            True, plan)

    return (new_temp_a_df, new_temp_b_df, new_temp_c_df)


def prepare_min_max_mean(sr_diff_all_sites, band_mutations, msr_diff_header,
    plot_plan, generate_df, **ack):

    products = plot_plan.get_products(**ack)
    for product in products:
        all_sites_df = sr_diff_all_sites[
            product
        ][
            sr_diff_all_sites[
                product
            ]['mean'].notna()
        ]
        all_sites_df.to_csv(
            plot_plan.get_all_sites_plot_target(
                product, **ack
            ) + 'all_sites_msr_diff_temp.csv',
            index=False, sep=',', quotechar='|')
        test_against_msr_diff_ref(
            all_sites_df,
            product,
            'all_sites_msr_diff_temp.csv',
            plot_plan,
            generate_df,
            **ack)
        new_rows = []
        for idx_band_ab, band_ab in enumerate(band_mutations.get(product)):
            band_id_df = all_sites_df.loc[all_sites_df['band'] == band_ab[0] + ':' + band_ab[1]]
            band_id_df['mean'] = pd.to_numeric(band_id_df['mean'])
            band_id_df['acq'] = pd.to_numeric(band_id_df['acq'])
            band_id_df['mean_x_acq'] = band_id_df['mean'] * band_id_df['acq']
            total_mean = band_id_df['mean_x_acq'].sum()
            total_acq = band_id_df['acq'].sum()
            all_sites_mean = total_mean / total_acq
            new_rows.append([band_ab[0] + ':' + band_ab[1], band_id_df['min'].min(), band_id_df['max'].max(), all_sites_mean, str(total_acq)])

        msr_diff_df = pd.DataFrame(new_rows, columns=msr_diff_header)
        msr_diff_df.to_csv(
            plot_plan.get_all_sites_plot_target(
                product, **ack
            ) + 'summary_msr_diff_temp.csv',
            index=False, sep=',', quotechar='|')
        test_against_msr_diff_ref(
            msr_diff_df,
            product,
            'summary_msr_diff_temp.csv',
            plot_plan,
            generate_df,
            **ack)

    return True


def test_against_msr_diff_ref(temp_df, product, file_name,
    plot_plan, generate_df, **ack):

    test_result = False
    if ack.get('test_ref_base') is not None:
        ref_file_path = plot_plan.get_test_ref_path(
            product, '.', **ack
        ) + file_name
        ref_df = generate_df.get_df_from_csv(Path(ref_file_path), ack.get('rec_max'), True)
        if temp_df is not None and ref_df is not None:
            ref_df[ack.get('date_col')] = pd.to_datetime(
                ref_df[ack.get('date_col')],
                format=ack.get('standardised_date_format'))
            #clean_index_temp_df = temp_df.reset_index(drop=True)
            #ref_df.reset_index(drop=True, inplace=True)
            print('Verifying DataFrame against reference output: ' + ref_file_path)
            test_result = (assert_frame_equal(
                temp_df,
                ref_df
            ) is None and True) or False

    return test_result

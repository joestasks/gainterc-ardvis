"""



"""

import pandas as pd


def p2f(x):
    return float(x.strip('%')) / 100


def get_df_from_csv(file_path, rec_max, no_p2f=False):
    """Read CSV file and return DataFrame."""

    converters_spec = {'valid_pixel_percentage': p2f}
    if no_p2f is not None and no_p2f:
        converters_spec = {}
    new_df = None
    if file_path.is_file():
        new_df = pd.read_csv(
            file_path,
            nrows=rec_max,
            sep=',',
            skipinitialspace=False,
            quotechar='|',
            converters=converters_spec)
            
        #print(new_df)

    return new_df


def generate_oa_dfs(in_a_measurements_df, in_b_measurements_df,
    oa_band_mutations, oa_plot_measurements, prepare_and_filter, plan):
    """Prepare other/additional attributes (OAs) and write the DataFrames
       used to name matched data files."""

    # Note that B(b) is not used yet, as only GA supported for now.
    oa_temp_a_df = None
    oa_temp_b_df = None
    if in_a_measurements_df is not None and len(oa_band_mutations) > 0:

        oa_temp_a_df, oa_temp_b_df, oa_temp_c_df = prepare_and_filter.prepare_ab_data(
            in_a_measurements_df, in_a_measurements_df, None,
            plan.get('band_col'),
            oa_band_mutations[0][0], oa_band_mutations[0][1], None,
            plan.get('in_a_measurements_min_valid_pixel_percentage'),
            plan.get('in_a_measurements_min_valid_pixel_percentage'),
            None,
            oa_plot_measurements[0][0],
            plan.get('sr_measurements_date_filtering'), plan)

        # Remove duplicate data set to prevent plotting;
        # occurs when single OA only.
        if oa_band_mutations[0][0] == oa_band_mutations[0][1]:
            oa_temp_b_df = None

    return (oa_temp_a_df, oa_temp_b_df)

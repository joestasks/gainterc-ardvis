"""



"""

import os
from pathlib import Path
import pandas as pd
from pandas._testing import assert_frame_equal
import matplotlib.pyplot as plt


def generate_indices_plots(in_a_indices_df, in_b_indices_df, in_c_indices_df,
    i_title, prepare_and_filter, generate_df, plan):
    """Plot indices and write the DataFrames used to name matched data files."""

    plt.style.use(plan.get('plot_style'))
    plt.close('all')

    if in_a_indices_df is not None and in_b_indices_df is not None:
        for idx_spec_ind, spec_ind in enumerate(plan.get('spectral_indices')):
            spec_ind_measurements = [*(plan.get('acd')[
                'SPECTRAL_INDICES'][spec_ind])]
            for measurement in spec_ind_measurements:
                i_fig, i_axs = plt.subplots(
                    1, 1, figsize=(12, 4), squeeze=False)

                temp_a_df, temp_b_df, temp_c_df = prepare_and_filter.prepare_ab_data(
                    in_a_indices_df, in_b_indices_df, in_c_indices_df,
                    plan.get('indices_col'),
                    spec_ind, spec_ind, spec_ind,
                    plan.get('in_a_indices_min_valid_pixel_percentage'),
                    plan.get('in_b_indices_min_valid_pixel_percentage'),
                    plan.get('in_c_indices_min_valid_pixel_percentage'),
                    measurement,
                    False, plan)
                if plan.get('indices_same_sensor_date_filtering'):
                    (
                        temp_a_df, temp_b_df, temp_c_df
                    ) = prepare_and_filter.apply_indices_same_sensor_date_filtering(
                        temp_a_df, temp_b_df, temp_c_df, spec_ind, measurement,
                        plan.get('product'), generate_df, plan)

                # Save data files of plot data.
                measurement_label = plan.get('acd')[
                    'SPECTRAL_INDICES'][spec_ind][measurement]
                temp_a_df.to_csv(
                    plan.get(
                        'plot_target'
                    ) + spec_ind.lower() + '_' + plan.get(
                        'in_a_source_name'
                    ).lower() + '_' + plan.get(
                        'in_a_satellite_name'
                    ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                test_against_indices_ref(
                    temp_a_df,
                    spec_ind.lower(),
                    plan.get('in_a_source_name').lower(),
                    plan.get('in_a_satellite_name').lower(),
                    generate_df,
                    plan)
                temp_b_df.to_csv(
                    plan.get(
                        'plot_target'
                    ) + spec_ind.lower() + '_' + plan.get(
                        'in_b_source_name'
                    ).lower() + '_' + plan.get(
                        'in_b_satellite_name'
                    ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                test_against_indices_ref(
                    temp_b_df,
                    spec_ind.lower(),
                    plan.get('in_b_source_name').lower(),
                    plan.get('in_b_satellite_name').lower(),
                    generate_df,
                    plan)
                if in_c_indices_df is not None and temp_c_df is not None:
                    temp_c_df.to_csv(
                        plan.get(
                            'plot_target'
                        ) + spec_ind.lower() + '_' + plan.get(
                            'in_c_source_name'
                        ).lower() + '_' + plan.get(
                            'in_c_satellite_name'
                        ).lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                    test_against_indices_ref(
                        temp_c_df,
                        spec_ind.lower(),
                        plan.get('in_c_source_name').lower(),
                        plan.get('in_c_satellite_name').lower(),
                        generate_df,
                        plan)

                # Do plotting.
                i_axs[0][0].set(
                    xlabel=plan.get('date_col'),
                    ylabel=spec_ind,
                    title=i_title,
                    xlim=[plan.get('plot_start_date'), plan.get('plot_end_date')]
                )
                ax = temp_a_df.plot(
                    kind=plan.get(
                        'indices_plot_type'
                    ), x=plan.get(
                        'date_col'
                    ), y=measurement, label=measurement_label + ' ' + plan.get(
                        'in_a_source_name'
                    ) + ' ' + plan.get(
                        'in_a_satellite_name'
                    ),
                    c='r',
                    marker='o',
                    edgecolors='black',
                    s=30,
                    ax=i_axs[0][0])
                ax = temp_b_df.plot(
                    kind=plan.get(
                        'indices_plot_type'
                    ), x=plan.get(
                        'date_col'
                    ), y=measurement, label=measurement_label + ' ' + plan.get(
                        'in_b_source_name'
                    ) + ' ' + plan.get(
                        'in_b_satellite_name'
                    ),
                    c='b',
                    marker='v',
                    ax=i_axs[0][0])
                if in_c_indices_df is not None and temp_c_df is not None:
                    ax = temp_c_df.plot(
                        kind=plan.get(
                            'indices_plot_type'
                        ), x=plan.get(
                            'date_col'
                        ), y=measurement, label=measurement_label + ' ' + plan.get(
                            'in_c_source_name'
                        ) + ' ' + plan.get(
                            'in_c_satellite_name'
                        ),
                        c='g',
                        marker='s',
                        s=10,
                        ax=i_axs[0][0])
                plt.ylabel(spec_ind)  # weird fix for scatter

                plot_path = plan.get(
                    'plot_target'
                ) + spec_ind.lower() + '_' + os.path.splitext(
                    plan.get('in_a_indices_file'))[0].lower() + '.png'
                print('Writing plot image: ' + plot_path)
                i_fig.autofmt_xdate()
                #plt.show()
                plt.savefig(plot_path)
                plt.close(i_fig)

    return True


def test_against_indices_ref(temp_df, spec_ind, source_name, satellite_name,
    generate_df, plan):

    test_result = False
    if plan.get('test_ref_base') is not None:
        ref_file_path = plan.get(
                'test_ref_path'
            ) + spec_ind + '_' + source_name + '_' + satellite_name + '_temp.csv'
        ref_df = generate_df.get_df_from_csv(Path(ref_file_path), plan.get('rec_max'), True)
        if temp_df is not None and ref_df is not None:
            ref_df[plan.get('date_col')] = pd.to_datetime(
                ref_df[plan.get('date_col')],
                format=plan.get('standardised_date_format'))
            #clean_index_temp_df = temp_df.reset_index(drop=True)
            #ref_df.reset_index(drop=True, inplace=True)
            print('Verifying DataFrame against reference output: ' + ref_file_path)
            test_result = (assert_frame_equal(
                temp_df,
                ref_df
            ) is None and True) or False

    return test_result

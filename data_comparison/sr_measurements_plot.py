"""



"""

import os
from pathlib import Path
import pandas as pd
from pandas._testing import assert_frame_equal
import matplotlib.pyplot as plt


def generate_measurements_plots(in_a_measurements_df, in_b_measurements_df,
    band_mutations, plot_measurements,
    oa_in_a_df, oa_in_b_df,
    oa_band_mutations, oa_plot_measurements,
    esa_oa_in_a_df, esa_oa_in_b_df,
    esa_oa_band_mutations, esa_oa_plot_measurements,
    sr_diff_all_sites,
    m_title, oa_title, esa_oa_title, msr_diff_header,
    prepare_and_filter, generate_df, plan):
    """Plot measurements and write the DataFrames used to name matched data files."""

    plt.close('all')
    plt.style.use(plan.get('plot_style'))
    temp_a_df = None
    temp_b_df = None
    oa_temp_a_df = None
    oa_temp_b_df = None
    ratio_dfs = {}

    if in_a_measurements_df is not None and in_b_measurements_df is not None:
        for idx_band_ab, band_ab in enumerate(band_mutations):
            m_fig, m_axs = plt.subplots(
                (len(esa_oa_band_mutations) > 0 and 3) or 2,
                1, figsize=(12, 10), squeeze=False)

            temp_a_df, temp_b_df, temp_c_df = prepare_and_filter.prepare_ab_data(
                in_a_measurements_df, in_b_measurements_df, None,
                plan.get('band_col'),
                band_ab[0], band_ab[1], None,
                plan.get('in_a_measurements_min_valid_pixel_percentage'),
                plan.get('in_b_measurements_min_valid_pixel_percentage'),
                None,
                plot_measurements[idx_band_ab][0],
                plan.get('sr_measurements_date_filtering'), plan)
            msr_diff_min, msr_diff_max, msr_diff_mean = prepare_and_filter.get_min_max_mean(temp_a_df, temp_b_df, plot_measurements[idx_band_ab][0], plan)
            msr_diff_df = pd.DataFrame(columns=msr_diff_header)
            msr_diff_df.loc[0] = [plan.get('site'), band_ab[0] + ':' + band_ab[1], msr_diff_min, msr_diff_max, msr_diff_mean, str(len(temp_a_df.index))]
            sr_diff_all_sites[plan.get('product')] = sr_diff_all_sites[plan.get('product')].append([msr_diff_df])

            msr_diff_df.to_csv(
                plan.get('plot_target') + band_ab[0].lower() + '_' + plot_measurements[
                    idx_band_ab
                ][0].lower() + '_diff_temp.csv',
                index=False, sep=',', quotechar='|')

            if len(oa_band_mutations) > 0:
                temp_a_df, oa_temp_a_df, oa_temp_b_df = prepare_and_filter.prepare_ab_data(
                    temp_a_df, oa_in_a_df, oa_in_b_df,
                    plan.get('band_col'),
                    band_ab[0], oa_band_mutations[0][0], oa_band_mutations[0][1],
                    plan.get('in_a_measurements_min_valid_pixel_percentage'),
                    plan.get('in_a_measurements_min_valid_pixel_percentage'),
                    plan.get('in_a_measurements_min_valid_pixel_percentage'),
                    oa_plot_measurements[0][0],
                    plan.get('sr_measurements_date_filtering'), plan)
            if oa_temp_a_df is not None:
                oa_temp_a_df.to_csv(
                    plan.get('plot_target') + oa_band_mutations[0][
                    0
                ].lower() + '_' + oa_plot_measurements[0][
                    0
                ].lower() + '_' + plan.get('in_a_source_name').lower() + '_temp.csv', index=False, sep=',', quotechar='|')
            if oa_temp_b_df is not None:
                oa_temp_b_df.to_csv(
                    plan.get('plot_target') + oa_band_mutations[0][
                    1
                ].lower() + '_' + oa_plot_measurements[0][
                    0
                ].lower() + '_' + plan.get('in_a_source_name').lower() + '_temp.csv', index=False, sep=',', quotechar='|')

            if len(esa_oa_band_mutations) > 0:
                temp_a_df, esa_oa_temp_a_df, esa_oa_temp_b_df = prepare_and_filter.prepare_ab_data(
                    temp_a_df, esa_oa_in_a_df, esa_oa_in_b_df,
                    plan.get('band_col'),
                    band_ab[0], esa_oa_band_mutations[0][0], esa_oa_band_mutations[0][1],
                    plan.get('in_b_measurements_min_valid_pixel_percentage'),
                    plan.get('in_b_measurements_min_valid_pixel_percentage'),
                    plan.get('in_b_measurements_min_valid_pixel_percentage'),
                    esa_oa_plot_measurements[0][0],
                    plan.get('sr_measurements_date_filtering'), plan)
                if esa_oa_temp_a_df is not None:
                    esa_oa_temp_a_df.to_csv(
                        plan.get('plot_target') + esa_oa_band_mutations[0][
                        0
                    ].lower() + '_' + esa_oa_plot_measurements[0][
                        0
                    ].lower() + '_' + plan.get('in_b_source_name').lower() + '_temp.csv', index=False, sep=',', quotechar='|')
                if esa_oa_temp_b_df is not None:
                    esa_oa_temp_b_df.to_csv(
                        plan.get('plot_target') + esa_oa_band_mutations[0][
                        1
                    ].lower() + '_' + esa_oa_plot_measurements[0][
                        0
                    ].lower() + '_' + plan.get('in_b_source_name').lower() + '_temp.csv', index=False, sep=',', quotechar='|')

            # Save data files of plot data.
            ga_product_label = ''
            if plan.get('in_a_source_name').upper() == 'GA':
                ga_product_label = plan.get('product_label')
            temp_a_df.to_csv(
                plan.get('plot_target') + band_ab[0].lower() + '_' + plot_measurements[
                    idx_band_ab
                ][0].lower() + '_' + plan.get('in_a_source_name').lower() + '_temp.csv', index=False, sep=',', quotechar='|')
            test_against_sr_measurements_ref(
                temp_a_df,
                band_ab[0].lower(),
                plot_measurements[idx_band_ab][0].lower(),
                plan.get('in_a_source_name').lower(),
                generate_df,
                plan)
            temp_b_df.to_csv(
                plan.get('plot_target') + band_ab[1].lower() + '_' + plot_measurements[
                    idx_band_ab
                ][0].lower() + '_' + plan.get('in_b_source_name').lower() + '_temp.csv', index=False, sep=',', quotechar='|')
            test_against_sr_measurements_ref(
                temp_b_df,
                band_ab[0].lower(),
                plot_measurements[idx_band_ab][0].lower(),
                plan.get('in_b_source_name').lower(),
                generate_df,
                plan)

            # Do plotting.
            m_axs[0][0].set(
                xlabel=plan.get('date_col'),
                ylabel=plan.get('measurements_plot_y_label'),
                title=m_title,
                xlim=[plan.get('plot_start_date'), plan.get('plot_end_date')]
            )
            ax = temp_a_df.plot(
                kind=plan.get('measurements_plot_type'), x=plan.get('date_col'), y=plot_measurements[idx_band_ab][0], label=plot_measurements[
                    idx_band_ab
                ][1] + ' ' + plan.get('in_a_source_name') + ga_product_label + ' ' + band_ab[2],
                #marker='o',
                ax=m_axs[0][0],
            #    sharex=m_axs[1][0]
            )
            ax = temp_b_df.plot(
                kind=plan.get(
                    'measurements_plot_type'
                ), x=plan.get(
                    'date_col'
                ), y=plot_measurements[idx_band_ab][0], label=plot_measurements[
                    idx_band_ab
                ][1] + ' ' + plan.get(
                    'in_b_source_name'
                ) + ' ' + band_ab[2],
                #marker='o',
                ax=m_axs[0][0],
            #    sharex=m_axs[1][0]
            )
            m_axs[0][0].legend(loc=2)
            #extra_ax = m_axs[0][0].twinx()
            #extra_ax.grid(None)
            #extra_ax.axhline(y=msr_diff_max, label='Max. = ' + str(msr_diff_max), color="gray", linestyle="--", alpha=0.35)
            #extra_ax.axhline(y=msr_diff_mean, label='Mean = ' + str(msr_diff_mean), color="darkgreen", linestyle=":", alpha=0.5)
            #extra_ax.axhline(y=msr_diff_min, label='Min. = ' + str(msr_diff_min), color="gray", linestyle="--", alpha=0.35)
            #extra_ax.set(ylabel=plot_measurements[idx_band_ab][1] + ' difference')
            #extra_ax.legend(prop={'size': 8})
            m_axs[1][0].set(
                xlabel=plan.get('date_col'),
                ylabel=plan.get('oa_plot_y_label'),
                title=oa_title,
                xlim=[plan.get('plot_start_date'), plan.get('plot_end_date')]
            )
            if oa_temp_a_df is not None:
                ax = oa_temp_a_df.plot(
                    kind=plan.get(
                        'measurements_plot_type'
                    ), x=plan.get('date_col'), y=oa_plot_measurements[0][
                        0
                    ], label=oa_band_mutations[0][
                        0
                    ][7:], ax=m_axs[1][0],
                #    sharex=m_axs[0][0]
                )
            if oa_temp_b_df is not None:
                ax = oa_temp_b_df.plot(
                    kind=plan.get(
                        'measurements_plot_type'
                    ), x=plan.get('date_col'), y=oa_plot_measurements[0][
                        0
                    ], label=oa_band_mutations[0][
                        1
                    ][7:], ax=m_axs[1][0],
                #    sharex=m_axs[0][0]
                )
            if len(esa_oa_band_mutations) > 0:
                m_axs[2][0].set(
                    xlabel=plan.get('date_col'),
                    ylabel=plan.get('oa_plot_y_label'),
                    title=esa_oa_title,
                    xlim=[plan.get('plot_start_date'), plan.get('plot_end_date')]
                )
                if esa_oa_temp_a_df is not None:
                    ax = esa_oa_temp_a_df.plot(
                        kind=plan.get(
                            'measurements_plot_type'
                        ), x=plan.get('date_col'), y=esa_oa_plot_measurements[0][
                            0
                        ], label=esa_oa_band_mutations[0][
                            0
                        ], ax=m_axs[2][0],
                    #    sharex=m_axs[0][0]
                    )
                if esa_oa_temp_b_df is not None:
                    ax = esa_oa_temp_b_df.plot(
                        kind=plan.get(
                            'measurements_plot_type'
                        ), x=plan.get('date_col'), y=esa_oa_plot_measurements[0][
                            0
                        ], label=esa_oa_band_mutations[0][
                            1
                        ], ax=m_axs[2][0],
                    #    sharex=m_axs[0][0]
                    )

            plot_path = plan.get(
                'plot_target'
            ) + band_ab[0].lower() + '_' + plot_measurements[
                idx_band_ab
            ][0].lower() + '_' + os.path.splitext(
                plan.get('in_a_sr_measurements_file'))[0].lower() + '.png'
            print('Writing plot image: ' + plot_path)
            m_fig.autofmt_xdate()
            #plt.show()
            plt.savefig(plot_path)
            plt.close(m_fig)

            ratio_dfs[band_ab[0]] = (
                band_ab[2], temp_a_df, temp_b_df,
                (len(oa_band_mutations) > 0 and oa_band_mutations[0][0]) or '',
                oa_temp_a_df,
                (len(oa_band_mutations) > 0 and oa_band_mutations[0][1]) or '',
                oa_temp_b_df
            )

    return ratio_dfs


def test_against_sr_measurements_ref(temp_df, band, measurement,
    source_name, generate_df, plan):

    test_result = False
    if plan.get('test_ref_base') is not None:
        ref_file_path = plan.get(
                'test_ref_path'
            ) + band + '_' + measurement + '_' + source_name + '_temp.csv'
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

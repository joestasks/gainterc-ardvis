
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_nbar_lam_ratio(nbar_ratio_dfs, lam_ratio_dfs, plot_plan, plan, **ack):

    plt.close('all')
    temp_a_df = None
    temp_b_df = None
    oa_temp_a_df = None
    oa_temp_b_df = None

    for site in [*nbar_ratio_dfs]:
        for ga_band in [*nbar_ratio_dfs[site]]:
            temp_a_df = nbar_ratio_dfs[site][ga_band][1]
            oa_temp_a_df = nbar_ratio_dfs[site][ga_band][4]
            if site in [*lam_ratio_dfs]:
                lam_ga_band = ga_band.replace('nbar', 'lambertian')
                temp_b_df = lam_ratio_dfs[site][lam_ga_band][1]
                oa_temp_b_df = lam_ratio_dfs[site][lam_ga_band][6]
            res = pd.merge(
                temp_a_df.assign(
                    grouper=pd.to_datetime(
                        temp_a_df[ack.get('date_col')]
                    ).dt.to_period('D')),
                temp_b_df.assign(
                    grouper=pd.to_datetime(
                        temp_b_df[ack.get('date_col')]
                    ).dt.to_period('D')),
                how='inner', on='grouper',
                suffixes=('_nbar', '_lam'))
            res['ratio'] = res['Mean_sr_nbar'] / res['Mean_sr_lam']
            m_fig, m_axs = plt.subplots(2, 1, figsize=(12, 10), squeeze=False)

            # Do plotting.
            m_axs[0][0].set(
                xlabel=ack.get('date_col'),
                ylabel='NBAR/LAM',
                title='NBAR / LAM Ratio for ' + ((ack.get('in_a_source_name') == 'GA' and ga_band.split('_nbar_')[1]) or ga_band) + ' at ' + site.replace('NBAR_', ''),
                xlim=[ack.get('plot_start_date'), ack.get('plot_end_date')]
            )
            if temp_a_df is not None:
                ax = res.plot(
                    kind=ack.get(
                        'measurements_plot_type'
                    ), x='Date_nbar',
                    y='ratio', label=((ack.get('in_a_source_name') == 'GA' and ga_band.split('_nbar_')[1]) or ga_band),
                    #marker='o',
                    ax=m_axs[0][0],
                #    sharex=m_axs[1][0]
                )
            #if temp_b_df is not None:
            #    ax = temp_b_df.plot(
            #        kind=ack.get(
            #            'measurements_plot_type'
            #        ), x=ack.get(
            #            'date_col'
            #        ), y='Mean_sr', label='B',
            #        #marker='o',
            #        ax=m_axs[0][0],
            #    #    sharex=m_axs[1][0]
            #    )
            m_axs[1][0].set(
                xlabel=ack.get('date_col'),
                ylabel=ack.get('oa_plot_y_label'),
                title='GA Additional Attribute(s)',
                xlim=[ack.get('plot_start_date'), ack.get('plot_end_date')]
            )
            if oa_temp_a_df is not None:
                ax = oa_temp_a_df.plot(
                    kind=ack.get(
                        'measurements_plot_type'
                    ), x=ack.get('date_col'), y='Mean_sr', label=nbar_ratio_dfs[site][ga_band][3][7:],
                    ax=m_axs[1][0],
                #    sharex=m_axs[0][0]
                )
            if oa_temp_b_df is not None:
                ax = oa_temp_b_df.plot(
                    kind=ack.get(
                        'measurements_plot_type'
                    ), x=ack.get('date_col'), y='Mean_sr', label=nbar_ratio_dfs[site][ga_band][5][7:],
                    ax=m_axs[1][0],
                #    sharex=m_axs[0][0]
                )

            plot_target = plot_plan.get_plot_target('NBAR', site.replace('NBAR_', ''), **ack)
            plot_path = plot_target + ga_band + '_nbar_lam_ratio.png'
            print('Writing plot image: ' + plot_path)
            m_fig.autofmt_xdate()
            #plt.show()
            plt.savefig(plot_path)
            plt.close(m_fig)

    return True
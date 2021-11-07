"""Comparison Logic



"""

import os
import sys
import importlib
import importlib.util
from pathlib import Path
import pandas as pd

SR_DIFF_ALL_SITES_HEADER = ('site', 'band', 'min', 'max', 'mean', 'acq')
SR_DIFF_SUMMARY_HEADER = ('band', 'min', 'max', 'mean', 'acq')


def all(plans, **ack):
    """Rules."""

    # Not sure if this is a good idea, so keeping it all in one place for now.
    sys.path.insert(0, './')
    subproject_name = os.path.basename(os.path.dirname(__file__))
    generate_df = importlib.import_module(subproject_name + '.generate_df')
    band_mutation = importlib.import_module(subproject_name + '.band_mutation')
    prepare_and_filter = importlib.import_module(subproject_name + '.prepare_and_filter')
    sr_measurements_plot = importlib.import_module(subproject_name + '.sr_measurements_plot')
    indices_plot = importlib.import_module(subproject_name + '.indices_plot')
    nbar_lam_ratio_plot = importlib.import_module(subproject_name + '.nbar_lam_ratio_plot')
    sys.path.remove('./')

    sr_diff_all_sites = {}
    nbar_ratio_dfs = {}
    lam_ratio_dfs = {}

    for plan in plans:
        if plan.product not in [*sr_diff_all_sites]:
            sr_diff_all_sites[plan.product] = pd.DataFrame(columns=SR_DIFF_ALL_SITES_HEADER)
        print('Working on product: ' + plan.product)
        print('Working on site: ' + plan.site)
        this_in_a_site_path = plan.in_a_site_path + plan.site
        this_in_b_site_path = plan.in_b_site_path + plan.site
        this_in_c_site_path = plan.in_c_site_path + plan.site
        in_a_measurements_path = Path(this_in_a_site_path + '/' + plan.in_a_sr_measurements_file)
        in_b_measurements_path = Path(this_in_b_site_path + '/' + plan.in_b_sr_measurements_file)
        in_a_indices_path = Path(this_in_a_site_path + '/' + plan.in_a_indices_file)
        in_b_indices_path = Path(this_in_b_site_path + '/' + plan.in_b_indices_file)
        in_c_indices_path = Path(this_in_c_site_path + '/' + plan.in_c_indices_file)
        print('Measurements input A: ' + str(in_a_measurements_path))
        print('Measurements input B: ' + str(in_b_measurements_path))
        print('Indices input A: ' + str(in_a_indices_path))
        print('Indices input B: ' + str(in_b_indices_path))
        if plan.in_c_source_name:
            print('Indices input C: ' + str(in_c_indices_path))
        print('Making DataFrame from: ' + str(in_a_measurements_path))
        in_a_measurements_df = generate_df.get_df_from_csv(in_a_measurements_path, plan.rec_max)
        print('Making DataFrame from: ' + str(in_b_measurements_path))
        in_b_measurements_df = generate_df.get_df_from_csv(in_b_measurements_path, plan.rec_max)
        print('Making DataFrame from: ' + str(in_a_indices_path))
        in_a_indices_df = generate_df.get_df_from_csv(in_a_indices_path, plan.rec_max)
        print('Making DataFrame from: ' + str(in_b_indices_path))
        in_b_indices_df = generate_df.get_df_from_csv(in_b_indices_path, plan.rec_max)
        in_c_indices_df = None
        if plan.in_c_source_name:
            print('Making DataFrame from: ' + str(in_c_indices_path))
            in_c_indices_df = generate_df.get_df_from_csv(in_c_indices_path, plan.rec_max)
        print('Making plot output directory: ' + plan.plot_target)
        Path(os.path.dirname(plan.plot_target)).mkdir(parents=True, exist_ok=True)

        if plan.plot_sr_measurements:
            (
                band_mutations, oa_band_mutations,
                plot_measurements, oa_plot_measurements
            ) = band_mutation.get_band_mutations(plan)
            (
                oa_temp_a_df, oa_temp_b_df
            ) = generate_df.generate_oa_dfs(
                in_a_measurements_df,
                in_b_measurements_df,
                oa_band_mutations,
                oa_plot_measurements,
                prepare_and_filter,
                plan)
            (
                esa_oa_band_mutations,
                esa_oa_plot_measurements
            ) = band_mutation.get_esa_oa_band_mutations(plan)
            (
                esa_oa_temp_a_df, esa_oa_temp_b_df
            ) = generate_df.generate_oa_dfs(
                in_b_measurements_df,
                in_a_measurements_df,
                esa_oa_band_mutations,
                esa_oa_plot_measurements,
                prepare_and_filter,
                plan)
            ratio_dfs = sr_measurements_plot.generate_measurements_plots(
                in_a_measurements_df,
                in_b_measurements_df,
                band_mutations,
                plot_measurements,
                oa_temp_a_df,
                oa_temp_b_df,
                oa_band_mutations,
                oa_plot_measurements,
                esa_oa_temp_a_df,
                esa_oa_temp_b_df,
                esa_oa_band_mutations,
                esa_oa_plot_measurements,
                sr_diff_all_sites,
                plan.srm_title, plan.srm_oa_title, plan.srm_esa_oa_title,
                SR_DIFF_ALL_SITES_HEADER,
                prepare_and_filter,
                plan)
            if plan.product.upper() == 'NBAR':
                nbar_ratio_dfs['NBAR_' + plan.site] = ratio_dfs
            elif plan.product.upper() == 'LAM':
                lam_ratio_dfs['NBAR_' + plan.site] = ratio_dfs
            else:
                False  # discard

        if plan.plot_indices:
            indices_plot.generate_indices_plots(
                in_a_indices_df,
                in_b_indices_df,
                in_c_indices_df,
                plan.indices_title, generate_df, plan)

        if plan.plot_sr_measurements:
            prepare_and_filter.prepare_min_max_mean(sr_diff_all_sites, band_mutations, SR_DIFF_SUMMARY_HEADER, plan)

        if plan.plot_sr_measurements:
            nbar_lam_ratio_plot.plot_nbar_lam_ratio(nbar_ratio_dfs, lam_ratio_dfs, plan, **ack)

    return True

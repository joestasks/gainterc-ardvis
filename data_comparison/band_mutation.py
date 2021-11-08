"""



"""


def get_band_mutations(plan):
    """Work out possible comparable band mutations."""

    band_mutations = []
    oa_band_mutations = []
    plot_measurements = []
    oa_plot_measurements = []
    ga_oas_and_bands = plan.get('ga_bands')
    ga_band_mappings = plan.get('ga_band_mappings')
    if plan.get('in_a_source_name') == 'GA':
        ga_oas_and_bands = plan.get('ga_oas') + plan.get('ga_bands')
        ga_band_mappings = {
            **(plan.get('ga_oa_mappings')),
            **(plan.get('ga_band_mappings'))}

    for band in ga_oas_and_bands:
        band_prefixes = [*ga_band_mappings[band]['PREFIXES']]
        band_plot_props = [*ga_band_mappings[band]['PLOT']]

        a_band_lookup_key = 'GA'
        a_band_lookup_key = (lambda x:
            (x.upper() == 'USGS' and 'USGS_LS8') or (a_band_lookup_key)
        )(plan.get('in_a_source_name'))
        a_band_lookup_key = (lambda x:
            (x.upper() == 'ESA' and 'ESA_S2AB') or (a_band_lookup_key)
        )(plan.get('in_a_source_name'))

        b_band_lookup_key = 'GA'
        b_band_lookup_key = (lambda x:
            (x.upper() == 'USGS' and 'USGS_LS8') or (b_band_lookup_key)
        )(plan.get('in_b_source_name'))
        b_band_lookup_key = (lambda x:
            (x.upper() == 'ESA' and 'ESA_S2AB') or (b_band_lookup_key)
        )(plan.get('in_b_source_name'))

        if (a_band_lookup_key == 'GA') and (
            band.lower().startswith(('satellite', 'solar'))
        ):
            b_band_lookup_key = 'GA'

        for band_prefix in band_prefixes:
            band_suffixes = [
                *ga_band_mappings[band]['PREFIXES'][band_prefix]['SUFFIXES']]
            for band_suffix in band_suffixes:

                # (A) Assume GA first.
                a_band_mut = band
                if a_band_lookup_key == 'GA':
                    a_band_mut = band_prefix + plan.get('product').lower() + '_' + band
                    if (a_band_lookup_key == 'GA') and (
                        plan.get('product').upper() == 'LAM'
                    ):
                        a_band_mut = band_prefix + plan.get('ga_band_lam_name') + '_' + band
                    if band_suffix != 'Empty':
                        a_band_mut = a_band_mut + band_suffix

                # (A) Check if there is a mapping to use and use if present.
                if a_band_lookup_key in [*ga_band_mappings[
                    band]['PREFIXES'][
                        band_prefix]['SUFFIXES'][
                            band_suffix]]:
                    a_band_mut = ga_band_mappings[
                        band]['PREFIXES'][
                            band_prefix]['SUFFIXES'][
                                band_suffix][a_band_lookup_key]

                # (B) Assume GA first.
                b_band_mut = band
                if b_band_lookup_key == 'GA':
                    b_band_mut = band_prefix + plan.get('product').lower() + '_' + band
                    if (b_band_lookup_key == 'GA') and (
                        plan.get('product').upper() == 'LAM'
                    ):
                        b_band_mut = band_prefix + plan.get('ga_band_lam_name') + '_' + band
                    if band_suffix != 'Empty':
                        b_band_mut = b_band_mut + band_suffix

                # (B) Check if there is a mapping to use and use if present.
                if b_band_lookup_key in [*ga_band_mappings[
                    band]['PREFIXES'][
                        band_prefix]['SUFFIXES'][
                            band_suffix]]:
                    b_band_mut = ga_band_mappings[
                        band]['PREFIXES'][
                            band_prefix]['SUFFIXES'][
                                band_suffix][b_band_lookup_key]

                # If false, not GA and b band lookup yielded no result;
                # therefore, no mapping and no comparison possible.
                if b_band_lookup_key == 'GA' or b_band_lookup_key in [
                    *ga_band_mappings[band]['PREFIXES'][band_prefix]['SUFFIXES'][
                        band_suffix]]:
                    if (a_band_lookup_key == 'GA') and (
                        band.lower().startswith(('satellite', 'solar')
                    )):
                        a_band_mut = band_prefix + plan.get('ga_band_oa_name') + '_' + band
                        if len(oa_band_mutations) > 0:
                            oa_band_mutations[0][1] = a_band_mut
                        else:
                            oa_band_mutations.append([a_band_mut, b_band_mut, band])
                            oa_plot_measurements.append([
                                band_plot_props[0],
                                ga_band_mappings[
                                    band]['PLOT'][band_plot_props[0]]])
                    else:
                        band_mutations.append([a_band_mut, b_band_mut, band])
                        plot_measurements.append([
                            band_plot_props[0],
                            ga_band_mappings[
                                band]['PLOT'][band_plot_props[0]]])
    print('Band mutations:-')
    print(band_mutations)
    print('Plot measurements:-')
    print(plot_measurements)
    print('OA band mutations:-')
    print(oa_band_mutations)
    print('OA plot measurements:-')
    print(oa_plot_measurements)

    return (band_mutations, oa_band_mutations,
            plot_measurements, oa_plot_measurements)


def get_esa_oa_band_mutations(plan):
    """Work out possible comparable band mutations."""

    esa_oa_band_mutations = []
    esa_oa_plot_measurements = []
    esa_oas = [*plan.get('esa_oa_mappings')]

    if len(esa_oas) > 0:
        band_prefixes = [*plan.get('esa_oa_mappings')[esa_oas[0]]['PREFIXES']]
        band_plot_props = [*plan.get('esa_oa_mappings')[esa_oas[0]]['PLOT']]
        a_band_mut = plan.get('esa_oa_mappings')[esa_oas[0]
            ]['PREFIXES'][
                'Empty'
            ]['SUFFIXES'][
                'Empty'
            ]['ESA_S2AB']
        esa_oa_band_mutations.append([a_band_mut, a_band_mut, esa_oas[0]])
        esa_oa_plot_measurements.append([
            band_plot_props[0],
            plan.get('esa_oa_mappings')[esa_oas[0]]['PLOT'][band_plot_props[0]]])
        if len(esa_oas) > 1:
            b_band_mut = plan.get('esa_oa_mappings')[esa_oas[1]
                ]['PREFIXES'][
                    'Empty'
                ]['SUFFIXES'][
                    'Empty'
                ]['ESA_S2AB']
            esa_oa_band_mutations[0][1] = b_band_mut

    return (esa_oa_band_mutations, esa_oa_plot_measurements)

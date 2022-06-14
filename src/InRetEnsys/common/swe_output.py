import os.path

import pandas as pd
from oemof import solph

from hsncommon.log import HsnLogger


def PrintSWEResults(dumpfile):
    logger = HsnLogger()

    logger.info('**** The script can be divided into two parts here.')
    logger.info('Restore the energy system and the results.')

    energysystem = solph.EnergySystem()

    wdir = os.path.dirname(dumpfile)
    dumpfilename = os.path.basename(dumpfile)

    energysystem.restore(dpath=wdir, filename=dumpfilename)


    Stundenteile = 1


    results = energysystem.results['main']

    Strombus_HS = solph.views.node(results, 'Strom_HS')
    Gasbus = solph.views.node(results, 'Gas')
    Fernwbus = solph.views.node(results, 'Fernwaerme')
    Dampfbus = solph.views.node(results, 'Dampfnetz')
    Frischdampfbus = solph.views.node(results, 'Frischdampf')
    WSP_drucklos_results = solph.views.node(results, 'WSP_drucklos')
    WSP_druck_results = solph.views.node(results, 'WSP_druck')
    Ausspeicherbus = solph.views.node(results, 'Ausspeicherbus')
    Nachheizbus = solph.views.node(results, 'Nachheizhilfebus')
    Solarthermiebus = solph.views.node(results, 'Solarthermiebus')
    FünfundneunzigGradbus = solph.views.node(results, 'FünfundneunzigGradbus')
    Abgas_GT_1bus = solph.views.node(results, 'Abgas_GT_1')
    Abgas_GT_2bus = solph.views.node(results, 'Abgas_GT_2')
    Abgas_GT_3bus = solph.views.node(results, 'Abgas_GT_3')
    Gas_fiktiv = solph.views.node(results, 'Gas_fiktiv')
    Gas2_fiktiv = solph.views.node(results, 'Gas2_fiktiv')

    FrischdampfHilfsbusLinie1 = solph.views.node(results, 'FrischdampfHilfsbus_Linie1')
    FrischdampfHilfsbusLinie2 = solph.views.node(results, 'FrischdampfHilfsbus_Linie2')

    eigenerzeugung = solph.views.node(results, 'Strom_HS_Eigenerzeugung')
    eigenverbrauch = solph.views.node(results, 'Strom_HS_Eigenverbrauch')
    Biobus_results = solph.views.node(results, 'Biobus')

    Direktleitungsbus_results = solph.views.node(results, 'Direktleitungsbus')
    Betriebsverbrauch = solph.views.node(results, 'Betriebsverbrauch')
    Eigenverbrauch_Stadtgebiet = solph.views.node(results, 'WP_Abwaerme_Netz')
    Strombus_WWk = solph.views.node(results, 'Strombus_WWk')

    Ueberschuss_fern = solph.views.node(results, 'Ueberschuss_fern')
    b_HWE_5_1_bus = solph.views.node(results, 'b_HWE_5_1')
    # Methanbus = solph.views.node(results, 'Methanbus')
    # Wasserstoffbus = solph.views.node(results, 'Wasserstoffbus')

    print('-----------------------------------------------------------------------')
    print('Energiemengen Strombus_HS: \n' + str(Strombus_HS['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    print('Energiemengen Gasbus: \n' + str(Gasbus['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    print('Energiemengen Fernwbus: \n' + str(Fernwbus['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    print('Energiemengen eigenerzeugung: \n' + str(eigenerzeugung['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    print('Energiemengen eigenverbrauch: \n' + str(eigenverbrauch['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    print('Energiemengen Biobus: \n' + str(Biobus_results['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    print('Energiemengen Direktleitungsbus_results: \n' + str(Direktleitungsbus_results['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    print('Betriebsverbrauch: \n' + str(Betriebsverbrauch['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    print('Solarthermiebus: \n' + str(Solarthermiebus['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    # print('Methanbus: \n' +str(Methanbus['sequences'].sum()))
    print('-----------------------------------------------------------------------')
    # print('Wasserstoffbus: \n' +str(Wasserstoffbus['sequences'].sum()))

    # %% Kosten
    E_Gas_Linie_1 = 0
    E_Gas_Linie_2 = 0
    E_Gas_Linie_3 = 0

    E_Gas_HWE_2 = 0
    E_Gas_HWE_5_1 = 0
    E_Gas_HWE_5_2 = 0

    Kosten_Gas_Linie_1 = 0
    Kosten_Gas_Linie_2 = 0
    Kosten_Gas_Linie_3 = 0

    Kosten_Gas_HWE_2 = 0
    Kosten_Gas_HWE_5_1 = 0
    Kosten_Gas_HWE_5_2 = 0

    E_Strom_AHK_1 = 0
    E_Strom_AHK_2 = 0
    E_Strom_AHK_3 = 0

    E_Strom_HWE_2 = 0
    E_Strom_HWE_5_1 = 0
    E_Strom_HWE_5_2 = 0

    E_Strom_ST_VL = 0
    E_Strom_ST_RL = 0

    Erloese_GT_1 = 0
    Erloese_GT_2 = 0
    Erloese_GT_3 = 0

    Erloese_Bestands_DT = 0
    Erloese_Tandem_DT = 0
    Erloese_PV = 0
    Importkosten_Biomasse = 0
    Importkosten_Strom = 0
    Importkosten_Gas = 0
    Importkosten_Gas_konv = 0
    Importkosten_Gas_gruen = 0
    Importkosten_H2 = 0
    E_GT_1 = 0
    E_GT_2 = 0
    E_GT_3 = 0
    E_Bestands_DT = 0
    E_Tandem_DT = 0
    # E_PV=0
    Erloese_Strom_Eigenerzeugung = 0
    E_Strom_WP_RABA_Rauchgas = 0
    E_Strom_WP_RABA_alternativ = 0
    E_Strom_WP_WWK = 0
    E_Strom_WP_Flusswasser_Seen = 0
    E_Strom_WP_Waescherei = 0
    E_Strom_WP_Luftwaerme = 0
    E_Strom_WP_Speicher = 0
    E_Strom_WP_Heisswasser = 0
    E_Strom_WP_AHK_RG = 0
    E_Strom_P2H_Heizstab = 0
    E_Biogasanlage = 0
    E_Biogaseinspeisung = 0
    Importkosten_Strom_eigenverb = 0
    Importkosten_Strom_betriebsverb = 0
    Importkosten_Strom_stadtg = 0
    E_Strom_WP_Abwasser_Industrie = 0
    Ferndampfbezug_Kosten = 0

    for i in range(0, len(eigenerzeugung['sequences'][('Strom_HS_Eigenerzeugung', 'Stromexport'), 'flow'])):
        E_Gas_Linie_1 += ((Gas_fiktiv['sequences'][('Gas_fiktiv', 'AHK_1_FB'), 'flow'][i] +
                           Gas_fiktiv['sequences'][('Gas_fiktiv', 'AHK_1_KB'), 'flow'][i] +
                           Gas_fiktiv['sequences'][('Gas_fiktiv', 'GT_1'), 'flow'][i]) / Stundenteile)
        E_Gas_Linie_2 += ((Gas2_fiktiv['sequences'][('Gas2_fiktiv', 'AHK_2_FB'), 'flow'][i] +
                           Gas2_fiktiv['sequences'][('Gas2_fiktiv', 'AHK_2_KB'), 'flow'][i] +
                           Gas2_fiktiv['sequences'][('Gas2_fiktiv', 'GT_2'), 'flow'][i]) / Stundenteile)
        E_Gas_Linie_3 += ((Gasbus['sequences'][('Gas', 'GT_3'), 'flow'][i]) / Stundenteile)

        E_Gas_HWE_2 += ((Gasbus['sequences'][('Gas', 'HWE_2'), 'flow'][i]) / Stundenteile)
        E_Gas_HWE_5_1 += ((Gasbus['sequences'][('Gas', 'HWE_5_1_Investblock'), 'flow'][i]) / Stundenteile)
        E_Gas_HWE_5_2 += ((Gasbus['sequences'][('Gas', 'HWE_5_2'), 'flow'][i]) / Stundenteile)

        Importkosten_Biomasse += (Biobus_results['sequences'][('Import_Festbrennstoffe', 'Biobus'), 'flow'][
                                      i] / Stundenteile) * data_Preis_Biomasse[i]
        E_Biogasanlage = (Biobus_results['sequences'][('Biobus', 'Biogas'), 'flow'][i] / Stundenteile)
        E_Biogaseinspeisung = (
                Biobus_results['sequences'][('Biobus', 'Biogaseinspeisung_Neuanlagen'), 'flow'][i] / Stundenteile)

        E_Strom_AHK_1 += ((Betriebsverbrauch['sequences'][('Betriebsverbrauch', 'AHK_1_FB'), 'flow'][i] +
                           Betriebsverbrauch['sequences'][('Betriebsverbrauch', 'AHK_1_KB'), 'flow'][i] +
                           Betriebsverbrauch['sequences'][('Betriebsverbrauch', 'AHK_1_AB'), 'flow'][i]) / Stundenteile)
        E_Strom_AHK_2 += ((Betriebsverbrauch['sequences'][('Betriebsverbrauch', 'AHK_2_FB'), 'flow'][i] +
                           Betriebsverbrauch['sequences'][('Betriebsverbrauch', 'AHK_2_KB'), 'flow'][i] +
                           Betriebsverbrauch['sequences'][('Betriebsverbrauch', 'AHK_2_AB'), 'flow'][i]) / Stundenteile)
        E_Strom_AHK_3 += ((Betriebsverbrauch['sequences'][('Betriebsverbrauch', 'AHK_3_AB'), 'flow'][i]) / Stundenteile)

        E_Strom_HWE_2 += ((Betriebsverbrauch['sequences'][('Betriebsverbrauch', 'HWE_2'), 'flow'][i]) / Stundenteile)
        E_Strom_HWE_5_1 += (
                (Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_1_Nachheizung'), 'flow'][
                     i] +
                 Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_1_Heißwasser'), 'flow'][
                     i]) / Stundenteile)
        E_Strom_HWE_5_2 += (
                (Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_2'), 'flow'][i]) / Stundenteile)

        E_Strom_ST_VL += ((Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'ST_roehr_VL'), 'flow'][
            i]) / Stundenteile)
        E_Strom_ST_RL += ((Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'ST_roehr_RL'), 'flow'][
            i]) / Stundenteile)

        E_Strom_WP_RABA_Rauchgas += ((Eigenverbrauch_Stadtgebiet['sequences'][
            ('WP_Abwaerme_Netz', 'WP_RABA_Rauchgas'), 'flow'][i]) / Stundenteile)
        E_Strom_WP_RABA_alternativ += ((Eigenverbrauch_Stadtgebiet['sequences'][
            ('WP_Abwaerme_Netz', 'WP_RABA_alternativ'), 'flow'][i]) / Stundenteile)
        E_Strom_WP_WWK += ((Strombus_WWk['sequences'][('Strombus_WWk', 'WP_WWK'), 'flow'][i]) / Stundenteile)
        E_Strom_WP_Waescherei += (
                (Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_Waescherei'), 'flow'][
                    i]) / Stundenteile)
        E_Strom_WP_Flusswasser_Seen += ((Eigenverbrauch_Stadtgebiet['sequences'][
            ('WP_Abwaerme_Netz', 'WP_Flusswasser_Seen'), 'flow'][i]) / Stundenteile)
        E_Strom_WP_Abwasser_Industrie += ((Eigenverbrauch_Stadtgebiet['sequences'][
            ('WP_Abwaerme_Netz', 'WP_Abwasser_Industrie'), 'flow'][i]) / Stundenteile)

        E_Strom_WP_Luftwaerme += (
                (eigenverbrauch['sequences'][('Strom_HS_Eigenverbrauch', 'WP_Luftwaerme'), 'flow'][i]) / Stundenteile)
        E_Strom_WP_Speicher += (
                (eigenverbrauch['sequences'][('Strom_HS_Eigenverbrauch', 'WP_Speicher'), 'flow'][i]) / Stundenteile)
        E_Strom_WP_Heisswasser += (
                (eigenverbrauch['sequences'][('Strom_HS_Eigenverbrauch', 'WP_Heisswasser'), 'flow'][i]) / Stundenteile)
        E_Strom_WP_AHK_RG += (
                (eigenverbrauch['sequences'][('Strom_HS_Eigenverbrauch', 'WP_AHK_RG'), 'flow'][i]) / Stundenteile)
        E_Strom_P2H_Heizstab += (
                (eigenverbrauch['sequences'][('Strom_HS_Eigenverbrauch', 'P2H_Heizstab'), 'flow'][i]) / Stundenteile)

        Importkosten_Strom_eigenverb += ((eigenverbrauch['sequences'][
            ('Import_Strom_Eigenverbrauch', 'Strom_HS_Eigenverbrauch'), 'flow'][i]) / Stundenteile) * \
                                        data_Boerse_Import[i]
        Importkosten_Strom_betriebsverb += ((Betriebsverbrauch['sequences'][
            ('Import_Betriebsverbrauch', 'Betriebsverbrauch'), 'flow'][i]) / Stundenteile) * data_Boerse_Import[i]
        Importkosten_Strom_stadtg += ((Eigenverbrauch_Stadtgebiet['sequences'][
            ('Import_Strom_WP', 'WP_Abwaerme_Netz'), 'flow'][i]) / Stundenteile) * data_Boerse_Import[i]

        Importkosten_Gas_gruen += ((Gasbus['sequences'][('Import_gruenesErdgas', 'Gas'), 'flow'][i]) / Stundenteile) * \
                                  data_Preis_gruenesErdgas[i]
        Importkosten_H2 += ((Gasbus['sequences'][('Import_H2', 'Gas'), 'flow'][i]) / Stundenteile) * float(
            Preis_H2['H2_Preis_obere_range']['Preis_2045'])

        Ferndampfbezug_Kosten += ((Dampfbus['sequences'][('Ferndampfbezug', 'Dampfnetz'), 'flow'][
            i]) / Stundenteile) * 20

        E_GT_1 += eigenerzeugung['sequences'][(('GT_1', 'Strom_HS_Eigenerzeugung'), 'flow')][i]
        E_GT_2 += eigenerzeugung['sequences'][(('GT_2', 'Strom_HS_Eigenerzeugung'), 'flow')][i]
        E_GT_3 += eigenerzeugung['sequences'][(('GT_3', 'Strom_HS_Eigenerzeugung'), 'flow')][i]

        E_Bestands_DT += eigenerzeugung['sequences'][(('DT-Bestand', 'Strom_HS_Eigenerzeugung'), 'flow')][i]
        E_Tandem_DT += eigenerzeugung['sequences'][(('DT-Tandem ND-Teil', 'Strom_HS_Eigenerzeugung'), 'flow')][i] + \
                       eigenerzeugung['sequences'][(('DT-Tandem HD-Teil', 'Strom_HS_Eigenerzeugung'), 'flow')][i]
        # E_PV += Strombus_HS['sequences'][(('PV_SWE','Strom_HS'), 'flow')][i]

        Erloese_Strom_Eigenerzeugung += (eigenerzeugung['sequences'][
                                             (('Strom_HS_Eigenerzeugung', 'Stromexport'), 'flow')][
                                             i] + eigenerzeugung['sequences'][
                                             (('Strom_HS_Eigenerzeugung', 'Trafo_Kosten_vnne'), 'flow')][i]) * \
                                        data_Boerse[
                                            i]

    # biomasse
    summe_biomasseverbrauch = E_Biogasanlage + E_Biogaseinspeisung
    E_Biogasanlage_rel = E_Biogasanlage / summe_biomasseverbrauch
    E_Biogaseinspeisung_rel = E_Biogaseinspeisung / summe_biomasseverbrauch

    Kosten_Biomasse_Biogasanlage = E_Biogasanlage_rel * Importkosten_Biomasse
    Kosten_Biomasse_Biogaseinspeisung = E_Biogaseinspeisung_rel * Importkosten_Biomasse

    Kosten_Strom_WP_WWK = E_Strom_WP_WWK * PtH_Technologien['WWK']['Strompreis']

    # eigenverbrauch
    summe_eigenverbrauch = E_Strom_WP_Luftwaerme + E_Strom_WP_Speicher + E_Strom_WP_Heisswasser + E_Strom_P2H_Heizstab + E_Strom_WP_AHK_RG
    E_Strom_WP_Luftwaerme_rel = E_Strom_WP_Luftwaerme / summe_eigenverbrauch
    E_Strom_WP_Speicher_rel = E_Strom_WP_Speicher / summe_eigenverbrauch
    E_Strom_WP_Heisswasser_rel = E_Strom_WP_Heisswasser / summe_eigenverbrauch
    E_Strom_WP_AHK_RG_rel = E_Strom_WP_AHK_RG / summe_eigenverbrauch
    E_Strom_P2H_Heizstab_rel = E_Strom_P2H_Heizstab / summe_eigenverbrauch

    Kosten_Strom_WP_Luftwaerme = E_Strom_WP_Luftwaerme_rel * Importkosten_Strom_eigenverb
    Kosten_Strom_WP_Speicher = E_Strom_WP_Speicher_rel * Importkosten_Strom_eigenverb
    Kosten_Strom_WP_Heisswasser = E_Strom_WP_Heisswasser_rel * Importkosten_Strom_eigenverb
    Kosten_Strom_WP_AHK_RG = E_Strom_WP_AHK_RG_rel * Importkosten_Strom_eigenverb
    Kosten_Strom_P2H_Heizstab = E_Strom_P2H_Heizstab_rel * Importkosten_Strom_eigenverb

    print('Importkosten_Strom_eigenverb:' + str(Importkosten_Strom_eigenverb))
    print('Importkosten_Strom_eigenverb:' + str(
        Kosten_Strom_WP_Luftwaerme + Kosten_Strom_WP_Speicher + Kosten_Strom_WP_Heisswasser + Kosten_Strom_P2H_Heizstab + Kosten_Strom_WP_AHK_RG))

    # gasverbrauch
    Importkosten_Gas = Importkosten_Gas_konv + Importkosten_Gas_gruen + Importkosten_H2

    summe_gasverbrauch = E_Gas_Linie_1 + E_Gas_Linie_2 + E_Gas_Linie_3 + E_Gas_HWE_2 + E_Gas_HWE_5_1 + E_Gas_HWE_5_2
    E_Gas_Linie_1_rel = E_Gas_Linie_1 / summe_gasverbrauch
    E_Gas_Linie_2_rel = E_Gas_Linie_2 / summe_gasverbrauch
    E_Gas_Linie_3_rel = E_Gas_Linie_3 / summe_gasverbrauch

    E_Gas_HWE_2_rel = E_Gas_HWE_2 / summe_gasverbrauch
    E_Gas_HWE_5_1_rel = E_Gas_HWE_5_1 / summe_gasverbrauch
    E_Gas_HWE_5_2_rel = E_Gas_HWE_5_2 / summe_gasverbrauch

    Kosten_Gas_Linie_1 = E_Gas_Linie_1_rel * Importkosten_Gas
    Kosten_Gas_Linie_2 = E_Gas_Linie_2_rel * Importkosten_Gas
    Kosten_Gas_Linie_3 = E_Gas_Linie_3_rel * Importkosten_Gas

    Kosten_Gas_HWE_2 = E_Gas_HWE_2_rel * Importkosten_Gas
    Kosten_Gas_HWE_5_1 = E_Gas_HWE_5_1_rel * Importkosten_Gas
    Kosten_Gas_HWE_5_2 = E_Gas_HWE_5_2_rel * Importkosten_Gas

    # betriebsverbrauch
    summe_betriebsverbrauch = E_Strom_AHK_1 + E_Strom_AHK_2 + E_Strom_AHK_3 + E_Strom_HWE_2
    E_Strom_AHK_1_rel = E_Strom_AHK_1 / summe_betriebsverbrauch
    E_Strom_AHK_2_rel = E_Strom_AHK_2 / summe_betriebsverbrauch
    E_Strom_AHK_3_rel = E_Strom_AHK_3 / summe_betriebsverbrauch
    E_Strom_HWE_2_rel = E_Strom_HWE_2 / summe_betriebsverbrauch

    Kosten_Strom_AHK_1 = E_Strom_AHK_1_rel * Importkosten_Strom_betriebsverb
    Kosten_Strom_AHK_2 = E_Strom_AHK_2_rel * Importkosten_Strom_betriebsverb
    Kosten_Strom_AHK_3 = E_Strom_AHK_3_rel * Importkosten_Strom_betriebsverb
    Kosten_Strom_HWE_2 = E_Strom_HWE_2_rel * Importkosten_Strom_betriebsverb

    print('Importkosten_Strom_betriebsverb:' + str(Importkosten_Strom_betriebsverb))
    print('Importkosten_Strom_betriebsverb:' + str(
        Kosten_Strom_AHK_1 + Kosten_Strom_AHK_2 + Kosten_Strom_AHK_3 + Kosten_Strom_HWE_2))

    # eigenverbrauch stadtgebiet
    summe_eigenverbrauch_stadtgebiet = (E_Strom_HWE_5_1 + E_Strom_HWE_5_2 + E_Strom_ST_VL
                                        + E_Strom_ST_RL
                                        + E_Strom_WP_RABA_Rauchgas
                                        + E_Strom_WP_RABA_alternativ
                                        # +E_Strom_WP_WWK
                                        + E_Strom_WP_Waescherei
                                        + E_Strom_WP_Flusswasser_Seen
                                        + E_Strom_WP_Abwasser_Industrie)

    E_Strom_HWE_5_1_rel = E_Strom_HWE_5_1 / summe_eigenverbrauch_stadtgebiet
    E_Strom_HWE_5_2_rel = E_Strom_HWE_5_2 / summe_eigenverbrauch_stadtgebiet
    E_Strom_ST_VL_rel = E_Strom_ST_VL / summe_eigenverbrauch_stadtgebiet
    E_Strom_ST_RL_rel = E_Strom_ST_RL / summe_eigenverbrauch_stadtgebiet

    E_Strom_WP_RABA_Rauchgas_rel = E_Strom_WP_RABA_Rauchgas / summe_eigenverbrauch_stadtgebiet
    E_Strom_WP_RABA_alternativ_rel = E_Strom_WP_RABA_alternativ / summe_eigenverbrauch_stadtgebiet
    # E_Strom_WP_WWK_rel = E_Strom_WP_WWK / summe_eigenverbrauch_stadtgebiet
    E_Strom_WP_Waescherei_rel = E_Strom_WP_Waescherei / summe_eigenverbrauch_stadtgebiet
    E_Strom_WP_Flusswasser_Seen_rel = E_Strom_WP_Flusswasser_Seen / summe_eigenverbrauch_stadtgebiet
    E_Strom_WP_Abwasser_Industrie_rel = E_Strom_WP_Abwasser_Industrie / summe_eigenverbrauch_stadtgebiet

    Kosten_Strom_HWE_5_1 = E_Strom_HWE_5_1_rel * Importkosten_Strom_stadtg
    Kosten_Strom_HWE_5_2 = E_Strom_HWE_5_2_rel * Importkosten_Strom_stadtg
    Kosten_Strom_ST_VL = E_Strom_ST_VL_rel * Importkosten_Strom_stadtg
    Kosten_Strom_ST_RL = E_Strom_ST_RL_rel * Importkosten_Strom_stadtg

    Kosten_Strom_WP_RABA_Rauchgas = E_Strom_WP_RABA_Rauchgas_rel * Importkosten_Strom_stadtg
    Kosten_Strom_WP_RABA_alternativ = E_Strom_WP_RABA_alternativ_rel * Importkosten_Strom_stadtg
    # Kosten_Strom_WP_WWK = E_Strom_WP_WWK_rel * Importkosten_Strom_stadtg
    Kosten_Strom_WP_Waescherei = E_Strom_WP_Waescherei_rel * Importkosten_Strom_stadtg
    Kosten_Strom_WP_Flusswasser_Seen = E_Strom_WP_Flusswasser_Seen_rel * Importkosten_Strom_stadtg
    Kosten_Strom_WP_Abwasser_Industrie = E_Strom_WP_Abwasser_Industrie_rel * Importkosten_Strom_stadtg

    print('Importkosten_Strom_stadtg:' + str(Importkosten_Strom_stadtg))
    print('Importkosten_Strom_stadtg:' + str(Kosten_Strom_HWE_5_1 + Kosten_Strom_HWE_5_2 +
                                             Kosten_Strom_ST_VL + Kosten_Strom_ST_RL +
                                             Kosten_Strom_WP_RABA_Rauchgas + Kosten_Strom_WP_RABA_alternativ +
                                             # Kosten_Strom_WP_WWK+
                                             Kosten_Strom_WP_Waescherei +
                                             Kosten_Strom_WP_Flusswasser_Seen + Kosten_Strom_WP_Abwasser_Industrie))

    kosten_strom_gesamt = (
            Kosten_Strom_WP_Luftwaerme + Kosten_Strom_WP_Speicher + Kosten_Strom_WP_Heisswasser + Kosten_Strom_P2H_Heizstab +
            Kosten_Strom_AHK_1 + Kosten_Strom_AHK_2 + Kosten_Strom_AHK_3 + Kosten_Strom_HWE_2 +
            Kosten_Strom_HWE_5_1 + Kosten_Strom_HWE_5_2 + Kosten_Strom_ST_VL + Kosten_Strom_ST_RL +
            Kosten_Strom_WP_RABA_Rauchgas + Kosten_Strom_WP_RABA_alternativ +
            # Kosten_Strom_WP_WWK+
            Kosten_Strom_WP_Waescherei +
            Kosten_Strom_WP_Flusswasser_Seen + Kosten_Strom_WP_AHK_RG + Kosten_Strom_WP_Abwasser_Industrie)

    print('kosten_strom_gesamt: ' + str(kosten_strom_gesamt))

    # erloese eigenerzeugungsanlagen
    Ertrag_gesamt_eigenerzeugung = E_GT_1 + E_GT_2 + E_GT_3 + E_Bestands_DT + E_Tandem_DT  # + E_PV
    Ertrag_GT_1_rel = E_GT_1 / Ertrag_gesamt_eigenerzeugung
    Ertrag_GT_2_rel = E_GT_2 / Ertrag_gesamt_eigenerzeugung
    Ertrag_GT_3_rel = E_GT_3 / Ertrag_gesamt_eigenerzeugung

    Ertrag_Bestands_DT_rel = E_Bestands_DT / Ertrag_gesamt_eigenerzeugung
    Ertrag_Tandem_DT_rel = E_Tandem_DT / Ertrag_gesamt_eigenerzeugung
    # Ertrag_PV_rel = E_PV / Ertrag_gesamt_eigenerzeugung

    Erloese_GT_1 = Ertrag_GT_1_rel * Erloese_Strom_Eigenerzeugung
    Erloese_GT_2 = Ertrag_GT_2_rel * Erloese_Strom_Eigenerzeugung
    Erloese_GT_3 = Ertrag_GT_3_rel * Erloese_Strom_Eigenerzeugung

    Erloese_DT_Bestand = Ertrag_Bestands_DT_rel * Erloese_Strom_Eigenerzeugung
    Erloese_DT_Tandem = Ertrag_Tandem_DT_rel * Erloese_Strom_Eigenerzeugung
    # Erloese_PV = Ertrag_PV_rel * Erloese_Strom_Eigenerzeugung

    print('-----------------------------------------------------------------------')
    print('Kosten aus variablen Kosten in €')
    # Kosten in Linie 1
    E_Linie_1 = Frischdampfbus['sequences'][(('FrischdampfHilfstrafo_Linie1', 'Frischdampf'), 'flow')].sum()
    E_Linie_1_HWS_AB = Fernwbus['sequences'][(('AHK_1_AB', 'Fernwaerme'), 'flow')].sum()
    E_Linie_1_HWS_KB = Fernwbus['sequences'][(('AHK_1_KB', 'Fernwaerme'), 'flow')].sum()
    E_Linie_1_HWS_FB = Fernwbus['sequences'][(('AHK_1_FB', 'Fernwaerme'), 'flow')].sum()

    # Kosten_Linie_1_HWS_AB = E_Linie_1_HWS_AB * var_Kosten_Linie_1_HWS_AB
    # Kosten_Linie_1_HWS_KB = E_Linie_1_HWS_KB * var_Kosten_Linie_1_HWS_KB
    # Kosten_Linie_1_HWS_FB = E_Linie_1_HWS_FB * var_Kosten_Linie_1_HWS_FB

    # Investkosten_Linie_1 = epc_AHK_1_KB * Frischdampfbus['scalars'][1] + epc_GT_1*eigenerzeugung['scalars'][4]
    # # HWS_Koste_Linie_1 = Kosten_Linie_1_HWS_AB + Kosten_Linie_1_HWS_KB + Kosten_Linie_1_HWS_FB#var_Kosten_Linie_1 * E_Linie_1_HWS
    # Kosten_Linie_1 = Investkosten_Linie_1 #+ HWS_Koste_Linie_1
    # print('Linie 1: '+str(round(Kosten_Linie_1, 0))+' €/a')

    # Kosten_Linie_1_alternativ = Investkosten_Linie_1 + Kosten_Gas_Linie_1 - Erloese_GT_1# + HWS_Koste_Linie_1
    OPEX_linie1 = Kosten_Strom_AHK_1 + Kosten_Gas_Linie_1 + (
            b_AHK_1_KB * Frischdampfbus['scalars'][1] + b_GT_1 * eigenerzeugung['scalars'][4])
    CAPEX_linie1 = (a_AHK_1_KB * Frischdampfbus['scalars'][1] + a_GT_1 * eigenerzeugung['scalars'][4])

    # Kosten in Linie 2
    E_Linie_2 = Frischdampfbus['sequences'][(('FrischdampfHilfstrafo_Linie2', 'Frischdampf'), 'flow')].sum()
    E_Linie_2_HWS_AB = Fernwbus['sequences'][(('AHK_2_AB', 'Fernwaerme'), 'flow')].sum()
    E_Linie_2_HWS_KB = Fernwbus['sequences'][(('AHK_2_KB', 'Fernwaerme'), 'flow')].sum()
    E_Linie_2_HWS_FB = Fernwbus['sequences'][(('AHK_2_FB', 'Fernwaerme'), 'flow')].sum()

    # Kosten_Linie_2_HWS_AB = E_Linie_2_HWS_AB * var_Kosten_Linie_2_HWS_AB
    # Kosten_Linie_2_HWS_KB = E_Linie_2_HWS_KB * var_Kosten_Linie_2_HWS_KB
    # Kosten_Linie_2_HWS_FB = E_Linie_2_HWS_FB * var_Kosten_Linie_2_HWS_FB

    # Investkosten_Linie_2 = epc_AHK_2_KB * Frischdampfbus['scalars'][2] + epc_GT_1*eigenerzeugung['scalars'][5]
    # # HWS_Koste_Linie_2 = Kosten_Linie_2_HWS_AB + Kosten_Linie_2_HWS_KB + Kosten_Linie_2_HWS_FB#var_Kosten_Linie_2 * E_Linie_2_HWS
    # Kosten_Linie_2 = Investkosten_Linie_2 #+ HWS_Koste_Linie_2
    # print('Linie 2: '+str(round(Kosten_Linie_2, 0))+' €/a')

    # Kosten_Linie_2_alternativ = Investkosten_Linie_2  + Kosten_Gas_Linie_2 - Erloese_GT_2#+ HWS_Koste_Linie_2
    OPEX_linie2 = Kosten_Strom_AHK_2 + Kosten_Gas_Linie_2 + (
            b_AHK_2_KB * Frischdampfbus['scalars'][2] + b_GT_1 * eigenerzeugung['scalars'][5])
    CAPEX_linie2 = (a_AHK_2_KB * Frischdampfbus['scalars'][2] + a_GT_1 * eigenerzeugung['scalars'][5])

    # Kosten in Linie 3
    E_Linie_3 = Frischdampfbus['sequences'][(('AHK_3_AB', 'Frischdampf'), 'flow')].sum()
    E_Linie_3_HWS_AB = Fernwbus['sequences'][(('AHK_3_AB', 'Fernwaerme'), 'flow')].sum()

    # Investkosten_Linie_3 = epc_AHK_3_AB * Frischdampfbus['scalars'][0] + epc_GT_3*eigenerzeugung['scalars'][6]
    # # Kosten_Linie_3_HWS_AB = E_Linie_3_HWS_AB * var_Kosten_Linie_3_HWS_AB
    # Kosten_Linie_3 = Investkosten_Linie_3 #+ Kosten_Linie_3_HWS_AB
    # print('Linie 3: '+str(round(Kosten_Linie_3, 0))+' €/a')

    # Kosten_Linie_3_alternativ = Investkosten_Linie_3  + Kosten_Gas_Linie_3 - Erloese_GT_3 #+ Kosten_Linie_3_HWS_AB
    OPEX_linie3 = Kosten_Strom_AHK_3 + Kosten_Gas_Linie_3 + (
            b_AHK_3_AB * Frischdampfbus['scalars'][0] + b_GT_3 * eigenerzeugung['scalars'][6])
    CAPEX_linie3 = (a_AHK_3_AB * Frischdampfbus['scalars'][0] + a_GT_3 * eigenerzeugung['scalars'][6])

    # Tandem-DT
    # E_Dampf_Tandem_DT = Dampfbus['sequences'][(('Anzapfung_Tandem_DT', 'Dampfnetz'), 'flow')].sum()
    # E_HW_Tandem_DT = Fernwbus['sequences'][(('DT-Tandem ND-Teil', 'Fernwaerme'), 'flow')].sum()
    # Kosten_Tandem_DT_HW = epc_DT_Tandem_HD * Fernwbus['scalars'][1]
    # Kosten_Tandem_DT_Dampf = epc_DT_Tandem_HD * Dampfbus['scalars'][0]
    # Kosten_Tandem_DT = Kosten_Tandem_DT_HW + Kosten_Tandem_DT_Dampf #var_Kosten_Tandem_DT_HD * (E_Dampf_Tandem_DT + E_HW_Tandem_DT)
    # print('Tandem DT: '+str(round(Kosten_Tandem_DT, 0))+' €/a')

    # Kosten_DT_Tandem_alternativ = Kosten_Tandem_DT_HW + Kosten_Tandem_DT_Dampf - Erloese_DT_Tandem
    # HD + ND-Teil
    CAPEX_DT_Tandem = a_DT_Tandem_HD * eigenerzeugung['scalars'][2] + a_DT_Tandem_HD * eigenerzeugung['scalars'][3]
    OPEX_DT_Tandem = b_DT_Tandem_HD * eigenerzeugung['scalars'][2] + b_DT_Tandem_HD * eigenerzeugung['scalars'][3]

    # Bestands-DT
    # E_Dampf_Bestands_DT = Dampfbus['sequences'][(('DT-Bestand', 'Dampfnetz'), 'flow')].sum()
    # E_HW_Bestands_DT = Fernwbus['sequences'][(('DT-Bestand', 'Fernwaerme'), 'flow')].sum()
    # Kosten_Bestand_DT_HW = epc_DT_Bestand * Fernwbus['scalars'][0]
    # # Kosten_Bestand_DT_Dampf = E_Dampf_Bestands_DT * var_Kosten_Bestands_DT_Dampf
    # Kosten_Bestands_DT = Kosten_Bestand_DT_HW #+ Kosten_Bestand_DT_Dampf #var_Kosten_Bestands_DT * (E_Dampf_Bestands_DT + E_HW_Bestands_DT)
    # print('Bestands-DT: '+str(round(Kosten_Bestands_DT, 0))+' €/a')

    # Kosten_DT_Bestand_alternativ = Kosten_Bestand_DT_HW  - Erloese_DT_Bestand #+ Kosten_Bestand_DT_Dampf
    CAPEX_DT_Bestand = a_DT_Bestand * eigenerzeugung['scalars'][1]
    OPEX_DT_Bestand = b_DT_Bestand * eigenerzeugung['scalars'][
        1]  # + E_Dampf_Bestands_DT * var_Kosten_Bestands_DT_Dampf

    # HWE 2
    # E_HWE_2 = Fernwbus['sequences'][(('HWE_2', 'Fernwaerme'), 'flow')].sum()
    # Investkosten_HWE_2 = epc_HWE_2 * Fernwbus['scalars'][2]
    Steuer_HWE_2 = Brennstoffenergiesteuer * Gasbus['sequences'][(('Gas', 'HWE_2'), 'flow')].sum()
    # Kosten_HWE_2 = Investkosten_HWE_2 + Steuer_HWE_2
    # print('HWE-2: '+str(round(Kosten_HWE_2, 0))+' €/a')

    # Kosten_HWE_2_alternativ = Investkosten_HWE_2 + Steuer_HWE_2 + Kosten_Gas_HWE_2 + Kosten_Strom_HWE_2
    OPEX_HWE_2 = Steuer_HWE_2 + Kosten_Gas_HWE_2 + Kosten_Strom_HWE_2 + b_HWE_2 * Fernwbus['scalars'][0]
    CAPEX_HWE_2 = a_HWE_2 * Fernwbus['scalars'][1]

    # HWE 5.1
    # E_HW_HWE_5_1 = Fernwbus['sequences'][(('HWE_5_1_Heißwasser', 'Fernwaerme'), 'flow')].sum()
    # E_Nachheiz_HWE_5_1 = Nachheizbus['sequences'][(('HWE_5_1_Nachheizung', 'Nachheizhilfebus'), 'flow')].sum()
    # Investkosten_HWE_5_1 = epc_HWE_5_1 * b_HWE_5_1_bus['scalars'][0]
    Steuer_HWE_5_1 = Brennstoffenergiesteuer * (Gasbus['sequences'][('Gas', 'HWE_5_1_Investblock'), 'flow'].sum())
    # Kosten_HWE_5_1 = Investkosten_HWE_5_1 + Steuer_HWE_5_1
    # print('HWE-5.1: '+str(round(Kosten_HWE_5_1, 0))+' €/a')

    # Kosten_HWE_5_1_alternativ = Investkosten_HWE_5_1 + Steuer_HWE_5_1 + Kosten_Gas_HWE_5_1 + Kosten_Strom_HWE_5_1
    OPEX_HWE_5_1 = Steuer_HWE_5_1 + Kosten_Gas_HWE_5_1 + Kosten_Strom_HWE_5_1 + Capex_HWE_5_1 * Opex_HWE_5_1 * \
                   b_HWE_5_1_bus['scalars'][0]
    CAPEX_HWE_5_1 = a_HWE_5_1 * b_HWE_5_1_bus['scalars'][0]  # var_Kosten_HWE_5_1 * (E_HW_HWE_5_1 + E_Nachheiz_HWE_5_1)

    # HWE 5.2
    # E_HWE_5_2 = Fernwbus['sequences'][(('HWE_5_2', 'Fernwaerme'), 'flow')].sum()
    # Investkosten_HWE_5_2 = epc_HWE_5_2 * Fernwbus['scalars'][3]
    Steuer_HWE_5_2 = Brennstoffenergiesteuer * Gasbus['sequences'][(('Gas', 'HWE_5_2'), 'flow')].sum()
    # Kosten_HWE_5_2 = Investkosten_HWE_5_2 + Steuer_HWE_5_2
    # print('HWE-5.2: '+str(round(Kosten_HWE_5_2, 0))+' €/a')

    # Kosten_HWE_5_2_alternativ = Investkosten_HWE_5_2 + Steuer_HWE_5_2 + Kosten_Gas_HWE_5_2 + Kosten_Strom_HWE_5_2
    OPEX_HWE_5_2 = Steuer_HWE_5_2 + Kosten_Gas_HWE_5_2 + Kosten_Strom_HWE_5_2 + b_HWE_5_2 * Fernwbus['scalars'][2]
    CAPEX_HWE_5_2 = a_HWE_5_2 * Fernwbus['scalars'][2]

    # Uebrschüsse
    E_Ueberschuss_Strom = Strombus_HS['sequences'][(('Strom_HS', 'Ueberschuss_HS'), 'flow')].sum()
    Kosten_Ueberschuss_Strom = E_Ueberschuss_Strom * 10000000
    print('Überschüsse_Strom: ' + str(round(Kosten_Ueberschuss_Strom, 0)) + ' €/a')
    E_Ueberschuss_Gas = Gasbus['sequences'][(('Gas', 'Ueberschuss_gas'), 'flow')].sum()
    Kosten_Ueberschuss_Gas = E_Ueberschuss_Gas * 10000
    print('Überschüsse_Gas: ' + str(round(Kosten_Ueberschuss_Gas, 0)) + ' €/a')
    E_Ueberschuss_Fernw = Fernwbus['sequences'][(('Fernwaerme', 'Ueberschuss_fern'), 'flow')].sum()
    Kosten_Ueberschuss_Fernw = E_Ueberschuss_Fernw * 0.1
    print('Überschüsse_Fernw: ' + str(round(Kosten_Ueberschuss_Strom, 0)) + ' €/a')
    E_Ueberschuss_Dampf = Dampfbus['sequences'][(('Dampfnetz', 'Ueberschuss_Dampf'), 'flow')].sum()
    Kosten_Ueberschuss_Dampf = E_Ueberschuss_Dampf * 0.1
    print('Überschüsse_Dampf: ' + str(round(Kosten_Ueberschuss_Dampf, 0)) + ' €/a')
    E_Ueberschuss_Frischdampf = Frischdampfbus['sequences'][(('Frischdampf', 'Ueberschuss_Frischdampf'), 'flow')].sum()
    Kosten_Ueberschuss_Frischdampf = E_Ueberschuss_Frischdampf * 0.1
    print('Überschüsse_Frischdampf: ' + str(round(Kosten_Ueberschuss_Frischdampf, 0)) + ' €/a')

    print('------------------------------------------')
    print('Kosten aus Investmodell in €')
    print('------------------------------------------')

    # PV
    # P_PV = Strombus_HS['scalars'][1]
    # Kosten_PV = P_PV * epc_PV
    # print('Photovoltaik: '+str(round(Kosten_PV, 0))+' €/a')
    # opex_pv = b_PV * Strombus_HS['scalars'][1]
    # capex_pv = a_PV * Strombus_HS['scalars'][1]

    # PV direkt
    # P_PV_direkt = Direktleitungsbus_results['scalars'][1]
    # Kosten_PV_direkt = P_PV_direkt * epc_PV
    # print('Photovoltaik direkt: '+str(round(Kosten_PV_direkt, 0))+' €/a')
    # opex_pv_direkt = b_PV * Direktleitungsbus_results['scalars'][1]
    # capex_pv_direkt = a_PV * Direktleitungsbus_results['scalars'][1]

    # PV eigenerzeugung
    P_PV_eigenerzeugung = eigenerzeugung['scalars'][7]
    Kosten_PV_eigenerzeugung = P_PV_eigenerzeugung * epc_PV
    print('PV eigenerzeugung: ' + str(round(Kosten_PV_eigenerzeugung, 0)) + ' €/a')
    opex_pv_eigenerzeugung = b_PV * eigenerzeugung['scalars'][7]
    capex_pv_eigenerzeugung = a_PV * eigenerzeugung['scalars'][7]

    # Wind
    Wind_energiemenge = Direktleitungsbus_results['sequences'][('Wind', 'Direktleitungsbus'), 'flow'].sum()
    Kosten_Wind = Wind_energiemenge * Erneuerbare_Energien['Wind']['variable_Kosten']
    print('Wind: ' + str(round(Kosten_Wind, 0)) + ' €/a')
    # opex_wind = b_Wind * Direktleitungsbus_results['scalars'][1]
    # capex_wind = a_Wind * Direktleitungsbus_results['scalars'][1]

    # ST_RK
    P_ST_roehr = Solarthermiebus['scalars'][0]
    Kosten_ST_roehr = P_ST_roehr * epc_ST_RK
    print('ST RL: ' + str(round(Kosten_ST_roehr, 0)) + ' €/a')
    opex_st_rl = b_ST_RK * Solarthermiebus['scalars'][0] + Kosten_Strom_ST_RL
    capex_st_rl = a_ST_RK * Solarthermiebus['scalars'][0]

    # Wärmepumpe Speicher
    P_WP_Speicher = FünfundneunzigGradbus['scalars'][1]
    Kosten_WP_Speicher = P_WP_Speicher * epc_WP_Speicher_HW
    print('WP_Speicher: ' + str(round(Kosten_WP_Speicher, 0)) + ' €/a')
    opex_wp_speicher = b_RABA_Rauchgas * FünfundneunzigGradbus['scalars'][1] + Kosten_Strom_WP_Speicher
    capex_wp_speicher = a_RABA_Rauchgas * FünfundneunzigGradbus['scalars'][1]

    ###################Fernwaerme-Bus

    # Biomasse Heizwerk
    P_BioHeizwerk = Fernwbus['scalars'][0]
    Kosten_BioHeizwerk = P_BioHeizwerk * epc_BioHeizwerk
    print('BioHeizwerk: ' + str(round(Kosten_BioHeizwerk, 0)) + ' €/a')
    opex_BioHeizwerk = b_BioHeizwerk * Fernwbus['scalars'][0]
    capex_BioHeizwerk = a_BioHeizwerk * Fernwbus['scalars'][0]

    # Heizstab / Elektrodenheizkessel
    P_Heizstab = Fernwbus['scalars'][3]  # direkt
    Kosten_Heizstab_direkt = P_Heizstab * epc_P2H
    print('Heizstab direkt: ' + str(round(Kosten_Heizstab_direkt, 0)) + ' €/a')
    opex_heizstab_direkt = b_P2H * Fernwbus['scalars'][3]
    capex_heizstab_direkt = a_P2H * Fernwbus['scalars'][3]

    P_Heizstab = Fernwbus['scalars'][4]
    Kosten_Heizstab = P_Heizstab * epc_P2H
    print('Heizstab: ' + str(round(Kosten_Heizstab, 0)) + ' €/a')
    opex_heizstab = b_P2H * Fernwbus['scalars'][4] + Kosten_Strom_P2H_Heizstab
    capex_heizstab = a_P2H * Fernwbus['scalars'][4]

    # ST_RK_VL
    P_ST_roehr_VL = Fernwbus['scalars'][5]
    Kosten_ST_roehr_VL = P_ST_roehr_VL * epc_ST_RK
    print('ST_VL: ' + str(round(Kosten_ST_roehr_VL, 0)) + ' €/a')
    opex_st_vl = b_ST_RK * Fernwbus['scalars'][5] + Kosten_Strom_ST_VL
    capex_st_vl = a_ST_RK * Fernwbus['scalars'][5]

    # WP_AHK_RG
    P_WP_AHK_RG = Fernwbus['scalars'][7]
    Kosten_WP_AHK_RG = P_WP_AHK_RG * epc_RABA_Rauchgas
    print('WP_AHK_RG: ' + str(round(Kosten_WP_AHK_RG, 0)) + ' €/a')
    opex_WP_AHK_RG = b_RABA_Rauchgas * Fernwbus['scalars'][7] + Kosten_Strom_WP_AHK_RG
    capex_WP_AHK_RG = a_RABA_Rauchgas * Fernwbus['scalars'][7]

    # Wärmepumpe Abwasser_Industrie
    P_WP_Abwasser_Industrie = Fernwbus['scalars'][8]
    Kosten_WP_Abwasser_Industrie = P_WP_Abwasser_Industrie * epc_Waescherei
    print('WP_Abwasser_Industrie: ' + str(round(Kosten_WP_Abwasser_Industrie, 0)) + ' €/a')
    opex_WP_Abwasser_Industrie = b_Waescherei * Fernwbus['scalars'][8] + Kosten_Strom_WP_Abwasser_Industrie
    capex_WP_Abwasser_Industrie = a_Waescherei * Fernwbus['scalars'][8]

    # Wärmepumpe Flusswasser/Seen
    P_WP_Flusswasser_Seen = Fernwbus['scalars'][9]
    Kosten_WP_Flusswasser_Seen = P_WP_Flusswasser_Seen * epc_WWK
    print('WP_Flusswasser_Seen: ' + str(round(Kosten_WP_Flusswasser_Seen, 0)) + ' €/a')
    opex_WP_Flusswasser_Seen = b_WWK * Fernwbus['scalars'][9] + Kosten_Strom_WP_Flusswasser_Seen
    capex_WP_Flusswasser_Seen = a_WWK * Fernwbus['scalars'][9]

    # Wärmepumpe Heisswasser
    P_WP_Heisswasser = Fernwbus['scalars'][10]
    Kosten_WP_Heisswasser = P_WP_Heisswasser * epc_WP_Speicher_HW
    print('WP_HW: ' + str(round(Kosten_WP_Heisswasser, 0)) + ' €/a')
    opex_wp_hw = b_RABA_Rauchgas * Fernwbus['scalars'][10] + Kosten_Strom_WP_Heisswasser
    capex_wp_hw = a_RABA_Rauchgas * Fernwbus['scalars'][10]

    # Wärmepumpe Luftwaerme
    P_WP_Luftwaerme = Fernwbus['scalars'][11]
    Kosten_WP_Luftwaerme = P_WP_Luftwaerme * epc_Luftwaerme
    print('WP Luftwaerme: ' + str(round(Kosten_WP_Luftwaerme, 0)) + ' €/a')
    opex_wp_luft = b_Luftwaerme * Fernwbus['scalars'][11] + Kosten_Strom_WP_Luftwaerme
    capex_wp_luft = a_Luftwaerme * Fernwbus['scalars'][11]

    # Wärmepumpe Luftwaerme direkt
    P_WP_Luftwaerme_direkt = Fernwbus['scalars'][12]
    Kosten_WP_Luftwaerme_direkt = P_WP_Luftwaerme_direkt * epc_Luftwaerme_direkt
    print('WP Luftwaerme direkt: ' + str(round(Kosten_WP_Luftwaerme_direkt, 0)) + ' €/a')
    opex_wp_luft_direkt = b_Luftwaerme_direkt * Fernwbus['scalars'][12]
    capex_wp_luft_direkt = a_Luftwaerme_direkt * Fernwbus['scalars'][12]

    # Wärmepumpe
    P_WP_RABA_Rauchgas = Fernwbus['scalars'][13]
    Kosten_WP_RABA_Rauchgas = P_WP_RABA_Rauchgas * epc_RABA_Rauchgas
    print('WP_RABA_Rauchgas: ' + str(round(Kosten_WP_RABA_Rauchgas, 0)) + ' €/a')
    opex_wp_raba_rg = b_RABA_Rauchgas * Fernwbus['scalars'][13] + Kosten_Strom_WP_RABA_Rauchgas
    capex_wp_raba_rg = a_RABA_Rauchgas * Fernwbus['scalars'][13]

    # Wärmepumpe RABA_alternativ
    P_WP_RABA_alternativ = Fernwbus['scalars'][14]
    Kosten_WP_RABA_alternativ = P_WP_RABA_alternativ * epc_RABA_alternativ
    print('WP_RABA_alternativ: ' + str(round(Kosten_WP_RABA_alternativ, 0)) + ' €/a')
    opex_wp_raba_a = b_RABA_alternativ * Fernwbus['scalars'][14] + Kosten_Strom_WP_RABA_alternativ
    capex_wp_raba_a = a_RABA_alternativ * Fernwbus['scalars'][14]

    # Wärmepumpe WWK
    P_WP_WWK = Fernwbus['scalars'][15]
    Kosten_WP_WWK = P_WP_WWK * epc_WWK
    print('WP_WWK: ' + str(round(Kosten_WP_WWK, 0)) + ' €/a')
    opex_wp_wwk = b_WWK * Fernwbus['scalars'][15] + Kosten_Strom_WP_WWK
    capex_wp_wwk = a_WWK * Fernwbus['scalars'][15]

    # Wärmepumpe Waescherei
    P_WP_Waescherei = Fernwbus['scalars'][16]
    Kosten_WP_Waescherei = P_WP_Waescherei * epc_Waescherei
    print('WP_Waescherei: ' + str(round(Kosten_WP_Waescherei, 0)) + ' €/a')
    opex_wp_waescherei = b_Waescherei * Fernwbus['scalars'][16] + Kosten_Strom_WP_Waescherei
    capex_wp_waescherei = a_Waescherei * Fernwbus['scalars'][16]

    # Tiefengeothermie
    # tiefengeothermie_energiemenge = Fernwbus['sequences'][('xTiefengeothermie','Fernwaerme'),'flow'].sum()
    # Kosten_Tiefengeothermie = tiefengeothermie_energiemenge * 20
    opex_geothermie = b_Geothermie * Fernwbus['scalars'][17]
    capex_geothermie = a_Geothermie * Fernwbus['scalars'][17]

    # Biomasse
    P_Biomasse = eigenerzeugung['scalars'][0]
    Kosten_Biomasse = P_Biomasse * epc_Biogas
    print('Biomasse BHKW: ' + str(round(Kosten_Biomasse, 0)) + ' €/a')
    opex_biogas = b_Biogas * eigenerzeugung['scalars'][0] + Kosten_Biomasse_Biogasanlage
    capex_biogas = a_Biogas * eigenerzeugung['scalars'][0]

    P_Biomasse_Einspeisung = Gasbus['scalars'][0]
    Kosten_Biomasse_Einspeisung = P_Biomasse * epc_Biogaseinspeisung
    print('Biomasse_Einspeisung: ' + str(round(Kosten_Biomasse_Einspeisung, 0)) + ' €/a')
    opex_biomasse_einsp = b_Biogas * Gasbus['scalars'][0] + Kosten_Biomasse_Biogaseinspeisung
    capex_biomasse_einsp = a_Biogas * Gasbus['scalars'][0]

    # Netznutzungsentgelte
    P_NNE = max(+Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_RABA_Rauchgas'), 'flow']
                + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_RABA_alternativ'), 'flow']
                # +Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz','WP_WWK'),'flow']
                + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_Waescherei'), 'flow']
                + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'ST_roehr_VL'), 'flow']
                + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'ST_roehr_RL'), 'flow']
                + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_1_Heißwasser'), 'flow']
                + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_1_Nachheizung'), 'flow']
                + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_2'), 'flow']
                + eigenverbrauch['sequences'][('Import_Strom_Eigenverbrauch', 'Strom_HS_Eigenverbrauch'), 'flow']
                + Betriebsverbrauch['sequences'][('Import_Betriebsverbrauch', 'Betriebsverbrauch'), 'flow']
                )
    Kosten_NNE = P_NNE * Stromnetze['Strom HS 110kV']['Leistungspreis_Netzentgelte']
    print('NNE: ' + str(round(Kosten_NNE, 0)) + ' €/a')
    # Wärmespeeicher
    C_Waermespeicher = WSP_drucklos_results['scalars'][3]
    Kosten_Waermespeicher = C_Waermespeicher * epc_WSP_drucklos
    print('Waermespeicher: ' + str(round(Kosten_Waermespeicher, 0)) + ' €/a')
    print('------------------------------------------')
    print('Import/Export in €')
    print('------------------------------------------')
    Erloese_Strom_HS = 0
    Importkosten_Strom2 = 0
    # Importkosten_Gas=0
    Importkosten_Biomasse = 0
    Import_Strom_SWE = [0] * len(eigenerzeugung['sequences'][('Strom_HS_Eigenerzeugung', 'Stromexport'), 'flow'])

    for i in range(0, len(eigenerzeugung['sequences'][('Strom_HS_Eigenerzeugung', 'Stromexport'), 'flow'])):
        # Importkosten_Gas += (Gasbus['sequences'][('Import_Gas','Gas'),'flow'][i]/Stundenteile) * data_Preise_2040_CH4_Eur_MWh_Import[i]
        Importkosten_Biomasse += (Biobus_results['sequences'][('Biobus', 'Biogas'), 'flow'][i] / Stundenteile) * \
                                 data_Preis_Biomasse[i]
        Importkosten_Strom2 += ((Betriebsverbrauch['sequences'][
                                     ('Import_Betriebsverbrauch', 'Betriebsverbrauch'), 'flow'][
                                     i] + eigenverbrauch['sequences'][
                                     ('Import_Strom_Eigenverbrauch', 'Strom_HS_Eigenverbrauch'), 'flow'][i] +
                                 Eigenverbrauch_Stadtgebiet['sequences'][
                                     ('Import_Strom_WP', 'WP_Abwaerme_Netz'), 'flow'][
                                     i]) / Stundenteile) * data_Boerse_Import[i]
        Erloese_Strom_HS += (eigenerzeugung['sequences'][(('Strom_HS_Eigenerzeugung', 'Stromexport'), 'flow')][i] +
                             eigenerzeugung['sequences'][(('Strom_HS_Eigenerzeugung', 'Trafo_Kosten_vnne'), 'flow')][
                                 i]) * \
                            data_Boerse[i]

    Importkosten_Strom_NNE = Importkosten_Strom2 + Kosten_NNE
    print('Gasbezug: ' + str(round(Importkosten_Gas, 0)) + ' €/a')
    print('Strombezug: ' + str(round(Importkosten_Strom_NNE, 0)) + ' €/a')
    print('Stromerlös: ' + str(round(Erloese_Strom_HS, 0)) + ' €/a')
    print('Importkosten_Biomasse: ' + str(round(Importkosten_Biomasse, 0)) + ' €/a')

    t1 = np.argmax(Strombus_HS['sequences'][('Strom_HS', 'Last_Strom'), 'flow']
                   + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_RABA_Rauchgas'), 'flow']
                   + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_RABA_alternativ'), 'flow']
                   # +Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz','WP_WWK'),'flow']
                   + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_Waescherei'), 'flow']
                   + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'ST_roehr_VL'), 'flow']
                   + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'ST_roehr_RL'), 'flow']
                   + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_1_Heißwasser'), 'flow']
                   + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_1_Nachheizung'), 'flow']
                   + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_2'), 'flow']
                   + eigenverbrauch['sequences'][('Import_Strom_Eigenverbrauch', 'Strom_HS_Eigenverbrauch'), 'flow']
                   + Betriebsverbrauch['sequences'][('Import_Betriebsverbrauch', 'Betriebsverbrauch'), 'flow']
                   )

    P_max_last = max(Strombus_HS['sequences'][('Strom_HS', 'Last_Strom'), 'flow']
                     + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_RABA_Rauchgas'), 'flow']
                     + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_RABA_alternativ'), 'flow']
                     # +Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz','WP_WWK'),'flow']
                     + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'WP_Waescherei'), 'flow']
                     + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'ST_roehr_VL'), 'flow']
                     + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'ST_roehr_RL'), 'flow']
                     + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_1_Heißwasser'), 'flow']
                     + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_1_Nachheizung'), 'flow']
                     + Eigenverbrauch_Stadtgebiet['sequences'][('WP_Abwaerme_Netz', 'HWE_5_2'), 'flow']
                     + eigenverbrauch['sequences'][('Import_Strom_Eigenverbrauch', 'Strom_HS_Eigenverbrauch'), 'flow']
                     + Betriebsverbrauch['sequences'][('Import_Betriebsverbrauch', 'Betriebsverbrauch'), 'flow'])

    P_bezug_t1 = Strombus_HS['sequences'][('Import_Strom', 'Strom_HS'), 'flow'][t1] + \
                 eigenverbrauch['sequences'][('Import_Strom_Eigenverbrauch', 'Strom_HS_Eigenverbrauch'), 'flow'][t1] + \
                 Eigenverbrauch_Stadtgebiet['sequences'][('Import_Strom_WP', 'WP_Abwaerme_Netz'), 'flow'][t1] + \
                 Betriebsverbrauch['sequences'][('Import_Betriebsverbrauch', 'Betriebsverbrauch'), 'flow'][t1]
    p_tE = P_max_last - P_bezug_t1

    p_max_bezug = max(Strombus_HS['sequences'][('Import_Strom', 'Strom_HS'), 'flow'] + eigenverbrauch['sequences'][
        ('Import_Strom_Eigenverbrauch', 'Strom_HS_Eigenverbrauch'), 'flow'] + Eigenverbrauch_Stadtgebiet['sequences'][
                          ('Import_Strom_WP', 'WP_Abwaerme_Netz'), 'flow'] + Betriebsverbrauch['sequences'][
                          ('Import_Betriebsverbrauch', 'Betriebsverbrauch'), 'flow'])
    p_vermieden = P_max_last - p_max_bezug

    s_vne = p_vermieden / p_tE
    p_verguetung = s_vne * p_vermieden
    verguetung_nne = p_verguetung * vnneLP

    E_GT = Strombus_HS['sequences'][(('Trafo_Kosten_vnne', 'Strom_HS'), 'flow')].sum()
    var_costs_vne = verguetung_nne / E_GT
    print('var_costs_vne: ' + str(round(var_costs_vne, 0)) + ' €/MWh')

    NNE_Kraftwerksgas = Gasbus['scalars'][2] * Gasnetz['Gasnetz']['NNE_Kraftwerksgas_2035']

    # %%

    bew_foerderung_wwk = Fernwbus['sequences'][('WP_WWK', 'Fernwaerme'), 'flow'].sum() * BEW_Foerderung_WP['WP_WWK'][
        'Betriebskostenfoerderung_max']
    # bew_foerderung_flusswasser_seen=Fernwbus['sequences'][('WP_Flusswasser_Seen','Fernwaerme'),'flow'].sum()*BEW_Foerderung_WP['WP_Flusswasser_Seen']['Betriebskostenfoerderung_max']
    # bew_foerderung_waescherei=Fernwbus['sequences'][('WP_Waescherei','Fernwaerme'),'flow'].sum()*BEW_Foerderung_WP['WP_Waescherei']['Betriebskostenfoerderung_max']
    # bew_foerderung_abwasser_industrie=Fernwbus['sequences'][('WP_Abwasser_Industrie','Fernwaerme'),'flow'].sum()*BEW_Foerderung_WP['WP_Abwasser_Industrie']['Betriebskostenfoerderung_max']
    # bew_foerderung_raba_rg=Fernwbus['sequences'][('WP_RABA_Rauchgas','Fernwaerme'),'flow'].sum()*BEW_Foerderung_WP['WP_RABA_Rauchgas']['Betriebskostenfoerderung_max']
    # bew_foerderung_raba_a=Fernwbus['sequences'][('WP_RABA_alternativ','Fernwaerme'),'flow'].sum()*BEW_Foerderung_WP['WP_RABA_alternativ']['Betriebskostenfoerderung_max']
    # bew_foerderung_luft_direkt=Fernwbus['sequences'][('WP_Luftwaerme_direkt','Fernwaerme'),'flow'].sum()*BEW_Foerderung_WP['WP_Luftwaerme_direkt']['Betriebskostenfoerderung_max']

    bew_summe = 0

    # %%
    gesamtkosten_alternativ2 = (CAPEX_linie1 + CAPEX_linie2 + CAPEX_linie3 +
                                CAPEX_DT_Tandem + CAPEX_DT_Bestand +
                                CAPEX_HWE_2 + CAPEX_HWE_5_1 + CAPEX_HWE_5_2 +
                                Kosten_Waermespeicher +

                                OPEX_linie1 + OPEX_linie2 + OPEX_linie3 +
                                OPEX_HWE_2 + OPEX_HWE_5_1 + OPEX_HWE_5_2 +
                                OPEX_DT_Tandem + OPEX_DT_Bestand +

                                capex_biogas + capex_biomasse_einsp + capex_BioHeizwerk +  # capex_pv +
                                capex_st_vl + capex_st_rl +
                                capex_wp_speicher + capex_wp_luft + capex_wp_hw +
                                capex_wp_raba_rg + capex_wp_raba_a + capex_wp_wwk + capex_wp_waescherei +
                                capex_WP_AHK_RG + capex_WP_Flusswasser_Seen + capex_WP_Abwasser_Industrie +
                                capex_heizstab + capex_heizstab_direkt +
                                # capex_pv_direkt +
                                # capex_wind +
                                capex_pv_eigenerzeugung + opex_pv_eigenerzeugung +
                                capex_wp_luft_direkt +

                                opex_biogas + opex_biomasse_einsp + opex_BioHeizwerk +  # opex_pv +
                                opex_st_vl + opex_st_rl +
                                opex_wp_speicher + opex_wp_luft + opex_wp_hw +
                                opex_wp_raba_rg + opex_wp_raba_a + opex_wp_wwk + opex_wp_waescherei +
                                opex_WP_AHK_RG + opex_WP_Flusswasser_Seen + opex_WP_Abwasser_Industrie +
                                opex_heizstab + opex_heizstab_direkt +
                                # opex_pv_direkt +
                                Kosten_Wind +
                                # opex_wind +
                                Ferndampfbezug_Kosten + capex_geothermie + opex_geothermie +
                                opex_wp_luft_direkt +

                                Kosten_Ueberschuss_Strom +
                                Kosten_Ueberschuss_Dampf +
                                Kosten_Ueberschuss_Frischdampf +
                                NNE_Kraftwerksgas +
                                Kosten_NNE -
                                Erloese_GT_1 - Erloese_GT_2 - Erloese_GT_3 -
                                Erloese_DT_Tandem - Erloese_DT_Bestand -  # Erloese_PV-
                                verguetung_nne -
                                bew_summe)

    print('Gesamtkosten: ' + str(round(gesamtkosten_alternativ2, 0)) + ' €/a')

    # %%

    capex_opex = pd.Series([CAPEX_linie1, CAPEX_linie2, CAPEX_linie3, CAPEX_DT_Tandem, CAPEX_DT_Bestand,
                            CAPEX_HWE_2, CAPEX_HWE_5_1, CAPEX_HWE_5_2,
                            Kosten_Waermespeicher,
                            OPEX_linie1, OPEX_linie2, OPEX_linie3,
                            OPEX_HWE_2, OPEX_HWE_5_1, OPEX_HWE_5_2,
                            OPEX_DT_Tandem, OPEX_DT_Bestand,

                            capex_biogas, capex_biomasse_einsp, capex_BioHeizwerk,
                            capex_st_vl, capex_st_rl,
                            capex_wp_speicher, capex_wp_luft, capex_wp_hw,
                            capex_wp_raba_rg, capex_wp_raba_a, capex_wp_wwk, capex_wp_waescherei,
                            capex_WP_AHK_RG, capex_WP_Flusswasser_Seen, capex_WP_Abwasser_Industrie,
                            capex_heizstab, capex_heizstab_direkt,
                            capex_geothermie,

                            capex_pv_eigenerzeugung, opex_pv_eigenerzeugung,
                            capex_wp_luft_direkt,

                            opex_biogas, opex_biomasse_einsp, opex_BioHeizwerk,
                            opex_st_vl, opex_st_rl,
                            opex_wp_speicher, opex_wp_luft, opex_wp_hw,
                            opex_wp_raba_rg, opex_wp_raba_a, opex_wp_wwk, opex_wp_waescherei,
                            opex_WP_AHK_RG, opex_WP_Flusswasser_Seen, opex_WP_Abwasser_Industrie,
                            opex_heizstab, opex_heizstab_direkt,
                            opex_geothermie,

                            Kosten_Wind, Ferndampfbezug_Kosten,
                            opex_wp_luft_direkt,

                            Kosten_Ueberschuss_Strom, Kosten_Ueberschuss_Dampf, Kosten_Ueberschuss_Frischdampf,
                            NNE_Kraftwerksgas, Kosten_NNE, Erloese_GT_1, Erloese_GT_2, Erloese_GT_3,
                            Erloese_DT_Tandem, Erloese_DT_Bestand,
                            verguetung_nne, bew_summe],
                           index=['CAPEX_linie1', 'CAPEX_linie2', 'CAPEX_linie3', 'CAPEX_DT_Tandem',
                                  'CAPEX_DT_Bestand',
                                  'CAPEX_HWE_2', 'CAPEX_HWE_5_1', 'CAPEX_HWE_5_2',
                                  'Kosten_Waermespeicher',
                                  'OPEX_linie1', 'OPEX_linie2', 'OPEX_linie3',
                                  'OPEX_HWE_2', 'OPEX_HWE_5_1', 'OPEX_HWE_5_2',
                                  'OPEX_DT_Tandem', 'OPEX_DT_Bestand',

                                  'capex_biogas', 'capex_biomasse_einsp', 'capex_BioHeizwerk',
                                  'capex_st_vl', 'capex_st_rl',
                                  'capex_wp_speicher', 'capex_wp_luft', 'capex_wp_hw',
                                  'capex_wp_raba_rg', 'capex_wp_raba_a', 'capex_wp_wwk', 'capex_wp_waescherei',
                                  'capex_WP_AHK_RG', 'capex_WP_Flusswasser_Seen', 'capex_WP_Abwasser_Industrie',
                                  'capex_heizstab', 'capex_heizstab_direkt',
                                  'capex_geothermie',

                                  'capex_pv_eigenerzeugung', 'opex_pv_eigenerzeugung',
                                  'capex_wp_luft_direkt',

                                  'opex_biogas', 'opex_biomasse_einsp', 'opex_BioHeizwerk',
                                  'opex_st_vl', 'opex_st_rl',
                                  'opex_wp_speicher', 'opex_wp_luft', 'opex_wp_hw',
                                  'opex_wp_raba_rg', 'opex_wp_raba_a', 'opex_wp_wwk', 'opex_wp_waescherei',
                                  'opex_WP_AHK_RG', 'opex_WP_Flusswasser_Seen', 'opex_WP_Abwasser_Industrie',
                                  'opex_heizstab', 'opex_heizstab_direkt',
                                  'opex_geothermie',

                                  'Kosten_Wind', 'Ferndampfbezug_Kosten',
                                  'opex_wp_luft_direkt',

                                  'Kosten_Ueberschuss_Strom', 'Kosten_Ueberschuss_Dampf',
                                  'Kosten_Ueberschuss_Frischdampf',
                                  'NNE_Kraftwerksgas', 'Kosten_NNE', 'Erloese_GT_1 ', 'Erloese_GT_2', 'Erloese_GT_3 ',
                                  'Erloese_DT_Tandem ', 'Erloese_DT_Bestand',
                                  'verguetung_nne', 'bew_summe'
                                  ])

    result_path = os.path.join(my_path, "07_Simulationsergebnisse", name)

    capex_opex.to_csv(result_path + '/capex_opex.csv', decimal=',')

    opex_strom_gas = pd.Series([Kosten_Strom_AHK_1, Kosten_Gas_Linie_1,
                                Kosten_Strom_AHK_2, Kosten_Gas_Linie_2,
                                Kosten_Strom_AHK_3, Kosten_Gas_Linie_3,
                                Kosten_Gas_HWE_2, Kosten_Strom_HWE_2,
                                Kosten_Gas_HWE_5_1, Kosten_Strom_HWE_5_1,
                                Kosten_Gas_HWE_5_2, Kosten_Strom_HWE_5_2,
                                Kosten_Strom_WP_Speicher, Kosten_Strom_WP_WWK,
                                Kosten_Strom_WP_Abwasser_Industrie,
                                Kosten_Strom_WP_Flusswasser_Seen,
                                Kosten_Strom_WP_Heisswasser,
                                Kosten_Strom_WP_RABA_alternativ, Kosten_Strom_WP_Luftwaerme,
                                Kosten_Strom_WP_Waescherei,
                                Kosten_Strom_P2H_Heizstab
                                ],
                               index=[
                                   'Kosten_Strom_AHK_1', 'Kosten_Gas_Linie_1',
                                   'Kosten_Strom_AHK_2', 'Kosten_Gas_Linie_2',
                                   'Kosten_Strom_AHK_3', 'Kosten_Gas_Linie_3',
                                   'Kosten_Gas_HWE_2', 'Kosten_Strom_HWE_2',
                                   'Kosten_Gas_HWE_5_1', 'Kosten_Strom_HWE_5_1',
                                   'Kosten_Gas_HWE_5_2', 'Kosten_Strom_HWE_5_2',
                                   'Kosten_Strom_WP_Speicher', 'Kosten_Strom_WP_WWK',
                                   'Kosten_Strom_WP_Abwasser_Industrie',
                                   'Kosten_Strom_WP_Flusswasser_Seen',
                                   'Kosten_Strom_WP_Heisswasser',
                                   'Kosten_Strom_WP_RABA_alternativ', 'Kosten_Strom_WP_Luftwaerme',
                                   'Kosten_Strom_WP_Waescherei',
                                   'Kosten_Strom_P2H_Heizstab'
                               ])

    opex_strom_gas.to_csv(result_path + '/opex_strom_gas.csv', decimal=',')

    print('#######################################################################')
    # linien
    kosten_energieeinheit_linie1 = (CAPEX_linie1 + OPEX_linie1) / (
            Frischdampfbus['sequences'][(('FrischdampfHilfstrafo_Linie1', 'Frischdampf'), 'flow')].sum() +
            Fernwbus['sequences'][(('AHK_1_AB', 'Fernwaerme'), 'flow')].sum() +
            Fernwbus['sequences'][(('AHK_1_KB', 'Fernwaerme'), 'flow')].sum() +
            Fernwbus['sequences'][(('AHK_1_FB', 'Fernwaerme'), 'flow')].sum())
    print('kosten_energieeinheit_linie1 dampf/HW: ' + str(round(kosten_energieeinheit_linie1, 2)) + ' €/MWh')
    kosten_energieeinheit_linie2 = (CAPEX_linie2 + OPEX_linie2) / (
            Frischdampfbus['sequences'][(('FrischdampfHilfstrafo_Linie2', 'Frischdampf'), 'flow')].sum() +
            Fernwbus['sequences'][(('AHK_2_AB', 'Fernwaerme'), 'flow')].sum() +
            Fernwbus['sequences'][(('AHK_2_KB', 'Fernwaerme'), 'flow')].sum() +
            Fernwbus['sequences'][(('AHK_2_FB', 'Fernwaerme'), 'flow')].sum())
    print('kosten_energieeinheit_linie2 dampf/HW: ' + str(round(kosten_energieeinheit_linie2, 2)) + ' €/MWh')
    kosten_energieeinheit_linie3 = (CAPEX_linie3 + OPEX_linie3) / (
            Frischdampfbus['sequences'][(('AHK_3_AB', 'Frischdampf'), 'flow')].sum() +
            Fernwbus['sequences'][(('AHK_3_AB', 'Fernwaerme'), 'flow')].sum())
    print('kosten_energieeinheit_linie3 dampf/HW: ' + str(round(kosten_energieeinheit_linie3, 2)) + ' €/MWh')

    # dt
    kosten_energieeinheit_dt_tandem = (CAPEX_DT_Tandem + OPEX_DT_Tandem) / (
            Fernwbus['sequences'][(('DT-Tandem ND-Teil', 'Fernwaerme'), 'flow')].sum() +
            Dampfbus['sequences'][(('Anzapfung_Tandem_DT', 'Dampfnetz'), 'flow')].sum())
    print('kosten_energieeinheit_dt_tandem dampf/HW: ' + str(round(kosten_energieeinheit_dt_tandem, 2)) + ' €/MWh')
    kosten_energieeinheit_dt_bestand = (CAPEX_DT_Bestand + OPEX_DT_Bestand) / (
            Fernwbus['sequences'][(('DT-Bestand', 'Fernwaerme'), 'flow')].sum() + Dampfbus['sequences'][
        (('DT-Bestand', 'Dampfnetz'), 'flow')].sum())
    print('kosten_energieeinheit_dt_bestand HW: ' + str(round(kosten_energieeinheit_dt_bestand, 2)) + ' €/MWh')

    # hwe
    kosten_energieeinheit_hwe_2 = (CAPEX_HWE_2 + OPEX_HWE_2) / Fernwbus['sequences'][
        (('HWE_2', 'Fernwaerme'), 'flow')].sum()
    print('kosten_energieeinheit_hwe_2 HW: ' + str(round(kosten_energieeinheit_hwe_2, 2)) + ' €/MWh')
    kosten_energieeinheit_hwe_5_1 = (CAPEX_HWE_5_1 + OPEX_HWE_5_1) / (
            Fernwbus['sequences'][(('HWE_5_1_Heißwasser', 'Fernwaerme'), 'flow')].sum() +
            Nachheizbus['sequences'][(('HWE_5_1_Nachheizung', 'Nachheizhilfebus'), 'flow')].sum())
    print('kosten_energieeinheit_hwe_5_1 HW: ' + str(round(kosten_energieeinheit_hwe_5_1, 2)) + ' €/MWh')
    kosten_energieeinheit_hwe_5_2 = (CAPEX_HWE_5_2 + OPEX_HWE_5_2) / Fernwbus['sequences'][
        (('HWE_5_2', 'Fernwaerme'), 'flow')].sum()
    print('kosten_energieeinheit_hwe_5_2 HW: ' + str(round(kosten_energieeinheit_hwe_5_2, 2)) + ' €/MWh')

    # erneuerbar
    kosten_energieeinheit_biogas_el = (capex_biogas + opex_biogas) / eigenerzeugung['sequences'][
        (('Biogas', 'Strom_HS_Eigenerzeugung'), 'flow')].sum()
    print('kosten_energieeinheit_biogas el: ' + str(round(kosten_energieeinheit_biogas_el, 2)) + ' €/MWh')

    kosten_energieeinheit_biogas_th = (capex_biogas + opex_biogas) / Fernwbus['sequences'][
        (('Biogas', 'Fernwaerme'), 'flow')].sum()
    print('kosten_energieeinheit_biogas th: ' + str(round(kosten_energieeinheit_biogas_th, 2)) + ' €/MWh')

    kosten_energieeinheit_pv_eigenerzeugung = (capex_pv_eigenerzeugung + opex_pv_eigenerzeugung) / \
                                              eigenerzeugung['sequences'][
                                                  (('PV_eigenerzeugung', 'Strom_HS_Eigenerzeugung'), 'flow')].sum()
    print(
        'kosten_energieeinheit_pv_eigenerzeugung: ' + str(round(kosten_energieeinheit_pv_eigenerzeugung, 2)) + ' €/MWh')

    kosten_energieeinheit_bioeinsp = (capex_biomasse_einsp + opex_biomasse_einsp) / Gasbus['sequences'][
        (('Biogaseinspeisung_Neuanlagen', 'Gas'), 'flow')].sum()
    print('kosten_energieeinheit_bioeinsp: ' + str(round(kosten_energieeinheit_bioeinsp, 2)) + ' €/MWh')

    kosten_energieeinheit_heizstab = (capex_heizstab + opex_heizstab) / Fernwbus['sequences'][
        (('P2H_Heizstab', 'Fernwaerme'), 'flow')].sum()
    print('kosten_energieeinheit_heizstab: ' + str(round(kosten_energieeinheit_heizstab, 2)) + ' €/MWh')

    kosten_energieeinheit_heizstab_direkt = (capex_heizstab_direkt + opex_heizstab_direkt) / Fernwbus['sequences'][
        (('Heizstab_Direkt', 'Fernwaerme'), 'flow')].sum()
    print('kosten_energieeinheit_heizstab_direkt: ' + str(round(kosten_energieeinheit_heizstab_direkt, 2)) + ' €/MWh')

    kosten_energieeinheit_wind = (Kosten_Wind) / Direktleitungsbus_results['sequences'][
        (('Wind', 'Direktleitungsbus'), 'flow')].sum()
    print('kosten_energieeinheit_wind: ' + str(round(kosten_energieeinheit_wind, 2)) + ' €/MWh')

    kosten_energieeinheit_st_vl = (capex_st_vl + opex_st_vl) / Fernwbus['sequences'][
        (('ST_roehr_VL', 'Fernwaerme'), 'flow')].sum()
    print('kosten_energieeinheit_st_vl: ' + str(round(kosten_energieeinheit_st_vl, 2)) + ' €/MWh')

    kosten_energieeinheit_st_rl = (capex_st_rl + opex_st_rl) / Solarthermiebus['sequences'][
        (('ST_roehr_RL', 'Solarthermiebus'), 'flow')].sum()
    print('kosten_energieeinheit_st_rl: ' + str(round(kosten_energieeinheit_st_rl, 2)) + ' €/MWh')

    # wp WP_AHK_RG
    kosten_energieeinheit_wp_raba_rg = (capex_wp_raba_rg + opex_wp_raba_rg) / Fernwbus['sequences'][
        (('WP_RABA_Rauchgas', 'Fernwaerme'), 'flow')].sum()
    kosten_energieeinheit_wp_raba_a = (capex_wp_raba_a + opex_wp_raba_a) / Fernwbus['sequences'][
        (('WP_RABA_alternativ', 'Fernwaerme'), 'flow')].sum()
    kosten_energieeinheit_wp_wwk = (capex_wp_wwk + opex_wp_wwk) / Fernwbus['sequences'][
        (('WP_WWK', 'Fernwaerme'), 'flow')].sum()
    kosten_energieeinheit_wp_waescherei = (capex_wp_waescherei + opex_wp_waescherei) / Fernwbus['sequences'][
        (('WP_Waescherei', 'Fernwaerme'), 'flow')].sum()
    kosten_energieeinheit_WP_Abwasser_Industrie = (capex_WP_Abwasser_Industrie + opex_WP_Abwasser_Industrie) / \
                                                  Fernwbus['sequences'][
                                                      (('WP_Abwasser_Industrie', 'Fernwaerme'), 'flow')].sum()
    kosten_energieeinheit_WP_Flusswasser_Seen = (capex_WP_Flusswasser_Seen + opex_WP_Flusswasser_Seen) / \
                                                Fernwbus['sequences'][
                                                    (('WP_Flusswasser_Seen', 'Fernwaerme'), 'flow')].sum()

    kosten_energieeinheit_wp_speicher = (capex_wp_speicher + opex_wp_speicher) / FünfundneunzigGradbus['sequences'][
        (('WP_Speicher', 'FünfundneunzigGradbus'), 'flow')].sum()
    kosten_energieeinheit_wp_luft = (capex_wp_luft + opex_wp_luft) / Fernwbus['sequences'][
        (('WP_Luftwaerme', 'Fernwaerme'), 'flow')].sum()
    kosten_energieeinheit_wp_hw = (capex_wp_hw + opex_wp_hw) / Fernwbus['sequences'][
        (('WP_Heisswasser', 'Fernwaerme'), 'flow')].sum()
    kosten_energieeinheit_WP_AHK_RG = (capex_WP_AHK_RG + opex_WP_AHK_RG) / Fernwbus['sequences'][
        (('WP_AHK_RG', 'Fernwaerme'), 'flow')].sum()
    kosten_energieeinheit_wp_luft_direkt = (capex_wp_luft_direkt + opex_wp_luft_direkt) / Fernwbus['sequences'][
        (('WP_Luftwaerme_direkt', 'Fernwaerme'), 'flow')].sum()

    print('#######################################################################')

    Resultate_spezifische_kosten = pd.Series(
        [kosten_energieeinheit_linie1, kosten_energieeinheit_linie2, kosten_energieeinheit_linie3,
         kosten_energieeinheit_dt_tandem, kosten_energieeinheit_dt_bestand,
         kosten_energieeinheit_hwe_2, kosten_energieeinheit_hwe_5_1, kosten_energieeinheit_hwe_5_2,
         kosten_energieeinheit_biogas_th, kosten_energieeinheit_pv_eigenerzeugung, kosten_energieeinheit_bioeinsp,
         kosten_energieeinheit_heizstab, kosten_energieeinheit_wind,
         kosten_energieeinheit_st_vl, kosten_energieeinheit_st_rl,
         kosten_energieeinheit_wp_raba_rg, kosten_energieeinheit_wp_raba_a, kosten_energieeinheit_wp_wwk,
         kosten_energieeinheit_wp_waescherei, kosten_energieeinheit_WP_Abwasser_Industrie,
         kosten_energieeinheit_WP_Flusswasser_Seen,
         kosten_energieeinheit_wp_speicher,
         kosten_energieeinheit_wp_luft,
         kosten_energieeinheit_wp_hw,
         kosten_energieeinheit_WP_AHK_RG,
         kosten_energieeinheit_wp_luft_direkt],
        index=['kosten_energieeinheit_linie1', 'kosten_energieeinheit_linie2', 'kosten_energieeinheit_linie3',
               'kosten_energieeinheit_dt_tandem', 'kosten_energieeinheit_dt_bestand',
               'kosten_energieeinheit_hwe_2', 'kosten_energieeinheit_hwe_5_1', 'kosten_energieeinheit_hwe_5_2',
               'kosten_energieeinheit_biogas', 'kosten_energieeinheit_pv_eigenerzeugung',
               'kosten_energieeinheit_bioeinsp',
               'kosten_energieeinheit_heizstab', 'kosten_energieeinheit_wind',
               'kosten_energieeinheit_st_vl', 'kosten_energieeinheit_st_rl',
               'kosten_energieeinheit_wp_raba_rg', 'kosten_energieeinheit_wp_raba_a', 'kosten_energieeinheit_wp_wwk',
               'kosten_energieeinheit_wp_waescherei', 'kosten_energieeinheit_WP_Abwasser_Industrie',
               'kosten_energieeinheit_WP_Flusswasser_Seen',
               'kosten_energieeinheit_wp_speicher',
               'kosten_energieeinheit_wp_luft',
               'kosten_energieeinheit_wp_hw',
               'kosten_energieeinheit_WP_AHK_RG',
               'kosten_energieeinheit_wp_luft_direkt'
               ])

    Resultate_spezifische_kosten.to_csv(result_path + '/spezifischeKosten.csv', decimal=',')

    # %% CO2-Berechnung
    Emissionen_Stromimport = (sum(
        Betriebsverbrauch['sequences'][('Import_Betriebsverbrauch', 'Betriebsverbrauch'), 'flow'] +
        eigenverbrauch['sequences'][('Import_Strom_Eigenverbrauch', 'Strom_HS_Eigenverbrauch'), 'flow'] +
        Eigenverbrauch_Stadtgebiet['sequences'][('Import_Strom_WP', 'WP_Abwaerme_Netz'), 'flow']) * float(
        Emissionsfaktoren['Emissionsfaktor_2045']['Strom']))
    # Emissionen_Gasimport=(Methanbus['sequences'][('Import_Gas', 'Methanbus'), 'flow'].sum()*float(Emissionsfaktoren['Emissionsfaktor_2020']['Gas']))

    print('-----------------------------------------------------------------------')
    print('Emissionen_Stromimport \n' + str(round(Emissionen_Stromimport, 1)) + ' t_CO2')
    # print('Emissionen_Gasimport \n' +str(round(Emissionen_Gasimport,1))+' t_CO2')

    # %% CO2-Berechnung

    # ImportmengeGasKonv = Methanbus['sequences'][('Import_Gas','Methanbus'),'flow'].sum()
    ImportmengeGasGruen = Gasbus['sequences'][('Import_gruenesErdgas', 'Gas'), 'flow'].sum()
    ImportmengeH2 = Gasbus['sequences'][('Import_H2', 'Gas'), 'flow'].sum()

    # %% Schreiben von Ergebnisfiles
    Resultate_system = pd.Series([gesamtkosten_alternativ2,
                                  Emissionen_Stromimport,
                                  # Emissionen_Gasimport,
                                  # ImportmengeGasKonv,
                                  ImportmengeGasGruen,
                                  ImportmengeH2],
                                 index=['Gesamtkosten', 'Emissionen_Strom',  # 'Emissionen_Gas',
                                        # 'ImportmengeGasKonv',
                                        'ImportmengeGasGruen', 'ImportmengeH2'])

    Resultate_system.to_csv(result_path + '/Kosten_Emissionen.csv', decimal=',')

    Strombus_HS['sequences'].to_csv(result_path + '/Strombus_sequences.csv', decimal=',')
    Gasbus['sequences'].to_csv(result_path + '/Gasbus_sequences.csv', decimal=',')
    Fernwbus['sequences'].to_csv(result_path + '/Fernwbus_sequences.csv', decimal=',')
    Dampfbus['sequences'].to_csv(result_path + '/Dampfbus_sequences.csv', decimal=',')
    Frischdampfbus['sequences'].to_csv(result_path + '/Frischdampfbus_sequences.csv', decimal=',')
    WSP_drucklos_results['sequences'].to_csv(result_path + '/Waermespeicher_sequences.csv', decimal=',')
    Ausspeicherbus['sequences'].to_csv(result_path + '/Ausspeicherbus_sequences.csv', decimal=',')
    Nachheizbus['sequences'].to_csv(result_path + '/Nachheizbus_sequences.csv', decimal=',')
    Solarthermiebus['sequences'].to_csv(result_path + '/Solarthermiebus_sequences.csv', decimal=',')
    FünfundneunzigGradbus['sequences'].to_csv(result_path + '/FünfundneunzigGradbus_sequences.csv', decimal=',')
    Abgas_GT_1bus['sequences'].to_csv(result_path + '/Abgas_GT_1bus_sequences.csv', decimal=',')
    Abgas_GT_2bus['sequences'].to_csv(result_path + '/Abgas_GT_2bus_sequences.csv', decimal=',')
    Abgas_GT_3bus['sequences'].to_csv(result_path + '/Abgas_GT_3bus_sequences.csv', decimal=',')
    FrischdampfHilfsbusLinie1['sequences'].to_csv(result_path + '/FrischdampfHilfsbusLinie1_sequences.csv', decimal=',')
    FrischdampfHilfsbusLinie2['sequences'].to_csv(result_path + '/FrischdampfHilfsbusLinie2_sequences.csv', decimal=',')

    Strombus_HS['scalars'].to_csv(result_path + '/Strombus_scalars.csv', decimal=',')
    Fernwbus['scalars'].to_csv(result_path + '/Fernwbus_scalars.csv', decimal=',')
    Solarthermiebus['scalars'].to_csv(result_path + '/Solarthermiebuss_scalars.csv', decimal=',')
    FünfundneunzigGradbus['scalars'].to_csv(result_path + '/FünfundneunzigGradbus_scalars.csv', decimal=',')
    eigenerzeugung['scalars'].to_csv(result_path + '/eigenerzeugung_scalars.csv', decimal=',')
    Gasbus['scalars'].to_csv(result_path + '/Gasbus_scalars.csv', decimal=',')
    # Methanbus['scalars'].to_csv('07_Simulationsergebnisse/'+name+'/Methanbus_scalars.csv', decimal=',')
    b_HWE_5_1_bus['scalars'].to_csv(result_path + '/HWE5_1_scalars.csv', decimal=',')

    Betriebsverbrauch['sequences'].to_csv(result_path + '/Betriebsverbrauch_sequences.csv', decimal=',')
    Eigenverbrauch_Stadtgebiet['sequences'].to_csv(result_path + '/Eigenverbrauch_Stadtgebiet_sequences.csv',
                                                   decimal=',')
    Direktleitungsbus_results['sequences'].to_csv(result_path + '/Direktleitungsbus_results_sequences.csv', decimal=',')
    eigenerzeugung['sequences'].to_csv(result_path + '/eigenerzeugung_sequences.csv', decimal=',')
    # Wasserstoffbus['sequences'].to_csv('07_Simulationsergebnisse/'+name+'/Wasserstoffbus_sequences.csv', decimal=',')
    # Methanbus['sequences'].to_csv('07_Simulationsergebnisse/'+name+'/Methanbus_sequences.csv', decimal=',')
    eigenverbrauch['sequences'].to_csv(result_path + '/eigenverbrauch_sequences.csv', decimal=',')
    Gas_fiktiv['scalars'].to_csv(result_path + '/Gas_fiktiv_scalars.csv', decimal=',')
    Gas2_fiktiv['scalars'].to_csv(result_path + '/Gas2_fiktiv_scalars.csv', decimal=',')

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 10:11:00 2020

@author: treinhardt01; cschmidt; aoberdorfer
Übergang zu Version 3:  - Berücksichtigung ausschließlich Vakuum-Röhrenkollektoren
                        - Solarthermie spielt auf separaten Bus, um die KWK-Anlagen nicht zu beeinflussen.
                        - 3 Wärmepumpenkonzepte um:     - Abwärmepotentiale zu nutzen
                                                        - ST auf Heißwassernetz einzuspeisen
                                                        - ST in Speicher einzuspeisen
                        - Anlegung weiterer Busse um die bisher genannten Aufgaben zu erfüllen.
"""
import os
import pickle

import numpy as np
import pandas as pd
from oemof.tools import economics

from ensys import EnsysSink, EnsysFlow, EnsysInvestment, EnsysTransformer, EnsysNonConvex, EnsysConstraints, \
    EnsysStorage, EnsysBus, EnsysSource, EnsysEnergysystem
from ensys.types import CONSTRAINT_TYPES
from hsncommon.log import HsnLogger

pd.options.mode.chained_assignment = None


def createConfigBinary(dumpfile, datapath):
    logger = HsnLogger()

    name = os.path.basename(__file__).replace(".py", "")
    my_path = datapath

    try:
        os.mkdir(os.path.join(my_path, '07_Simulationsergebnisse'))
        os.mkdir(os.path.join(my_path, '07_Simulationsergebnisse', name))
    except OSError:
        logger.info("Verzeichnis für Ergebnisse existiert bereits!")
    else:
        logger.info("Verzeichnis für Ergebnisse wurde erfolgreich angelegt.")

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Einspeicherung_Heisswasser.csv')
    Einspeicherung_Heisswasser = pd.read_csv(pfad, sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Erneuerbare_Energien_2045.csv')
    Erneuerbare_Energien = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Biomasse.csv')
    Biomasse = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Gasturbinen_2030.csv')
    Gasturbinen = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Abhitzekessel_Abhitzebetrieb_2030.csv')
    Abhitzekessel_Abhitzebetrieb = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Abhitzekessel_Frischluftbetrieb.csv')
    Abhitzekessel_Frischluftbetrieb = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index',
                                                  decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Abhitzekessel_Kombibetrieb.csv')
    Abhitzekessel_Kombibetrieb = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path,
                        '04_Bearbeitete_Inputdaten/V04_Inputdaten_Heisswasserschleife_Abhitzebetrieb_und_Kombibetrieb.csv')
    Heisswasserschleife_Abhitze_und_Kombibetrieb = pd.read_csv(pfad, sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path,
                        '04_Bearbeitete_Inputdaten/V04_Inputdaten_Heisswasserschleife_Frischluftbetrieb.csv')
    Heisswasserschleife_Frischluftbetrieb = pd.read_csv(pfad, sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Dampfturbinen.csv')
    Dampfturbinen = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Tandemdampfturbine_HD_Teil.csv')
    Tandemdampfturbine = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Heisswassererzeuger.csv')
    HWE = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_PtH_Technologien_WP_2045.csv')
    PtH_Technologien = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Speicher.csv')
    Speicher = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Emissionsfaktoren.csv')
    Emissionsfaktoren = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Stromnetze.csv')
    Stromnetze = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_TAB.csv')
    TAB = pd.read_csv(pfad, sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '03_Rohdaten/CO2_Preise_Energy_Brainpool.csv')
    CO2_Preise_Energy_Brainpool = pd.read_csv(pfad, encoding='unicode_escape', index_col='Index', sep=';', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '03_Rohdaten/Ganglinie_RABA.csv')
    Ganglinie_RABA = pd.read_csv(pfad, sep=';', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '03_Rohdaten/V04_Einspeiseprofile.csv')
    Einspeiseprofile = pd.read_csv(pfad, sep=';', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '03_Rohdaten/V04_Einspeiseprofile_PV_Wind.csv')
    Einspeiseprofile_PV_Wind = pd.read_csv(pfad, sep=';', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '03_Rohdaten/V04_Lastprofile.csv')
    Lastprofile = pd.read_csv(pfad, encoding='unicode_escape', sep=';', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '03_Rohdaten/Netzverluste.csv')
    Netzverluste = pd.read_csv(pfad, encoding='unicode_escape', sep=';', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '03_Rohdaten/Preise.csv')
    Preise = pd.read_csv(pfad, sep=';', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '03_Rohdaten/Preise_EnergyBrainpool.csv')
    Preise_Strom_Gas = pd.read_csv(pfad, sep=';', decimal=',')
    ###############################################################################

    ###############################################################################

    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_CO2_Grenzen.csv')
    CO2_Grenzen = pd.read_csv(pfad, encoding='unicode_escape', sep=';', index_col='index', decimal=',')
    ###############################################################################

    CO2_Grenze = CO2_Grenzen['CO2_Menge']['Grenze_2045']

    data_Boerse = Preise_Strom_Gas['Strompreis_2045']  # Strompreis_2020
    data_Preise_2040_CH4_Eur_MWh = Preise_Strom_Gas['Gaspreis_2035']  # nicht relevant !!!
    data_Preis_Biomasse = Preise['Biomassepreise']
    data_Preis_gruenesErdgas = Preise['gruenenErdgasPreis_2045']

    Last_Strom_SWE = Lastprofile['Last_Strom']
    Last_Waerme_SWE = Lastprofile['Heisswasserlast_2030']  # Heisswasserlast_2020 Last_Heiswasser Heisswasserlast_2030
    data_Grundlast = Einspeiseprofile['data_Grundlast']

    nne_arbeitspreis = Stromnetze['Strom HS 110kV']['Arbeitspreis_Netzentgelte']
    konzession = Stromnetze['Strom HS 110kV']['Konzessionsabgabe']
    kwk = Stromnetze['Strom HS 110kV']['KWK-Umlage']
    offshore = Stromnetze['Strom HS 110kV']['Offshore_Netzumlage']
    stromNEV = Stromnetze['Strom HS 110kV']['StromNEV_Umlage']
    abschaltL = Stromnetze['Strom HS 110kV']['Umlage_fuer_abschaltbare_Lasten']
    eeg = Stromnetze['Strom HS 110kV']['EEG_Umlage_2045_S1']

    vnneLP = Stromnetze['Strom HS 110kV']['vermiedene_Netznutzung_Leistungspreis']
    vnneAP = Stromnetze['Strom HS 110kV']['vermiedene_Netznutzung_Arbeitspreis']

    Stromsteuer = Stromnetze['Strom HS 110kV']['Stromsteuer']
    Stromsteuerentlastung = Stromnetze['Strom HS 110kV']['Stromsteuerentlastung']

    # Ruecklauftemperatur_auslesen = Lastprofile['T_RL_2040']
    Ruecklauftemperatur = Lastprofile['T_RL_2030']
    Vorlauftemperatur = Lastprofile['T_VL_2030']
    # Vorlauftemperatur_2030 = Lastprofile['T_VL_2040']
    # Ruecklauftemperatur_2030 = Lastprofile['T_RL_2040']
    Aussentemperatur = Lastprofile['Aussentemperatur_U5']

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/V04_Inputdaten_Gasnetz.csv')
    Gasnetz = pd.read_csv(pfad, sep=';', index_col='index', encoding='unicode_escape', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/Anteile_Gase_im_Netz.csv')
    Anteile_Gase_im_Netz = pd.read_csv(pfad, sep=';', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/BEW_Foerderung_WP.csv')
    BEW_Foerderung_WP = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################

    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/BEW_Foerderung_ST.csv')
    BEW_Foerderung_ST = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/Preis_H2.csv')
    Preis_H2 = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index', decimal=',')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/SWE_Input_Preise.csv')
    SWE_Input_Preise = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='Jahre')
    ###############################################################################

    ###############################################################################
    pfad = os.path.join(my_path, '04_Bearbeitete_Inputdaten/Tiefengeothermie.csv')
    Geothermie = pd.read_csv(pfad, sep=';', encoding='unicode_escape', index_col='index', decimal=',')
    ###############################################################################

    Last_Waerme_SWE_Netzverlust = [None] * len(Last_Waerme_SWE)
    for i in range(0, len(Last_Waerme_SWE)):
        Last_Waerme_SWE_Netzverlust[i] = Last_Waerme_SWE[i] + Netzverluste['Netzverluste_2045'][i]

    PV_Erfurt_60 = [None] * len(Last_Waerme_SWE)
    Wind_Erfurt_60 = [None] * len(Last_Waerme_SWE)

    data_Wind_Erfurt = Einspeiseprofile_PV_Wind['Wind_Erfurt']
    data_PV_Erfurt = Einspeiseprofile_PV_Wind['PV_Freifeld_Erfurt']

    i = 0
    for a in range(0, len(Last_Waerme_SWE)):
        Summe_PV_Erfurt = 0
        Summe_Wind_Erfurt = 0
        for k in range(0, 4):
            Summe_Wind_Erfurt += data_Wind_Erfurt[i]
            Summe_PV_Erfurt += data_PV_Erfurt[i]
            i += 1
        PV_Erfurt_60[a] = Summe_PV_Erfurt / 4
        Wind_Erfurt_60[a] = Summe_Wind_Erfurt / 4

    # %% Bildung Eigenverbrauch
    Lastgang_Eigenverbrauch = [None] * len(Last_Waerme_SWE)
    Lastgang_Eigenverbrauch1 = [None] * len(Last_Waerme_SWE)
    Lastgang_Eigenverbrauch2 = [None] * len(Last_Waerme_SWE)
    for a in range(0, len(Last_Waerme_SWE)):
        Lastgang_Eigenverbrauch[a] = 0.0156 * (Last_Waerme_SWE[a] + 7.5) + 0.4

    # CO2-Preisberechnungen
    CO2_Preis_2045 = SWE_Input_Preise['CO2_Preis_ETS_S1'][2045.0]

    # Strompreis inklusive CO2-Preis

    # HPFC_ohne_CO2 = [None]*len(data_Boerse)
    data_Boerse_Import = [None] * len(data_Boerse)
    Umlagen_Netzanschluss = nne_arbeitspreis + konzession + kwk + offshore + stromNEV + abschaltL + eeg - vnneAP
    Umlagen_Eigenverbrauch = 0.4 * eeg + Stromsteuer - Stromsteuerentlastung - vnneAP
    for a in range(0, len(data_Boerse)):
        if data_Boerse[a] > 500:
            data_Boerse[a] = data_Boerse[a - 1]
        elif data_Boerse[a] < 0:
            data_Boerse[a] = 0
        # HPFC_ohne_CO2[a] = data_Boerse[a] - CO_2_Aufschlag_2020
        # data_Boerse_Import[a] = HPFC_ohne_CO2[a] + CO_2_Aufschlag_2020 +119 + Stromnetze['Strom HS 110kV']['Arbeitspreis_Netzentgelte']
        data_Boerse_Import[a] = data_Boerse[
                                    a] + nne_arbeitspreis + konzession + kwk + offshore + stromNEV + abschaltL + eeg

    # %% Umrechnung der Gaspreise
    # Umrechnung Gaspreis von €/MWh_Ho in €/MWh_Hu
    data_CH4_neu = [None] * len(data_Preise_2040_CH4_Eur_MWh)
    for a in range(0, len(data_Preise_2040_CH4_Eur_MWh)):
        data_CH4_neu[a] = data_Preise_2040_CH4_Eur_MWh[a] / Gasnetz['Gasnetz']['Umrechnungsfaktor_Hu_zu_Ho_Preis']
    # Ersetzen der alten Werte: 
    data_Preise_2040_CH4_Eur_MWh = data_CH4_neu
    # Umrechnung der Brennstoffenergiesteuer auf €/MWh_Hu
    Brennstoffenergiesteuer = Gasnetz['Gasnetz']['Brennstoffenergiesteuer'] / Gasnetz['Gasnetz'][
        'Umrechnungsfaktor_Hu_zu_Ho_Preis']

    number_of_time_steps = 8760  # 24*7*52.142857*4#8760#

    logger.info('Initialize the energy system')
    date_time_index = pd.date_range('1/1/2021', periods=number_of_time_steps,
                                    freq='H')
    energysystem = EnsysEnergysystem(
        timeindex=date_time_index,
        busses=[],
        sinks=[],
        sources=[],
        transformers=[],
        storages=[],
        constraints=[]
    )

    # Berechnung der Ruecklauftemperatur
    # Einlesen der Kenngrößen aus der Technischen Anschlussbedingung (TAB):
    TAB_x1 = TAB['Temp_Aussen']['TAB_Punkt_1']
    TAB_x2 = TAB['Temp_Aussen']['TAB_Punkt_2']
    TAB_y1 = TAB['Temp_VL']['TAB_Punkt_1']
    TAB_y2 = TAB['Temp_VL']['TAB_Punkt_2']

    # Berechnung des Anstiegs der Geradengleichung:
    TAB_m = (TAB_y2 - TAB_y1) / (TAB_x2 - TAB_x1)
    TAB_n = TAB_y2 - TAB_m * TAB_x2
    Testtemp_Aussen = np.linspace(TAB_x1, TAB_x2 + 10, 100)
    Test_T_VL = [None] * len(Testtemp_Aussen)
    for a in range(0, len(Testtemp_Aussen)):
        if Testtemp_Aussen[a] < 15:
            Test_T_VL[a] = TAB_m * Testtemp_Aussen[
                a] + TAB_n  # y=mx+n       m=(130-115)/(-15-15)=15/-30=-0-5    n=Punkt einsetzen y=mx+n, n=y-mx: y=115, m=-0.5, x=15: n=115+0.5*15
        else:
            Test_T_VL[a] = TAB_y2  # °C

    # Berechnungen aus den Temperaturen
    Speichermax_Temp = Speicher['Waermespeicher_drucklos']['Temperaturniveau']

    Abwaerme_Temp_max_Waescherei = PtH_Technologien['Waescherei']['Temperaturniveau']
    Guetegrad_WP_Waescherei = float(PtH_Technologien['Waescherei']['Guetegrad'])

    Abwaerme_Temp_max_WWK = PtH_Technologien['WWK']['Temperaturniveau']
    Guetegrad_WP_WWK = float(PtH_Technologien['WWK']['Guetegrad'])

    Abwaerme_Temp_max_AHK_RG = PtH_Technologien['AHK_RG']['Temperaturniveau']
    Guetegrad_WP_AHK_RG = float(PtH_Technologien['AHK_RG']['Guetegrad'])

    Abwaerme_Temp_max_RABA_Rauchgas = PtH_Technologien['RABA_Rauchgas']['Temperaturniveau']
    Guetegrad_WP_RABA_Rauchgas = float(PtH_Technologien['RABA_Rauchgas']['Guetegrad'])

    Abwaerme_Temp_max_RABA_alternativ = PtH_Technologien['RABA_alternativ']['Temperaturniveau']
    Guetegrad_WP_RABA_alternativ = float(PtH_Technologien['RABA_alternativ']['Guetegrad'])

    # Abwaerme_Temp_max_Luftwaerme = PtH_Technologien['Luftwaerme']['Temperaturniveau']
    Guetegrad_WP_Luftwaerme = float(PtH_Technologien['Luftwaerme']['Guetegrad'])

    Abwaerme_Temp_max_Flusswasser_Seen = PtH_Technologien['Flusswasser_Seen']['Temperaturniveau']
    Guetegrad_WP_Flusswasser_Seen = float(PtH_Technologien['Flusswasser_Seen']['Guetegrad'])

    eta_speicher_aus = [None] * len(Ruecklauftemperatur)
    eta_nachheiz_aus = [None] * len(Ruecklauftemperatur)

    spez_Ertrag_HFK = [None] * len(Ruecklauftemperatur)
    spez_Ertrag_FK = [None] * len(Ruecklauftemperatur)
    spez_Ertrag_CPC = [None] * len(Ruecklauftemperatur)
    spez_Ertrag_CPC_VL = [None] * len(Ruecklauftemperatur)

    COP_WP_Speicher = [None] * len(Ruecklauftemperatur)
    COP_WP_Heisswasser = [None] * len(Ruecklauftemperatur)
    COP_WP_Abwaerme_Waescherei = [None] * len(Ruecklauftemperatur)
    COP_WP_Abwaerme_WWK = [None] * len(Ruecklauftemperatur)
    COP_WP_Abwaerme_RABA_Rauchgas = [None] * len(Ruecklauftemperatur)
    COP_WP_Abwaerme_RABA_alternativ = [None] * len(Ruecklauftemperatur)
    COP_WP_Abwaerme_Luftwaerme = [None] * len(Ruecklauftemperatur)
    COP_WP_Abwaerme_AHK_RG = [None] * len(Ruecklauftemperatur)
    COP_WP_Abwaerme_Flusswasser_Seen = [None] * len(Ruecklauftemperatur)

    eta_WP_Speicher_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Speicher_st = [None] * len(Ruecklauftemperatur)
    eta_WP_Heisswasser_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Heisswasser_st = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_Waescherei_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_Waescherei_st = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_WWK_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_WWK_st = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_AHK_RG_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_AHK_RG_st = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_RABA_Rauchgas_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_RABA_Rauchgas_st = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_RABA_alternativ_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_RABA_alternativ_st = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_Luftwaerme_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_Luftwaerme_st = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_Flusswasser_Seen_el = [None] * len(Ruecklauftemperatur)
    eta_WP_Abwaerme_Flusswasser_Seen_st = [None] * len(Ruecklauftemperatur)

    data_WP_Abwaerme_Milchwerke = [None] * len(Ruecklauftemperatur)
    data_WP_Abwaerme_Waescherei = [None] * len(Ruecklauftemperatur)
    data_WP_Abwaerme_WWK = [None] * len(Ruecklauftemperatur)
    data_WP_Abwaerme_RABA_Rauchgas = [None] * len(Ruecklauftemperatur)
    data_WP_Abwaerme_RABA_alternativ = [None] * len(Ruecklauftemperatur)
    data_WP_Abwaerme_Luftwaerme = [None] * len(Ruecklauftemperatur)
    data_WP_Abwaerme_Abwasser_Industrie = [None] * len(Ruecklauftemperatur)
    data_WP_Abwaerme_Flusswasser_Seen = [None] * len(Ruecklauftemperatur)
    data_WP_Abwaerme_Luftwaerme_direkt = [None] * len(Ruecklauftemperatur)

    for a in range(0, len(Ruecklauftemperatur)):
        eta_speicher_aus[a] = 1 - ((1) / (1 + ((95 - Ruecklauftemperatur[a]) / (Vorlauftemperatur[a] - 95))))
        eta_nachheiz_aus[a] = ((1) / (1 + ((95 - Ruecklauftemperatur[a]) / (Vorlauftemperatur[a] - 95))))
        # COP in Abhängigkeit der Temperaturen
        COP_WP_Speicher[a] = (273.15 + Speichermax_Temp) / (
                Speichermax_Temp - Ruecklauftemperatur[a]) * Guetegrad_WP_Waescherei
        COP_WP_Heisswasser[a] = (273.15 + Vorlauftemperatur[a]) / (
                Vorlauftemperatur[a] - Ruecklauftemperatur[a]) * Guetegrad_WP_Waescherei
        # COP_WP_Abwaerme_Milchwerke[a] = (273.15 + Vorlauftemperatur[a])/(Vorlauftemperatur[a] - Abwaerme_Temp_max_Milchwerke) * Guetegrad_WP_Waescherei
        COP_WP_Abwaerme_Waescherei[a] = (273.15 + Vorlauftemperatur[a]) / (
                Vorlauftemperatur[a] - Abwaerme_Temp_max_Waescherei) * Guetegrad_WP_Waescherei
        COP_WP_Abwaerme_WWK[a] = (273.15 + Vorlauftemperatur[a]) / (
                Vorlauftemperatur[a] - Abwaerme_Temp_max_WWK) * Guetegrad_WP_WWK
        COP_WP_Abwaerme_AHK_RG[a] = (273.15 + Vorlauftemperatur[a]) / (
                Vorlauftemperatur[a] - Abwaerme_Temp_max_AHK_RG) * Guetegrad_WP_AHK_RG
        COP_WP_Abwaerme_RABA_Rauchgas[a] = (273.15 + Vorlauftemperatur[a]) / (
                Vorlauftemperatur[a] - Abwaerme_Temp_max_RABA_Rauchgas) * Guetegrad_WP_RABA_Rauchgas
        COP_WP_Abwaerme_RABA_alternativ[a] = (273.15 + Vorlauftemperatur[a]) / (
                Vorlauftemperatur[a] - Abwaerme_Temp_max_RABA_alternativ) * Guetegrad_WP_RABA_alternativ
        COP_WP_Abwaerme_Luftwaerme[a] = (273.15 + Vorlauftemperatur[a]) / (
                Vorlauftemperatur[a] - Aussentemperatur[a]) * Guetegrad_WP_Luftwaerme
        COP_WP_Abwaerme_Flusswasser_Seen[a] = ((273.15 + Vorlauftemperatur[a]) / (
                Vorlauftemperatur[a] - Abwaerme_Temp_max_Flusswasser_Seen) * Guetegrad_WP_Flusswasser_Seen) - 0.1

        eta_WP_Speicher_el[a] = 1 / COP_WP_Speicher[a]
        eta_WP_Speicher_st[a] = 1 / (COP_WP_Speicher[a] / (COP_WP_Speicher[a] - 1))
        eta_WP_Heisswasser_el[a] = 1 / COP_WP_Heisswasser[a]
        eta_WP_Heisswasser_st[a] = 1 / (COP_WP_Heisswasser[a] / (COP_WP_Heisswasser[a] - 1))
        # eta_WP_Abwaerme_Milchwerke_el[a]=1/COP_WP_Abwaerme_Milchwerke[a]
        # eta_WP_Abwaerme_Milchwerke_st[a]= 1/ (COP_WP_Abwaerme_Milchwerke[a]/(COP_WP_Abwaerme_Milchwerke[a]-1))
        eta_WP_Abwaerme_Waescherei_el[a] = 1 / COP_WP_Abwaerme_Waescherei[a]
        eta_WP_Abwaerme_Waescherei_st[a] = 1 / (COP_WP_Abwaerme_Waescherei[a] / (COP_WP_Abwaerme_Waescherei[a] - 1))
        eta_WP_Abwaerme_WWK_el[a] = 1 / COP_WP_Abwaerme_WWK[a]
        eta_WP_Abwaerme_WWK_st[a] = 1 / (COP_WP_Abwaerme_WWK[a] / (COP_WP_Abwaerme_WWK[a] - 1))
        eta_WP_Abwaerme_AHK_RG_el[a] = 1 / COP_WP_Abwaerme_AHK_RG[a]
        eta_WP_Abwaerme_AHK_RG_st[a] = 1 / (COP_WP_Abwaerme_AHK_RG[a] / (COP_WP_Abwaerme_AHK_RG[a] - 1))
        eta_WP_Abwaerme_RABA_Rauchgas_el[a] = 1 / COP_WP_Abwaerme_RABA_Rauchgas[a]
        eta_WP_Abwaerme_RABA_Rauchgas_st[a] = 1 / (
                COP_WP_Abwaerme_RABA_Rauchgas[a] / (COP_WP_Abwaerme_RABA_Rauchgas[a] - 1))
        eta_WP_Abwaerme_RABA_alternativ_el[a] = 1 / COP_WP_Abwaerme_RABA_alternativ[a]
        eta_WP_Abwaerme_RABA_alternativ_st[a] = 1 / (
                COP_WP_Abwaerme_RABA_alternativ[a] / (COP_WP_Abwaerme_RABA_alternativ[a] - 1))
        eta_WP_Abwaerme_Luftwaerme_el[a] = 1 / COP_WP_Abwaerme_Luftwaerme[a]
        eta_WP_Abwaerme_Luftwaerme_st[a] = 1 / (COP_WP_Abwaerme_Luftwaerme[a] / (COP_WP_Abwaerme_Luftwaerme[a] - 1))
        eta_WP_Abwaerme_Flusswasser_Seen_el[a] = 1 / COP_WP_Abwaerme_Flusswasser_Seen[a]
        eta_WP_Abwaerme_Flusswasser_Seen_st[a] = 1 / (
                COP_WP_Abwaerme_Flusswasser_Seen[a] / (COP_WP_Abwaerme_Flusswasser_Seen[a] - 1))

        # E_WP_low_Milchwerke = PtH_Technologien['Waermepumpe_Milchwerke']['Volllaststunden'] * PtH_Technologien['Waermepumpe_Milchwerke']['max_Leistung']
        E_WP_low_Waescherei = PtH_Technologien['Waescherei']['Volllaststunden'] * PtH_Technologien['Waescherei'][
            'max_Leistung']
        E_WP_low_WWK = PtH_Technologien['WWK']['Volllaststunden'] * PtH_Technologien['WWK']['max_Leistung']
        E_WP_low_RABA_Rauchgas = PtH_Technologien['RABA_Rauchgas']['Volllaststunden'] * \
                                 PtH_Technologien['RABA_Rauchgas'][
                                     'max_Leistung']
        E_WP_low_RABA_alternativ = PtH_Technologien['RABA_alternativ']['Volllaststunden'] * \
                                   PtH_Technologien['RABA_alternativ']['max_Leistung']
        E_WP_low_Luftwaerme = PtH_Technologien['Luftwaerme']['Volllaststunden'] * PtH_Technologien['Luftwaerme'][
            'max_Leistung']
        E_WP_low_Abwasser_Industrie = PtH_Technologien['Abwasser_Industrie']['Volllaststunden'] * \
                                      PtH_Technologien['Abwasser_Industrie']['max_Leistung']
        E_WP_low_Flusswasser_Seen = PtH_Technologien['Flusswasser_Seen']['Volllaststunden'] * \
                                    PtH_Technologien['Flusswasser_Seen']['max_Leistung']
        E_WP_low_Luftwaerme_direkt = PtH_Technologien['Luftwaerme_direkt']['Volllaststunden'] * \
                                     PtH_Technologien['Luftwaerme_direkt']['max_Leistung']

        # data_WP_Abwaerme_Milchwerke[a] = E_WP_low_Milchwerke/number_of_time_steps
        data_WP_Abwaerme_Waescherei[a] = E_WP_low_Waescherei / number_of_time_steps
        data_WP_Abwaerme_WWK[a] = E_WP_low_WWK / number_of_time_steps
        data_WP_Abwaerme_RABA_Rauchgas[a] = E_WP_low_RABA_Rauchgas / number_of_time_steps
        data_WP_Abwaerme_RABA_alternativ[a] = E_WP_low_RABA_alternativ / number_of_time_steps
        data_WP_Abwaerme_Luftwaerme[a] = E_WP_low_Luftwaerme / number_of_time_steps
        data_WP_Abwaerme_Abwasser_Industrie[a] = E_WP_low_Abwasser_Industrie / number_of_time_steps
        data_WP_Abwaerme_Flusswasser_Seen[a] = E_WP_low_Flusswasser_Seen / number_of_time_steps
        data_WP_Abwaerme_Luftwaerme_direkt[a] = E_WP_low_Luftwaerme_direkt / number_of_time_steps

        # data_WP_Abwaerme_Milchwerke[a] = PtH_Technologien['Waermepumpe']['Energiemenge']/number_of_time_steps

        # Funktion für Hochtemperatur-Flachkollektor aus Norm in kWh/m^2/a
        spez_Ertrag_HFK[a] = -5.86 * (Ruecklauftemperatur[a] + 5) + 871
        # Funktion für Flachkollektor aus Norm in kWh/m^2/a
        spez_Ertrag_FK[a] = -7.666 * (Ruecklauftemperatur[a] + 5) + 916
        # Funktion für CPC-Kollektor aus Norm in kWh/m^2/a
        spez_Ertrag_CPC[a] = -3.18 * (Ruecklauftemperatur[a] + 5) + 743.1
        spez_Ertrag_CPC_VL[a] = -3.18 * (Vorlauftemperatur[a] + 5) + 743.1

    mittlerer_Ertrag_HFK = np.mean(spez_Ertrag_HFK)
    # print(mittlerer_Ertrag_HFK)
    mittlerer_Ertrag_FK = np.mean(spez_Ertrag_FK)
    # print(mittlerer_Ertrag_FK)
    mittlerer_Ertrag_CPC = np.mean(spez_Ertrag_CPC)
    # print(mittlerer_Ertrag_CPC)
    mittlerer_Ertrag_HFK_array = [mittlerer_Ertrag_HFK] * len(Ruecklauftemperatur)
    mittlerer_Ertrag_FK_array = [mittlerer_Ertrag_FK] * len(Ruecklauftemperatur)
    mittlerer_Ertrag_CPC_array = [mittlerer_Ertrag_CPC] * len(Ruecklauftemperatur)
    # Einspeiseprofil neu normieren mit mittleren Erträgen der Rücklauftemperatur

    # %%
    Ertrag_alt_FK = Einspeiseprofile['ST_Erfurt_normiert'].sum()
    #print(Ertrag_alt_FK * 1000)
    data_ST_CPC = [None] * len(Ruecklauftemperatur)
    data_ST_CPC_VL = [None] * len(Ruecklauftemperatur)
    data_ST_HFK = [None] * len(Ruecklauftemperatur)
    data_ST_FK = [None] * len(Ruecklauftemperatur)
    for a in range(0, len(Ruecklauftemperatur)):
        data_ST_CPC[a] = Einspeiseprofile['ST_Erfurt_normiert'][a] * (spez_Ertrag_CPC[a]) / (Ertrag_alt_FK * 1000)
        data_ST_CPC_VL[a] = Einspeiseprofile['ST_Erfurt_normiert'][a] * (spez_Ertrag_CPC_VL[a]) / (Ertrag_alt_FK * 1000)
        data_ST_HFK[a] = Einspeiseprofile['ST_Erfurt_normiert'][a] * (spez_Ertrag_HFK[a]) / (Ertrag_alt_FK * 1000)
        data_ST_FK[a] = Einspeiseprofile['ST_Erfurt_normiert'][a] * (spez_Ertrag_FK[a]) / (Ertrag_alt_FK * 1000)

    # Einlesen Komponenten

    # Würde erstmal nur die Wirkungsgrade hingeschrieben und Platzhalter,
    # für falls wir die Tabelle umstrukturieren oder umbenennen

    # P2H
    eta_P2H = PtH_Technologien['Heizstab']['Wirkungsgrad_el']
    Nennleistung_P2H_th = PtH_Technologien['Heizstab']['max_Leistung']

    Capex_P2H = PtH_Technologien['Heizstab']['CAPEX']
    Opex_P2H = PtH_Technologien['Heizstab']['OPEX'] / 100
    Amort_a_P2H = PtH_Technologien['Heizstab']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_P2H = PtH_Technologien['Heizstab']['Zinssatz'] / 100
    a_P2H = economics.annuity(capex=Capex_P2H, n=Amort_a_P2H, wacc=Zinssatz_P2H)
    b_P2H = Capex_P2H * Opex_P2H
    epc_P2H = a_P2H + b_P2H

    # ST_RK
    P_ST_RK_max = Erneuerbare_Energien['ST_RK']['max_Leistung']
    P_ST_RK_min = Erneuerbare_Energien['ST_RK']['min_Leistung']
    P_ST_RK_RL_min = Erneuerbare_Energien['ST_RK_RL']['min_Leistung']
    eta_ST_RK = Erneuerbare_Energien['ST_RK']['Eigenerzeugungsfaktor']

    Capex_ST_RK = Erneuerbare_Energien['ST_RK']['CAPEX']
    Opex_ST_RK = Erneuerbare_Energien['ST_RK']['OPEX'] / 100
    Amort_a_ST_RK = Erneuerbare_Energien['ST_RK']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_ST_RK = Erneuerbare_Energien['ST_RK']['Zinssatz'] / 100
    a_ST_RK = economics.annuity(capex=Capex_ST_RK, n=Amort_a_ST_RK, wacc=Zinssatz_ST_RK)
    b_ST_RK = Capex_ST_RK * Opex_ST_RK
    epc_ST_RK = a_ST_RK + b_ST_RK

    # ST KfW Foerderung
    ST_RK_kfw_foerderung = Erneuerbare_Energien['ST_RK']['CAPEX'] * 0.45
    capex_ST_abzglFoerderung = Erneuerbare_Energien['ST_RK']['CAPEX'] - ST_RK_kfw_foerderung
    a_ST_RK_kfw = economics.annuity(capex=capex_ST_abzglFoerderung, n=Amort_a_ST_RK, wacc=Zinssatz_ST_RK)
    epc_ST_RK_kfw = a_ST_RK_kfw + b_ST_RK

    # PV
    P_PV_max_eigenerzeugung = Erneuerbare_Energien['PV_eigenerzeugung']['max_Leistung']
    P_PV_min = Erneuerbare_Energien['PV_eigenerzeugung']['min_Leistung']
    Capex_PV = Erneuerbare_Energien['PV_eigenerzeugung']['CAPEX']
    Opex_PV = Erneuerbare_Energien['PV_eigenerzeugung']['OPEX'] / 100
    Amort_a_PV = Erneuerbare_Energien['PV_eigenerzeugung']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_PV = Erneuerbare_Energien['PV_eigenerzeugung']['Zinssatz'] / 100

    a_PV = economics.annuity(capex=Capex_PV, n=Amort_a_PV, wacc=Zinssatz_PV)
    b_PV = Capex_PV * Opex_PV
    epc_PV = a_PV + b_PV

    # Waermepumpe
    Capex_RABA_Rauchgas = PtH_Technologien['RABA_Rauchgas']['CAPEX'] * 0.5
    Opex_RABA_Rauchgas = PtH_Technologien['RABA_Rauchgas']['OPEX'] / 100
    Amort_a_WP = PtH_Technologien['RABA_Rauchgas']['Amortisierungszeitraum_in_Jahren']
    Amort_a_WP_Ab = PtH_Technologien['RABA_Rauchgas']['Amortisationszeit_Netzausbau']
    Zinssatz_WP = PtH_Technologien['RABA_Rauchgas']['Zinssatz'] / 100

    Netzausbaukosten = PtH_Technologien['RABA_Rauchgas']['Kosten_Fernwaermenetzausbau'] * \
                       PtH_Technologien['RABA_Rauchgas'][
                           'Laenge_Fernwaermeleitung']
    a_WP_Ab = economics.annuity(capex=Netzausbaukosten, n=Amort_a_WP_Ab, wacc=Zinssatz_WP)

    a_RABA_Rauchgas = economics.annuity(capex=Capex_RABA_Rauchgas, n=Amort_a_WP, wacc=Zinssatz_WP)
    b_RABA_Rauchgas = Capex_RABA_Rauchgas * Opex_RABA_Rauchgas
    epc_RABA_Rauchgas = a_RABA_Rauchgas + b_RABA_Rauchgas + a_WP_Ab

    # WP Speicher + WP Heißwasser
    Nennleistung_WP_th = PtH_Technologien['RABA_Rauchgas']['max_Leistung']
    epc_WP_Speicher_HW = a_RABA_Rauchgas + b_RABA_Rauchgas

    # RABA_alternativ
    Capex_RABA_alternativ = PtH_Technologien['RABA_alternativ']['CAPEX'] * 0.5
    Opex_RABA_alternativ = PtH_Technologien['RABA_alternativ']['OPEX'] / 100
    Amort_a_WP = PtH_Technologien['RABA_alternativ']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_WP = PtH_Technologien['RABA_alternativ']['Zinssatz'] / 100

    a_RABA_alternativ = economics.annuity(capex=Capex_RABA_alternativ, n=Amort_a_WP, wacc=Zinssatz_WP)
    b_RABA_alternativ = Capex_RABA_alternativ * Opex_RABA_alternativ
    epc_RABA_alternativ = a_RABA_alternativ + b_RABA_alternativ + a_WP_Ab

    # Luftwaerme
    Capex_Luftwaerme = PtH_Technologien['Luftwaerme']['CAPEX']
    Opex_Luftwaerme = PtH_Technologien['Luftwaerme']['OPEX'] / 100
    Amort_a_WP = PtH_Technologien['Luftwaerme']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_WP = PtH_Technologien['Luftwaerme']['Zinssatz'] / 100

    a_Luftwaerme = economics.annuity(capex=Capex_Luftwaerme, n=Amort_a_WP, wacc=Zinssatz_WP)
    b_Luftwaerme = Capex_Luftwaerme * Opex_Luftwaerme
    epc_Luftwaerme = a_Luftwaerme + b_Luftwaerme + a_WP_Ab

    # Luftwaerme direkt
    Capex_Luftwaerme_direkt = PtH_Technologien['Luftwaerme_direkt']['CAPEX']
    Opex_Luftwaerme_direkt = PtH_Technologien['Luftwaerme_direkt']['OPEX'] / 100
    Amort_a_WP = PtH_Technologien['Luftwaerme_direkt']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_WP = PtH_Technologien['Luftwaerme_direkt']['Zinssatz'] / 100

    a_Luftwaerme_direkt = economics.annuity(capex=Capex_Luftwaerme_direkt, n=Amort_a_WP, wacc=Zinssatz_WP)
    b_Luftwaerme_direkt = Capex_Luftwaerme_direkt * Opex_Luftwaerme_direkt
    epc_Luftwaerme_direkt = a_Luftwaerme_direkt + b_Luftwaerme_direkt + a_WP_Ab

    # WWK
    Capex_WWK = PtH_Technologien['WWK']['CAPEX']
    Opex_WWK = PtH_Technologien['WWK']['OPEX'] / 100
    Amort_a_WP = PtH_Technologien['WWK']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_WP = PtH_Technologien['WWK']['Zinssatz'] / 100

    a_WWK = economics.annuity(capex=Capex_WWK, n=Amort_a_WP, wacc=Zinssatz_WP)
    b_WWK = Capex_WWK * Opex_WWK
    epc_WWK = a_WWK + b_WWK + a_WP_Ab

    # Flusswasser Seen (entspricht WWK in der Höhe der Kosten)
    Capex_FlusswasserSeen = PtH_Technologien['WWK']['CAPEX'] * 0.5
    Opex_FlusswasserSeen = PtH_Technologien['WWK']['OPEX'] / 100
    Amort_a_WP = PtH_Technologien['WWK']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_WP = PtH_Technologien['WWK']['Zinssatz'] / 100

    a_FlusswasserSeen = economics.annuity(capex=Capex_FlusswasserSeen, n=Amort_a_WP, wacc=Zinssatz_WP)
    b_FlusswasserSeen = Capex_FlusswasserSeen * Opex_FlusswasserSeen
    epc_FlusswasserSeen = a_FlusswasserSeen + b_FlusswasserSeen + a_WP_Ab

    # Waescherei
    Capex_Waescherei = PtH_Technologien['Waescherei']['CAPEX'] * 0.5
    Opex_Waescherei = PtH_Technologien['Waescherei']['OPEX'] / 100
    Amort_a_WP = PtH_Technologien['Waescherei']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_WP = PtH_Technologien['Waescherei']['Zinssatz'] / 100

    a_Waescherei = economics.annuity(capex=Capex_Waescherei, n=Amort_a_WP, wacc=Zinssatz_WP)
    b_Waescherei = Capex_Waescherei * Opex_Waescherei
    epc_Waescherei = a_Waescherei + b_Waescherei + a_WP_Ab

    # Wind
    P_Wind_max = Erneuerbare_Energien['Wind']['max_Leistung']
    Capex_Wind = Erneuerbare_Energien['Wind']['CAPEX']
    Opex_Wind = Erneuerbare_Energien['Wind']['OPEX'] / 100
    Amort_a_Wind = Erneuerbare_Energien['Wind']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_Wind = Erneuerbare_Energien['Wind']['Zinssatz'] / 100

    EnergiemengeWind = Erneuerbare_Energien['Wind']['Energiemenge_je_Windrad']
    LeistungWindrad = Erneuerbare_Energien['Wind']['Leistung_je_Windrad']
    LeistungWindBestand = ((Erneuerbare_Energien['Wind']['Bestand'] / 4) / sum(Wind_Erfurt_60))

    EnergiemengeWind_red = EnergiemengeWind * 0.9
    Leistung_Windpark_Summe = (EnergiemengeWind_red / sum(Wind_Erfurt_60)) * Erneuerbare_Energien['Wind'][
        'Anzahl_Windraeder']
    Leistung_Windpark_gesamt = LeistungWindBestand + Leistung_Windpark_Summe

    a_Wind = economics.annuity(capex=Capex_Wind, n=Amort_a_Wind, wacc=Zinssatz_Wind)
    b_Wind = Capex_Wind * Opex_Wind
    epc_Wind = a_Wind + b_Wind

    # Waermespeicher_drucklos
    C_Rate_WSP_drucklos = Speicher['Waermespeicher_drucklos']['C-Rate']
    Einspeicherwirkungsgrad_WSP_drucklos = Speicher['Waermespeicher_drucklos']['Einspeicherwirkungsgrad']
    Ausspeicherwirkungsgrad_WSP_drucklos = Speicher['Waermespeicher_drucklos']['Ausspeicherwirkungsgrad']
    Init_Speicherzustand_WSP_drucklos = Speicher['Waermespeicher_drucklos']['Anfangslevel']
    Status_balanced_WSP_drucklos = bool(Speicher['Waermespeicher_drucklos']['balanced'])
    Max_Speicherkapazitaet_WSP_drucklos = Speicher['Waermespeicher_drucklos']['Speicherkapazität_max']
    Min_Speicherkapazitaet_WSP_drucklos = Speicher['Waermespeicher_drucklos']['Speicherkapazität_min']

    Capex_WSP_drucklos = Speicher['Waermespeicher_drucklos']['CAPEX']
    Opex_WSP_drucklos = Speicher['Waermespeicher_drucklos']['OPEX'] / 100
    Amort_a_WSP_drucklos = Speicher['Waermespeicher_drucklos']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_WSP_drucklos = Speicher['Waermespeicher_drucklos']['Zinssatz'] / 100
    a_WSP_drucklos = economics.annuity(capex=Capex_WSP_drucklos, n=Amort_a_WSP_drucklos, wacc=Zinssatz_WSP_drucklos)
    b_WSP_drucklos = Capex_WSP_drucklos * Opex_WSP_drucklos
    epc_WSP_drucklos = a_WSP_drucklos + b_WSP_drucklos

    # elektr_Speicher
    C_Rate_ESP = Speicher['elektr_Speicher']['C-Rate']
    Einspeicherwirkungsgrad_ESP = Speicher['elektr_Speicher']['Einspeicherwirkungsgrad']
    Ausspeicherwirkungsgrad_ESP = Speicher['elektr_Speicher']['Ausspeicherwirkungsgrad']
    Init_Speicherzustand_ESP = Speicher['elektr_Speicher']['Anfangslevel']
    Status_balanced_ESP = bool(Speicher['elektr_Speicher']['balanced'])
    Max_Speicherkapazitaet_ESP = Speicher['elektr_Speicher']['Speicherkapazität_max']
    Min_Speicherkapazitaet_ESP = Speicher['elektr_Speicher']['Speicherkapazität_min']

    Capex_ESP = Speicher['elektr_Speicher']['CAPEX']
    Opex_ESP = Speicher['elektr_Speicher']['OPEX'] / 100
    Amort_a_ESP = Speicher['elektr_Speicher']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_WSP = Speicher['elektr_Speicher']['Zinssatz'] / 100
    a_ESP = economics.annuity(capex=Capex_ESP, n=Amort_a_ESP, wacc=Zinssatz_WSP)
    b_ESP = Capex_ESP * Opex_ESP
    epc_ESP = a_ESP + b_ESP

    # ------------------------------------------------------------------------------
    # Gasturbine_1
    # ------------------------------------------------------------------------------
    # Wirkungsgrade und Leistungen
    eta_el_GT_1_brutto = Gasturbinen['Gasturbine_1']['Wirkungsgrad_el_brutto'] / 100
    eta_Abgas_GT_1 = 1 - eta_el_GT_1_brutto
    P_el_max_GT_1_brutto = Gasturbinen['Gasturbine_1']['max_Leistung_el_brutto']
    Gasbezug_GT_1 = P_el_max_GT_1_brutto / eta_el_GT_1_brutto
    P_el_eigen_GT_1 = Gasturbinen['Gasturbine_1']['Eigenverbrauchsfaktor'] * P_el_max_GT_1_brutto
    P_el_max_GT_1_netto = P_el_max_GT_1_brutto - P_el_eigen_GT_1
    # Eigenverbrauchsfaktor_GT_1 = Gasturbinen['Gasturbine_1']['Eigenverbrauchsfaktor']
    # P_el_max_GT_1_netto = P_el_max_GT_1_brutto * Eigenverbrauchsfaktor_GT_1
    eta_el_GT_1_netto = P_el_max_GT_1_netto / Gasbezug_GT_1
    P_Abgas_GT_1_max = Gasbezug_GT_1 * eta_Abgas_GT_1
    P_Abgas_GT_1_min = Abhitzekessel_Abhitzebetrieb['AHK_1']['min_Leistung_Frischdampf'] / (
            Abhitzekessel_Abhitzebetrieb['AHK_1']['Wirkungsgrad_Frischdampf'] / 100)
    Gasbezug_GT_1_min = P_Abgas_GT_1_min / eta_Abgas_GT_1
    P_el_min_GT_1_netto = Gasbezug_GT_1_min * eta_el_GT_1_netto
    P_el_min_GT_1_netto_relativ = P_el_min_GT_1_netto / P_el_max_GT_1_netto
    # Haltezeiten
    Betriebszeit_GT_1_min = Gasturbinen['Gasturbine_1']['Mindestbetriebszeit']
    Stillstandszeit_GT_1_min = Gasturbinen['Gasturbine_1']['Mindeststillstandszeit']
    # Investitionsmodell
    Capex_GT_1 = Gasturbinen['Gasturbine_1']['CAPEX']
    Capex_GT_1_gas = Gasturbinen['Gasturbine_1']['CAPEX'] * eta_el_GT_1_netto
    Opex_GT_1 = Gasturbinen['Gasturbine_1']['OPEX'] / 100
    Amort_a_GT_1 = Gasturbinen['Gasturbine_1']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_GT_1 = Gasturbinen['Gasturbine_1']['Zinssatz'] / 100
    # Umrechnung auf jährliche Investkosten:
    a_GT_1 = economics.annuity(capex=Capex_GT_1, n=Amort_a_GT_1, wacc=Zinssatz_GT_1)
    a_GT_1_gas = economics.annuity(capex=Capex_GT_1_gas, n=Amort_a_GT_1, wacc=Zinssatz_GT_1)
    b_GT_1 = Capex_GT_1 * Opex_GT_1
    b_GT_1_gas = Capex_GT_1_gas * Opex_GT_1
    epc_GT_1 = a_GT_1 + b_GT_1
    epc_GT_1_gas = a_GT_1_gas + b_GT_1_gas

    # ------------------------------------------------------------------------------
    # Gasturbine_2
    # ------------------------------------------------------------------------------
    # Wirkungsgrade und Leistungen
    eta_el_GT_2_brutto = Gasturbinen['Gasturbine_2']['Wirkungsgrad_el_brutto'] / 100
    eta_Abgas_GT_2 = 1 - eta_el_GT_2_brutto
    P_el_max_GT_2_brutto = Gasturbinen['Gasturbine_2']['max_Leistung_el_brutto']
    Gasbezug_GT_2 = P_el_max_GT_2_brutto / eta_el_GT_2_brutto
    P_el_eigen_GT_2 = Gasturbinen['Gasturbine_2']['Eigenverbrauchsfaktor'] * P_el_max_GT_2_brutto
    P_el_max_GT_2_netto = P_el_max_GT_2_brutto - P_el_eigen_GT_2
    # Eigenverbrauchsfaktor_GT_2 = Gasturbinen['Gasturbine_2']['Eigenverbrauchsfaktor']
    # P_el_max_GT_2_netto = P_el_max_GT_2_brutto * Eigenverbrauchsfaktor_GT_2
    eta_el_GT_2_netto = P_el_max_GT_2_netto / Gasbezug_GT_2
    P_Abgas_GT_2_max = Gasbezug_GT_2 * eta_Abgas_GT_2
    P_Abgas_GT_2_min = Abhitzekessel_Abhitzebetrieb['AHK_2']['min_Leistung_Frischdampf'] / (
            Abhitzekessel_Abhitzebetrieb['AHK_2']['Wirkungsgrad_Frischdampf'] / 100)
    Gasbezug_GT_2_min = P_Abgas_GT_2_min / eta_Abgas_GT_2
    P_el_min_GT_2_netto = Gasbezug_GT_2_min * eta_el_GT_2_netto
    P_el_min_GT_2_netto_relativ = P_el_min_GT_2_netto / P_el_max_GT_2_netto
    # Haltezeiten
    Betriebszeit_GT_2_min = Gasturbinen['Gasturbine_2']['Mindestbetriebszeit']
    Stillstandszeit_GT_2_min = Gasturbinen['Gasturbine_2']['Mindeststillstandszeit']

    # ------------------------------------------------------------------------------
    # Gasturbine_3
    # ------------------------------------------------------------------------------
    # Wirkungsgrade und Leistungen
    eta_el_GT_3_brutto = Gasturbinen['Gasturbine_3']['Wirkungsgrad_el_brutto'] / 100
    eta_Abgas_GT_3 = 1 - eta_el_GT_3_brutto
    P_el_max_GT_3_brutto = Gasturbinen['Gasturbine_3']['max_Leistung_el_brutto']
    Gasbezug_GT_3 = P_el_max_GT_3_brutto / eta_el_GT_3_brutto
    P_el_eigen_GT_3 = Gasturbinen['Gasturbine_3']['Eigenverbrauchsfaktor'] * P_el_max_GT_3_brutto
    P_el_max_GT_3_netto = P_el_max_GT_3_brutto - P_el_eigen_GT_3

    eta_el_GT_3_netto = P_el_max_GT_3_netto / Gasbezug_GT_3
    P_Abgas_GT_3_max = Gasbezug_GT_3 * eta_Abgas_GT_3
    P_Abgas_GT_3_min = Abhitzekessel_Abhitzebetrieb['AHK_3']['min_Leistung_Frischdampf'] / (
            Abhitzekessel_Abhitzebetrieb['AHK_3']['Wirkungsgrad_Frischdampf'] / 100)
    Gasbezug_GT_3_min = P_Abgas_GT_3_min / eta_Abgas_GT_3
    P_el_min_GT_3_netto = Gasbezug_GT_3_min * eta_el_GT_3_netto
    P_el_min_GT_3_netto_relativ = P_el_min_GT_3_netto / P_el_max_GT_3_netto
    # Haltezeiten
    Betriebszeit_GT_3_min = Gasturbinen['Gasturbine_3']['Mindestbetriebszeit']
    Stillstandszeit_GT_3_min = Gasturbinen['Gasturbine_3']['Mindeststillstandszeit']
    # Investitionsmodell
    Capex_GT_3 = Gasturbinen['Gasturbine_3']['CAPEX']
    Opex_GT_3 = Gasturbinen['Gasturbine_3']['OPEX'] / 100
    Amort_a_GT_3 = Gasturbinen['Gasturbine_3']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_GT_3 = Gasturbinen['Gasturbine_3']['Zinssatz'] / 100
    # Umrechnung auf jährliche Investkosten:
    a_GT_3 = economics.annuity(capex=Capex_GT_3, n=Amort_a_GT_3, wacc=Zinssatz_GT_3)
    b_GT_3 = Capex_GT_3 * Opex_GT_3
    epc_GT_3 = a_GT_3 + b_GT_3

    # ------------------------------------------------------------------------------
    # Abhitzekessel 1
    # ------------------------------------------------------------------------------
    # Abhitzebetrieb (AB)
    eta_AHK_1_AB = Abhitzekessel_Abhitzebetrieb['AHK_1']['Wirkungsgrad_Frischdampf'] / 100
    P_min_AHK_1_AB = Abhitzekessel_Abhitzebetrieb['AHK_1']['min_Leistung_Frischdampf']
    P_max_AHK_1_AB = Abhitzekessel_Abhitzebetrieb['AHK_1']['max_Leistung_Frischdampf']
    P_min_AHK_1_AB_relativ = P_min_AHK_1_AB / P_max_AHK_1_AB
    P_max_HWS_1_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_1']['max_Leistung_Heisswasser']
    P_in_AHK_1_AB = P_max_AHK_1_AB / eta_AHK_1_AB
    P_max_RG_1_AB = Abhitzekessel_Abhitzebetrieb['AHK_1']['P_RG']

    P_el_eigen_AHK_1_AB = Abhitzekessel_Abhitzebetrieb['AHK_1']['Eigenbedarfsfaktor'] * (
            P_max_AHK_1_AB + P_max_HWS_1_AB_u_KB)

    eta_el_AHK_1_AB = P_el_eigen_AHK_1_AB / (P_el_eigen_AHK_1_AB + P_in_AHK_1_AB)
    eta_Abgas_AHK_1_AB = P_in_AHK_1_AB / (P_el_eigen_AHK_1_AB + P_in_AHK_1_AB)
    eta_FD_AHK_1_AB = P_max_AHK_1_AB / (P_el_eigen_AHK_1_AB + P_in_AHK_1_AB)
    eta_HWS_AHK_1_AB = P_max_HWS_1_AB_u_KB / (P_el_eigen_AHK_1_AB + P_in_AHK_1_AB)
    eta_RG_AHK_1_AB = P_max_RG_1_AB / (P_el_eigen_AHK_1_AB + P_in_AHK_1_AB)

    Betriebszeit_AHK_1_AB_min = Abhitzekessel_Abhitzebetrieb['AHK_1']['Mindestbetriebszeit']
    Stillstandszeit_AHK_1_AB_min = Abhitzekessel_Abhitzebetrieb['AHK_1']['Mindeststillstandszeit']

    # Frischluftbetrieb (FB)
    eta_AHK_1_FB = Abhitzekessel_Frischluftbetrieb['AHK_1']['Wirkungsgrad_Frischdampf'] / 100
    P_min_AHK_1_FB = Abhitzekessel_Frischluftbetrieb['AHK_1']['min_Leistung_Frischdampf']
    P_max_AHK_1_FB = Abhitzekessel_Frischluftbetrieb['AHK_1']['max_Leistung_Frischdampf']
    P_max_HWS_1_FB = Heisswasserschleife_Frischluftbetrieb['HWS_1']['max_Leistung_Heisswasser']
    P_in_AHK_1_FB = P_max_AHK_1_FB / eta_AHK_1_FB
    P_max_RG_1_FB = Abhitzekessel_Frischluftbetrieb['AHK_1']['P_RG']

    P_el_eigen_AHK_1_FB = Abhitzekessel_Abhitzebetrieb['AHK_1']['Eigenbedarfsfaktor'] * (
                P_max_AHK_1_FB + P_max_HWS_1_FB)

    eta_el_AHK_1_FB = P_el_eigen_AHK_1_FB / (P_el_eigen_AHK_1_FB + P_in_AHK_1_FB)
    eta_Gas_AHK_1_FB = P_in_AHK_1_FB / (P_el_eigen_AHK_1_FB + P_in_AHK_1_FB)
    eta_FD_AHK_1_FB = P_max_AHK_1_FB / (P_el_eigen_AHK_1_FB + P_in_AHK_1_FB)
    eta_HWS_AHK_1_FB = P_max_HWS_1_FB / (P_el_eigen_AHK_1_FB + P_in_AHK_1_FB)
    eta_RG_AHK_1_FB = P_max_RG_1_FB / (P_el_eigen_AHK_1_FB + P_in_AHK_1_FB)

    # eta_AHK_1_FB_HWS = P_max_HWS_1_FB / P_in_AHK_1_FB

    Betriebszeit_AHK_1_FB_min = Abhitzekessel_Frischluftbetrieb['AHK_1']['Mindestbetriebszeit']
    Stillstandszeit_AHK_1_FB_min = Abhitzekessel_Frischluftbetrieb['AHK_1']['Mindeststillstandszeit']

    # Capex_AHK_1_FB = Abhitzekessel_Frischluftbetrieb['AHK_1']['CAPEX']
    # Opex_AHK_1_FB = Abhitzekessel_Frischluftbetrieb['AHK_1']['OPEX']/100
    # Amort_a_AHK_1_FB = Abhitzekessel_Frischluftbetrieb['AHK_1']['Amortisierungszeitraum_in_Jahren']
    # Zinssatz_AHK_1_FB = Abhitzekessel_Frischluftbetrieb['AHK_1']['Zinssatz']/100
    # # Umrechnung auf jährliche Investkosten:
    # a_AHK_1_FB = economics.annuity(capex=Capex_AHK_1_FB, n=Amort_a_AHK_1_FB, wacc=Zinssatz_AHK_1_FB)
    # b_AHK_1_FB = Capex_AHK_1_FB * Opex_AHK_1_FB
    # epc_AHK_1_FB = a_AHK_1_FB + b_AHK_1_FB

    # Kombibetrieb (KB)
    eta_AHK_1_KB = Abhitzekessel_Kombibetrieb['AHK_1']['Wirkungsgrad_Frischdampf'] / 100
    P_min_AHK_1_KB = Abhitzekessel_Kombibetrieb['AHK_1']['min_Leistung_Frischdampf']
    P_max_AHK_1_KB = Abhitzekessel_Kombibetrieb['AHK_1']['max_Leistung_Frischdampf']
    P_in_AHK_1_KB = P_max_AHK_1_KB / eta_AHK_1_KB
    P_Zusatz_AHK_1_KB = P_in_AHK_1_KB - P_Abgas_GT_1_max
    P_max_RG_AHK_1_KB = Abhitzekessel_Kombibetrieb['AHK_1']['P_RG']

    P_el_eigen_AHK_1_KB = Abhitzekessel_Abhitzebetrieb['AHK_1']['Eigenbedarfsfaktor'] * (
            P_max_AHK_1_KB + P_max_HWS_1_AB_u_KB)

    eta_el_AHK_1_KB = P_el_eigen_AHK_1_KB / (P_Abgas_GT_1_max + P_Zusatz_AHK_1_KB + P_el_eigen_AHK_1_KB)
    eta_Gas_AHK_1_KB = P_Zusatz_AHK_1_KB / (P_Abgas_GT_1_max + P_Zusatz_AHK_1_KB + P_el_eigen_AHK_1_KB)
    eta_Abgas_AHK_1_KB = P_Abgas_GT_1_max / (P_Abgas_GT_1_max + P_Zusatz_AHK_1_KB + P_el_eigen_AHK_1_KB)
    eta_FD_AHK_1_KB = P_max_AHK_1_KB / (P_Abgas_GT_1_max + P_Zusatz_AHK_1_KB + P_el_eigen_AHK_1_KB)
    eta_HWS_AHK_1_KB = P_max_HWS_1_AB_u_KB / (P_Abgas_GT_1_max + P_Zusatz_AHK_1_KB + P_el_eigen_AHK_1_KB)
    eta_RG_AHK_1_KB = P_max_RG_AHK_1_KB / (P_Abgas_GT_1_max + P_Zusatz_AHK_1_KB + P_el_eigen_AHK_1_KB)

    Betriebszeit_AHK_1_KB_min = Abhitzekessel_Kombibetrieb['AHK_1']['Mindestbetriebszeit']
    Stillstandszeit_AHK_1_KB_min = Abhitzekessel_Kombibetrieb['AHK_1']['Mindeststillstandszeit']

    Capex_AHK_1_KB = Abhitzekessel_Kombibetrieb['AHK_1'][
        'CAPEX']  # * ((P_max_AHK_1_KB + P_max_HWS_1_AB_u_KB) / P_max_AHK_1_KB)
    Opex_AHK_1_KB = Abhitzekessel_Kombibetrieb['AHK_1']['OPEX'] / 100
    Amort_a_AHK_1_KB = Abhitzekessel_Kombibetrieb['AHK_1']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_AHK_1_KB = Abhitzekessel_Kombibetrieb['AHK_1']['Zinssatz'] / 100
    # Umrechnung auf jährliche Investkosten:
    a_AHK_1_KB = economics.annuity(capex=Capex_AHK_1_KB, n=Amort_a_AHK_1_KB, wacc=Zinssatz_AHK_1_KB)
    b_AHK_1_KB = Capex_AHK_1_KB * Opex_AHK_1_KB
    epc_AHK_1_KB = a_AHK_1_KB + b_AHK_1_KB

    # ------------------------------------------------------------------------------
    # Abhitzekessel 2
    # ------------------------------------------------------------------------------
    # Abhitzebetrieb (AB)
    eta_AHK_2_AB = Abhitzekessel_Abhitzebetrieb['AHK_2']['Wirkungsgrad_Frischdampf'] / 100
    P_min_AHK_2_AB = Abhitzekessel_Abhitzebetrieb['AHK_2']['min_Leistung_Frischdampf']
    P_max_AHK_2_AB = Abhitzekessel_Abhitzebetrieb['AHK_2']['max_Leistung_Frischdampf']
    P_max_HWS_2_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_2']['max_Leistung_Heisswasser']
    P_in_AHK_2_AB = P_max_AHK_2_AB / eta_AHK_2_AB
    P_max_AHK_RG_2_AB = Abhitzekessel_Abhitzebetrieb['AHK_2']['P_RG']

    P_el_eigen_AHK_2_AB = Abhitzekessel_Abhitzebetrieb['AHK_2']['Eigenbedarfsfaktor'] * (
            P_max_AHK_2_AB + P_max_HWS_2_AB_u_KB)

    eta_el_AHK_2_AB = P_el_eigen_AHK_2_AB / (P_el_eigen_AHK_2_AB + P_in_AHK_2_AB)
    eta_Abgas_AHK_2_AB = P_in_AHK_2_AB / (P_el_eigen_AHK_2_AB + P_in_AHK_2_AB)
    eta_FD_AHK_2_AB = P_max_AHK_2_AB / (P_el_eigen_AHK_2_AB + P_in_AHK_2_AB)
    eta_HWS_AHK_2_AB = P_max_HWS_2_AB_u_KB / (P_el_eigen_AHK_2_AB + P_in_AHK_2_AB)
    eta_RG_AHK_2_AB = P_max_AHK_RG_2_AB / (P_el_eigen_AHK_2_AB + P_in_AHK_2_AB)

    # eta_AHK_2_AB_HWS = P_max_HWS_2_AB_u_KB / P_in_AHK_2_AB

    Betriebszeit_AHK_2_AB_min = Abhitzekessel_Abhitzebetrieb['AHK_2']['Mindestbetriebszeit']
    Stillstandszeit_AHK_2_AB_min = Abhitzekessel_Abhitzebetrieb['AHK_2']['Mindeststillstandszeit']

    # Frischluftbetrieb (FB)
    eta_AHK_2_FB = Abhitzekessel_Frischluftbetrieb['AHK_2']['Wirkungsgrad_Frischdampf'] / 100
    P_min_AHK_2_FB = Abhitzekessel_Frischluftbetrieb['AHK_2']['min_Leistung_Frischdampf']
    P_max_AHK_2_FB = Abhitzekessel_Frischluftbetrieb['AHK_2']['max_Leistung_Frischdampf']
    P_max_HWS_2_FB = Heisswasserschleife_Frischluftbetrieb['HWS_2']['max_Leistung_Heisswasser']
    P_in_AHK_2_FB = P_max_AHK_2_FB / eta_AHK_2_FB
    P_max_AHK_RG_2_FB = Abhitzekessel_Frischluftbetrieb['AHK_2']['P_RG']

    P_el_eigen_AHK_2_FB = Abhitzekessel_Abhitzebetrieb['AHK_2']['Eigenbedarfsfaktor'] * (
                P_max_AHK_2_FB + P_max_HWS_2_FB)

    eta_el_AHK_2_FB = P_el_eigen_AHK_2_FB / (P_el_eigen_AHK_2_FB + P_in_AHK_2_FB)
    eta_Gas_AHK_2_FB = P_in_AHK_2_FB / (P_el_eigen_AHK_2_FB + P_in_AHK_2_FB)
    eta_FD_AHK_2_FB = P_max_AHK_2_FB / (P_el_eigen_AHK_2_FB + P_in_AHK_2_FB)
    eta_HWS_AHK_2_FB = P_max_HWS_2_FB / (P_el_eigen_AHK_2_FB + P_in_AHK_2_FB)
    eta_RG_AHK_2_FB = P_max_AHK_RG_2_FB / (P_el_eigen_AHK_2_FB + P_in_AHK_2_FB)

    # eta_AHK_2_FB_HWS = P_max_HWS_2_FB / P_in_AHK_2_FB

    Betriebszeit_AHK_2_FB_min = Abhitzekessel_Frischluftbetrieb['AHK_2']['Mindestbetriebszeit']
    Stillstandszeit_AHK_2_FB_min = Abhitzekessel_Frischluftbetrieb['AHK_2']['Mindeststillstandszeit']

    # Kombibetrieb (KB)
    eta_AHK_2_KB = Abhitzekessel_Kombibetrieb['AHK_2']['Wirkungsgrad_Frischdampf'] / 100
    P_min_AHK_2_KB = Abhitzekessel_Kombibetrieb['AHK_2']['min_Leistung_Frischdampf']
    P_max_AHK_2_KB = Abhitzekessel_Kombibetrieb['AHK_2']['max_Leistung_Frischdampf']
    P_in_AHK_2_KB = P_max_AHK_2_KB / eta_AHK_2_KB
    P_Zusatz_AHK_2_KB = P_in_AHK_2_KB - P_Abgas_GT_2_max
    P_max_AHK_RG_2_KB = Abhitzekessel_Kombibetrieb['AHK_2']['P_RG']

    P_el_eigen_AHK_2_KB = Abhitzekessel_Abhitzebetrieb['AHK_2']['Eigenbedarfsfaktor'] * (
            P_max_AHK_2_KB + P_max_HWS_2_AB_u_KB)

    eta_el_AHK_2_KB = P_el_eigen_AHK_2_KB / (P_Abgas_GT_2_max + P_Zusatz_AHK_2_KB + P_el_eigen_AHK_2_KB)
    eta_Gas_AHK_2_KB = P_Zusatz_AHK_2_KB / (P_Abgas_GT_2_max + P_Zusatz_AHK_2_KB + P_el_eigen_AHK_2_KB)
    eta_Abgas_AHK_2_KB = P_Abgas_GT_2_max / (P_Abgas_GT_2_max + P_Zusatz_AHK_2_KB + P_el_eigen_AHK_2_KB)
    eta_FD_AHK_2_KB = P_max_AHK_2_KB / (P_Abgas_GT_2_max + P_Zusatz_AHK_2_KB + P_el_eigen_AHK_2_KB)
    eta_HWS_AHK_2_KB = P_max_HWS_2_AB_u_KB / (P_Abgas_GT_2_max + P_Zusatz_AHK_2_KB + P_el_eigen_AHK_2_KB)
    eta_RG_AHK_2_KB = P_max_AHK_RG_2_KB / (P_Abgas_GT_2_max + P_Zusatz_AHK_2_KB + P_el_eigen_AHK_2_KB)

    Betriebszeit_AHK_2_KB_min = Abhitzekessel_Kombibetrieb['AHK_2']['Mindestbetriebszeit']
    Stillstandszeit_AHK_2_KB_min = Abhitzekessel_Kombibetrieb['AHK_2']['Mindeststillstandszeit']

    Capex_AHK_2_KB = Abhitzekessel_Kombibetrieb['AHK_2'][
        'CAPEX']  # * ((P_max_AHK_2_KB + P_max_HWS_2_AB_u_KB) / P_max_AHK_2_KB)
    Opex_AHK_2_KB = Abhitzekessel_Kombibetrieb['AHK_2']['OPEX'] / 100
    Amort_a_AHK_2_KB = Abhitzekessel_Kombibetrieb['AHK_2']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_AHK_2_KB = Abhitzekessel_Kombibetrieb['AHK_2']['Zinssatz'] / 100
    # Umrechnung auf jährliche Investkosten:
    a_AHK_2_KB = economics.annuity(capex=Capex_AHK_2_KB, n=Amort_a_AHK_2_KB, wacc=Zinssatz_AHK_2_KB)
    b_AHK_2_KB = Capex_AHK_2_KB * Opex_AHK_2_KB
    epc_AHK_2_KB = a_AHK_2_KB + b_AHK_2_KB

    # ------------------------------------------------------------------------------
    # Abhitzekessel 3
    # ------------------------------------------------------------------------------
    # Abhitzebetrieb (AB)
    eta_AHK_3_AB = Abhitzekessel_Abhitzebetrieb['AHK_3']['Wirkungsgrad_Frischdampf'] / 100
    P_min_AHK_3_AB = Abhitzekessel_Abhitzebetrieb['AHK_3']['min_Leistung_Frischdampf']
    P_max_AHK_3_AB = P_Abgas_GT_3_max * eta_AHK_3_AB
    P_max_HWS_3_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_3']['max_Leistung_Heisswasser']
    # P_in_AHK_3_AB = P_max_AHK_3_AB / eta_AHK_3_AB
    P_max_AHK_RG_3_AB = Abhitzekessel_Abhitzebetrieb['AHK_3']['P_RG']

    P_el_eigen_AHK_3 = Abhitzekessel_Abhitzebetrieb['AHK_3']['Eigenbedarfsfaktor'] * (
                P_max_AHK_3_AB + P_max_HWS_3_AB_u_KB)
    eta_el_AHK_3 = P_el_eigen_AHK_3 / (P_el_eigen_AHK_3 + P_Abgas_GT_3_max)
    eta_AG_AHK_3 = P_Abgas_GT_3_max / (P_el_eigen_AHK_3 + P_Abgas_GT_3_max)
    eta_HWS_AHK_3 = P_max_HWS_3_AB_u_KB / (P_el_eigen_AHK_3 + P_Abgas_GT_3_max)
    eta_FD_AHK_3 = P_max_AHK_3_AB / (P_el_eigen_AHK_3 + P_Abgas_GT_3_max)
    # eta_AHK_3_AB_HWS = P_max_HWS_3_AB_u_KB / P_in_AHK_3_AB
    eta_RG_AHK_3 = P_max_AHK_RG_3_AB / (P_el_eigen_AHK_3 + P_Abgas_GT_3_max)

    Betriebszeit_AHK_3_AB_min = Abhitzekessel_Abhitzebetrieb['AHK_3']['Mindestbetriebszeit']
    Stillstandszeit_AHK_3_AB_min = Abhitzekessel_Abhitzebetrieb['AHK_3']['Mindeststillstandszeit']

    Capex_AHK_3_AB = Abhitzekessel_Abhitzebetrieb['AHK_3'][
        'CAPEX']  # * ((P_max_AHK_3_AB+P_max_HWS_3_AB_u_KB) / P_max_AHK_3_AB)
    Opex_AHK_3_AB = Abhitzekessel_Abhitzebetrieb['AHK_3']['OPEX'] / 100
    Amort_a_AHK_3_AB = Abhitzekessel_Abhitzebetrieb['AHK_3']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_AHK_3_AB = Abhitzekessel_Abhitzebetrieb['AHK_3']['Zinssatz'] / 100
    # Umrechnung auf jährliche Investkosten:
    a_AHK_3_AB = economics.annuity(capex=Capex_AHK_3_AB, n=Amort_a_AHK_3_AB, wacc=Zinssatz_AHK_3_AB)
    b_AHK_3_AB = Capex_AHK_3_AB * Opex_AHK_3_AB
    epc_AHK_3_AB = a_AHK_3_AB + b_AHK_3_AB

    # ------------------------------------------------------------------------------
    # Heißwasserschleife 1 (HWS)
    # ------------------------------------------------------------------------------
    # Abhitze- und Kombibetrieb
    P_min_HWS_1_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_1']['min_Leistung_Heisswasser']
    P_max_HWS_1_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_1']['max_Leistung_Heisswasser']

    # Frischluftbetrieb
    P_min_HWS_1_FB = Heisswasserschleife_Frischluftbetrieb['HWS_1']['min_Leistung_Heisswasser']
    P_max_HWS_1_FB = Heisswasserschleife_Frischluftbetrieb['HWS_1']['max_Leistung_Heisswasser']

    # ------------------------------------------------------------------------------
    # Heißwasserschleife 2 (HWS)
    # ------------------------------------------------------------------------------
    # Abhitze- und Kombibetrieb
    P_min_HWS_2_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_2']['min_Leistung_Heisswasser']
    P_max_HWS_2_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_2']['max_Leistung_Heisswasser']

    # Frischluftbetrieb
    P_min_HWS_2_FB = Heisswasserschleife_Frischluftbetrieb['HWS_2']['min_Leistung_Heisswasser']
    P_max_HWS_2_FB = Heisswasserschleife_Frischluftbetrieb['HWS_2']['max_Leistung_Heisswasser']

    # ------------------------------------------------------------------------------
    # Heißwasserschleife 3 (HWS)
    # ------------------------------------------------------------------------------
    # Abhitze- und Kombibetrieb
    P_min_HWS_3_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_3']['min_Leistung_Heisswasser']
    P_max_HWS_3_AB_u_KB = Heisswasserschleife_Abhitze_und_Kombibetrieb['HWS_3']['max_Leistung_Heisswasser']

    # ------------------------------------------------------------------------------
    # Dampfturbine - Bestand
    # ------------------------------------------------------------------------------
    # Eigenverbrauchsfaktor_DT_Bestand = Dampfturbinen['Bestand']['Eigenverbrauchsfaktor']
    P_el_max_DT_Bestand_brutto = Dampfturbinen['Bestand']['max_Leistung_el_brutto']
    P_el_eigen_DT_Bestand = Dampfturbinen['Bestand']['Eigenverbrauchsfaktor'] * P_el_max_DT_Bestand_brutto
    Eigenverbrauchsfaktor_DT_Bestand = (P_el_max_DT_Bestand_brutto - P_el_eigen_DT_Bestand) / (
        P_el_max_DT_Bestand_brutto)

    P_el_min_DT_Bestand_netto = Dampfturbinen['Bestand']['min_Leistung_el_brutto'] * Eigenverbrauchsfaktor_DT_Bestand
    P_el_max_DT_Bestand_netto = Dampfturbinen['Bestand']['max_Leistung_el_brutto'] * Eigenverbrauchsfaktor_DT_Bestand
    Q_max_FD_DT_Bestand = Dampfturbinen['Bestand']['max_Leistung_Frischdampf']
    Q_max_FW_DT_Bestand = Q_max_FD_DT_Bestand - Dampfturbinen['Bestand']['max_Leistung_el_brutto']
    Q_max_HW_DT_Bestand = Dampfturbinen['Bestand']['max_Leistung_Heisswasser']
    # Q_max_FW_DT_Bestand = Dampfturbinen['Bestand']['max_Leistung_Frischwasser']
    Q_max_Dampf_DT_Bestand = Dampfturbinen['Bestand']['max_Leistung_Dampf']

    Verhaeltnis_HW_zu_dampf = Q_max_HW_DT_Bestand / Q_max_Dampf_DT_Bestand

    Q_Dampf_DT_Bestand = (Q_max_FW_DT_Bestand) / (Verhaeltnis_HW_zu_dampf + 1)
    Q_HW_DT_Bestand = Q_max_FW_DT_Bestand - Q_Dampf_DT_Bestand
    Q_max_HW_DT_Bestand = Q_HW_DT_Bestand
    Q_max_Dampf_DT_Bestand = Q_Dampf_DT_Bestand
    eta_el_DT_Bestand = P_el_max_DT_Bestand_netto / Q_max_FD_DT_Bestand
    eta_HW_DT_Bestand = Q_HW_DT_Bestand / Q_max_FD_DT_Bestand
    eta_Dampf_DT_Bestand = Q_Dampf_DT_Bestand / Q_max_FD_DT_Bestand

    Betriebszeit_DT_Bestand_min = Dampfturbinen['Bestand']['Mindestbetriebszeit']
    Stillstandszeit_DT_Bestand_min = Dampfturbinen['Bestand']['Mindeststillstandszeit']

    Capex_DT_Bestand = Dampfturbinen['Bestand'][
        'CAPEX']  # * ((Q_HW_DT_Bestand + Q_Dampf_DT_Bestand )/ Q_HW_DT_Bestand )
    Opex_DT_Bestand = Dampfturbinen['Bestand']['OPEX'] / 100
    Amort_a_DT_Bestand = Dampfturbinen['Bestand']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_DT_Bestand = Dampfturbinen['Bestand']['Zinssatz'] / 100
    # Umrechnung auf jährliche Investkosten:
    a_DT_Bestand = economics.annuity(capex=Capex_DT_Bestand, n=Amort_a_DT_Bestand, wacc=Zinssatz_DT_Bestand)
    b_DT_Bestand = Capex_DT_Bestand * Opex_DT_Bestand
    epc_DT_Bestand = a_DT_Bestand + b_DT_Bestand

    # Hochdruck-Teil:
    Eigenverbrauchsfaktor_Tandem_DT = (1 - Tandemdampfturbine['Tandem_HD']['Eigenverbrauchsfaktor'])
    P_el_min_netto_Tandem_DT_HD = Tandemdampfturbine['Tandem_HD'][
                                      'min_Leistung_el_brutto'] * Eigenverbrauchsfaktor_Tandem_DT
    P_el_max_netto_Tandem_DT_HD = Tandemdampfturbine['Tandem_HD'][
                                      'max_Leistung_el_brutto'] * Eigenverbrauchsfaktor_Tandem_DT
    Q_Frischdampf_Tandem_DT_HD = (P_el_max_netto_Tandem_DT_HD) / (
    (Tandemdampfturbine['Tandem_HD']['eta_el_brutto'] / 100))
    Q_Dampf_Tandem_DT_HD = Q_Frischdampf_Tandem_DT_HD - Tandemdampfturbine['Tandem_HD']['max_Leistung_el_brutto']

    eta_el_netto_Tandem_DT_HD = P_el_max_netto_Tandem_DT_HD / Q_Frischdampf_Tandem_DT_HD
    eta_Dampf_Tandem_DT_HD = Q_Dampf_Tandem_DT_HD / Q_Frischdampf_Tandem_DT_HD

    Max_Dampfauskopplung_Tandem_DT_HD = Tandemdampfturbine['Tandem_HD']['Max_Dampfauskopplung']

    Capex_DT_Tandem_HD = Tandemdampfturbine['Tandem_HD']['CAPEX']
    Opex_DT_Tandem_HD = Tandemdampfturbine['Tandem_HD']['OPEX'] / 100
    Amort_a_DT_Tandem_HD = Tandemdampfturbine['Tandem_HD']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_DT_Tandem_HD = Tandemdampfturbine['Tandem_HD']['Zinssatz'] / 100
    # Umrechnung auf jährliche Investkosten:
    a_DT_Tandem_HD = economics.annuity(capex=Capex_DT_Tandem_HD, n=Amort_a_DT_Tandem_HD, wacc=Zinssatz_DT_Tandem_HD)
    b_DT_Tandem_HD = Capex_DT_Tandem_HD * Opex_DT_Tandem_HD
    epc_DT_Tandem_HD = a_DT_Tandem_HD + b_DT_Tandem_HD
    # Volllaststunden_Tandem_DT_HD = 0.00001 #Tandemdampfturbine['Tandem_HD']['Volllaststunden']
    # var_Kosten_Tandem_DT_HD = epc_DT_Tandem_HD/Volllaststunden_Tandem_DT_HD

    Betriebszeit_min_DT_Tandem_HD = Tandemdampfturbine['Tandem_HD']['Mindestbetriebszeit']
    Stillstandszeit_min_DT_Tandem_HD = Tandemdampfturbine['Tandem_HD']['Mindeststillstandszeit']

    # Niederdruck-Teil:
    # Eigenverbrauchsfaktor_Tandem_DT = Tandemdampfturbine['Tandem_HD']['Eigenverbrauchsfaktor']
    P_el_min_netto_Tandem_DT_ND = Tandemdampfturbine['Tandem_ND'][
                                      'min_Leistung_el_brutto'] * Eigenverbrauchsfaktor_Tandem_DT
    P_el_max_netto_Tandem_DT_ND = Tandemdampfturbine['Tandem_ND'][
                                      'max_Leistung_el_brutto'] * Eigenverbrauchsfaktor_Tandem_DT
    Q_Dampf_Tandem_DT_ND = (P_el_max_netto_Tandem_DT_ND) / ((Tandemdampfturbine['Tandem_ND']['eta_el_brutto'] / 100))
    Q_HW_Tandem_DT_ND = Q_Dampf_Tandem_DT_ND - Tandemdampfturbine['Tandem_ND']['max_Leistung_el_brutto']

    eta_el_netto_Tandem_DT_ND = P_el_max_netto_Tandem_DT_ND / Q_Dampf_Tandem_DT_ND
    eta_HW_Tandem_DT_ND = Q_HW_Tandem_DT_ND / Q_Dampf_Tandem_DT_ND

    Betriebszeit_min_DT_Tandem_ND = Tandemdampfturbine['Tandem_ND']['Mindestbetriebszeit']
    Stillstandszeit_min_DT_Tandem_ND = Tandemdampfturbine['Tandem_ND']['Mindeststillstandszeit']

    # ------------------------------------------------------------------------------
    # Heißwassererzeuger - 2 (HWE_2) --> Erfurt Ost
    # ------------------------------------------------------------------------------
    eta_HWE_2 = HWE['HWE_2']['Wirkungsgrad_th']
    Q_min_HWE_2 = HWE['HWE_2']['min_Leistung']
    Q_max_HWE_2 = HWE['HWE_2']['max_Leistung']

    P_el_eigen_HWE_2 = HWE['HWE_2']['Eigenverbrauchsfaktor'] * (Q_max_HWE_2)

    eta_el_HWE_2 = Q_max_HWE_2 / P_el_eigen_HWE_2
    eta_Gas_HWE_2 = eta_HWE_2

    Capex_HWE_2 = HWE['HWE_2']['CAPEX']
    Opex_HWE_2 = HWE['HWE_2']['OPEX'] / 100
    Amort_a_HWE_2 = HWE['HWE_2']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_HWE_2 = HWE['HWE_2']['Zinssatz'] / 100

    a_HWE_2 = economics.annuity(capex=Capex_HWE_2, n=Amort_a_HWE_2, wacc=Zinssatz_HWE_2)
    b_HWE_2 = Capex_HWE_2 * Opex_HWE_2
    epc_HWE_2 = a_HWE_2 + b_HWE_2
    Volllaststunden_HWE_2 = 1500  # HWE['HWE_2']['Volllaststunden']
    var_Kosten_HWE_2 = epc_HWE_2 / Volllaststunden_HWE_2

    # ------------------------------------------------------------------------------
    # Heißwassererzeuger - 5.1 (HWE_5_1) --> Erfurt Iderhoffstraße
    # ------------------------------------------------------------------------------
    eta_HWE_5_1 = HWE['HWE_5_1']['Wirkungsgrad_th']
    Q_min_HWE_5_1 = HWE['HWE_5_1']['min_Leistung']
    Q_max_HWE_5_1 = HWE['HWE_5_1']['max_Leistung']
    Q_max_HWE_5_1_Gas = Q_max_HWE_5_1 / eta_HWE_5_1

    P_el_eigen_HWE_5_1 = HWE['HWE_5_1']['Eigenverbrauchsfaktor'] * (Q_max_HWE_5_1)

    eta_el_HWE_5_1 = Q_max_HWE_5_1 / P_el_eigen_HWE_5_1
    eta_Gas_HWE_5_1 = eta_HWE_5_1

    Capex_HWE_5_1 = HWE['HWE_5_1']['CAPEX'] * (Q_max_HWE_5_1 / Q_max_HWE_5_1_Gas)
    Opex_HWE_5_1 = HWE['HWE_5_1']['OPEX'] / 100
    Amort_a_HWE_5_1 = HWE['HWE_5_1']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_HWE_5_1 = HWE['HWE_5_1']['Zinssatz'] / 100

    a_HWE_5_1 = economics.annuity(capex=Capex_HWE_5_1, n=Amort_a_HWE_5_1, wacc=Zinssatz_HWE_5_1)
    b_HWE_5_1 = Capex_HWE_5_1 * Opex_HWE_5_1
    epc_HWE_5_1 = a_HWE_5_1 + b_HWE_5_1
    Volllaststunden_HWE_5_1 = 1000  # HWE['HWE_5_1']['Volllaststunden']
    var_Kosten_HWE_5_1 = epc_HWE_5_1 / Volllaststunden_HWE_5_1

    eta_Einspeicherung_Heisswasser = Einspeicherung_Heisswasser['Einspeicherung_Heißwasser']['Wirkungsgrad'] / 100

    # ------------------------------------------------------------------------------
    # Heißwassererzeuger - 5.2 (HWE_5_2) --> Erfurt Iderhoffstraße
    # ------------------------------------------------------------------------------
    eta_HWE_5_2 = HWE['HWE_5_2']['Wirkungsgrad_th']
    Q_min_HWE_5_2 = HWE['HWE_5_2']['min_Leistung']
    Q_max_HWE_5_2 = HWE['HWE_5_2']['max_Leistung']

    P_el_eigen_HWE_5_2 = HWE['HWE_5_2']['Eigenverbrauchsfaktor'] * (Q_max_HWE_5_2)

    eta_el_HWE_5_2 = Q_max_HWE_5_2 / P_el_eigen_HWE_5_2
    eta_Gas_HWE_5_2 = eta_HWE_5_2

    Capex_HWE_5_2 = HWE['HWE_5_2']['CAPEX']
    Opex_HWE_5_2 = HWE['HWE_5_2']['OPEX'] / 100
    Amort_a_HWE_5_2 = HWE['HWE_5_2']['Amortisierungszeitraum_in_Jahren']
    Zinssatz_HWE_5_2 = HWE['HWE_5_2']['Zinssatz'] / 100

    a_HWE_5_2 = economics.annuity(capex=Capex_HWE_5_2, n=Amort_a_HWE_5_2, wacc=Zinssatz_HWE_5_2)
    b_HWE_5_2 = Capex_HWE_5_2 * Opex_HWE_5_2
    epc_HWE_5_2 = a_HWE_5_2 + b_HWE_5_2
    Volllaststunden_HWE_5_2 = 4000  # HWE['HWE_5_2']['Volllaststunden']
    var_Kosten_HWE_5_2 = epc_HWE_5_2 / Volllaststunden_HWE_5_2

    # ------------------------------------------------------------------------------
    # Biomasse
    # ------------------------------------------------------------------------------
    # P_Biogas_max = Biomasse['Biogas']['Potential_Summe']
    eta_Biogas_el = Biomasse['Biogas']['Wirkungsgrad_el']
    eta_Biogas_th = Biomasse['Biogas']['Wirkungsgrad_th']

    Capex_Biogas = Biomasse['Biogas']['CAPEX']
    Opex_Biogas = Biomasse['Biogas']['OPEX'] / 100
    Amort_Biogas = Biomasse['Biogas']['Amortisierungszeit']
    Zinssatz_Biogas = Biomasse['Biogas']['Zinssatz']
    a_Biogas = economics.annuity(capex=Capex_Biogas, n=Amort_Biogas, wacc=Zinssatz_Biogas / 100)
    b_Biogas = Capex_Biogas * Opex_Biogas
    epc_Biogas = a_Biogas + b_Biogas

    P_BioHeizwerk_max = Biomasse['Biomasse_Heizwerk']['Potential_Summe']
    Capex_BioHeizwerk = Biomasse['Biomasse_Heizwerk']['CAPEX']
    Opex_BioHeizwerk = Biomasse['Biomasse_Heizwerk']['OPEX'] / 100
    Amort_BioHeizwerk = Biomasse['Biomasse_Heizwerk']['Amortisierungszeit']
    Zinssatz_BioHeizwerk = Biomasse['Biomasse_Heizwerk']['Zinssatz']
    a_BioHeizwerk = economics.annuity(capex=Capex_BioHeizwerk, n=Amort_BioHeizwerk, wacc=Zinssatz_Biogas / 100)
    b_BioHeizwerk = Capex_BioHeizwerk * Opex_BioHeizwerk
    epc_BioHeizwerk = a_BioHeizwerk + b_BioHeizwerk

    P_Biogaseinspeisung_max = Biomasse['Biogaseinspeisung_Neuanlagen']['Potential_Summe']
    eta_Biogaseinspeisung = Biomasse['Biogaseinspeisung_Neuanlagen']['Wirkungsgrad_el']

    Capex_Biogaseinspeisung = Biomasse['Biogaseinspeisung_Neuanlagen']['CAPEX']
    Opex_Biogaseinspeisung = Biomasse['Biogaseinspeisung_Neuanlagen']['OPEX'] / 100
    Amort_a_Biogaseinspeisung = Biomasse['Biogaseinspeisung_Neuanlagen']['Amortisierungszeit']
    Zinssatz_Biogaseinspeisung = Biomasse['Biogaseinspeisung_Neuanlagen']['Zinssatz']
    a_Biogaseinspeisung = economics.annuity(capex=Capex_Biogaseinspeisung,
                                            n=Amort_a_Biogaseinspeisung, wacc=Zinssatz_Biogaseinspeisung / 100)
    b_Biogaseinspeisung = Capex_Biogaseinspeisung * Opex_Biogaseinspeisung
    epc_Biogaseinspeisung = a_Biogaseinspeisung + b_Biogaseinspeisung

    Capex_Geothermie = Geothermie['Tiefengeothermie']['CAPEX']
    Opex_Geothermie = Geothermie['Tiefengeothermie']['OPEX'] / 100
    Amort_Geothermie = Geothermie['Tiefengeothermie']['Amortisationszeit']
    Zinssatz_Geothermie = Geothermie['Tiefengeothermie']['Zinssatz']
    a_Geothermie = economics.annuity(capex=Capex_Geothermie, n=Amort_Geothermie,
                                     wacc=Zinssatz_Geothermie / 100)
    b_Geothermie = Capex_Geothermie * Opex_Geothermie
    epc_Geothermie = a_Geothermie + b_Geothermie

    # Netz
    P_Strom_nom_HS = Stromnetze['Strom HS 110kV']['Max_Export_Leistung']
    data_Preise_2040_CH4_Eur_MWh_Import = [None] * len(Preise['Gaspreis_2020'])
    data_Preise_2040_CH4_Eur_MWh_neu = [None] * len(Preise['Gaspreis_2020'])
    for a in range(0, len(Preise['Gaspreis_2020'])):
        data_Preise_2040_CH4_Eur_MWh_neu[a] = data_Preise_2040_CH4_Eur_MWh[a] + CO2_Preis_2045 * \
                                              Emissionsfaktoren['Emissionsfaktor_2020']['Gas']
        data_Preise_2040_CH4_Eur_MWh_Import[a] = data_Preise_2040_CH4_Eur_MWh_neu[a]
    # %%
    ############################################################################################################################################
    b_el_HS = EnsysBus(label="Strom_HS")
    b_gas = EnsysBus(label="Gas")
    b_fern = EnsysBus(label="Fernwaerme")
    b_frischdampf = EnsysBus(label="Frischdampf")
    b_Dampfnetz = EnsysBus(label="Dampfnetz")
    b_Speicher = EnsysBus(label="Ausspeicherbus")
    b_Nachheiz = EnsysBus(label="Nachheizhilfebus")
    b_ST = EnsysBus(label="Solarthermiebus")
    b_95Grad = EnsysBus(label="FünfundneunzigGradbus")
    b_Abgas_GT_1 = EnsysBus(label="Abgas_GT_1")
    b_Abgas_GT_2 = EnsysBus(label="Abgas_GT_2")
    b_Abgas_GT_3 = EnsysBus(label="Abgas_GT_3")
    b_Dampf_Tandem_intern = EnsysBus(label="Dampf_Tandem_intern")
    b_Frischdampf_Linie1_Hilfe = EnsysBus(label="FrischdampfHilfsbus_Linie1")
    b_Frischdampf_Linie2_Hilfe = EnsysBus(label="FrischdampfHilfsbus_Linie2")
    # b_Abwaerme_Milchwerke = EnsysBus(label="Abwaerme_Milchwerke")
    b_Abwaerme_Waescherei = EnsysBus(label="Abwaerme_Waescherei")
    b_Abwaerme_WWK = EnsysBus(label="Abwaerme_WWK")
    b_Abwaerme_RABA_Rauchgas = EnsysBus(label="Abwaerme_RABA_Rauchgas")
    b_Abwaerme_RABA_alternativ = EnsysBus(label="Abwaerme_RABA_alternativ")
    b_Abwaerme_Luftwaerme = EnsysBus(label="Abwaerme_Luftwaerme")
    b_el_HS_eigenerzeugung = EnsysBus(label="Strom_HS_Eigenerzeugung")
    b_el_HS_eigenverbrauch = EnsysBus(label="Strom_HS_Eigenverbrauch")
    b_biomasse = EnsysBus(label="Biobus")
    b_direktleitung = EnsysBus(label="Direktleitungsbus")
    b_WP_Netz = EnsysBus(label="WP_Abwaerme_Netz")
    b_Betriebsverbrauch = EnsysBus(label="Betriebsverbrauch")
    b_HWE_5_1 = EnsysBus(label="b_HWE_5_1")
    b_AHK_RG = EnsysBus(label="AHK_RG_bus")
    b_Abwaerme_Abwasser_Industrie = EnsysBus(label="Abwaerme_Abwasser_Industrie")
    b_Abwaerme_Flusswasser_Seen = EnsysBus(label="Abwaerme_Flusswasser_Seen")
    b_Abwaerme_Luftwaerme_direkt = EnsysBus(label="Abwaerme_Luftwaerme_direkt")
    b_strom_wwk = EnsysBus(label="Strombus_WWk")
    b_HolzStroh = EnsysBus(label="HolzStroh_Bus")
    b_gas_fiktiv = EnsysBus(label="Gas_fiktiv")
    b_gas2_fiktiv = EnsysBus(label="Gas2_fiktiv")

    # adding the buses to the energy system
    energysystem.busses = [b_el_HS,
                           b_gas,
                           b_fern,
                           b_frischdampf,
                           b_Dampfnetz,
                           b_Speicher,
                           b_Nachheiz,
                           b_ST,
                           b_95Grad,
                           b_Abgas_GT_1,
                           b_Abgas_GT_2,
                           b_Abgas_GT_3,
                           b_Dampf_Tandem_intern,
                           b_Frischdampf_Linie1_Hilfe,
                           b_Frischdampf_Linie2_Hilfe,
                           b_Abwaerme_Waescherei,
                           b_Abwaerme_WWK,
                           b_Abwaerme_RABA_Rauchgas,
                           b_Abwaerme_RABA_alternativ,
                           b_Abwaerme_Luftwaerme,
                           b_el_HS_eigenverbrauch,
                           b_el_HS_eigenerzeugung,
                           b_biomasse,
                           b_direktleitung,
                           b_WP_Netz,
                           b_Betriebsverbrauch,
                           b_HWE_5_1,
                           b_AHK_RG,
                           b_Abwaerme_Abwasser_Industrie,
                           b_Abwaerme_Flusswasser_Seen,
                           b_Abwaerme_Luftwaerme_direkt,
                           b_strom_wwk,
                           b_HolzStroh,
                           b_gas_fiktiv,
                           b_gas2_fiktiv]

    ''' Quellen '''
    energysystem.sources.append(
        EnsysSource(
            label='xTiefengeothermie',
            outputs={b_fern.label: EnsysFlow(
                investment=EnsysInvestment(ep_costs=epc_Geothermie,
                                           maximum=Geothermie['Tiefengeothermie']['max_Leistung'] - 30,
                                           minimum=Geothermie['Tiefengeothermie']['max_Leistung'] - 30)
            )}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Import_Festbrennstoffe',
            outputs={b_biomasse.label: EnsysFlow(
                variable_costs=data_Preis_Biomasse,
                nominal_value=23,
                summed_max=P_Biogaseinspeisung_max / 23
            )}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Import_HolzStroh',
            outputs={b_HolzStroh.label: EnsysFlow(
                variable_costs=data_Preis_Biomasse,
                nominal_value=9.5,
                summed_max=P_BioHeizwerk_max / 9.5
            )}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Strombezug_WWK',
            outputs={b_strom_wwk.label: EnsysFlow(
                variable_costs=PtH_Technologien['WWK']['Strompreis']
            )}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Import_Strom',
            outputs={b_el_HS.label: EnsysFlow(
                investment=EnsysInvestment(ep_costs=Stromnetze['Strom HS 110kV']['Leistungspreis_Netzentgelte'],
                                           maximum=300
                                           )
            )}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Import_Strom_WP',
            outputs={b_WP_Netz.label: EnsysFlow(
                investment=EnsysInvestment(ep_costs=Stromnetze['Strom HS 110kV']['Leistungspreis_Netzentgelte'],
                                           maximum=300
                                           ),
                variable_costs=data_Boerse_Import,
                CO2_factor=float(Emissionsfaktoren['Emissionsfaktor_2045']['Strom'])
            )}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Import_Betriebsverbrauch',
            outputs={b_Betriebsverbrauch.label: EnsysFlow(
                investment=EnsysInvestment(ep_costs=Stromnetze['Strom HS 110kV']['Leistungspreis_Netzentgelte'],
                                           maximum=300
                                           ),
                variable_costs=data_Boerse_Import,
                CO2_factor=float(Emissionsfaktoren['Emissionsfaktor_2045']['Strom'])
            )}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Import_Strom_Eigenverbrauch',
            outputs={b_el_HS_eigenverbrauch.label: EnsysFlow(
                investment=EnsysInvestment(ep_costs=Stromnetze['Strom HS 110kV']['Leistungspreis_Netzentgelte'],
                                           maximum=300
                                           ),
                variable_costs=data_Boerse_Import,
                CO2_factor=float(Emissionsfaktoren['Emissionsfaktor_2045']['Strom'])
            )}
        )
    )

    Capex_Windleitung = 8000000 / 40
    Opex_Windleitung = 2 / 100
    Amort_Windleitung = 40
    Zinssatz_Windleitung = Speicher['elektr_Speicher']['Zinssatz'] / 100
    a_Windleitung = economics.annuity(capex=Capex_Windleitung, n=Amort_Windleitung, wacc=Zinssatz_Windleitung)
    b_Windleitung = Capex_Windleitung * Opex_Windleitung
    epc_Windleitung = a_Windleitung + b_Windleitung

    # Erstellung der Windkraft und Einbindung an den Elektro-BUS
    energysystem.sources.append(
        EnsysSource(
            label='Wind',
            outputs={b_direktleitung.label: EnsysFlow(
                fix=Wind_Erfurt_60,
                variable_costs=Erneuerbare_Energien['Wind']['variable_Kosten'],
                investment=EnsysInvestment(ep_costs=epc_Windleitung,
                                           maximum=Leistung_Windpark_gesamt,
                                           minimum=Leistung_Windpark_gesamt)
            )}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='PV_eigenerzeugung',
            outputs={b_el_HS_eigenerzeugung.label: EnsysFlow(
                fix=PV_Erfurt_60,
                investment=EnsysInvestment(ep_costs=epc_PV,
                                           maximum=P_PV_max_eigenerzeugung,
                                           minimum=0)
            )}
        )
    )

    energysystem.sources.append(
        EnsysTransformer(
            label="ST_roehr_RL",
            inputs={b_WP_Netz.label: EnsysFlow()},
            outputs={b_ST.label: EnsysFlow(fix=data_ST_CPC,
                                           variable_costs=(
                                                       -1 * BEW_Foerderung_ST['ST']['Betriebskostenfoerderung_max']),
                                           investment=EnsysInvestment(ep_costs=epc_ST_RK,
                                                                      minimum=P_ST_RK_RL_min,
                                                                      maximum=P_ST_RK_max)
                                           )
                     },
            conversion_factors={b_ST.label: eta_ST_RK}
        )
    )

    energysystem.sources.append(
        EnsysTransformer(
            label="ST_roehr_VL",
            inputs={b_WP_Netz.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(fix=data_ST_CPC_VL,
                                             variable_costs=(
                                                         -1 * BEW_Foerderung_ST['ST']['Betriebskostenfoerderung_max']),
                                             investment=EnsysInvestment(ep_costs=epc_ST_RK,
                                                                        minimum=P_ST_RK_min,
                                                                        maximum=P_ST_RK_max)
                                             )},
            conversion_factors={b_fern.label: eta_ST_RK}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="ST_roehr_RL_KfW",
            inputs={b_WP_Netz.label: EnsysFlow()},
            outputs={b_ST.label: EnsysFlow(fix=data_ST_CPC,
                                           investment=EnsysInvestment(ep_costs=epc_ST_RK_kfw,
                                                                      minimum=P_ST_RK_RL_min,
                                                                      maximum=P_ST_RK_max)
                                           )},
            conversion_factors={b_ST.label: eta_ST_RK}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="ST_roehr_VL_KfW",
            inputs={b_WP_Netz.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(fix=data_ST_CPC_VL,
                                             investment=EnsysInvestment(ep_costs=epc_ST_RK_kfw,
                                                                        minimum=P_ST_RK_min,
                                                                        maximum=P_ST_RK_max)
                                             )},
            conversion_factors={b_fern.label: eta_ST_RK}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Abwaermepotential_Waescherei',
            outputs={b_Abwaerme_Waescherei.label: EnsysFlow(nominal_value=1,
                                                            fix=data_WP_Abwaerme_Waescherei
                                                            )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Abwaermepotential_Abwasser_Industrie',
            outputs={b_Abwaerme_Abwasser_Industrie.label: EnsysFlow(nominal_value=1,
                                                                    fix=data_WP_Abwaerme_Abwasser_Industrie
                                                                    )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Abwaermepotential_WWK',
            outputs={b_Abwaerme_WWK.label: EnsysFlow(nominal_value=1,
                                                     fix=data_WP_Abwaerme_WWK
                                                     )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Abwaermepotential_Flusswasser_Seen',
            outputs={b_Abwaerme_Flusswasser_Seen.label: EnsysFlow(nominal_value=1,
                                                                  fix=data_WP_Abwaerme_Flusswasser_Seen
                                                                  )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Abwaermepotential_RABA_Rauchgas',
            outputs={b_Abwaerme_RABA_Rauchgas.label: EnsysFlow(nominal_value=1,
                                                               fix=data_WP_Abwaerme_RABA_Rauchgas
                                                               )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Abwaermepotential_RABA_alternativ',
            outputs={b_Abwaerme_RABA_alternativ.label: EnsysFlow(nominal_value=1,
                                                                 fix=data_WP_Abwaerme_RABA_alternativ
                                                                 )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Abwaermepotential_Luftwaerme',
            outputs={b_Abwaerme_Luftwaerme.label: EnsysFlow(nominal_value=1,
                                                            fix=data_WP_Abwaerme_Luftwaerme
                                                            )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Abwaermepotential_Luftwaerme_direkt',
            outputs={b_Abwaerme_Luftwaerme_direkt.label: EnsysFlow(nominal_value=1,
                                                                   fix=data_WP_Abwaerme_Luftwaerme_direkt
                                                                   )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Import_gruenesErdgas',
            outputs={b_gas.label: EnsysFlow(variable_costs=data_Preis_gruenesErdgas,
                                            investment=EnsysInvestment(
                                                ep_costs=Gasnetz['Gasnetz']['NNE_Kraftwerksgas_2035'],
                                                maximum=420)
                                            )
                     }
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Import_H2',
            outputs={b_gas.label: EnsysFlow(variable_costs=float(Preis_H2['H2_Preis_obere_range']['Preis_2045']),
                                            investment=EnsysInvestment(
                                                ep_costs=Gasnetz['Gasnetz']['NNE_Kraftwerksgas_2035'],
                                                maximum=420)
                                            )
                     }
        )
    )

    '''Senken '''
    energysystem.sinks.append(
        EnsysSink(
            label='Last_Strom',
            inputs={b_el_HS.label: EnsysFlow(fix=Last_Strom_SWE,
                                             nominal_value=1
                                             )
                    }
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Last_Heiswasser',
            inputs={b_fern.label: EnsysFlow(fix=Last_Waerme_SWE_Netzverlust,
                                            nominal_value=1
                                            )
                    }
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Last_Dampfnetz',
            inputs={b_Dampfnetz.label: EnsysFlow(fix=data_Grundlast,
                                                 nominal_value=7.5
                                                 )
                    }
        )
    )

    ''' Wandler'''
    energysystem.transformers.append(
        EnsysTransformer(
            label="HWE_2",
            inputs={b_gas.label: EnsysFlow(variable_costs=Brennstoffenergiesteuer),
                    b_Betriebsverbrauch.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_HWE_2,
                                                                        maximum=0
                                                                        )
                                             )
                     },
            conversion_factors={
                b_gas.label: 1 / eta_Gas_HWE_2,
                b_Betriebsverbrauch.label: 1 / eta_el_HWE_2}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="HWE_5_1_Heißwasser",
            inputs={b_HWE_5_1.label: EnsysFlow(variable_costs=Brennstoffenergiesteuer),
                    b_WP_Netz.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(nominal_value=Q_max_HWE_5_1,
                                             keywordHWE51=1,
                                             min=Q_min_HWE_5_1 / Q_max_HWE_5_1,
                                             max=1.0,
                                             nonconvex=EnsysNonConvex()
                                             )
                     },
            conversion_factors={b_HWE_5_1.label: 1 / eta_Gas_HWE_5_1,
                                b_WP_Netz.label: 1 / eta_el_HWE_5_1}
        )
    )

    energysystem.transformers.append(EnsysTransformer(
        label='HWE_5_1_Investblock',
        inputs={b_gas.label: EnsysFlow()},
        outputs={b_HWE_5_1.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_HWE_5_1,
                                                                       maximum=Q_max_HWE_5_1_Gas
                                                                       )
                                            )},
        conversion_factors={b_HWE_5_1.label: 0.9999}
    )
    )

    energysystem.transformers.append(EnsysTransformer(
        label="HWE_5_1_Nachheizung",
        inputs={b_HWE_5_1.label: EnsysFlow(
            variable_costs=Brennstoffenergiesteuer,
        ),
            b_WP_Netz.label: EnsysFlow()},
        outputs={b_Nachheiz.label: EnsysFlow(
            nominal_value=Q_max_HWE_5_1,
            keywordHWE51=1,
            min=Q_min_HWE_5_1 / Q_max_HWE_5_1,
            max=1.0,
            nonconvex=EnsysNonConvex()
        )},
        conversion_factors={b_HWE_5_1.label: 1 / eta_Gas_HWE_5_1,
                            b_WP_Netz.label: 1 / eta_el_HWE_5_1},
    ))

    energysystem.transformers.append(EnsysTransformer(
        label="Heizstab_Nachheizung",
        inputs={b_WP_Netz.label: EnsysFlow()},
        outputs={b_Nachheiz.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_P2H)
                                             )},
        conversion_factors={b_Nachheiz.label: eta_P2H}
    ))

    energysystem.transformers.append(EnsysTransformer(
        label="HWE_5_2",
        inputs={b_gas.label: EnsysFlow(variable_costs=Brennstoffenergiesteuer),
                b_WP_Netz.label: EnsysFlow()},
        outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_HWE_5_2,
                                                                    maximum=0
                                                                    )
                                         )
                 },
        conversion_factors={b_gas.label: 1 / eta_Gas_HWE_5_2,
                            b_WP_Netz.label: 1 / eta_el_HWE_5_2}
    ))

    P_max_GT_1_gas = P_el_max_GT_1_netto / eta_el_GT_1_netto
    energysystem.transformers.append(EnsysTransformer(
        label='GT_1_fiktiv',
        inputs={b_gas.label: EnsysFlow()},
        outputs={b_gas_fiktiv.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_GT_1_gas,
                                                                          maximum=0
                                                                          )
                                               )
                 },
        conversion_factors={b_gas_fiktiv.label: 0.99999}))

    energysystem.transformers.append(EnsysTransformer(
        label='GT_1',
        inputs={b_gas_fiktiv.label: EnsysFlow()},
        outputs={b_el_HS_eigenerzeugung.label: EnsysFlow(investment=EnsysInvestment(ep_costs=0,
                                                                                    maximum=0,
                                                                                    # minimum=P_el_max_GT_1_netto
                                                                                    )),
                 b_Abgas_GT_1.label: EnsysFlow(),
                 },
        conversion_factors={b_el_HS_eigenerzeugung.label: eta_el_GT_1_netto,
                            b_Abgas_GT_1.label: eta_Abgas_GT_1
                            }))

    P_el_max_GT_2_netto = 15
    P_max_GT_2_gas = P_el_max_GT_2_netto / eta_el_GT_2_netto
    energysystem.transformers.append(EnsysTransformer(
        label='GT_2_fiktiv',
        inputs={b_gas.label: EnsysFlow()},
        outputs={b_gas2_fiktiv.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_GT_1_gas,
                                                                           maximum=P_max_GT_2_gas,
                                                                           # minimum=P_el_max_GT_1_netto
                                                                           ))},
        conversion_factors={b_gas2_fiktiv.label: 0.99999}))

    energysystem.transformers.append(EnsysTransformer(
        label='GT_2',
        inputs={b_gas2_fiktiv.label: EnsysFlow()},
        outputs={b_el_HS_eigenerzeugung.label: EnsysFlow(investment=EnsysInvestment(ep_costs=0,
                                                                                    maximum=P_el_max_GT_2_netto,
                                                                                    minimum=P_el_max_GT_2_netto
                                                                                    )),
                 b_Abgas_GT_2.label: EnsysFlow(
                     # min=0,
                     # max=1.0,
                     # investment = EnsysInvestment(ep_costs=epc_GT_1,
                     #                            maximum=P_Abgas_GT_2_max,
                     #                            #minimum=P_Abgas_GT_2_max
                     #                            ),
                 ),
                 },
        conversion_factors={b_el_HS_eigenerzeugung.label: eta_el_GT_2_netto,
                            b_Abgas_GT_2.label: eta_Abgas_GT_2
                            }))

    energysystem.transformers.append(EnsysTransformer(
        label='GT_3',
        inputs={b_gas.label: EnsysFlow()},
        outputs={b_el_HS_eigenerzeugung.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_GT_3,
                                                                                    maximum=15,
                                                                                    minimum=15
                                                                                    )),
                 b_Abgas_GT_3.label: EnsysFlow(
                     # min=0,
                     # max=1.0,
                     # investment = EnsysInvestment(ep_costs=epc_GT_3,
                     #                            maximum=P_Abgas_GT_3_max,
                     #                            #minimum=P_Abgas_GT_3_max
                     #                            ),
                 ),
                 },
        conversion_factors={b_el_HS_eigenerzeugung.label: eta_el_GT_3_netto,
                            b_Abgas_GT_3.label: eta_Abgas_GT_3
                            }))

    energysystem.transformers.append(EnsysTransformer(
        label="AHK_1_AB",
        inputs={b_Abgas_GT_1.label: EnsysFlow(),
                b_Betriebsverbrauch.label: EnsysFlow()},
        outputs={b_Frischdampf_Linie1_Hilfe.label: EnsysFlow(nominal_value=P_max_AHK_1_AB,
                                                             keywordAHK1=1,
                                                             min=P_min_AHK_1_AB / P_max_AHK_1_AB,
                                                             max=1.0,
                                                             nonconvex=EnsysNonConvex()),
                 b_fern.label: EnsysFlow(),
                 b_AHK_RG.label: EnsysFlow()},
        conversion_factors={b_Abgas_GT_1.label: eta_Abgas_AHK_1_AB,
                            b_Betriebsverbrauch.label: eta_el_AHK_1_AB,
                            b_Frischdampf_Linie1_Hilfe.label: eta_FD_AHK_1_AB,
                            b_fern.label: eta_HWS_AHK_1_AB,
                            b_AHK_RG.label: eta_RG_AHK_1_AB}
    ))

    energysystem.transformers.append(EnsysTransformer(
        label="AHK_1_FB",
        inputs={b_gas_fiktiv.label: EnsysFlow(),
                b_Betriebsverbrauch.label: EnsysFlow()
                },
        outputs={b_Frischdampf_Linie1_Hilfe.label: EnsysFlow(nominal_value=P_max_AHK_1_FB,
                                                             keywordAHK1=1,
                                                             min=P_min_AHK_1_FB / P_max_AHK_1_FB,
                                                             max=1.0,
                                                             nonconvex=EnsysNonConvex()),
                 b_fern.label: EnsysFlow(),
                 b_AHK_RG.label: EnsysFlow()
                 },
        conversion_factors={b_gas_fiktiv.label: eta_Gas_AHK_1_FB,
                            b_Betriebsverbrauch.label: eta_el_AHK_1_AB,
                            b_Frischdampf_Linie1_Hilfe.label: eta_FD_AHK_1_FB,
                            b_fern.label: eta_HWS_AHK_1_FB,
                            b_AHK_RG.label: eta_RG_AHK_1_FB}
    ))

    energysystem.transformers.append(EnsysTransformer(
        label='AHK_1_KB',
        inputs={b_Abgas_GT_1.label: EnsysFlow(),
                b_gas_fiktiv.label: EnsysFlow(),
                b_Betriebsverbrauch.label: EnsysFlow()
                },
        outputs={b_Frischdampf_Linie1_Hilfe.label: EnsysFlow(nominal_value=P_max_AHK_1_KB,
                                                             keywordAHK1=1,
                                                             min=P_min_AHK_1_KB / P_max_AHK_1_KB,
                                                             max=1.0,
                                                             nonconvex=EnsysNonConvex()),
                 b_fern.label: EnsysFlow(),
                 b_AHK_RG.label: EnsysFlow()
                 },
        conversion_factors={b_Abgas_GT_1.label: eta_Abgas_AHK_1_KB,
                            b_Betriebsverbrauch.label: eta_el_AHK_1_KB,
                            b_gas_fiktiv.label: eta_Gas_AHK_1_KB,
                            b_fern.label: eta_HWS_AHK_1_KB,
                            b_Frischdampf_Linie1_Hilfe.label: eta_FD_AHK_1_KB,
                            b_AHK_RG.label: eta_RG_AHK_1_KB
                            }
    ))

    energysystem.transformers.append(EnsysTransformer(
        label='FrischdampfHilfstrafo_Linie1',
        inputs={b_Frischdampf_Linie1_Hilfe.label: EnsysFlow()
                },
        outputs={b_frischdampf.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_AHK_1_KB,
                                                                           maximum=0,
                                                                           # minimum=P_max_AHK_1_KB
                                                                           )
                                                )},
        conversion_factors={b_frischdampf.label: 0.9999}
    )
    )

    energysystem.transformers.append(EnsysTransformer(
        label="AHK_2_AB",
        inputs={b_Abgas_GT_2.label: EnsysFlow(),
                b_Betriebsverbrauch.label: EnsysFlow()
                },
        outputs={b_Frischdampf_Linie2_Hilfe.label: EnsysFlow(nominal_value=P_max_AHK_2_AB,
                                                             keywordAHK2=1,
                                                             min=P_min_AHK_2_AB / P_max_AHK_2_AB,
                                                             max=1.0,
                                                             nonconvex=EnsysNonConvex()),
                 b_fern.label: EnsysFlow(),
                 b_AHK_RG.label: EnsysFlow()
                 },
        conversion_factors={b_Abgas_GT_2.label: eta_Abgas_AHK_2_AB,
                            b_Betriebsverbrauch.label: eta_el_AHK_2_AB,
                            b_Frischdampf_Linie2_Hilfe.label: eta_FD_AHK_2_AB,
                            b_fern.label: eta_HWS_AHK_2_AB,
                            b_AHK_RG.label: eta_RG_AHK_2_AB}
    ))

    energysystem.transformers.append(EnsysTransformer(
        label="AHK_2_FB",
        inputs={b_gas2_fiktiv.label: EnsysFlow(),
                b_Betriebsverbrauch.label: EnsysFlow()
                },
        outputs={b_Frischdampf_Linie2_Hilfe.label: EnsysFlow(nominal_value=P_max_AHK_2_FB,
                                                             keywordAHK2=1,
                                                             min=P_min_AHK_2_FB / P_max_AHK_2_FB,
                                                             max=1.0,
                                                             nonconvex=EnsysNonConvex()),
                 b_fern.label: EnsysFlow(),
                 b_AHK_RG.label: EnsysFlow()
                 },
        conversion_factors={b_gas2_fiktiv.label: eta_Gas_AHK_2_FB,
                            b_Betriebsverbrauch.label: eta_el_AHK_2_FB,
                            b_Frischdampf_Linie2_Hilfe.label: eta_FD_AHK_2_FB,
                            b_fern.label: eta_HWS_AHK_2_FB,
                            b_AHK_RG.label: eta_RG_AHK_2_FB}
    ))

    energysystem.transformers.append(EnsysTransformer(
        label='AHK_2_KB',
        inputs={b_Abgas_GT_2.label: EnsysFlow(),
                b_gas2_fiktiv.label: EnsysFlow(),
                b_Betriebsverbrauch.label: EnsysFlow()},
        outputs={b_Frischdampf_Linie2_Hilfe.label: EnsysFlow(nominal_value=P_max_AHK_2_KB,
                                                             keywordAHK2=1,
                                                             min=P_min_AHK_2_KB / P_max_AHK_2_KB,
                                                             max=1.0,
                                                             nonconvex=EnsysNonConvex()),
                 b_fern.label: EnsysFlow(),
                 b_AHK_RG.label: EnsysFlow()
                 },
        conversion_factors={b_Betriebsverbrauch.label: eta_el_AHK_2_KB,
                            b_Abgas_GT_2.label: eta_Abgas_AHK_2_KB,
                            b_gas2_fiktiv.label: eta_Gas_AHK_2_KB,
                            b_Frischdampf_Linie2_Hilfe.label: eta_FD_AHK_2_KB,
                            b_fern.label: eta_HWS_AHK_2_KB,
                            b_AHK_RG.label: eta_RG_AHK_2_KB
                            }
    )
    )

    energysystem.transformers.append(EnsysTransformer(
        label='FrischdampfHilfstrafo_Linie2',
        inputs={b_Frischdampf_Linie2_Hilfe.label: EnsysFlow()
                },
        outputs={b_frischdampf.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_AHK_2_KB,
                                                                           maximum=P_max_AHK_2_KB,
                                                                           # minimum=P_max_AHK_2_KB
                                                                           )
                                                )},
        conversion_factors={b_frischdampf.label: 0.9999}
    )
    )

    energysystem.transformers.append(EnsysTransformer(
        label="AHK_3_AB",
        inputs={b_Abgas_GT_3.label: EnsysFlow(),
                b_Betriebsverbrauch.label: EnsysFlow()},
        outputs={b_frischdampf.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_AHK_3_AB,
                                                                           maximum=P_max_AHK_3_AB,
                                                                           # minimum=P_max_AHK_3_AB
                                                                           )),
                 b_fern.label: EnsysFlow(),
                 b_AHK_RG.label: EnsysFlow()
                 },
        conversion_factors={b_Abgas_GT_3.label: eta_AG_AHK_3,
                            b_Betriebsverbrauch.label: eta_el_AHK_3,
                            b_frischdampf.label: eta_FD_AHK_3,
                            b_fern.label: eta_HWS_AHK_3,
                            b_AHK_RG.label: eta_RG_AHK_3}
    ))

    energysystem.transformers.append(EnsysTransformer(
        label='DT-Tandem HD-Teil',
        inputs={b_frischdampf.label: EnsysFlow()},
        outputs={b_el_HS_eigenerzeugung.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_DT_Tandem_HD,
                                                                                    # minimum=P_el_max_netto_Tandem_DT_HD,
                                                                                    maximum=0)
                                                         # nominal_value=P_el_max_netto_Tandem_DT_HD,

                                                         # min=P_el_min_netto_Tandem_DT_HD/P_el_max_netto_Tandem_DT_HD,
                                                         # max=1.0,
                                                         # nonconvex=EnsysNonConvex(
                                                         #     #minimum_uptime=int(Betriebszeit_min_DT_Tandem_HD),
                                                         # #                           minimum_downtime=int(Stillstandszeit_min_DT_Tandem_HD)
                                                         # )

                                                         ),
                 b_Dampf_Tandem_intern.label: EnsysFlow()
                 },
        conversion_factors={b_el_HS_eigenerzeugung.label: eta_el_netto_Tandem_DT_HD,
                            b_Dampf_Tandem_intern.label: eta_Dampf_Tandem_DT_HD
                            }))

    energysystem.transformers.append(
        EnsysTransformer(
            label='DT-Tandem ND-Teil',
            inputs={b_Dampf_Tandem_intern.label: EnsysFlow()},
            outputs={b_el_HS_eigenerzeugung.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_DT_Tandem_HD,
                                                                                        maximum=0)
                                                             ),
                     b_fern.label: EnsysFlow()},
            conversion_factors={b_el_HS_eigenerzeugung.label: eta_el_netto_Tandem_DT_ND,
                                b_fern.label: eta_HW_Tandem_DT_ND}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="Anzapfung_Tandem_DT",
            inputs={b_Dampf_Tandem_intern.label: EnsysFlow()},
            outputs={b_Dampfnetz.label: EnsysFlow()},
            conversion_factors={b_Dampfnetz.label: 0.99}
        )
    )

    energysystem.sources.append(
        EnsysSource(
            label='Ferndampfbezug',
            outputs={b_Dampfnetz.label: EnsysFlow(fix=Ganglinie_RABA['Modell Q RABA'],
                                                  variable_costs=20,
                                                  investment=EnsysInvestment(ep_costs=0, maximum=1, minimum=0)
                                                  )
                     }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='DT-Bestand',
            inputs={b_frischdampf.label: EnsysFlow()},
            outputs={b_el_HS_eigenerzeugung.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_DT_Bestand,
                                                                                        maximum=P_el_max_DT_Bestand_netto,
                                                                                        )
                                                             ),
                     b_fern.label: EnsysFlow(),
                     b_Dampfnetz.label: EnsysFlow()
                     },
            conversion_factors={b_el_HS_eigenerzeugung.label: eta_el_DT_Bestand,
                                b_fern.label: eta_HW_DT_Bestand,
                                b_Dampfnetz.label: eta_Dampf_DT_Bestand
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='Trafo_Kosten_vnne',
            inputs={b_el_HS_eigenerzeugung.label: EnsysFlow()},
            outputs={b_el_HS.label: EnsysFlow(variable_costs=(data_Boerse * (-1)))},
            conversion_factors={b_el_HS.label: 0.999}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='Trafo_Netz_WP_Abwaerme',
            inputs={b_el_HS_eigenerzeugung.label: EnsysFlow()},
            outputs={b_WP_Netz.label: EnsysFlow(variable_costs=Umlagen_Netzanschluss)},
            conversion_factors={b_WP_Netz.label: 0.999}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='Trafo_Betriebsverbrauch',
            inputs={b_el_HS_eigenerzeugung.label: EnsysFlow()},
            outputs={b_Betriebsverbrauch.label: EnsysFlow()},
            conversion_factors={b_el_HS_eigenverbrauch.label: 0.999}
        )
    )

    energysystem.transformers.append(EnsysTransformer(
        label='Trafo_Kosten_Eigenverbrauch',
        inputs={b_el_HS_eigenerzeugung.label: EnsysFlow()},
        outputs={b_el_HS_eigenverbrauch.label: EnsysFlow(variable_costs=Umlagen_Eigenverbrauch
                                                         ),
                 },
        conversion_factors={b_el_HS_eigenverbrauch.label: 0.999}))

    energysystem.transformers.append(
        EnsysTransformer(
            label="Einspeicherung_Heisswasser",
            inputs={b_fern.label: EnsysFlow()},
            outputs={b_95Grad.label: EnsysFlow()},
            conversion_factors={b_95Grad.label: eta_Einspeicherung_Heisswasser}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="Umleitstation - Dampf-HW",
            inputs={b_Dampfnetz.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow()},
            conversion_factors={b_fern.label: 0.99}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="Umleitstation - Frischdampf-Dampf",
            inputs={b_frischdampf.label: EnsysFlow()},
            outputs={b_Dampfnetz.label: EnsysFlow()},
            conversion_factors={b_Dampfnetz.label: 0.99}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WSP_Nachheizung',
            inputs={b_Speicher.label: EnsysFlow(),
                    b_Nachheiz.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow()},
            conversion_factors={b_Speicher.label: eta_speicher_aus,
                                b_Nachheiz.label: eta_nachheiz_aus
                                }
        )
    )

    '''grosstechnische Waermepumpen auf dem Gelände der SWE'''
    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_Speicher',
            inputs={b_el_HS_eigenverbrauch.label: EnsysFlow(),
                    b_ST.label: EnsysFlow()},
            outputs={b_95Grad.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_WP_Speicher_HW,
                                                                          maximum=5,
                                                                          minimum=5
                                                                          )
                                               )
                     },
            conversion_factors={b_el_HS_eigenverbrauch.label: eta_WP_Speicher_el,
                                b_ST.label: eta_WP_Speicher_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_Heisswasser',
            inputs={b_el_HS_eigenverbrauch.label: EnsysFlow(),
                    b_ST.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_WP_Speicher_HW,
                                                                        maximum=2,
                                                                        minimum=2
                                                                        )
                                             )
                     },
            conversion_factors={b_el_HS_eigenverbrauch.label: eta_WP_Heisswasser_el,
                                b_ST.label: eta_WP_Heisswasser_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_Luftwaerme',
            inputs={b_el_HS_eigenverbrauch.label: EnsysFlow(),
                    b_Abwaerme_Luftwaerme.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_Luftwaerme,
                                                                        maximum=0)
                                             )
                     },
            conversion_factors={b_el_HS_eigenverbrauch.label: eta_WP_Abwaerme_Luftwaerme_el,
                                b_Abwaerme_Luftwaerme.label: eta_WP_Abwaerme_Luftwaerme_st}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_AHK_RG',
            inputs={b_el_HS_eigenverbrauch.label: EnsysFlow(),
                    b_AHK_RG.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_RABA_Rauchgas,
                                                                        maximum=0)
                                             )
                     },
            conversion_factors={b_el_HS_eigenverbrauch.label: eta_WP_Abwaerme_AHK_RG_el,
                                b_AHK_RG.label: eta_WP_Abwaerme_AHK_RG_st
                                }
        )
    )

    '''dezentrale Waermepumpen'''

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_Waescherei',
            inputs={b_WP_Netz.label: EnsysFlow(),
                    b_Abwaerme_Waescherei.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_Waescherei,
                                                                        maximum=PtH_Technologien['Waescherei'][
                                                                            'max_Leistung'])
                                             )
                     },
            conversion_factors={b_WP_Netz.label: eta_WP_Abwaerme_Waescherei_el,
                                b_Abwaerme_Waescherei.label: eta_WP_Abwaerme_Waescherei_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_Abwasser_Industrie',
            inputs={b_WP_Netz.label: EnsysFlow(),
                    b_Abwaerme_Abwasser_Industrie.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_Waescherei,
                                                                        maximum=PtH_Technologien['Abwasser_Industrie'][
                                                                            'max_Leistung'],
                                                                        minimum=PtH_Technologien['Abwasser_Industrie'][
                                                                            'max_Leistung']
                                                                        )
                                             )
                     },
            conversion_factors={b_WP_Netz.label: eta_WP_Abwaerme_Waescherei_el,
                                b_Abwaerme_Abwasser_Industrie.label: eta_WP_Abwaerme_Waescherei_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_WWK',
            inputs={b_strom_wwk.label: EnsysFlow(),
                    b_Abwaerme_WWK.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_WWK,
                                                                        maximum=PtH_Technologien['WWK']['max_Leistung'],
                                                                        minimum=PtH_Technologien['WWK']['max_Leistung']
                                                                        )
                                             )
                     },
            conversion_factors={b_strom_wwk.label: eta_WP_Abwaerme_WWK_el,
                                b_Abwaerme_WWK.label: eta_WP_Abwaerme_WWK_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_Flusswasser_Seen',
            inputs={b_WP_Netz.label: EnsysFlow(),
                    b_Abwaerme_Flusswasser_Seen.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_FlusswasserSeen,
                                                                        maximum=2.5,
                                                                        minimum=2.5
                                                                        )
                                             )
                     },
            conversion_factors={b_WP_Netz.label: eta_WP_Abwaerme_Flusswasser_Seen_el,
                                b_Abwaerme_Flusswasser_Seen.label: eta_WP_Abwaerme_Flusswasser_Seen_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_RABA_Rauchgas',
            inputs={b_WP_Netz.label: EnsysFlow(),
                    b_Abwaerme_RABA_Rauchgas.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_RABA_Rauchgas,
                                                                        maximum=0)
                                             )
                     },
            conversion_factors={b_WP_Netz.label: eta_WP_Abwaerme_RABA_Rauchgas_el,
                                b_Abwaerme_RABA_Rauchgas.label: eta_WP_Abwaerme_RABA_Rauchgas_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='Einspeisung_RL',
            inputs={b_Abwaerme_RABA_Rauchgas.label: EnsysFlow()},
            outputs={b_ST.label: EnsysFlow(nominal_value=5)},
            conversion_factors={b_ST.label: 0.99999999}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_RABA_alternativ',
            inputs={b_WP_Netz.label: EnsysFlow(),
                    b_Abwaerme_RABA_alternativ.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_RABA_alternativ,
                                                                        maximum=PtH_Technologien['RABA_alternativ'][
                                                                            'max_Leistung'],
                                                                        minimum=PtH_Technologien['RABA_alternativ'][
                                                                            'max_Leistung'])
                                             )
                     },
            conversion_factors={b_WP_Netz.label: eta_WP_Abwaerme_RABA_alternativ_el,
                                b_Abwaerme_RABA_alternativ.label: eta_WP_Abwaerme_RABA_alternativ_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="P2H_Heizstab",
            inputs={b_el_HS_eigenverbrauch.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_P2H,
                                                                        maximum=0
                                                                        )
                                             )
                     },
            conversion_factors={b_fern.label: eta_P2H}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="Heizstab_Direkt",
            inputs={b_direktleitung.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_P2H,
                                                                        maximum=39.5,
                                                                        minimum=39.5
                                                                        )
                                             )
                     },
            conversion_factors={b_fern.label: eta_P2H}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='WP_Luftwaerme_direkt',
            inputs={b_direktleitung.label: EnsysFlow(),
                    b_Abwaerme_Luftwaerme_direkt.label: EnsysFlow()},
            outputs={b_fern.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_Luftwaerme_direkt,
                                                                        maximum=2,
                                                                        minimum=2
                                                                        )
                                             )
                     },
            conversion_factors={b_direktleitung.label: eta_WP_Abwaerme_Luftwaerme_el,
                                b_Abwaerme_Luftwaerme_direkt.label: eta_WP_Abwaerme_Luftwaerme_st
                                }
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="Biomasse_Heizwerk",
            inputs={b_HolzStroh.label: EnsysFlow(fix=data_Grundlast)},
            outputs={b_fern.label: EnsysFlow(fix=data_Grundlast,
                                             investment=EnsysInvestment(ep_costs=epc_BioHeizwerk)
                                             )
                     },
            conversion_factors={b_fern.label: Biomasse['Biomasse_Heizwerk']['Wirkungsgrad_th']}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label='Biogas',
            inputs={b_biomasse.label: EnsysFlow(fix=data_Grundlast)},
            outputs={b_el_HS_eigenerzeugung.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_Biogas,
                                                                                        maximum=0),
                                                             fix=data_Grundlast),
                     b_fern.label: EnsysFlow(fix=data_Grundlast)
                     },
            conversion_factors={b_el_HS_eigenerzeugung.label: eta_Biogas_el,
                                b_fern.label: eta_Biogas_th}
        )
    )

    energysystem.transformers.append(
        EnsysTransformer(
            label="Biogaseinspeisung_Neuanlagen",
            inputs={b_biomasse.label: EnsysFlow()},
            outputs={b_gas.label: EnsysFlow(investment=EnsysInvestment(ep_costs=epc_Biogaseinspeisung))},
            conversion_factors={b_gas.label: eta_Biogaseinspeisung}
        )
    )

    C_th_Speicher_max = 438
    '''Speicher'''
    # WSP drucklos
    # Investmodell
    energysystem.storages.append(
        EnsysStorage(
            label='WSP_drucklos',
            inputs={b_95Grad.label: EnsysFlow()},
            outputs={b_Speicher.label: EnsysFlow()},
            loss_rate=(0.003 / 24),
            inflow_conversion_factor=Einspeicherwirkungsgrad_WSP_drucklos,
            outflow_conversion_factor=1,
            initial_storage_level=Init_Speicherzustand_WSP_drucklos,
            invest_relation_input_capacity=1 / (C_Rate_WSP_drucklos),
            invest_relation_output_capacity=1 / (C_Rate_WSP_drucklos),
            investment=EnsysInvestment(ep_costs=epc_WSP_drucklos,
                                       minimum=Min_Speicherkapazitaet_WSP_drucklos)
        )
    )

    '''Export'''
    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_AHK_RG',
            inputs={b_AHK_RG.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Stromexport',
            inputs={b_el_HS_eigenerzeugung.label: EnsysFlow(nominal_value=P_Strom_nom_HS,
                                                            variable_costs=[i * (-1) for i in data_Boerse]
                                                            )
                    }
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_HS',
            inputs={b_el_HS.label: EnsysFlow(variable_costs=10000000)}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_gas',
            inputs={b_gas.label: EnsysFlow(variable_costs=10000)}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_fern',
            inputs={b_fern.label: EnsysFlow(variable_costs=10000)}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Dampf',
            inputs={b_Dampfnetz.label: EnsysFlow(variable_costs=0.1)}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Frischdampf',
            inputs={b_frischdampf.label: EnsysFlow(variable_costs=0.1)}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Abwaerme_Waescherei',
            inputs={b_Abwaerme_Waescherei.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Abwaerme_WWK',
            inputs={b_Abwaerme_WWK.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Abwaerme_RABA_Rauchgas',
            inputs={b_Abwaerme_RABA_Rauchgas.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Abwaerme_RABA_alternativ',
            inputs={b_Abwaerme_RABA_alternativ.label: EnsysFlow()}
        )
    )
    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Abwaerme_Luftwaerme',
            inputs={b_Abwaerme_Luftwaerme.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Abwaerme_Flusswasser_Seen',
            inputs={b_Abwaerme_Flusswasser_Seen.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Abwaerme_Abwasser_Industrie',
            inputs={b_Abwaerme_Abwasser_Industrie.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Abwaerme_Luftwaerme_direkt',
            inputs={b_Abwaerme_Luftwaerme_direkt.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_direkt',
            inputs={b_direktleitung.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_Biomasse',
            inputs={b_biomasse.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_b_ST',
            inputs={b_ST.label: EnsysFlow()}
        )
    )

    energysystem.sinks.append(
        EnsysSink(
            label='Ueberschuss_HolzStroh',
            inputs={b_HolzStroh.label: EnsysFlow()}
        )
    )

    energysystem.constraints.append(
        EnsysConstraints(
            typ=CONSTRAINT_TYPES.limit_active_flow_count_by_keyword,
            keyword="keywordHWE51",
            upper_limit=1
        )
    )

    energysystem.constraints.append(
        EnsysConstraints(
            typ=CONSTRAINT_TYPES.limit_active_flow_count_by_keyword,
            keyword="keywordAHK1",
            upper_limit=1
        )
    )

    energysystem.constraints.append(
        EnsysConstraints(
            typ=CONSTRAINT_TYPES.limit_active_flow_count_by_keyword,
            keyword="keywordAHK2",
            upper_limit=1
        )
    )

    energysystem.constraints.append(
        EnsysConstraints(
            typ=CONSTRAINT_TYPES.generic_integral_limit,
            keyword="CO2_factor",
            limit=CO2_Grenze
        )
    )

    xf = open(dumpfile, 'wb')
    pickle.dump(energysystem, xf)
    xf.close()

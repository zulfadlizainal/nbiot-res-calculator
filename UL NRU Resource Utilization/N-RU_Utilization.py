#Created by github.com/zulfadlizainal

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###################################Data Import##################################

df_nru = pd.read_excel('ML1_DCI_Info_TTI.xlsx', encoding='utf-8')

# Define NRU Dictionary - 3GPP TS36.213 Sec 16
dic_nru = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 8, 7: 10}

# Define Tone Number Dictionary - 3GPP TS36.213 Sec 16
dic_tone = {0: 1, 1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1,
            10: 1, 11: 1, 12: 3, 13: 3, 14: 3, 15: 3, 16: 6, 17: 6, 18: 12}

###################################Data Celanup#################################

# Data Cosmetics
df_nru.columns = ['Time', 'NRSRP', 'NRSRQ', 'NPDCCH_HSFN', 'NPDCCH_SFN', 'NPDCCH_SubFN', 'RNTI',
                  'UL_Grant', 'DL_Grant', 'PDCCH_Order', 'NDI', 'SC_Index', 'RV', 'NRU',
                  'Scheduling_Delay', 'MCS', 'I_Rep', 'N_Rep', 'DCI_Rep', 'HARQ-ACK Resource']

# Remove
df_nru['Time'] = df_nru['Time'].dt.round('1s')

# Delete Unused columns
del df_nru['RV']

# Fill & Round Down RSRP and RSRQ
df_nru['NRSRP'].fillna(method='ffill', inplace=True)
df_nru['NRSRQ'].fillna(method='ffill', inplace=True)
df_nru = df_nru[np.isfinite(df_nru['NRSRP'])]

df_nru['NRSRP'] = df_nru['NRSRP'].apply(np.floor)
df_nru['NRSRQ'] = df_nru['NRSRQ'].apply(np.floor)

# Filter only row with DCI for DL Grant
df_nru = df_nru.loc[df_nru['UL_Grant'] == 'DCI grant is UL grant(DCI N0)']

# Correcting NRU Values - 3GPP TS36.213 Sec 16
df_nru['NRU_Temp'] = df_nru['NRU'].map(dic_nru)
df_nru['NRU'] = df_nru['NRU_Temp']
df_nru.drop(columns=['NRU_Temp'], inplace=True)

# Correcting Tone Values - 3GPP TS36.213 Sec 16
df_nru['SC_Index_Temp'] = df_nru['SC_Index'].map(dic_tone)
df_nru['SC_Index'] = df_nru['SC_Index_Temp']
df_nru.drop(columns=['SC_Index_Temp'], inplace=True)

# Calculate NRU` with Repetition
df_nru['NRU_with_Rep'] = df_nru['NRU'] * df_nru['N_Rep']

##################################Groupby Sum###################################

# Groupby per Second (Sum NRU Count per Sec)
df_nru_1sec = df_nru.groupby('Time').aggregate(
    {'NRSRP': np.min, 'NRSRQ': np.min, 'NRU': np.sum, 'NRU_with_Rep': np.sum, 'N_Rep': np.mean})

# Groupby per RF (Avg NRU Count per RF)
df_nru_rp = df_nru_1sec.groupby('NRSRP').aggregate(
    {'NRU': np.mean, 'NRU_with_Rep': np.mean, 'N_Rep': np.mean})

df_nru_rq = df_nru_1sec.groupby('NRSRQ').aggregate(
    {'NRU': np.mean, 'NRU_with_Rep': np.mean, 'N_Rep': np.mean})

# Groupby NRU Avg
df_nru_rp_nruavg = df_nru.groupby('NRSRP').aggregate({'NRU': np.mean})
df_nru_rp_nruavg.columns = ['NRU_Avg']
df_nru_rq_nruavg = df_nru.groupby('NRSRQ').aggregate({'NRU': np.mean})
df_nru_rq_nruavg.columns = ['NRU_Avg']

import pandas as pd
import numpy as np

mydateparser = lambda x: pd.datetime.strptime(x, "%Y %m %d %H:%M:%S")
df_nsf = pd.read_excel('ML1_DCI_Info_TTI.xlsx', encoding='utf-8', parse_dates=['TIME_STAMP'], date_parser=mydateparser)
#df_nsf = pd.read_excel('ML1_DCI_Info_TTI.xlsx', encoding='utf-8')

# Define NSF Dictionary - 3GPP TS36.213 Sec 16
dic_nsf = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 8, 7: 10}

# Data Cosmetics
df_nsf.columns = ['Time', 'NRSRP', 'NRSRQ', 'NPDCCH_HSFN', 'NPDCCH_SFN', 'NPDCCH_SubFN', 'RNTI',
                  'UL_Grant', 'DL_Grant', 'PDCCH_Order', 'NDI', 'SC_Index', 'RV', 'NSF',
                  'Scheduling_Delay', 'MCS', 'I_Rep', 'N_Rep', 'DCI_Rep', 'HARQ-ACK Resource']

#Delete Unused columns
del df_nsf['SC_Index']
del df_nsf['RV']

# Fill & Round Down RSRP and RSRQ
df_nsf['NRSRP'].fillna(method='ffill', inplace=True)
df_nsf['NRSRQ'].fillna(method='ffill', inplace=True)
df_nsf = df_nsf[np.isfinite(df_nsf['NRSRP'])]

df_nsf['NRSRP'] = df_nsf['NRSRP'].apply(np.floor)
df_nsf['NRSRQ'] = df_nsf['NRSRQ'].apply(np.floor)

# Filter only row with DCI for DL Grant
df_nsf = df_nsf.loc[df_nsf['DL_Grant'] == 'DCI grant is DL grant(DCI N1)']

# Correcting NSF Values - 3GPP TS36.213 Sec 16
df_nsf['NSF_Temp'] = df_nsf['NSF'].map(dic_nsf)
df_nsf['NSF'] = df_nsf['NSF_Temp']
df_nsf.drop(columns=['NSF_Temp'], inplace=True)

#Calculate NSF with Repetition
df_nsf['NSF_wRep'] = df_nsf['NSF']*df_nsf['N_Rep']

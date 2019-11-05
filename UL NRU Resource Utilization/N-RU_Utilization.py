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

# Define Subframe number based on Tone
dic_subframe = {1: 8, 3: 4, 6: 2, 12: 1}

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

# Calculate NRU with Repetition
df_nru['NRU_with_Rep'] = df_nru['NRU'] * df_nru['N_Rep']

# Calculate NRU Length (ms)
df_nru['NRU_Length'] = df_nru['SC_Index'].map(dic_subframe)

# Calculate NRU Length with repetition (ms)
df_nru['NRU_Length_with_Rep'] = df_nru['NRU_Length'] * df_nru['N_Rep']

# Calculate NRU Size (Tone x ms)
df_nru['NRU_Size'] = df_nru['SC_Index'] * df_nru['NRU_Length']

# Calculate NRU Size with repetition
df_nru['NRU_Size_with_Rep'] = df_nru['NRU_Size'] * df_nru['N_Rep']

##################################Groupby Sum###################################

# Groupby per Second (Sum NRU Count per Sec)
df_nru_1sec = df_nru.groupby('Time').aggregate(
    {'NRSRP': np.min, 'NRSRQ': np.min, 'NRU': np.sum, 'NRU_with_Rep': np.sum,
     'NRU_Length': np.sum, 'NRU_Length_with_Rep': np.sum,
     'NRU_Size': np.sum, 'NRU_Size_with_Rep': np.sum,
     'N_Rep': np.mean, 'SC_Index': np.mean})

# Groupby per RF (Avg NRU Count per RF)
df_nru_rp = df_nru_1sec.groupby('NRSRP').aggregate(
    {'NRU': np.mean, 'NRU_with_Rep': np.mean,
     'NRU_Length': np.mean, 'NRU_Length_with_Rep': np.mean,
     'NRU_Size': np.mean, 'NRU_Size_with_Rep': np.mean,
     'N_Rep': np.mean, 'SC_Index': np.mean})

df_nru_rq = df_nru_1sec.groupby('NRSRQ').aggregate(
    {'NRU': np.mean, 'NRU_with_Rep': np.mean,
     'NRU_Length': np.mean, 'NRU_Length_with_Rep': np.mean,
     'NRU_Size': np.mean, 'NRU_Size_with_Rep': np.mean,
     'N_Rep': np.mean, 'SC_Index': np.mean})

# Groupby NRU Avg
df_nru_rp_nruavg = df_nru.groupby('NRSRP').aggregate({'NRU': np.mean})
df_nru_rp_nruavg.columns = ['NRU_Avg']
df_nru_rq_nruavg = df_nru.groupby('NRSRQ').aggregate({'NRU': np.mean})
df_nru_rq_nruavg.columns = ['NRU_Avg']

# Pivot RF by Tone Number
df_nru_rp_tonedist = df_nru[['NRSRP', 'SC_Index', 'SC_Index']].copy()
df_nru_rp_tonedist.columns = ['NRSRP', 'SC_Index', 'Tone']
df_nru_rp_tonedist = df_nru_rp_tonedist.loc[(df_nru_rp_tonedist['NRSRP'] >= -140) & (df_nru_rp_tonedist['NRSRP'] <= -90)]
df_nru_rp_tonedist_pivot = df_nru_rp_tonedist.pivot_table(index = 'NRSRP', columns = 'SC_Index', values = 'Tone', aggfunc = 'count')
df_nru_rp_tonedist_pivot = df_nru_rp_tonedist_pivot.replace(np.nan, 0)

df_nru_rq_tonedist = df_nru[['NRSRQ', 'SC_Index', 'SC_Index']].copy()
df_nru_rq_tonedist.columns = ['NRSRQ', 'SC_Index', 'Tone']
df_nru_rq_tonedist = df_nru_rq_tonedist.loc[(df_nru_rq_tonedist['NRSRQ'] >= -30) & (df_nru_rq_tonedist['NRSRQ'] <= 0)]
df_nru_rq_tonedist_pivot = df_nru_rq_tonedist.pivot_table(index = 'NRSRQ', columns = 'SC_Index', values = 'Tone', aggfunc = 'count')
df_nru_rq_tonedist_pivot = df_nru_rq_tonedist_pivot.replace(np.nan, 0)

####################################Plotting####################################

#Plotting NRU Length
df_nru_rp.plot(y=["NRU_Length", "NRU_Length_with_Rep"])

plt.xlabel("NRSRP (dBm)")
plt.ylabel("NSF Length (ms)")
plt.title("Average NRU Allocation Time / Second")
plt.legend()
plt.grid()
plt.xlim(-140,-90)
plt.ylim(0,1000)

df_nru_rq.plot(y=["NRU_Length", "NRU_Length_with_Rep"])

plt.xlabel("NRSRQ (dB)")
plt.ylabel("NRU Length (ms)")
plt.title("Average NRU Allocation Time / Second")
plt.legend()
plt.grid()
plt.xlim(-30,0)
plt.ylim(0,1000)

#Plotting NRU Size
df_nru_rp.plot(y=["NRU_Size", "NRU_Size_with_Rep"])

plt.xlabel("NRSRP (dBm)")
plt.ylabel("NRU Size (Tone x ms)")
plt.title("Average NRU Allocation Size / Second")
plt.legend()
plt.grid()
plt.xlim(-140,-90)
plt.ylim(0,1000)

df_nru_rq.plot(y=["NRU_Size", "NRU_Size_with_Rep"])

plt.xlabel("NRSRQ (dB)")
plt.ylabel("NRU Size (ms)")
plt.title("Average NRU Allocation Size / Second")
plt.legend()
plt.grid()
plt.xlim(-30,0)
plt.ylim(0,1000)

#Plotting Rep Num
df_nru_rp.plot(y=["N_Rep"])

plt.xlabel("NRSRP (dBm)")
plt.ylabel("N_Rep")
plt.title("Average NPUSCH Repetition Number (N_Rep)")
plt.legend()
plt.grid()
plt.xlim(-140,-90)

df_nru_rq.plot(y=["N_Rep"])

plt.xlabel("NRSRQ (dB)")
plt.ylabel("N_Rep")
plt.title("Average NPUSCH Repetition Number (N_Rep)")
plt.legend()
plt.grid()
plt.xlim(-30,0)

#Plotting NRU Avg Num
df_nru_rp_nruavg.plot(y=["NRU_Avg"])

plt.xlabel("NRSRP (dBm)")
plt.ylabel("NRU Count")
plt.title("Average NRU Allocation Number")
plt.legend()
plt.grid()
plt.xlim(-140,-90)

df_nru_rq_nruavg.plot(y=["NRU_Avg"])

plt.xlabel("NRSRQ (dB)")
plt.ylabel("NRU Count")
plt.title("Average NRU Allocation Number")
plt.legend()
plt.grid()
plt.xlim(-30,0)

#Plotting Tone Number Distribution
df_nru_rp_tonedist_pivot = df_nru_rp_tonedist_pivot.div(df_nru_rp_tonedist_pivot.sum(1), axis=0)
df_nru_rp_tonedist_pivot.plot(kind='bar', stacked=True)
plt.xlabel("NRSRP (dBm)")
plt.ylabel("Tone DIstribution")
plt.title("Uplink Tone Number Distribution")
plt.legend(title = 'Tone Number')

df_nru_rq_tonedist_pivot = df_nru_rq_tonedist_pivot.div(df_nru_rq_tonedist_pivot.sum(1), axis=0)
df_nru_rq_tonedist_pivot.plot(kind='bar', stacked=True)
plt.xlabel("NRSRQ (dB)")
plt.ylabel("Tone DIstribution")
plt.title("Uplink Tone Number Distribution")
plt.legend(title = 'Tone Number')

plt.show()


#############################Data Prepare Export################################

df_nru_rp_exp = pd.concat([df_nru_rp,df_nru_rp_nruavg], axis=1)
df_nru_rq_exp = pd.concat([df_nru_rq,df_nru_rq_nruavg], axis=1)

#Export Data
df_nru_rp.to_csv("Result_RP.csv", encoding='utf-8-sig', index=True)
df_nru_rq.to_csv("Result_RQ.csv", encoding='utf-8-sig', index=True)
df_nru_rp_tonedist_pivot.to_csv("Result_RP_Tone.csv", encoding='utf-8-sig', index=True)
df_nru_rq_tonedist_pivot.to_csv("Result_RQ_Tone.csv", encoding='utf-8-sig', index=True)

print(' ')
print('Terima Kasih')
print('Download this program: https://github.com/zulfadlizainal')
print('Author: https://www.linkedin.com/in/zulfadlizainal')
print(' ')

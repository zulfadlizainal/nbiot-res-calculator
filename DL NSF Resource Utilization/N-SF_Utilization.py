#Created by github.com/zulfadlizainal

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

###################################Data Import##################################

df_nsf = pd.read_excel('ML1_DCI_Info_TTI.xlsx', encoding='utf-8')

# Define NSF Dictionary - 3GPP TS36.213 Sec 16
dic_nsf = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 8, 7: 10}

###################################Data Celanup#################################

# Data Cosmetics
df_nsf.columns = ['Time', 'NRSRP', 'NRSRQ', 'NPDCCH_HSFN', 'NPDCCH_SFN', 'NPDCCH_SubFN', 'RNTI',
                  'UL_Grant', 'DL_Grant', 'PDCCH_Order', 'NDI', 'SC_Index', 'RV', 'NSF',
                  'Scheduling_Delay', 'MCS', 'I_Rep', 'N_Rep', 'DCI_Rep', 'HARQ-ACK Resource']

# Remove
df_nsf['Time'] = df_nsf['Time'].dt.round('1s')

# Delete Unused columns
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

# Calculate NSF with Repetition
df_nsf['NSF_with_Rep'] = df_nsf['NSF'] * df_nsf['N_Rep']

##################################Groupby Sum###################################

# Groupby per Second (Sum NSF Count per Sec)
df_nsf_1sec = df_nsf.groupby('Time').aggregate(
    {'NRSRP': np.min, 'NRSRQ': np.min, 'NSF': np.sum, 'NSF_with_Rep': np.sum, 'N_Rep': np.mean})

# Groupby per RF (Avg NSF Count per RF)
df_nsf_rp = df_nsf_1sec.groupby('NRSRP').aggregate(
    {'NSF': np.mean, 'NSF_with_Rep': np.mean, 'N_Rep': np.mean})

df_nsf_rq = df_nsf_1sec.groupby('NRSRQ').aggregate(
    {'NSF': np.mean, 'NSF_with_Rep': np.mean, 'N_Rep': np.mean})

# Groupby NSF Avg
df_nsf_rp_nsfavg = df_nsf.groupby('NRSRP').aggregate({'NSF': np.mean})
df_nsf_rp_nsfavg.columns = ['NSF_Avg']
df_nsf_rq_nsfavg = df_nsf.groupby('NRSRQ').aggregate({'NSF': np.mean})
df_nsf_rq_nsfavg.columns = ['NSF_Avg']

####################################Plotting####################################

#Plotting NSF Length
df_nsf_rp.plot(y=["NSF", "NSF_with_Rep"])

plt.xlabel("NRSRP (dBm)")
plt.ylabel("NSF Length (ms)")
plt.title("Average NSF Allocation Time / Second (NSF Incl 0)")
plt.legend()
plt.grid()
plt.xlim(-140,-90)
plt.ylim(0,1000)

df_nsf_rq.plot(y=["NSF", "NSF_with_Rep"])

plt.xlabel("NRSRQ (dB)")
plt.ylabel("NSF Length (ms)")
plt.title("Average NSF Allocation Time / Second (NSF Incl 0)")
plt.legend()
plt.grid()
plt.xlim(-30,0)
plt.ylim(0,1000)

#Plotting Rep Num

df_nsf_rp.plot(y=["N_Rep"])

plt.xlabel("NRSRP (dBm)")
plt.ylabel("N_Rep")
plt.title("Average NPDSCH Repetition Number (N_Rep)")
plt.legend()
plt.grid()
plt.xlim(-140,-90)

df_nsf_rq.plot(y=["N_Rep"])

plt.xlabel("NRSRQ (dB)")
plt.ylabel("N_Rep")
plt.title("Average NPDSCH Repetition Number (N_Rep)")
plt.legend()
plt.grid()
plt.xlim(-30,0)

#Plotting NSF Avg Num

df_nsf_rp_nsfavg.plot(y=["NSF_Avg"])

plt.xlabel("NRSRP (dBm)")
plt.ylabel("NSF Count")
plt.title("Average NSF Allocation Number")
plt.legend()
plt.grid()
plt.xlim(-140,-90)

df_nsf_rq_nsfavg.plot(y=["NSF_Avg"])

plt.xlabel("NRSRQ (dB)")
plt.ylabel("NSF Count")
plt.title("Average NSF Allocation Number")
plt.legend()
plt.grid()
plt.xlim(-30,0)

plt.show()

#############################Data Prepare Export################################

df_nsf_rp = pd.concat([df_nsf_rp,df_nsf_rp_nsfavg], axis=1)
df_nsf_rq = pd.concat([df_nsf_rq,df_nsf_rq_nsfavg], axis=1)

#Export Data
df_nsf_rp.to_csv("Result_RP.csv", encoding='utf-8-sig', index=True)
df_nsf_rq.to_csv("Result_RQ.csv", encoding='utf-8-sig', index=True)

print(' ')
print('ありがとうございました！！')
print('Download this program: https://github.com/zulfadlizainal')
print('Author: https://www.linkedin.com/in/zulfadlizainal')
print(' ')

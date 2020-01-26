# UL NSF Resource Utilization

Calculation method of LTE NB-IoT UL N-RU utilization based on scheduled NPUSCH. Calculation is being done based on the reference of 3GPP and captured DCI (NPDCCH) data from Qualcomm Chipset.

### Explanation
For NB-IoT uplink, new concept of UL resource assignment is being introduced called RU (Resource Unit). RU is the smallest unit to map with a transport block. The definition of RU is depending on NPUSCH format and subcarrier spacing.

The concept of NRU can be visualize with below diagram. Important concept to notice is RU can be shaped based on time domain and frequency domain. The number of subcarrier utilize to shape an RU is called Tone number.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_RUSizeMapping.png" alt="RU" title="RU" width=100% height=100% />
<br />
<br />
In NB-IoT uplink, its important to notice that its supports multiple subcarrier spacing.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_SubcarrierSpacing.png" alt="Subcarrier Spacing" title="Subcarrier Spacing" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_SubcarrierSpacing2.png" alt="Subcarrier Spacing" title="Subcarrier Spacing" width=100% height=100% />
<br />
<br />
Scheduling for N-RU is based on following rules from 3GPP:
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_Scheduling.png" alt="N-RU Scheduling" title="N-RU Scheduling" width=100% height=100% />
<br />

### Calculation

Simply, the way to calculate the resource can also be in multiple ways. But I prefer to calculate through the decoded DCI (NPDCCH) gathered from the UE chipset. In that case, we need to study the scheduling method of NPDSCH. Below are simple visual understanding:
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_DCIData.png" alt="DCI for NPUSCH" title="DCI for NPUSCH" width=100% height=100% />
<br />
<br />
If you are not familiar with DCI data, you can head over to this link. I have explain the similar thing using DL N-SF as example. ([Link](https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/tree/master/DL%20NSF%20Resource%20Utilization))
<br />
<br />

### The Codes ([Link](https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/UL%20NRU%20Resource%20Utilization/N-RU_Utilization.py))

Head over to the link above for the python codes. Snapshot below is not a complete codes.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_Codes.png" alt="Codes" title="Codes" width=100% height=100% />
<br />
<br />

### Results

Expected results shown based on given input. Raw data is exactly everything from the UE decoded DCI. The program will calculate NB-IoT UL Resource Utilization KPI based on actual decoded DCI from the UE.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_Result1.png" alt="NRU Avg" title="NRU Avg" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_Result2.png" alt="NRU Length" title="NRU Length" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_Result3.png" alt="NRU Size" title="NRU Size" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_Result4.png" alt="NPUSCH Rep" title="NPUSCH Rep" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NRUUtil_Result5.png" alt="Tone Number" title="Tone Number" width=100% height=100% />
<br />
<br />

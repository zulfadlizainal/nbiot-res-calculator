# DL NSF Resource Utilization

Calculation method of LTE NB-IoT DL N-SF utilization based on scheduled NPDSCH. Calculation is being done based on the reference of 3GPP and captured DCI (NPDCCH) data from Qualcomm Chipset.

### Explanation
In LTE NB-IoT, DL resource unit is known as N-SF. This is due to in LTE NB-IoT, frequency domain will always be 1 PRB or 12 subcarriers. Hence, the important metric to indicate DL NB-IoT resource would be measuring the N-SF, which is the number of subframes allocated.

DL Frame structure in LTE NB-IoT:
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_DLFrame.png" alt="DL Frame Structure" title="DL Frame Structure" width=100% height=100% />
<br />
<br />
Roughly, N-SF can be explained as below figure:
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_NSF.png" alt="NSF" title="NSF" width=100% height=100% />
<br />
<br />
Many ways can interpret the performance of N-SF. However, I focus on certain important key metrics that can summarized the resource utilization in NB-IoT DL.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_KPI.png" alt="KPI" title="KPI" width=100% height=100% />
<br />

### Calculation

Simply, the way to calculate the resource can also be in multiple ways. But I prefer to calculate through the decoded DCI (NPDCCH) gathered from the UE chipset. In that case, we need to study the scheduling method of NPDSCH. Below are simple visual understanding:
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_DCI1.png" alt="NPDSCH Scheduling" title="NPDSCH Scheduling" width=100% height=100% />
<br />
<br />
From the DCI itself, information regarding how many NPDSCH being allocated to the UE and how many NPDSCH repetition is expected for the UE can be retrieved.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_DCI2.png" alt="DCI" title="DCI" width=100% height=100% />
<br />
<br />
Sample actual message decoded by Qualcomm UE chipset.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_DCI3.png" alt="Chipset Msg" title="Chipset Msg" width=100% height=100% />
<br />
<br />
The decoded message need to be converted properly based on 3GPP TS 36.213 to have an absolute NPDSCH that is allocated for the UE.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_DCI4.png" alt="3GPP" title="3GPP" width=100% height=100% />
<br />
<br />

## The Codes ([Link](https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/DL%20NSF%20Resource%20Utilization/N-SF_Utilization.py))

### Results

Expected results shown based on given input. Raw data is exactlly everything from the UE decoded DCI. The program will calculate NB-IoT DL Resource Utilization KPI based on actual decoded DCI from the UE.
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_Result1.png" alt="NSF Avg" title="NSF Avg" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_Result2.png" alt="NSF Incl 0" title="NSF Incl 0" width=100% height=100% />
<br />
<br />
<img src="https://github.com/zulfadlizainal/4G-NB-IoT-Resource-Utilization/blob/master/img/NSFUtil_Result3.png" alt="NPDSCH Rep" title="NPDSCH Rep" width=100% height=100% />
<br />
<br />

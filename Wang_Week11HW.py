
# coding: utf-8

# In[ ]:


# WRITE THE CODE TO IMPORT THE ABOVE FUNCTIONS
import hydrofunctions as hf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


def AR_baseflow(strflow):
    print ("Baseflow Separation Method 1 - Execution started")
    
    ## Intial conditions
    a = .925
    b = (1+a) / 2
    flow = np.array(strflow)
    DR = np.array(strflow)
    BFlow = np.zeros([len(DR),3])
    DR[0] = flow[0] * 0.5
    BFlow[0,0] = flow[0] - DR[0]
    BFlow[0,1] = BFlow[0,0]
    BFlow[0,2] = BFlow[0,0]
    # First pass [forward]
    for i in range(1,len(flow)):
        DR[i] = a * DR[i-1] + b * (flow[i] - flow[i-1])
        if (DR[i] < 0):
            DR[i] = 0
            
        BFlow[i,0] = flow[i] - DR[i]
        if (BFlow[i,0] < 0):
            BFlow[i,0] = 0
            
        if (BFlow[i,0] > flow[i]):
            BFlow[i,0] = flow[i]
    
    ## Second pass [backward]
    BFlow[len(flow)-1,1] = BFlow[len(flow)-1,0]
    for i in range(len(flow)-2,-1,-1):    
        DR[i] = a * DR[i+1] + b * (BFlow[i,0] - BFlow[i+1,0])
        if DR[i] < 0:
            DR[i] = 0
        BFlow[i,1] = BFlow[i,0] - DR[i]
        if BFlow[i,1] < 0:
            BFlow[i,1] = 0
        if BFlow[i,1] > BFlow[i,0]:
            BFlow[i,1] = BFlow[i,0]
    
    ## Third pass [forward]
    BFlow[len(flow)-1,2] = BFlow[len(flow)-1,0]
    for i in range(1,len(flow)):
        DR[i] = a * DR[i-1] + b * (BFlow[i,1]- BFlow[i-1,1])
        if DR[i] < 0:
            DR[i] = 0
        BFlow[i,2] = BFlow[i,1] - DR[i]
        if BFlow[i,2] < 0:
            BFlow[i,2] = 0
        if BFlow[i,2] > BFlow[i,1]:
            BFlow[i,2] = BFlow[i,1]
    print ("Baseflow Separation Method 1 - Execution completed successfully \n")
    return(BFlow[:,2])


# In[ ]:


def EK_baseflow(strflow):
    
    print ("Baseflow Separation Method 2 - Execution started")
    
    alpha=0.98
    BFI_max = 0.8
    flow = np.array(strflow)
    BFlow = np.zeros([len(flow)])
    BFlow[0] = flow[0]
    for i in range(1,len(flow)):
    # algorithm
            BFlow[i] = ((1 - BFI_max) * alpha * BFlow[i-1] + (1 - alpha) * BFI_max * flow[i]) / (1 - alpha * BFI_max)
            if BFlow[i] > flow[i]:
                BFlow[i] = flow[i]
    print ("Baseflow Separation Method 2 - Execution completed successfully \n")
    return(BFlow)


# In[ ]:


# WRITE A CODE TO DEFINE VARIABLES FOR STATION NUMBER,START DATE AND END DATE
USGS_StationCode=input(str("Enter USGS Station Code:\n"))
Start_Date=input(str("Enter the Start Date (YYYY-MM-DD):\n"))
End_Date=input(str("Enter the End Date (YYYY-MM-DD):\n"))


# In[ ]:


#WRITE THE CODE TO DOWNLOAD DAILY STREAMFLOW FROM USGS USING HYDROFUNCTION
data=hf.NWIS(USGS_StationCode,'dv',Start_Date,End_Date)
data.get_data()
print ("download finished")


# In[ ]:


#WRITE YOUR CODE HERE
print(data.df().head())
print("\n")


# In[ ]:


strflow=pd.DataFrame(data.df())
strflow=strflow.drop(columns='USGS:03335500:00060:00003_qualifiers')
strflow=strflow.rename(columns={'USGS:03335500:00060:00003': 'Total_Runoff'})


# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')
#WRITE YOUR CODE HERE TO PLOT THE DISCHARGE HYDROGRAPH
#ALSO PROVIDE AXIS TITLES WITH UNITS
strflow.plot()
plt.xlabel('Days')
plt.ylabel('Discharge (cfs)')
plt.title('Dishcarge Hydrograph (without baseflow)')
plt.show()


# In[ ]:


strflow['AR_baseflow'] = AR_baseflow(strflow['Total_Runoff'])#WRITE YOUR OWN CODE
strflow['EK_baseflow'] = EK_baseflow(strflow['Total_Runoff'])#WRITE YOUR OWN CODE
print(sum(strflow['AR_baseflow'])/len(strflow['AR_baseflow']))
print(sum(strflow['EK_baseflow'])/len(strflow['AR_baseflow']))


# In[ ]:


#WRITE YOUR CODE HERE TO PLOT THE DISCHARGE HYDROGRAPH WITH BASEFLOW SEPARATIONS
#ALSO PROVIDE AXIS TITLES WITH UNITS
strflow.plot()
plt.xlabel('Days')
plt.ylabel('Discharge (cfs)')
plt.title('Dishcarge Hydrograph (with baseflow)')
plt.legend()
plt.show()


# In[ ]:


## Total Streamflow Volume. Direct Runoff Volume, and Baseflow Volume Calculation in m3
Convertion=24*3600*0.0283168
# Total Streamflow
Streamflow=0
for i in strflow['Total_Runoff']:
    Streamflow += i*Convertion
ARBF=0
for i in strflow['AR_baseflow']:
    ARBF+= i*Convertion
EKBF=0
for i in strflow['EK_baseflow']:
    EKBF+= i*Convertion
print ('Convertion Finished')
print ('Data in cubic meter unit:\n')
print ('Total Streamflow Volume:'+str(Streamflow))
print ('AR_Basflow Method:')
print ('Baseflow Volume: ' + str(ARBF))
print ('Direct Runoff Volume: ' + str(Streamflow-ARBF))
print ('EK_Basflow Method:')
print ('Baseflow Volume: ' + str(EKBF))
print ('Direct Runoff Volume: ' + str(Streamflow-EKBF))


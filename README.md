# Trial_CyberWeek16
Cyber Training Class Week16 Assignment
Python script for baseflow seperation with accomendating plots.
 
This script uses 2 methods presented by Arnold et. al. (1995) and Eckhardt (2005). Details can be found in the reference and the Baseflow_Separation.pdf file.

The first method utilizes a digital filter technique which was originally used in signal analysis and processing.In this method, streamflow data are to be filtered three times (forward, backward, and forward again). Each pass will reduce the baseflow as a percentage of total flow.

The second method utilizes a special separation technique which involves recursive digital filtering of hydrographs.

Input data for this script, which is daily streamflow time series, can be obtaimed from USGS NWIS interface: https://waterdata.usgs.gov/nwis/sw

The code was constructed in Jupyter notebook with Anaconda 5.1 in a python 3 environment.
 
 
 References
J.G. Arnold and P.M Allen. Automated methods for estimating BFlow and groundwater recharge from streamflow records. Journal of the Americam Water Resources Association vol 35(2) (April 1999): 411-424.
J.G. Arnold, P.M. Allen, R. Muttiah, and G. Bernhardt, Automated base flow separation and recession analysis techniques. Ground Water vol 33(6): 1010-1018.
Eckhardt, Klaus., How to construct recursive digital filters for baseflow separation, Hydrological Processes: An International Journal 19, no. 2 (2005): 507-515

# FinViz-Intradata
The Updated minute by minute.py file is the code that is used to pull the historical minute by minute screener data from Finviz. Once run, the code will run every minute until it is shut off. While running, the code will update a csv file with the newest data as well as deleting the oldest 10 rows of data. The code can be changed to pull data from any company from Finviz's website, currently it is set to TSLA or Tesla.

The TSLA_Minute_Dataset.csv is the extracted minute by minute data that the Python code pulled from FinViz. The csv file displays data such as date & time, volume, the open and closing prices, as well as a buy/sell signal.

The CandleStick Visualization v2.py is a code that shows how that data that was pulled from FinViz was visualized inte the different charts that were to be used as a popout on the Finviz website. There are both candle and bubble charts in the visualization.

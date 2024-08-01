import datetime
from typing import Tuple, Union
import requests
import pandas as pd
from enum import Enum


class Constant(Enum):

    STOCK = 'stock'
    CURRENCY = 'currency'



class FinViz:
    ticker_list = ["EURUSD", "GBPUSD", "USDJPY", "USDCAD", "USDCHF", "AUDUSD", "NZDUSD", "EURGBP", "GBPJPY", "BTCUSD",
                   "TOP"]
    time_frame_list = ["i1", "i3", "i5", "h", "d", "w", "m"]
    URL = "https://elite.finviz.com/api/quote.ashx?instrument=forex&rev=356737"

    # URL = "https://elite.finviz.com/api/quote.ashx?instrument=stock&rev=356737"
    def __init__(self, asset_type: str, timeout: int = 10, time_frame: str = 'i1') -> None:
        """FinViz class to interact with the finviz website

        Args:
            timeout (int, optional): Specifies the timeout to server in seconds. Defaults to 10.
        """

        self.time_frame = time_frame
        self.asset_type = asset_type
        self._timeout = timeout
        self._time: int = -1
        self._volume: int = -1
        self._price: float = -1.0
        if asset_type == Constant.STOCK:

            self.URL = "https://elite.finviz.com/api/quote.ashx?instrument=stock&rev=356737"

        else:
            self.URL = "https://elite.finviz.com/api/quote.ashx?instrument=forex&rev=356737"

    def get_data(self, time_frame: str = "i1", ticker: str = "EURUSD") -> Tuple[int, int, float]:
        """Get the volume in the last specified time frame

        Args:
            time_frame (str): Choose from time_frame_list:
            ticker (str): Ticker chosen from ticker list e.g.: EURUSD

        Raises:
            Exception: If incorrect timeframe specified
            Exception: If incorrect ticker specified
            Exception: No/Error response from server

        Returns:
            int: time in POSIX format
            int: volume
            float: price
        """
        if time_frame not in self.time_frame_list:
            raise Exception("Incorrect time frame specified, please choose from the list", FinViz.time_frame_list)

        # if ticker not in self.ticker_list:
        #     raise Exception("Incorrect ticker specified, please choose from the list", FinViz.ticker_list)

        payload = {"ticker": ticker, "timeframe": time_frame, "type": "new"}

        # Headers required to show that it is an actual computer
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        response = requests.get(self.URL, params=payload, timeout=self._timeout, headers=headers)

        if response.status_code != 200:
            raise Exception("No response from server")

        json_response = response.json()
        self._time = int(json_response["date"][-1])
        self._volume = int(json_response["volume"][-1])
        self._price = float(json_response["close"][-1])
        return self._time, self._volume, self._price

    def get_all_data(self, time_frame: str = "i1", ticker: str = "EURUSD"):

        """Get the volume in the last specified time frame

        Args:
            time_frame (str): Choose from time_frame_list:
            ticker (str): Ticker chosen from ticker list e.g.: EURUSD

        Raises:
            Exception: If incorrect timeframe specified
            Exception: If incorrect ticker specified
            Exception: No/Error response from server

        Returns:
            int: time in POSIX format
            int: volume
            float: price
        """
        if time_frame not in self.time_frame_list:
            raise Exception("Incorrect time frame specified, please choose from the list", FinViz.time_frame_list)

        # if ticker not in self.ticker_list:
        #     raise Exception("Incorrect ticker specified, please choose from the list", FinViz.ticker_list)

        payload = {"ticker": ticker, "timeframe": time_frame, "type": "new"}

        # Headers required to show that it is an actual computer
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'}
        response = requests.get(self.URL, params=payload, timeout=self._timeout, headers=headers)

        if response.status_code != 200:
            print(f'asset type: {self.asset_type}')
            raise Exception("No response from server")

        json_response = response.json()
        # self._time = int(json_response["date"][:-2])
        # self._volume = int(json_response["volume"][:-2])
        # self._price = float(json_response["lastOpen"])
        # return self._time, self._volume, self._price
        all_volumes = [float(i) for i in json_response["volume"]]
        all_opens = [float(i) for i in json_response["open"]]
        all_closes = [float(i) for i in json_response["close"]]
        all_dates = [float(i) for i in json_response["date"]]

        return all_volumes, all_opens, all_closes, all_dates

    def get_time(self, human_readable: bool = True) -> Union[int, datetime.datetime]:
        """Returns time from server

        Args:
            human_readable (bool, optional): Set to True if you want in datetime format. Defaults to True.

        Raises:
            Exception: If get_data() method not called for first initialization

        Returns:
            Union[int, datetime.datetime]: time in either POSIX or datetime format
        """
        if self._time == -1:
            raise Exception("Please run the API get_data() method before accessing the time")
        if human_readable:
            return datetime.datetime.fromtimestamp(self._time)
        else:
            return self._time

    def get_volume(self):
        if self._volume == -1:
            raise Exception("Please run the API get_data() method before accessing this variable")
        return self._volume

    def get_price(self):
        if self._price == -1.0:
            raise Exception("Please run the API get_data() method before accessing this variable")
if __name__ == "__main__":
    test = FinViz(asset_type=Constant.STOCK)
    # r = test.get_all_data()
    # for k in r:
    #     print(len(k))
    #     print(k)
    # print(jr)
    all_volumes, all_opens, all_closes, all_dates = test.get_all_data(ticker='TSLA')

    print(all_volumes)
    data_dict = {
        'date-time': [datetime.datetime.fromtimestamp(t) for t in all_dates],
        'open': all_opens,
        'close': all_closes,
        'volume': all_volumes
    }

    df = pd.DataFrame(data_dict)

    df.to_csv('./TSLA_Minute_Dataset.csv')
  

    # time, volume, price = test.get_data(ticker='TSLA')
    # print(type(time))
    # print("Time:", time, "Volume:", volume, "Price:", price, sep="\n")
    #
    # print("Human readable Time:", test.get_time())


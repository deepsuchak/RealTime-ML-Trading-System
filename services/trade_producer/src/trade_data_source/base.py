from abc import ABC, abstractmethod
from typing import List

from src.trade_data_source.trade import Trade

class TradeSource(ABC):

    @abstractmethod
    def get_trades(self) -> List[Trade]:
        '''
        Retrieves the trades from whatever source you connect to
        '''
        pass

    @abstractmethod
    def is_done(self)->bool:
        '''
        Returns True if there are no more trades to read, otherwise False
        '''
        pass
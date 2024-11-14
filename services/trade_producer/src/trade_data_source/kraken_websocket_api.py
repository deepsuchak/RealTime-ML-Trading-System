from typing import List
from time import sleep
from websocket import create_connection
from loguru import logger
import json
from pydantic import BaseModel

# class Trade(BaseModel):
#     product_id: str
#     price: float
#     quantity: float
#     timestamp_ms: int

from src.trade_data_source.trade import Trade
from src.trade_data_source.base import TradeSource
class KrakenWebsocketAPI(TradeSource):
    URL = "wss://ws.kraken.com/v2"
    
    '''
    Class for reading realtime trades from Kraken Websocket API
    '''
    
    def __init__(self, product_id: str):
        '''
        Initialize the KrakenWebsocketAPI instance

        Args:
            product_id: Product id to filter the trades
        '''
        
        self.product_id = product_id

        ## establish connection with Kraken Websocket API
        self._ws = create_connection(self.URL)
        logger.info("Connected to Kraken Websocket API")

        self._subscribe(product_id=product_id)
    
    def _subscribe(self, product_id: str):
        '''
        Establish connection with Kraken Websocket API and subscribe to the trades for a given product_id

        Args:
            product_id: Product id to filter the trades
        '''

        logger.info(f"Subscribing to trades for {product_id}")
        msg = { 
            'method': 'subscribe',
            'params': {
                'channel': 'trade',
                'symbol': [product_id],
                'snapshot': False                
            }
        }

        self._ws.send(json.dumps(msg))

        logger.info("Subscription worked")


        ## the first 2 messages we get from kraken websocket API are not useful
        ## as they contain no trade data just confirmation that subscription worked

        for product_id in [product_id]:
            _ = self._ws.recv()
            _ = self._ws.recv()

    
    def get_trades(self) -> List[Trade]:
        '''
        Returns the latest batch of trades from Kraken Websocket API
        '''
        message = self._ws.recv()

        if 'heartbeat' in message:
            # When there are no trades, we get a heartbeat
            logger.info("Heartbeat received")
            return []  # Return an empty list instead of None

        # Parse the message JSON
        message = json.loads(message)
        
        trades = []
        for trade in message['data']:
            # Extract relevant trade data and create Trade objects
            ## so again in meesage['data'] we have multiple things like side,price,qty,timestamp etc
    #        ## we only want the price,qty,timestamp(in ms) and product_id
            trades.append(
                Trade(
                    product_id=trade['symbol'],
                    price=trade['price'],
                    quantity=trade['qty'],
                    timestamp_ms=self.to_ms(trade['timestamp'])
                     # timestamp=trade['timestamp'] ## this will error out becuase in the Pydantic setting above we've defined what datatypes should be in the timestamp
                )
            )

        return trades

        ## below is an example of how to return a list of dummy trades
        # event = [{

        #         "product_id": "ETH/USD",
        #         "price": 1000.0,
        #         "qty": 6423.46326,
        #         "timestamp_ms": 1622220000000
        #     }]
        # # Wait for 1 second before sending the next message 
                
        # sleep(1)
        
        # return trades


    def is_done(self)->bool:
        '''
        Returns True if there are no more trades to read
        '''
        False

    def to_ms(self, timestamp: str)->int:
        '''
        Converts a timestamp to milliseconds

        Args:
            timestamp: Timestamp to convert

        Returns:
            timestamp in milliseconds
        '''
        # parse a string like '2024-01-01T00:36:45.456789Z' to a datetime object
        # assuming utc timezone
        # then transform this datetime object into a unix timezone
        from datetime import datetime, timezone

        timestamp = datetime.fromisoformat(timestamp[:-1]).replace(tzinfo=timezone.utc)
        return int(timestamp.timestamp() * 1000)

    def is_done(self)->bool:
        '''
        Returns True if there are no more trades to read
        '''
        False

# from datetime import datetime, timezone
# from typing import List
# import json
# from websocket import create_connection

# from loguru import logger

# from pydantic import BaseModel

# class Trade(BaseModel):
#     product_id: str
#     quantity: float
#     price: float
#     timestamp_ms: int


from quixstreams import Application
from src.trade_data_source.kraken_websocket_api import KrakenWebsocketAPI
from loguru import logger
from typing import List
from src.trade_data_source.trade import Trade
from src.trade_data_source.base import TradeSource
def produce_trades(
        kafka_broker_address: str,
        kafka_topic: str,
        trade_data_source: TradeSource,
):
    '''
    Reads from a Kraken Websocket API endpoint and save them in a given Kafka topic

    Args:
        kafka_broker_address: Kafka broker address
        kafka_topic: Kafka topic to save the trades
        product_id: Product id to filter the trades

    Returns:
        None
    '''
    

    # Create an Application instance with Kafka config
    app = Application(broker_address=kafka_broker_address)

    # Define a topic "my_topic" with JSON serialization
    topic = app.topic(name=kafka_topic, value_serializer='json')

    # Create a KrakenWebsocketAPI instance
    
    # Create a Producer instance
    with app.get_producer() as producer:
        while True:
            
            trades: List[Trade] = trade_data_source.get_trades() # this will the trades which will be a list of dictionaries with a product_id key and a list of trades as value.
            
            for trade in trades:
            
                # Serialize an event using the defined Topic
                # transform it into a sequence of bytes
                message = topic.serialize(key=trade.product_id, value=trade.model_dump()) # the point of adding key here is to partition the data which helps to read the data from the kafka topic in parallel 
                
                # Produce a message into the Kafka topic
                producer.produce(topic=topic.name, value=message.value, key=message.key)

                logger.debug(f"Pushed trade to Kafka topic: {trade}")
            
                
if __name__ == "__main__":
    
    from src.config import config


    if config.live_or_historical == "live":
            
        from src.trade_data_source.kraken_websocket_api import KrakenWebsocketAPI
        kraken_api = KrakenWebsocketAPI(product_id=config.product_id)

    elif config.live_or_historical == "historical":

        from src.trade_data_source.kraken_rest_api import KrakenRestAPI
        kraken_api = KrakenRestAPI(product_id=config.product_id, last_n_days=config.last_n_days)

    else:
        raise ValueError(f"live_or_historical must be 'live' or 'historical', but got {config.live_or_historical}")    
    produce_trades(
        kafka_broker_address=config.kafka_broker_address,
        kafka_topic=config.kafka_topic,
        trade_data_source=kraken_api
    )
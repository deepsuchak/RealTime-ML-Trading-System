from datetime import timedelta
from loguru import logger
from quixstreams import Application


def transform_trade_to_ohlcv(
    kafka_broker_address: str,
    kafka_input_topic: str,
    kafka_output_topic: str,
    ohlcv_window_seconds: int,
    kafka_consumer_group: str
) -> None:
    """
    Reads trades from redpanda topic
    Aggregates them into OHLC candles using the window size in 'ohlc_window_seconds'
    Sends aggregated candles to output redpanda topic

    Args:
        kafka_broker_address(str): address of kafka broker
        kafak_input_topic(str): kafka topic to read trade data from
        kafak_output_topic(str): kafka topic to write aggregated candles to
        ohlc_window_seconds(int): window size in seconds for OHLC aggregation

    Returns:
        None
    """
    # to handle all low-level communication with redpanda
    app = Application(
        broker_address=kafka_broker_address,
        consumer_group=kafka_consumer_group,
        #   auto_offset_reset="earliest", # process all msgs from the input topic when this service started
        #   auto_create_reset='latest' # forget about past msgs, process only one which come from this moment
    )

    input_topic = app.topic(name=kafka_input_topic, value_serializer='json')
    output_topic = app.topic(name=kafka_output_topic, value_serializer='json')

    ## create a streaming dataframe as per quixstream's docs
    sdf = app.dataframe(input_topic)

    def init_ohlc_candle(trade: dict) -> dict:
        """
        Initializes OHLC candle
        """
        return {
            'open': trade['price'],
            'high': trade['price'],
            'low': trade['price'],
            'close': trade['price'],
            'volume': trade['quantity'],
            # 'product_id': trade['product_id'],
            # 'timestamp': trade['timestamp'],
        }

    def update_ohlcv_candle(candle: dict, trade: dict) -> dict:
        """
        Updates OHLC candle
        """
        candle['high'] = max(candle['high'], trade['price'])
        candle['low'] = min(candle['low'], trade['price'])
        candle['close'] = trade['price']
        candle['volume'] += trade['quantity']

        return candle

    sdf = sdf.tumbling_window(duration_ms=timedelta(seconds=ohlcv_window_seconds))
    sdf = sdf.reduce(reducer=update_ohlcv_candle, initializer=init_ohlc_candle
    ).final()  # current()
    
    ## apply transformations -- end

    sdf['open'] = sdf['value']['open']
    sdf['high'] = sdf['value']['high']
    sdf['low'] = sdf['value']['low']
    sdf['close'] = sdf['value']['close']
    sdf['volume'] = sdf['value']['volume']
    # sdf['product_id'] = sdf['value']['product_id']
    sdf['timestamp_ms'] = sdf['end']

    # keep only the columns we're interested in
    sdf = sdf[['timestamp_ms', 'open', 'high', 'low', 'close', 'volume']]

    # print the output to the console
    sdf.update(logger.debug)

    ## send aggregated candles to output redpanda topic
    sdf = sdf.to_topic(output_topic)

    # kickoff the streaming dataframe
    app.run(sdf)


if __name__ == '__main__':

    transform_trade_to_ohlcv(
        kafka_broker_address='localhost:19092',
        kafka_input_topic='trades',
        kafka_output_topic='ohlcv',
        ohlcv_window_seconds=10,
        kafka_consumer_group='consumer_group_trade_to_ohlcv'
    )


    
    
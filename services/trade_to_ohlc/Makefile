run-live-dev:
	KAFKA_INPUT_TOPIC=live_trades KAFKA_OUTPUT_TOPIC=ohlcv_live KAFKA_CONSUMER_GROUP=trade_to_ohlc_live_consumer_group poetry run python src/main.py

run-historical-dev:
	KAFKA_INPUT_TOPIC=historical_trades KAFKA_OUTPUT_TOPIC=ohlcv_historical KAFKA_CONSUMER_GROUP=trade_to_ohlc_historical_consumer_group poetry run python src/main.py

build:
	docker build -t trade_to_ohlc .

run-live: build
	docker run \
	 --network=redpanda_network \
	 --env KAFKA_BROKER_ADDRESS=redpanda:9092 \
	 --env KAFKA_INPUT_TOPIC=live_trades \
	 --env KAFKA_OUTPUT_TOPIC=ohlcv_live \
	 --env KAFKA_CONSUMER_GROUP=trade_to_ohlc_live_consumer_group \
	  trade_to_ohlc

run-historical: build
	docker run \
	 --network=redpanda_network \
	 --env KAFKA_BROKER_ADDRESS=redpanda:9092 \
	 --env KAFKA_INPUT_TOPIC=historical_trades \
	 --env KAFKA_OUTPUT_TOPIC=ohlcv_historical \
	 --env KAFKA_CONSUMER_GROUP=trade_to_ohlc_historical_consumer_group \
	  trade_to_ohlc
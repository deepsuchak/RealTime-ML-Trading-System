run-live-dev:
	KAFKA_INPUT_TOPIC=ohlcv_live KAFKA_CONSUMER_GROUP=consumer_group_ohlcv_live_to_feature_store poetry run python src/main.py

run-historical-dev:
	KAFKA_INPUT_TOPIC=ohlcv_historical KAFKA_CONSUMER_GROUP=consumer_group_ohlcv_historical_to_feature_store START_OFFLINE_MATERIALIZATION=True BATCH_SIZE=1000 poetry run python src/main.py

build:
	docker build -t topic_to_feature_store .

run-live: build
	docker run \
	 --network=redpanda_network \
	 --env KAFKA_BROKER_ADDRESS=redpanda:9092 \
	 --env KAFKA_INPUT_TOPIC=ohlcv_live \
	 --env KAFKA_CONSUMER_GROUP=consumer_group_ohlcv_live_to_feature_store \
	 --env BATCH_SIZE=1 \
 	  topic_to_feature_store

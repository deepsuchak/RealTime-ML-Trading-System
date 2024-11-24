run-live-dev:
	KAFKA_TOPIC=live_trades LIVE_OR_HISTORICAL=live poetry run python src/main.py 

run-historical-dev:
	LIVE_OR_HISTORICAL=historical KAFKA_TOPIC=historical_trades LAST_N_DAYS=30 poetry run python src/main.py 

build:
	docker build -t trade_producer .

run-live: build
	docker run \
	 --network=redpanda_network \
	 --env KAFKA_BROKER_ADDRESS=redpanda:9092 \
	  trade_producer
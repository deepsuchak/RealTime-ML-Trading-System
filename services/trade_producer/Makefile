run-live-dev:
	KAFKA_TOPIC=live_trades LIVE_OR_HISTORICAL=live poetry run python src/main.py 

run-historical-dev:
	KAFKA_TOPIC=historical_trades LIVE_OR_HISTORICAL=historical LAST_N_DAYS=30 poetry run python src/main.py 

build:
	docker build -t trade_producer .

run-live: build
	docker run \
	 --network=redpanda_network \
	 --env KAFKA_BROKER_ADDRESS=redpanda:9092 \
	  trade_producer

run-historical: build
	docker run \
	 --network=redpanda_network \
	 --env KAFKA_BROKER_ADDRESS=redpanda:9092 \
	 --env LAST_N_DAYS=30 \
	 --env KAFKA_TOPIC=historical_trades \
	 --env LIVE_OR_HISTORICAL=historical \
	  trade_producer
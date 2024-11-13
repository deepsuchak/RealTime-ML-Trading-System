run-dev:
	poetry run python src/main.py

build:
	docker build -t trade_to_ohlc .

run: build
	docker run \
	 --network=redpanda_network \
	 --env KAFKA_BROKER_ADDRESS=redpanda:9092 \
	  trade_to_ohlc
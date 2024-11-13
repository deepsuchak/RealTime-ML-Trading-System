from quixstreams import Application
from typing import List
from loguru import logger
import json
from src.config import config
from src.hopsworks_api import push_value_to_feature_store
def topic_to_feature_store(kafka_broker_address: str,
                            kafka_input_topic: str,
                            kafka_consumer_group: str,
                            feature_group_name: str,
                            feature_group_version: int,
                            feature_group_primary_key: List[str],
                            feature_group_event_time: str
                            ):
    '''
    Reads from a Kafka input topic and pushes them in a feature store
    
    Args:
        kafka_broker_address: Kafka broker address
        kafka_input_topic: Kafka topic to read the data from
        kafka_consumer_group: Kafka consumer group
        feature_group_name: Feature group name
        feature_group_version: Feature group version

    Returns:
        None
    '''

    # Create an Application instance with Kafka config
    app = Application(broker_address=kafka_broker_address,
                      consumer_group=kafka_consumer_group,)
    
    with app.get_consumer() as consumer:

        consumer.subscribe(topics=[kafka_input_topic])

        while True:
            msg = consumer.poll(0.1)

            if msg is None:
                continue
            elif msg.error():
                logger.error(msg.error())
                continue

            value = msg.value()
            value = json.loads(value.decode('utf-8'))
            
            push_value_to_feature_store(
                  value,
                  feature_group_name,
                  feature_group_version,
                  feature_group_primary_key,
                  feature_group_event_time              
            )            

if __name__ == "__main__":
   
    from src.config import config
    topic_to_feature_store(
    kafka_broker_address=config.kafka_broker_address,
    kafka_input_topic=config.kafka_input_topic,
    kafka_consumer_group=config.kafka_consumer_group,
    feature_group_name=config.feature_group_name,
    feature_group_version=config.feature_group_version ,
    feature_group_primary_key=config.feature_group_primary_keys,
    feature_group_event_time=config.feature_group_event_time  
   )


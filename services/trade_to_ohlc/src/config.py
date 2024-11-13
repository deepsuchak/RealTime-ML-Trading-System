from typing import Optional

from pydantic_settings import BaseSettings

class AppConfig(BaseSettings):

    kafka_broker_address: str
    kafka_input_topic: str
    kafka_output_topic: str
    kafka_consumer_group: str
    ohlcv_window_seconds: int
   
    # this is the first time I use this construct to load the environment variables from
    # an .env file
    # I used another method in the past, which Jason Singer found during the live session
    # Jason Singer
    # For those curious, an alternative way to set the env_file in the Config class would be to set the attribute via `model_config` instead of using an inner class.
    # ```
    # model_config = {'env_file': '.env'}
    # ```
    class Config:
        env_file = ".env"

config = AppConfig()
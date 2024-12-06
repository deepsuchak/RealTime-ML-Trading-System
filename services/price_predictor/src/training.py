from src.config import HopsworksConfig
from typing import Optional

from loguru import logger
def train_model(
    feature_view_name: str,
    feature_view_version: int,
    feature_group_name: str,
    feature_group_version: int,
    ohlc_window_sec: int,
    last_n_days: int,
    product_id: str,
    hopsworks_config: HopsworksConfig,
    forecast_steps: int,
    perc_test_data: Optional[float] = 0.3

):
    '''
    Reads feature from the feature store,
    Trains the predictive model and
    saves it to a model registry
    
    '''
    # Read data from the feature store
    from src.ohlc_data_reader import OhlcDataReader

    ohlc_data_reader = OhlcDataReader(
        feature_view_name=feature_view_name,
        feature_view_version=feature_view_version,
        feature_group_name=feature_group_name,
        feature_group_version=feature_group_version,
        ohlc_window_sec=ohlc_window_sec,
        hopsworks_config=hopsworks_config
    )

    # the data gathered here is already sorted
    ohlc_data = ohlc_data_reader.read_from_offline_store(
        last_n_days=last_n_days,
        product_id=product_id,
    )
    logger.debug(f'Reading {len(ohlc_data)} rows from the offline feature store')

    # split the data into train and test sets
    test_size = int(len(ohlc_data) * perc_test_data)
    train_df = ohlc_data[:-test_size]
    test_df = ohlc_data[-test_size:]
    logger.debug(f'Training data: {len(train_df)} rows')
    logger.debug(f'Test data: {len(test_df)} rows')

    # add a column with the target variable for the model to predict
    train_df['target_price'] = train_df['close'].shift(-forecast_steps)
    test_df['target_price'] = test_df['close'].shift(-forecast_steps)
    logger.debug(f'Added target variable to training and testing data')
    
    # drop rows with missing values
    train_df = train_df.dropna()
    test_df = test_df.dropna()
    logger.debug(f'Dropped rows with missing values from training and testing data')
    logger.debug(f'Training data: {len(train_df)} rows')
    logger.debug(f'Test data: {len(test_df)} rows')

    # split the data into features and target
    X_train = train_df.drop('target_price', axis=1)
    y_train = train_df['target_price']

    X_test = test_df.drop('target_price', axis=1)
    y_test = test_df['target_price']

    logger.debug(f'Splitting training and testing data')

    # log dimensions of feature and target data
    logger.debug(f'X_train shape: {X_train.shape}')
    logger.debug(f'y_train shape: {y_train.shape}')
    logger.debug(f'X_test shape: {X_test.shape}')
    logger.debug(f'y_test shape: {y_test.shape}')
    
    # build a model
    from src.models.current_price_baseline import CurrentPriceBaseline

    model = CurrentPriceBaseline()
    model.fit(X_train, y_train)
    logger.debug(f'Fitted model')

    # evaluate the model
    y_pred = model.predict(X_test)

    from sklearn.metrics import mean_absolute_error

    mae = mean_absolute_error(y_test, y_pred)
    logger.debug(f'MAE (mean absolute error): {mae}')
    # save the model to the model registry
if __name__ == "__main__":

    from src.config import config, hopsworks_config
    train_model(
        feature_view_name=config.feature_view_name,
        feature_view_version=config.feature_view_version,
        feature_group_name=config.feature_group_name,
        feature_group_version=config.feature_group_version,
        ohlc_window_sec=config.ohlc_window_sec,
        product_id=config.product_id,
        last_n_days=config.last_n_days,
        hopsworks_config=hopsworks_config,
        forecast_steps=config.forecast_steps

    )
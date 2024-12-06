import pandas as pd


class CurrentPriceBaseline:
    def __init__(self):
        pass
    
    def fit(self, X: pd.DataFrame, y: pd.Series):
        pass
    def predict(self, X: pd.DataFrame) -> pd.Series:
        '''
        Predicts the next price based on the current price
        '''
        return X['close']
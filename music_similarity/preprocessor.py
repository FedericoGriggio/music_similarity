# Data Manipulation
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)
from sklearn.utils import shuffle

# Pipeline and Column Transformers
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn import set_config
set_config(display = "diagram")

# Scaling
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler

# Package classes
from music_similarity.search_engine import SearchEngine

class Preprocessor():
    def __init__(self, se):
        '''
        Preprocessor class
        Input: a songs dataset extracted from spotify API
        '''
        self.se = se

    def scale_data(self):
        '''
        Adapting data function
        '''
        # drop non numerical features before scaling
        self.X=self.se.data.drop(columns=['name','artists', 'uri'])
        self.X_target=self.se.target.drop(columns=['name','artists', 'uri'])
        # fit and transofrm with MinMaxScaler
        mmscaler = MinMaxScaler().fit(self.X)
        self.X_mmscaled=mmscaler.transform(self.X)
        self.X_target_mmscaled=mmscaler.transform(self.X_target)
        # fit and transofrm with RobustScaler
        roscaler = RobustScaler().fit(self.X)
        self.X_roscaled=roscaler.transform(self.X)
        self.X_target_roscaled=roscaler.transform(self.X_target)

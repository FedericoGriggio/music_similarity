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
from music_similarity.api_extractor import ApiExtractor

class Preprocessor():
    def __init__(self, se, ae):
        '''
        Preprocessor class
        Input: a songs dataset extracted from spotify API
        '''
        # Search Engine
        self.se = se
        # Api Extractor
        self.ae = ae

    def scale_se(self):
        '''
        Adapting data with target song present in the local dataset
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

    def scale_ae(self):
        '''
        Adapting data with target song present in the local dataset
        '''
        # drop non numerical features before scaling
        self.X=self.se.data.drop(columns=['name','artists', 'uri'])
        self.X_target=self.ae.df_tfa.drop(columns=['name','artists', 'uri'])
        # fit and transofrm with MinMaxScaler
        mmscaler = MinMaxScaler().fit(self.X)
        self.X_mmscaled=mmscaler.transform(self.X)
        self.X_target_mmscaled=mmscaler.transform(self.X_target)
        # fit and transofrm with RobustScaler
        roscaler = RobustScaler().fit(self.X)
        self.X_roscaled=roscaler.transform(self.X)
        self.X_target_roscaled=roscaler.transform(self.X_target)

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
from sklearn.preprocessing import RobustScaler, StandardScaler, MinMaxScaler, OneHotEncoder

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
        # Categorical columns
        self.categorical_features = ['key']
        # Numerical columns
        self.numeric_features = ['acousticness', 'energy',
                                 'instrumentalness',
                                 'liveness',
                                 'valence', 'tempo', 'sp1',
                                 'sp2', 'sp3', 'sp4', 'sp5',
                                 'sp6', 'sp7', 'sp8', 'sp9',
                                 'sp10', 'sp11', 'sp12', 'tm1',
                                 'tm2', 'tm3', 'tm4', 'tm5',
                                 'tm6', 'tm7', 'tm8', 'tm9',
                                 'tm10', 'tm11', 'tm12', 'mode']
        self.string_features = ['name', 'artists']
        # Categorical transformer
        self.categorical_transformer = Pipeline(steps=[(
            'onehot', OneHotEncoder(handle_unknown='ignore'))])
        # Numerical transformer
        self.numeric_transformer = Pipeline(steps=[(
            'scaler', MinMaxScaler())])
        # String transformer
        # self.string_transformer = Pipeline(steps=[(
        #     'pass', 'passthrough')])
        # Transformer
        self.transformer = ColumnTransformer(
            transformers=[
                ('minmax', self.numeric_transformer, self.numeric_features),
                ('cat', self.categorical_transformer, self.categorical_features)])

    def scale_se(self):
        '''
        Adapting data with target song present in the local dataset
        '''
        # Fit and transform data and target
        self.X_mmscaled = self.transformer.fit_transform(self.se.data)
        # Only apply a transformation to the target
        self.X_target_mmscaled = self.transformer.transform(self.se.target)
        # Transform np.array to dataset
        self.X_mmscaled = pd.DataFrame(self.X_mmscaled,
                        columns=self.transformer.get_feature_names_out())
        self.X_target_mmscaled = pd.DataFrame(self.X_target_mmscaled,
                        columns=self.transformer.get_feature_names_out())

    def scale_ae(self):
        '''
        Adapting data with target song present in Spotify database
        '''
        # Fit and transform data and target
        self.X_mmscaled = self.transformer.fit_transform(self.se.data)
        self.X_target_mmscaled = self.transformer.transform(self.ae.df_tfa)
        # Transform np.array to dataset
        self.X_mmscaled = pd.DataFrame(self.X_mmscaled,
                        columns=self.transformer.get_feature_names_out())
        self.X_target_mmscaled = pd.DataFrame(self.X_target_mmscaled,
                        columns=self.transformer.get_feature_names_out())

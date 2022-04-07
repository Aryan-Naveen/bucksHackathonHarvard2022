import pandas as pd
from sklearn import tree
import numpy as np

feature_cols = ['startGameClock', 'shotClock', 'distance', 'dribblesBefore', 'assistOpp', 'complexShotType', 'closestDefDist', 'rearViewContest', 'shotAngle', 'shooterSpeed', 'shooterVelAngle']
class LeagueWideShotPredictModel():
    def __init__(self, df1, df2):
        self.X1 = df1.loc[:, feature_cols]
        self.Y1 = df1['fg3']
        self.X2 = df2.loc[:, feature_cols]
        self.Y2 = df2['fg3']

        self.clf1 = tree.DecisionTreeClassifier()
        self.clf2 = tree.DecisionTreeClassifier()
    
    def train_model(self):
        self.clf1 = self.clf1.fit(self.X1, self.Y1)
        self.clf2 = self.clf2.fit(self.X2, self.Y2)
    
    def getPredicitons(self):
        return np.concatenate((self.clf2.predict(self.X1), self.clf1.predict(self.X2)), axis = None)
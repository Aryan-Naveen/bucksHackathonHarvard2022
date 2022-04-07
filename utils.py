import pandas as pd
import numpy as np

class Results():
    def __init__(self, dataset):
        self.dataset = dataset
        self.df = pd.DataFrame()
        self.df['playerName'] = []
        self.df['predictedFg%'] = []
        self.df['numTrials'] = []
        self.THRESHOLD = 200
    
    def addTrial(self, playerName, fg):
        if playerName in self.df['playerName']:
            self.df.loc[df['playerName'] == playerName,['numTrials']] += 1
            num_trials = df.loc[df['playerName'] == playerName,['numTrials']]
            cur = df.loc[df['playerName'] == playerName,['predictedFg%']]

            self.df.loc[df['playerName'] == playerName,['predictedFg%']] = ((num_trials - 1)*cur + fg)/num_trials
        
        else:
            self.df = self.df.append({'playerName': playerName, 'predictedFg%': fg, 'numTrials': 1}, ignore_index = True)
    
    def updateResults(self, prediction):
        if "Prediction" in self.dataset:
            self.dataset["Prediction"] = prediction
        else:
            self.dataset.insert(4, "Prediction", prediction)

        players = self.dataset.player.unique()
        for player in players:
            playerData = self.dataset[self.dataset['player'] == player]
            totalShotAttempts = len(playerData)
            if totalShotAttempts > self.THRESHOLD:
                self.addTrial(player, np.mean(playerData['Prediction']))
    
    def computeMetric(self, shotAttempts, actualFg, predictedFg, normalizedFg):
        difficultMetric = (actualFg - predictedFg)/predictedFg
        return np.arcsinh(shotAttempts)*(difficultMetric)*normalizedFg

    def getDataFrame(self):
        players = self.df.playerName.unique()
        actualFgPercent = []
        shotAttempts = []
        metric = []
        for player in players:
            playerDataFg = self.dataset[self.dataset['player'] == player]
            playerData = self.df[self.df['playerName'] == player]
        
            actualFgPercent.append(np.mean(playerDataFg['fg3']))
            shotAttempts.append(len(playerData))
        
        self.df.insert(1, "ActualFgPercent", actualFgPercent)
        self.df.insert(2, "ShotAttempts", shotAttempts)
        normalized = self.df["ActualFgPercent"]/self.df["ActualFgPercent"].abs().max()

        metric = []
        for i, player in enumerate(players):
            playerData = self.df[self.df['playerName'] == player]
            shotAttempts = playerData["ShotAttempts"]
            actualFg = playerData["ActualFgPercent"]
            predictedFg = playerData["predictedFg%"]
            normalizedActual = normalized[i]
            metric.append(self.computeMetric(shotAttempts, actualFg, predictedFg, normalizedActual))

        self.df.insert(3, "Metrics", metric)
        # print(self.df)
        return self.df.sort_values(by = ['ActualFgPercent'], ascending=False)
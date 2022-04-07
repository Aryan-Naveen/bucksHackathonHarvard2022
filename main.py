import pandas as pd
import numpy as np
import time
from model import LeagueWideShotPredictModel
from utils import Results
from tqdm import tqdm


dataset = pd.read_csv(r'hackathon_basketball_distribution.csv')

ignoredShots = ['heave', 'drivingFloater', 'cutFloater', 'tip', 'lob', 'cutLayup', 'standstillLayup', 'postLeft', 'drivingLayup']
for shot in ignoredShots:
    dataset.drop(dataset.index[dataset['complexShotType'] == shot], inplace=True)

shotTypes = dataset.complexShotType.unique()

shotIds = [i for i in range(len(shotTypes))]

dataset['complexShotType'].replace(shotTypes, shotIds, inplace=True)

results = Results(dataset)


num_trials = 1


for trial in tqdm(range(num_trials)):
    df1 = dataset.sample(frac=0.5, random_state=int(time.time()))
    df2 = dataset.drop(df1.index)
    model = LeagueWideShotPredictModel(df1, df2)
    model.train_model()
    prediction = model.getPredicitons()
    results.updateResults(prediction)    
    
print(results.getDataFrame().to_string())



import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from math import sqrt
from tqdm import tqdm_notebook as tqdm

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error


def eval(true, pred, metric, mean = True):
    '''
    For arrays TRUE and PRED, calculates METRIC and returns 
    the result as a single value
    '''
    
    # Use a mask to remove any nan or inf values
    mask = ( (true.isna()==False) & (pred.isna()==False) )
    true = true[mask]
    pred = pred[mask]
    
    # Confirm that there is at least one value for the calculation
    if len(true)>0:
        
        if metric=="pred_acc":
            val = pred/true
            val = val.replace([np.inf, -np.inf], np.nan)

        elif metric=="mape":
            val =  np.abs((pred - true)/true)*100
            val = val.replace([np.inf, -np.inf], np.nan)

        elif metric=="mae":
            val =  np.abs(pred-true) #mean_absolute_error(true,pred)

        elif metric=="mse":
            val =  (pred-true)**2 #mean_squared_error(true,pred)

        elif metric=="rmse":
            val =  np.array(sqrt(mean_squared_error(true,pred)))
        
        elif metric=="r2":
            val =  r2_score(true,pred)
            
        elif metric=="pcc":
            #return pred,true
            val =  pred/true
            val = val.replace([np.inf, -np.inf], np.nan)
        
        '''
        elif metric=="sign_acc":
            # NEED TO REVISIT ->  THIS IS IN RELATION TO PREVIOUS MONTH
            true_pos = [true>=0]
            pred_pos = [pred>=0]
            
            val = (true_pos==pred_pos).mean()
        '''
        if mean == True:
            return val.mean()
        else:
            return val
    else:
        return np.nan
    
    
def make_train_test(df, datecol, split_date):
    '''
    Takes a dataframe and splits it into a train and test set
    '''
    
    dates = df.index.get_level_values(datecol).unique().tolist()
    train_dates = [i for i in dates if i<=pd.to_datetime(split_date)]
    test_dates  = [i for i in dates if i>pd.to_datetime(split_date)]

    train_df  = df.loc[train_dates]
    test_df  = df.loc[test_dates]
    
    return train_df, test_df


def make_results(fpath, split_date):
    '''
    Produces a dataframe of results
    '''
    master=pd.read_csv(f"ml/output_data/master_{fpath}.csv", 
                       parse_dates=['date'], 
                       index_col=['date', 'region'])

    master.drop(columns=['dataset','ml_dataset',
                         #'ml_true', 'eur_true', 
                         #'internal_true', 'external_true', 'h2o_true'
                        ], inplace=True)
    
    # Remove periods for which any model is missing, 
    # so that all models are evaluated on the same set of months
    master.dropna(how='any', inplace=True)
    
    train_df, test_df = make_train_test(master, 'date', split_date)
    
    models = [i for i in train_df.columns.tolist() if i!='true']
    metrics = ['pred_acc', 'mape', 'mae', 
               'mse', 'rmse', 'r2', 'pcc']

    results = pd.DataFrame(columns=[fpath],
                          index=pd.MultiIndex.from_arrays([
                              sorted(models*len(metrics)*2),
                              sorted(metrics*2)*len(models),
                              ['train', 'test']*len(models)*len(metrics)
                          ]))
    
    results.index.names=['model', 'metric', 'dataset']

    for m in tqdm(models):
        for metric in metrics:
            results.loc[(m, metric, 'train')] = eval(train_df['true'], 
                                                     train_df[m], 
                                                     metric)
            results.loc[(m, metric, 'test')]  = eval(test_df['true'], 
                                                     test_df[m], 
                                                     metric)

    return results


def plot_results(results, metric='mape',ylim=[1,1000], lb=0.5, ub=2, logy=True):
    '''
    Plots results by region, where each row in the plot is a different model
    '''
    
    fig, ax = plt.subplots(1, 1, figsize=[15,5], sharex=True)

    (results.unstack(level=0).loc[metric].T[['train', 'test']]
           .plot(kind='bar', width=0.9, ax=ax, 
                 logy=logy, ylim=ylim, alpha=0.5, 
                 color=['green', 'blue']))
    
    ax.axhline(lb,  color='black', alpha=0.5)
    ax.axhline(ub,  color='black', alpha=0.5)

    

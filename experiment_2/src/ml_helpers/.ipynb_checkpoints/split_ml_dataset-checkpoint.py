import pandas as pd
import numpy as np

from sklearn.impute          import SimpleImputer, MissingIndicator
from sklearn.preprocessing   import StandardScaler, MinMaxScaler, PolynomialFeatures
from sklearn.pipeline        import Pipeline, make_pipeline, make_union


def split_ml_dataset(learn_df, split_date):

    learn_df.sort_index(level='date', inplace=True)

    # Divide features and target
    y = learn_df['arrivals']    
    X = learn_df[[i for i in learn_df.columns 
                  if i!="arrivals"]].astype(float)

    # Fill missing values 
    # - First, move historical values forward
    # - Then, put in zeroes where this was not possible
    X.ffill(inplace=True)
    X.fillna(0, inplace=True)

    # Split the train/test set sequentially
    months = sorted(learn_df.index.get_level_values('date').unique().tolist())
    n = months.index(pd.to_datetime(split_date)) + 1

    y_train, y_test = y.loc[months[:n]], y.loc[months[n:]]
    X_train, X_test = X.loc[months[:n]], X.loc[months[n:]]

    print ("Training months:\n", [str(i)[:7] for i in months[:n]], "\n")
    print ("Testing months:\n",  [str(i)[:7] for i in months[n:]])

    y_train = np.array(y_train)
    y_test = np.array(y_test)


    pp_pipeline = make_pipeline(
                    #make_union(
                    #    SimpleImputer(missing_values=np.nan, strategy='mean'), #, add_indicator=True),
                        #MissingIndicator(missing_values=np.nan)
                    #),
                    #PolynomialFeatures(2),
                    MinMaxScaler() # https://scikit-learn.org/stable/auto_examples/preprocessing/plot_all_scaling.html
    )


    X_train_scaled = pp_pipeline.fit_transform(X_train)
    X_test_scaled  = pp_pipeline.transform(X_test)

    return X_train_scaled, y_train, X_test_scaled, y_test, X,y
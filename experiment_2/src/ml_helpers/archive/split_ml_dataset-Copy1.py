import pandas as pd
import numpy as np

from sklearn.impute          import SimpleImputer, MissingIndicator
from sklearn.preprocessing   import StandardScaler, MinMaxScaler, PolynomialFeatures
from sklearn.pipeline        import Pipeline, make_pipeline, make_union


def split_ml_dataset(learn_df, split_date, y_col, X_cols):
    
    # Split the train/test set sequentially
    months = sorted(learn_df.index.get_level_values('date').unique().tolist())
    n = months.index(pd.to_datetime(split_date)) + 1
    
    
    train_months = months[:n]
    test_months = months[n:]
    
    print ("Total months:", len(months))
    print ("Training months:\n", [str(i)[:7] for i in trai], "\n")
    print ("Testing months:\n",  [str(i)[:7] for i in months[n:]])
    
    # Divide features and target
    y = learn_df[y_col]    
    X = learn_df[X_cols].astype(float) 
    
    
    # Now, drop missing values for the purposes of learning
    learn_df.dropna(subset=[y_col], inplace=True)
    
    y_nomissing = learn_df[y_col]      
    X_nomissing = learn_df[X_cols].astype(float) 
    
    y_train, y_test = y_nomissing.loc[months[:n]], y_nomissing.loc[months[n:]]
    X_train, X_test = X_nomissing.loc[months[:n]], X_nomissing.loc[months[n:]]
    

    y_train = np.array(y_train)
    y_test  = np.array(y_test)

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

import pandas as pd
import numpy as np

def fit_only(X_train_scaled, y_train, 
             X_test_scaled, y_test, 
             X, y, 
             m, mname, fpath, tscv):
    
    # Fit model
    m.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_train_pred  = m.predict(X_train_scaled)
    y_test_pred   = m.predict(X_test_scaled)
    
    # Save the results
    res = {'train': {'true':      y_train,
                    'predicted':  y_train_pred
                    },
          'test':   {'true':      y_test,
                     'predicted': y_test_pred
                    }}
    
    # Store the results as a dataframe
    res_test  = pd.DataFrame(res['test'])
    res_train = pd.DataFrame(res['train'])
    
    res_test ['dataset'] = 'test'
    res_train['dataset'] = 'train'

    res_final = res_train.append(res_test)
    res_final.index = y.index
    res_final.to_csv(f"ml/output_data/{fpath}/results_{mname}.csv")
    
    
    # Save the coefficients  
    try:
        coefs = pd.DataFrame(m.best_estimator_.coef_, X.columns)
        coefs.columns = ["coef"]
        coefs.to_csv(f"ml/explainability/{fpath}/coefwts_{mname}.csv")
    except:  
        
        # --- If we are not doing grid search
        try:
            coefs = pd.DataFrame(m.coef_, X.columns)
            coefs.columns = ["coef"]
            coefs.to_csv(f"ml/explainability/{fpath}/coefwts_{mname}.csv")
        except:
            pass

    
    # Save the importance weights    
    try:
        coefs = pd.DataFrame(m.best_estimator_.feature_importances_, X.columns)
        coefs.columns = ["coef"]
        coefs.to_csv(f"ml/explainability/{fpath}/coefwts_{mname}.csv")
    except:
        
        # --- If we are not doing grid search
        try:
            coefs = pd.DataFrame(m.feature_importances_, X.columns)
            coefs.columns = ["coef"]
            coefs.to_csv(f"ml/explainability/{fpath}/impwts_{mname}.csv")
        except:
            pass
    

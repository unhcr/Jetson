from sklearn.externals import joblib
import pandas as pd
import numpy as np
from dateutil.relativedelta import *

def fit_ml_models(X_train_scaled, y_train, 
             X_scaled, 
             X, y, 
             train_months, test_months,
             m, mname, fpath):
    
    # Fit model
    m.fit(X_train_scaled, y_train)
    
    # Save model and cross-validation
    joblib.dump(m.best_estimator_, open(f"ml/models/{fpath}/{mname}.pkl", 'wb'))
    pd.DataFrame(m.cv_results_).to_csv(f"ml/results/{fpath}/cv_search_{mname}.csv")

    # Make predictions
    y_pred  = m.predict(X_scaled)
    
    # Save the results
    res = {'true':      y,
           'predicted': y_pred}
    
    # Store the results as a dataframe
    res  = pd.DataFrame(res, index=y.index)
    
    res['dataset'] = np.where(res.index.get_level_values('date').isin(train_months), "train", "") 
    res['dataset'] = np.where(res.index.get_level_values('date').isin(test_months),  "test", res['dataset']) 
    res.to_csv(f"ml/output_data/{fpath}/results_{mname}.csv")
    
    
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
        coefs.to_csv(f"ml/explainability/{fpath}/impwts_{mname}.csv")
    except:
        
        # --- If we are not doing grid search
        try:
            coefs = pd.DataFrame(m.feature_importances_, X.columns)
            coefs.columns = ["coef"]
            coefs.to_csv(f"ml/explainability/{fpath}/impwts_{mname}.csv")
        except:
            pass
    

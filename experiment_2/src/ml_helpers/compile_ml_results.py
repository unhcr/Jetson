import os
import pandas as pd

def compile_ml_results(fpath):
    
    ####################
    # Collect output files
    results_files = [i.replace(".csv", "").replace("results_", "") 
                     for i in os.listdir(f"ml/output_data/{fpath}")
                     if "results_" in i and 'baseline' not in i and 'compiled' not in i]

    first = True

    for f in results_files:
        if first == True:
            df = pd.read_csv(f"ml/output_data/{fpath}/results_{f}.csv", 
                             parse_dates=['date'], 
                             index_col=['region', 'date'])
            df.columns = [i + "_" + f for i in df.columns]
            first=False
        else:
            merge_df = pd.read_csv(f"ml/output_data/{fpath}/results_{f}.csv", 
                                   parse_dates=['date'], 
                                   index_col=['region', 'date'])
            merge_df.columns = [i + "_" + f for i in merge_df.columns]

            df = df.merge(merge_df, 
                          left_index=True, 
                          right_index=True, how='outer')


    ####################
    # Now, check that all models are using the same data
    # Same true values
    # Same dataset

    # List all "true" and "dataset" columns
    true_cols    = [i for i in df.columns if "true_" in i ]
    dataset_cols = [i for i in df.columns if "dataset_" in i ]
    pred_cols = [i for i in df.columns if "predicted_" in i]

    # Assert all true columns are the same
    for i in true_cols[1:]:
        try:
            assert ((df[i] == df[true_cols[0]]) | (df[i].isna() | df[true_cols[0]].isna())).all()
        except:
            print(df[
                (df[i] != df[true_cols[0]]) & (~df[i].isna() & ~df[true_cols[0]].isna())
            ][[i, true_cols[0]]].head())
        df.drop(i, axis=1, inplace=True)  

    # Assert all dataset columns are the same
    for i in dataset_cols[1:]:
        #try:
        assert ((df[i] == df[dataset_cols[0]]) | (df[i].isna() | df[dataset_cols[0]].isna()) ).all()
        #except:
        #    print(df[df[i] != df[dataset_cols[0]]][[i, dataset_cols[0]]].head())
            
        df.drop(i, axis=1, inplace=True)


    # If that worked, then we should rename 
    # so there is only one "true" column and one "dataset" column
    df.rename(columns = {true_cols[0]: 'ml_true',
                         dataset_cols[0]: "ml_dataset"}, inplace=True)

    df.set_index("ml_dataset", append=True, inplace=True)

    '''
    # Get mean predictions
    pred_cols = [i for i in df.columns if "predicted_" in i]
    df['predicted_logmean'] = df[pred_cols].mean(axis=1)

    # Reverse log transform
    df = np.exp(df) - 1

    # Get mean predictions
    df['predicted_mean'] = df[pred_cols].mean(axis=1)
    '''

    #df[pred_cols].astype(int)

    df.to_csv(f"ml/output_data/{fpath}/results_ml_compiled.csv")
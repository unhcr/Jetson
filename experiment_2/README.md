# jetson_v1.1


File structure:

| File | Description |
|---|---|
| `jetson_configs.py` | Configurations for the whole machine learning pipeline. |
| `pipeline_1a_collect_data.ipynb`| Pulls data in from raw data sources, restructures, cleans |
| `pipeline_2a_compile_data.ipynb`| Compile three datasets: the region-specific datasets initially fed into Eureqa, a single dataset representing all regions, and a single dataset representing all pairwise flows. |
| `pipeline_2b_build_ml_dataset.ipynb`| Prepares the training data - adds lagged variables, one-hot encodes missing values, and gets dummies. |
| `pipeline_2c_explore_arrivals.ipynb`| EDA on arrivals data |
| `pipeline_2d_explore_flows.ipynb`| EDA on flows data |
| `pipeline_3a_fit_baseline_models.ipynb`| Fits naive models with 4 strategies: LOCF, HM, expanding mean, and exponential weighted mean. |
| `pipeline_3b_fit_ml_models.ipynb`| Tries standard regression techniques: linear, ridge, lasso, boosting, xgboost, adaboost, decision tree, random forest, SVM, perceptron. |
| `pipeline_3c_fit_rnn_models.ipynb`|  Fits deep learning forecasting models on the time series. |
| `pipeline_4_compile_all_results.ipynb`|  Gathers results of all approaches together. |
| `pipeline_5a_score_results.ipynb`| Scores the predictions of the models. |
| `pipeline_5c_explain.ipynb`| Applies explainability techniques to the ML models. |
| `pipeline_5d_explore_crossval.ipynb`| Explores the results of the crossvalidation performed on the ML models. |


Baselines:

| File | Description |
|---|---|
| LOCF1 | Previous period's reading |
| LOCF3 | Three periods prior's reading |
| HM1 | Mean in the past 12 months -- as of previous period |
| HM3 | Mean in the past 12 months -- as of three periods prior |
| EM1| Expanding mean with minimum periods 1 -- as of previous period |
| EM3| Expanding mean with minimum periods 1 -- as of three periods prior |
| EWM1 | Exponentially weighted mean with a 12-month span -- as of previous period  |
| EWM3 | Exponentially weighted mean with a 12-month span -- as of three periods prior |



The results of each model are produced in a table with the following format:

| date | region | model1 | model2 | ... |
|---|---|---|---|---|
2010-01-01 | Awdal | ... | ... | ...
















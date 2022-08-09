# Overview 
This repository contains the code from Experiment #2 of the Jetson project, adapted for sharing with the general public.
This experiment was described in the following [paper](https://arxiv.org/pdf/2201.08006.pdf): 

> Hoffmann Pham, Katherine and Miguel Luengo-Oroz. 2022. "Predictive modelling of movements of refugees and internally displaced people: towards a computational framework." Forthcoming in the _Journal of Ethnic Migration Studes_.

We have continued to adapt and improve the code since the manuscript was submitted. To see the version of the code used to produce the results in the paper, please see the following branch of this repository: https://github.com/unhcr/Jetson/tree/JEMS_replication/experiment_2


## File structure

| File | Description |
|---|---|
| `jetson_configs.py` | Configurations for the whole machine learning pipeline. We include a sample template above. |
| `pipeline_0_make_postgresql.ipynb`| Makes a PostGRES database for storing the datasets. |
| `pipeline_1a_collect_data.ipynb`| Downloads individual datasets from raw data sources; cleans, compiles, and plots the results |
| `pipeline_2a_compile_data.ipynb`| Compiles the data at the admin1 and admin2 levels, including the creation of an admin1 dataset with only public-facing data (no private PRMN). |
| `pipeline_2b_build_ml_dataset.ipynb`| Prepares and plots the training data - adds lagged variables, one-hot encodes missing values, and gets dummies. |
| `pipeline_2c_explore_arrivals.ipynb`| EDA on arrivals data |
| `pipeline_2d_explore_flows.ipynb`| EDA on flows data |
| `pipeline_3a_fit_baseline_models.ipynb`| Fits naive models with 4 strategies: LOCF, HM, EM, EWM. |
| `pipeline_3b_fit_ml_models.ipynb`| Tries standard regression techniques: ridge, lasso, xgboost, adaboost, decision tree, random forest, SVM, perceptron. |
| `pipeline_3c_fit_rnn_models.ipynb`|  Fits deep learning forecasting models on the time series. |
| `pipeline_4_compile_all_results.ipynb`|  Gathers results of all approaches together. |
| `pipeline_5a_score_results.ipynb`| Scores the predictions of the models. |
| `pipeline_5c_explain.ipynb`| Applies explainability techniques to the ML models. |
| `pipeline_5d_explore_crossval.ipynb`| Explores the results of the crossvalidation performed on the ML models. |


### Baselines:

| File | Description |
|---|---|
| LOCF |  Last observation carried forward |
| HM | Historical mean |
| EM| Expanding mean |
| EWM | Exponentially weighted mean |



The results of each model are produced in a table with the following format:

| date | region | model1 | model2 | ... |
|---|---|---|---|---|
2010-01-01 | Awdal | ... | ... | ...
















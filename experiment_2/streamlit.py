import streamlit as st
import numpy as np
import pandas as pd
import geopandas as gp
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

from src.compile_data.compile_acled import *

split_date = '2018-08-01'
fpath = "admin1_lag1"


##############################
# Get the data in

@st.cache
def get_map():
    ''' The importance weights of a model '''
    somalia = gp.read_file("data/raw/gis/somalia_boundaries_admin1")
    return somalia

somalia = get_map()

@st.cache
def get_compiled_data():
    ''' The dataset used to prepare ml datasets '''
    return pd.read_csv(f"data/compiled/master_admin1.csv",
                      parse_dates=['date'],
                      index_col = ['date', 'region'])

compiled = get_compiled_data()

@st.cache
def get_master():
    ''' Predictions produced by the ML models '''
    return pd.read_csv(f"ml/output_data/master_{fpath}.csv", 
                       parse_dates=['date'], 
                       index_col=['date', 'region'])

master = get_master()


@st.cache
def get_scores():
    ''' The scores of the models '''
    return pd.read_csv(f"ml/results/scored_models.csv", 
                       index_col=['model', 'metric', 'dataset'])
scores = get_scores()

@st.cache
def get_coefwts(model):
    ''' The importance weights of a model '''
    coefwts = pd.read_csv(f"ml/explainability/admin1_lag1/coefwts_{model}.csv")
    coefwts.columns=['varname', 'Randomforest']
    coefwts.set_index(['varname'], inplace=True)
    return coefwts

@st.cache
def get_acled():
    acled_df = collect_acled()
    acled_df['log_fatalities'] = np.log(1+acled_df['fatalities'])
    return acled_df

acled = get_acled()


##############################
# Define the plots

# Time trends of input variables
def plot_model_inputs(df, indicator, regions, logy):
    fig, ax = plt.subplots(1,1, figsize=[10,5])
    plot_df = df[indicator].unstack(level='region')

    plot_df[regions].plot(kind='line', ax=ax, logy=logy, alpha=0.75)
    plot_df.mean(axis=1).plot(kind='line', ax=ax, color="black", linewidth=3, label="mean (all regions)")

    ax.set_title(indicator, fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    st.pyplot()
    
# Time trends of model predictions
def plot_model_predictions(df, models, region, logy, split_date = split_date):
    fig, ax = plt.subplots(1,1, figsize=[10,5])
    plot_df = df.xs(region, level='region')

    plot_df[models].plot(ax=ax, logy=logy, legend=True)
    plot_df['true'].plot(ax=ax, color='black', linewidth=3, label="True")

    ax.axvline(split_date, color='black')
    ax.text(split_date,5,'train-test split',rotation=90)
    ax.set_title(region, fontsize=14)
    ax.set_xlabel("")
    ax.set_ylabel("Arrivals")
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()

    st.pyplot()

# Bar plot of model scores
def plot_model_scores(df, models, metric, all_regions):
    fig, ax = plt.subplots(1,1, figsize=[10,5])
    plot_df = df.loc[models].xs(metric, level='metric').round(0)
    plot_df = plot_df.unstack(level='dataset').sort_values(('admin1_lag1', 'test'))
    plot_df.columns.set_names(['Dataset', "Subset"], inplace=True)

    if all_regions==False:
        plot_df = plot_df.xs(region, level="region")
        ax.set_title(region)
    else:
        ax.set_title("All regions")

    plot_df.plot(kind='bar',
          color=['salmon', 'crimson', 'cornflowerblue', 'blue'], width=.75, ax=ax) 

    ax.set_ylabel(metric)
    ax.set_title("All regions")
    plt.tight_layout()
    
    st.pyplot()
    

# Scatterplot of model performance
def plot_model_performance(df, models, region):
    fig, ax = plt.subplots(1,2, figsize=[10,5], sharex=True, sharey=True)
    plot_df = df.copy()
    plot_df.set_index("dataset", inplace=True, append=True)
    plot_df = np.log(1+plot_df[['true']+models])

    if region!="All":
        plot_df = plot_df.xs(region, level="region")
        plt.suptitle(region)
    else:
        plt.suptitle("All regions")

    i=0
    for d in ['train', 'test']:
        color=iter(cm.rainbow(np.linspace(0,1,len(models))))

        for m in models:
            c = next(color)
            plot_df.xs(d, level="dataset").plot(
                x='true', y=m, kind='scatter', ax=ax[i], 
                color="None", edgecolor=c, s=30,
                label=f"{m}", legend=i)

        i+=1

    limits = list(ax[0].get_ylim() + ax[0].get_xlim() + ax[1].get_ylim() + ax[1].get_xlim())
    mmin = min(limits)
    mmax = max(limits)

    for i in [0,1]:
        ax[i].set_xlim(mmin, mmax)
        ax[i].set_ylim(mmin, mmax)

        ax[i].plot([mmin, mmax], [mmin, mmax], ls=":", c=".3")

        ax[i].set_xlabel("Log true arrivals")
        ax[i].set_ylabel("Log predicted arrivals")

    ax[1].legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    
    st.pyplot()
    
    
# Bar plot of model importance weights
def plot_importance_weights(df, model):
    fig, ax = plt.subplots(1,1)
    df.sort_values(model, ascending=True)[-10:].plot(kind='barh', width=0.9, ax=ax)    
    plt.tight_layout()
    
    st.pyplot()
    
##############################
# Set the options for widgets
regions = sorted(master.index.get_level_values('region').unique())
models_all = [i for i in master.columns if i not in ["true", "ml_true", 'dataset', 'ml_dataset']]
indicators = [i for i in compiled.columns if i not in ['shared_border', 'distance_driving_km', 
                                                       'distance_driving_hr', 'distance_straight']]


################################################
################################################
################################################
################################################
################################################

# Setup the dashboard

# Setup the dashboard

# Select the page of interest
tab = st.selectbox(
    "", 
    ["Data", "Predictions", "Explainability"]
)

''' 
# Jetson Dashboard 
'''

if tab == "Data": ##################################################
    '''
    ## Data
    
    We use data from a variety of sources, including: PRMN, ACLED, and FSNAU.
    
    ### In and outflows
    '''
    fig, ax = plt.subplots(1,3)
    
    plot_df = compiled.sort_index().loc['2019-10-01'].reset_index(level=0)
    plot_df = somalia.merge(plot_df, left_on="admin1Name", right_index=True)
        
    plot_df['log_arrivals']   = np.log(1+plot_df['arrivals'])
    plot_df['log_departures'] = np.log(1+plot_df['departures'])
    
    plot_df_acled = acled[acled.month=='2019-10']
    plot_df_acled.plot(x='longitude', y='latitude', 
                       kind='scatter', 
                       c='log_fatalities', 
                       s=(25*plot_df_acled['log_fatalities']), 
                       ax=ax[0],
                       cmap='RdYlGn_r',
                       alpha=0.5,
                       edgecolor='black', 
                       colorbar=None)
    plot_df.plot(color='None', edgecolor="black", ax=ax[0], alpha=0.25)
    plot_df.plot('log_departures', ax=ax[1], cmap="Reds")
    plot_df.plot('log_arrivals',   ax=ax[2], cmap="Reds")
    
    
    ax[0].axis("Off")
    ax[1].axis("Off")
    ax[2].axis("Off")
    
    ax[0].set_title("Conflicts")
    ax[1].set_title("Departures")
    ax[2].set_title("Arrivals")
    
    plt.tight_layout()
    st.pyplot()
    
        
    '''
    ### Explore the model inputs
    '''
    indicator = st.selectbox(
        'Select the variable you want to view:',
         indicators
    )

    logy1 = st.checkbox(
        "Log Scale?", 
        value=True, 
        key="logy1"
    )

    plot_model_inputs(compiled, indicator, regions, logy1)
    
    
    
elif tab == "Predictions": ##################################################

    '''
    ## Predictions
    ### View the predictions of the models
    '''
    

    # Select the models of interest
    models1 = st.multiselect(
        "Select models", 
        models_all, 
        default=models_all
    )

    st.slider(
        "Select date",
        min_value = 0, 
        max_value = 228,
        value=[0,228],
        step = 12

    )

    # Select the region
    region1 = st.selectbox(
        'Region:',
         regions
    )

    logy2 = st.checkbox(
        "Log Scale?", 
        value=True, 
        key="logy2"
    )

    plot_model_predictions(master, models1, region1, logy2, split_date = split_date)


    ''' 
    ### Model Scores
    '''

    #all_regions2 = st.checkbox(
    #    "All regions?", 
    #    value=False, 
    #    key="all_regions2"
    #)
    metric = 'mse'

    plot_model_scores(scores, models1, metric, all_regions=True)

elif tab == "Explainability": ##################################################

    ''' 
    ## Explainability
    ### Inspect the model errors
    '''
    #n_rows = len(models)//2 + min(len(models)%2,1)
    #fig, ax = plt.subplots(n_rows,2, figsize=[15,n_rows*5])

    models2 = st.multiselect(
        "Select models", 
        models_all, 
        default=models_all
    )


    region2 = st.selectbox(
        'Region:',
         ['All'] + regions 
    )
    
    plot_model_performance(master, models2, region2)


    ''' 
    ### View Importance Weights
    '''

    model = 'Randomforest'
    coefwts = get_coefwts(model)
    plot_importance_weights(coefwts, model)
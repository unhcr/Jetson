import pandas as pd

def get_public_prmn(data_dir ='data/raw/prmn'):
    ''' Downloads PRMN from UNHCR website (2016 - present)'''

    prmn = pd.read_excel("https://unhcr.github.io/dataviz-somalia-prmn/data/UNHCR-PRMN-Displacement-Dataset.xlsx")

    prmn.to_csv(f"{data_dir}/prmn_public.csv")

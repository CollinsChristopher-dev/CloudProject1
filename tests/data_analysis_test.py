import os
import pandas as pd
from data_analysis import NUM_COLS

def test_csv_exists():
    assert os.path.exists("All_Diets.csv")

def test_required_columns_exist():
    df = pd.read_csv("All_Diets.csv")
    df.columns = [c.strip() for c in df.columns]

    for col in NUM_COLS:
        assert col in df.columns

def test_groupby_average_runs():
    df = pd.read_csv("All_Diets.csv")
    df.columns = [c.strip() for c in df.columns]

    avg = df.groupby("Diet_type")[NUM_COLS].mean()
    assert not avg.empty

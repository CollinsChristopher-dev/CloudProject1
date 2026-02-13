import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# file name
CSV_FILE = "All_Diets.csv"

# folder to save outputs
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# columns we care about
NUM_COLS = ["Protein(g)", "Carbs(g)", "Fat(g)"]

def main():

    # print date and time (for screenshot proof)
    print("Run date/time:", datetime.now())

    # check if file exists
    if not os.path.exists(CSV_FILE):
        print("CSV file not found")
        return

    # load the dataset
    df = pd.read_csv(CSV_FILE)

    # remove extra spaces from column names
    df.columns = [c.strip() for c in df.columns]

    # clean string columns
    df["Diet_type"] = df["Diet_type"].astype(str).str.strip()
    df["Cuisine_type"] = df["Cuisine_type"].astype(str).str.strip()
    df["Recipe_name"] = df["Recipe_name"].astype(str).str.strip()

    # convert numeric columns properly
    for col in NUM_COLS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # fill missing values with average
    df[NUM_COLS] = df[NUM_COLS].fillna(df[NUM_COLS].mean())

    # calculate average protein, carbs, fat per diet
    avg_macros = df.groupby("Diet_type")[NUM_COLS].mean()

    # get top 5 protein recipes per diet
    top_protein = df.sort_values("Protein(g)", ascending=False).groupby("Diet_type").head(5)

    # find diet with highest average protein
    highest_protein_diet = avg_macros["Protein(g)"].idxmax()

    # find most common cuisines per diet
    common_cuisines = df.groupby(["Diet_type", "Cuisine_type"]).size().reset_index(name="Count")

    # create new ratio columns
    df["Protein_to_Carbs_ratio"] = df["Protein(g)"] / df["Carbs(g)"].replace(0, np.nan)
    df["Carbs_to_Fat_ratio"] = df["Carbs(g)"] / df["Fat(g)"].replace(0, np.nan)

    # print results
    print("\nAverage macros by diet:")
    print(avg_macros)

    print("\nDiet with highest protein:")
    print(highest_protein_diet)

    print("\nTop protein recipes:")
    print(top_protein[["Diet_type", "Recipe_name", "Protein(g)"]])

    # save results
    avg_macros.to_csv(os.path.join(OUTPUT_DIR, "avg_macros.csv"))
    df.to_csv(os.path.join(OUTPUT_DIR, "cleaned_data.csv"), index=False)

    # bar chart
    plt.figure(figsize=(10,5))
    sns.barplot(x=avg_macros.index, y=avg_macros["Protein(g)"])
    plt.xticks(rotation=45)
    plt.title("Average Protein by Diet")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "bar_chart.png"))
    plt.show()

    # heatmap
    plt.figure(figsize=(8,6))
    sns.heatmap(avg_macros, cmap="viridis")
    plt.title("Average Macronutrients Heatmap")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "heatmap.png"))
    plt.show()

    # scatter plot
    plt.figure(figsize=(10,6))
    sns.scatterplot(data=top_protein, x="Protein(g)", y="Carbs(g)", hue="Cuisine_type")
    plt.title("Top Protein Recipes")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "scatter_plot.png"))
    plt.show()

    print("\nDone. Files saved in outputs folder.")

if __name__ == "__main__":
    main()

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/health_indicators_nga.csv")
df = df[
    [
        "GHO (DISPLAY)",
        "ENDYEAR",
        "DIMENSION (TYPE)",
        "DIMENSION (CODE)",
        "Numeric",
        "Low",
        "High",
    ]
]
df = df.iloc[1:]

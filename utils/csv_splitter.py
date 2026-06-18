import pandas as pd
import os

def split_csv(df, chunk_size=1000):

    os.makedirs("outputs/chunks", exist_ok=True)

    total_rows = len(df)

    for i in range(0, total_rows, chunk_size):

        chunk = df.iloc[i:i+chunk_size]

        chunk.to_csv(
            f"outputs/chunks/chunk_{i//chunk_size + 1}.csv",
            index=False
        )
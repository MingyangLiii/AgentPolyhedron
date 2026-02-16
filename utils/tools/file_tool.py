from utils.tool import Tool, InputSchema, Property
import pandas as pd



def load_csv(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def load_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)


def load_json(file_path: str) -> pd.DataFrame:
    return pd.read_json(file_path)


def load_parquet(file_path: str) -> pd.DataFrame:
    return pd.read_parquet(file_path)



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







# Define tools for loading different file types

load_csv_tool = Tool(
    name="load_csv",
    title="Load CSV File",
    description="Load a CSV file and return a DataFrame",
    func=load_csv,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="file_path",
                type="string",
                description="Path to the CSV file"
            )
        ],
        required=["file_path"]
    )
)

load_excel_tool = Tool(
    name="load_excel",
    title="Load Excel File",
    description="Load an Excel file and return a DataFrame",
    func=load_excel,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="file_path",
                type="string",
                description="Path to the Excel file"
            )
        ],
        required=["file_path"]
    )
)

load_json_tool = Tool(
    name="load_json",
    title="Load JSON File",
    description="Load a JSON file and return a DataFrame",
    func=load_json,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="file_path",
                type="string",
                description="Path to the JSON file"
            )
        ],
        required=["file_path"]
    )
)

load_parquet_tool = Tool(
    name="load_parquet",
    title="Load Parquet File",
    description="Load a Parquet file and return a DataFrame",
    func=load_parquet,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="file_path",
                type="string",
                description="Path to the Parquet file"
            )
        ],
        required=["file_path"]
    )
)       


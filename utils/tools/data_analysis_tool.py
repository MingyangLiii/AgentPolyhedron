from utils.tool import Tool, InputSchema, Property
import pandas as pd
from utils.tools.file_tool import load_csv, load_excel, load_json, load_parquet


def analyze_data(file_path: str) -> str:
    # 1. Load the data
    if file_path.endswith(".csv"):
        data = load_csv(file_path)
    elif file_path.endswith(".xlsx") or file_path.endswith(".xls"):
        data = load_excel(file_path)  
    elif file_path.endswith(".json"):
        data = load_json(file_path)
    elif file_path.endswith(".parquet"):
        data = load_parquet(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    # 2. Analyze the data
    analysis_result = f"Data Analysis Result for {file_path}:\n"
    analysis_result += f"Number of rows: {data.shape[0]}\n"
    analysis_result += f"Number of columns: {data.shape[1]}\n"
    analysis_result += f"Column names: {', '.join(data.columns)}\n"
    analysis_result += f"Data types:\n{data.dtypes}\n"
    analysis_result += f"Summary statistics:\n{data.describe()}\n" 
    return analysis_result





analyze_data_tool = Tool(
    name="analyze_data",
    title="Data Analysis Tool",
    description="Analyze data from a file and provide insights",
    func=analyze_data, 
    inputSchema=InputSchema(
        properties=[
            Property(
                name="file_path",
                type="string",
                description="Path to the data file (supports .csv, .xlsx, .xls, .json, .parquet)"
            )
        ],
        required=["file_path"]
    )
)
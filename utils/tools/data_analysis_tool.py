from utils.tool import Tool, InputSchema, Property
import pandas as pd


def describe_data(data_path: str, file_type: str = "csv") -> str:
    """Generate descriptive statistics for a dataset"""
    if file_type == "csv":
        df = pd.read_csv(data_path)
    elif file_type == "excel":
        df = pd.read_excel(data_path)
    elif file_type == "json":
        df = pd.read_json(data_path)
    elif file_type == "parquet":
        df = pd.read_parquet(data_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    return df.describe().to_string()


def filter_data(data_path: str, column: str, condition: str, file_type: str = "csv") -> str:
    """Filter data based on column and condition"""
    if file_type == "csv":
        df = pd.read_csv(data_path)
    elif file_type == "excel":
        df = pd.read_excel(data_path)
    elif file_type == "json":
        df = pd.read_json(data_path)
    elif file_type == "parquet":
        df = pd.read_parquet(data_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    if condition.startswith(">"):
        value = float(condition[1:].strip())
        filtered_df = df[df[column] > value]
    elif condition.startswith("<"):
        value = float(condition[1:].strip())
        filtered_df = df[df[column] < value]
    elif condition.startswith("="):
        value = condition[1:].strip()
        try:
            value = float(value)
            filtered_df = df[df[column] == value]
        except ValueError:
            filtered_df = df[df[column].astype(str) == value]
    elif condition.startswith("!="):
        value = condition[2:].strip()
        try:
            value = float(value)
            filtered_df = df[df[column] != value]
        except ValueError:
            filtered_df = df[df[column].astype(str) != value]
    else:
        filtered_df = df[df[column].astype(str).str.contains(condition, na=False)]
    
    return filtered_df.to_string()


def group_and_aggregate(data_path: str, group_column: str, agg_column: str, agg_func: str = "mean", file_type: str = "csv") -> str:
    """Group data by column and apply aggregation function"""
    if file_type == "csv":
        df = pd.read_csv(data_path)
    elif file_type == "excel":
        df = pd.read_excel(data_path)
    elif file_type == "json":
        df = pd.read_json(data_path)
    elif file_type == "parquet":
        df = pd.read_parquet(data_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")
    
    if agg_func == "mean":
        result = df.groupby(group_column)[agg_column].mean()
    elif agg_func == "sum":
        result = df.groupby(group_column)[agg_column].sum()
    elif agg_func == "count":
        result = df.groupby(group_column)[agg_column].count()
    elif agg_func == "max":
        result = df.groupby(group_column)[agg_column].max()
    elif agg_func == "min":
        result = df.groupby(group_column)[agg_column].min()
    else:
        raise ValueError(f"Unsupported aggregation function: {agg_func}")
    
    return result.to_string()


describe_data_tool = Tool(
    name="describe_data",
    title="Describe Data",
    description="Generate descriptive statistics for a dataset",
    func=describe_data,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="data_path",
                type="string",
                description="Path to the data file"
            ),
            Property(
                name="file_type",
                type="string",
                description="Type of the file (csv, excel, json, parquet)"
            )
        ],
        required=["data_path"]
    )
)

filter_data_tool = Tool(
    name="filter_data",
    title="Filter Data",
    description="Filter data based on column and condition (e.g., '>100', '<50', '=value', '!=value', or substring match)",
    func=filter_data,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="data_path",
                type="string",
                description="Path to the data file"
            ),
            Property(
                name="column",
                type="string",
                description="Column name to filter on"
            ),
            Property(
                name="condition",
                type="string",
                description="Filter condition (e.g., '>100', '<50', '=value', '!=value', or substring)"
            ),
            Property(
                name="file_type",
                type="string",
                description="Type of the file (csv, excel, json, parquet)"
            )
        ],
        required=["data_path", "column", "condition"]
    )
)

group_and_aggregate_tool = Tool(
    name="group_and_aggregate",
    title="Group and Aggregate",
    description="Group data by column and apply aggregation function (mean, sum, count, max, min)",
    func=group_and_aggregate,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="data_path",
                type="string",
                description="Path to the data file"
            ),
            Property(
                name="group_column",
                type="string",
                description="Column name to group by"
            ),
            Property(
                name="agg_column",
                type="string",
                description="Column name to aggregate"
            ),
            Property(
                name="agg_func",
                type="string",
                description="Aggregation function (mean, sum, count, max, min)"
            ),
            Property(
                name="file_type",
                type="string",
                description="Type of the file (csv, excel, json, parquet)"
            )
        ],
        required=["data_path", "group_column", "agg_column"]
    )
)

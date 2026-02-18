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



def load_file_as_pd(file_path: str) -> pd.DataFrame:
    if file_path.endswith('.csv'):
        return load_csv(file_path)
    elif file_path.endswith('.xlsx') or file_path.endswith('.xls'):
        return load_excel(file_path)
    elif file_path.endswith('.json'):
        return load_json(file_path)
    elif file_path.endswith('.parquet'):
        return load_parquet(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")
    

def write_file_to_txt(file_path: str, content: str) -> None:
    # if file_path does not exist, it will be created. If it exists, it will be overwritten.
    with open(file_path, 'w') as f:
        f.write(content)
        


write_file_tool = Tool(
    name="write_file_to_txt",
    title="Write File",
    func=write_file_to_txt,
    description="Write content to a text file.",
    inputSchema=InputSchema(
        properties=[Property(
                        name="file_path",
                        type="string",
                        description="The path to the file to be written."),
                    Property(
                        name="content",
                        type="string",
                        description="The content to be written to the file.")
                    ]
        ,
        required=["file_path", "content"]
    )
)

load_file_tool = Tool(
    name="load_file_as_pd",
    title="Load File",
    func=load_file_as_pd,
    description="Load a file (CSV, Excel, JSON, Parquet) into a DataFrame.",
    inputSchema=InputSchema(
        properties=[Property(
                name="file_path",
                type="string",
                description="The path to the file to be loaded.")]
        ,
        required=["file_path"]
    )
)
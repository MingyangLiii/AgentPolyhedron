from utils.tool import Tool, InputSchema, Property
import pandas as pd



def analyze_data(dataframe: pd.DataFrame) -> str:
    analysis_result = f"Data Analysis Result:\n"
    analysis_result += f"Number of rows: {dataframe.shape[0]}\n"
    analysis_result += f"Number of columns: {dataframe.shape[1]}\n"
    analysis_result += f"Column names: {', '.join(dataframe.columns)}\n"
    analysis_result += f"Data types:\n{dataframe.dtypes}\n"
    analysis_result += f"Summary statistics:\n{dataframe.describe()}\n" 
    return analysis_result



analyze_data_tool = Tool(
    name="analyze_data",
    title="Data Analysis Tool",
    description="Analyze data from a dataframe and provide insights",
    func=analyze_data, 
    inputSchema=InputSchema(
        properties=[
            Property(
                name="dataframe",
                type="object",
                description="The dataframe to be analyzed"
            )
        ],
        required=["dataframe"]
    )
)
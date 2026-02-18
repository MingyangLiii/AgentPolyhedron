# Get Current Time Given Timezone
import datetime
import pytz

from utils.tool import Tool, InputSchema, Property





def get_current_time_by_timezone(location: str) -> str:
    timezone = pytz.timezone(location)
    return datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S")


tool_get_current_time_by_timezone = Tool(
    name="get_current_time_by_timezone",
    title="Get Current Time By Timezone",
    description="Get current time by timezone",
    func=get_current_time_by_timezone,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="location",
                type="string",
                description="Timezone location (example: 'Asia/Shanghai')"
            )
        ],
        required=["location"]
    )
)




def main():
    print(get_current_time_by_timezone("Asia/Shanghai"))

if __name__ == "__main__":
    main()



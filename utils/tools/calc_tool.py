from utils.tool import Tool, InputSchema, Property



def multiply(a: str, b: str) -> str:
    return str(float(a) * float(b))


def divide(a: str, b: str) -> str:
    return str(float(a) / float(b))


def power(a: str, b: str) -> str:
    return str(float(a) ** float(b))


tool_multiply = Tool(
    name="multiply",
    title="Multiply",
    description="Multiply two numbers",
    func=multiply,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="a",
                type="string",
                description="First number (should not be an expression, but a single number)"
            ),
            Property(
                name="b",
                type="string",
                description="Second number (should not be an expression, but a single number)"
            )
        ],
        required=["a", "b"]
    )
)

tool_divide = Tool(
    name="divide",
    title="Divide",
    description="Divide two numbers",
    func=divide,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="a",
                type="string",
                description="First number (should not be an expression, but a single number)"
            ),
            Property(
                name="b",
                type="string",
                description="Second number (should not be an expression, but a single number)"
            )
        ],
        required=["a", "b"]
    )
)

tool_power = Tool(
    name="power",
    title="Power",
    description="Power of two numbers",
    func=power,
    inputSchema=InputSchema(
        properties=[
            Property(
                name="a",
                type="string",
                description="Base number (should not be an expression, but a single number)"
            ),
            Property(
                name="b",
                type="string",
                description="Exponent number (should not be an expression, but a single number)"
            )
        ],
        required=["a", "b"]
    )
)
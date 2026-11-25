from fastmcp import FastMCP

mcp = FastMcp('Math')

@mcp.tool()
def add(a:float | int, b:float | int) -> float | int:
  return a + b

@mcp.tool()
def multiply(a:float | int, b:float | int) -> float | int:
  return a * b

if __name__ == "__main__":
  mcp.run(transport = "stdio")
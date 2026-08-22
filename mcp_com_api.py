"""Servidor MCP gerado a partir da API pública Petstore.

O módulo carrega o schema OpenAPI da Petstore durante a inicialização e usa o
FastMCP para expor como tools os endpoints descritos nessa especificação.
"""

import httpx2
from fastmcp import FastMCP

spec = httpx2.get("https://petstore3.swagger.io/api/v3/openapi.json").json()
mcp = FastMCP.from_openapi(
    spec,
    httpx2.AsyncClient(base_url="https://petstore3.swagger.io/api/v3"),
    name="MCP_API",
)

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

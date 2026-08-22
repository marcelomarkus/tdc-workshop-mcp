"""Servidor MCP gerado automaticamente a partir da API pública Petstore.

O schema OpenAPI é carregado durante a inicialização e convertido pelo FastMCP
em tools correspondentes aos endpoints da API, usando transporte HTTP com
streaming para atender clientes MCP.
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

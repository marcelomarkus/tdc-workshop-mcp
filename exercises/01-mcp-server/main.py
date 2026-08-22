"""Servidor MCP mínimo usado para apresentar a estrutura básica do protocolo.

Este primeiro exercício cria uma instância do FastMCP e inicia um endpoint
HTTP com streaming, sem registrar tools ou resources adicionais.
"""

from fastmcp import FastMCP

# Instância do servidor
mcp = FastMCP("workshop", version="1.0", instructions="Workshop")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")

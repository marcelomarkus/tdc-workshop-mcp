"""Servidor MCP que demonstra resources estáticos e parametrizados.

O exercício disponibiliza uma explicação sobre MCP e um resource de previsão
do tempo por cidade, consultando a temperatura atual no serviço `wttr.in`.
"""

import httpx2
from fastmcp import FastMCP

# Instância do servidor com auth Auth0 tenant
mcp = FastMCP("workshop", version="1.0", instructions="Workshop")


async def consulta_api(cidade: str) -> str:
    """Consulta a temperatura atual de uma cidade no serviço `wttr.in`.

    Args:
        cidade: Nome da cidade usado na URL da consulta.

    Returns:
        Texto retornado pelo serviço meteorológico, normalmente uma
        temperatura formatada.
    """

    return httpx2.get(f"https://wttr.in/{cidade}?format=%t").text


@mcp.resource("workshop://oque-o-mcp-nao-e")
def guia_mcp() -> str:
    """Retorna um texto introdutório sobre o que MCP não representa."""

    return """
    O QUE O MCP NÃO É
    - NÃO É UM FRAMEWORK
    - NÃO EXECUTA IA NO SERVIDOR
    - NÃO É RAG TRADICIONAL
    """


@mcp.resource("previsao://{cidade}")
async def previsao(cidade: str) -> str:
    """Fornece a previsão de uma cidade como um recurso MCP.

    Args:
        cidade: Cidade que será consultada no serviço meteorológico.

    Returns:
        Mensagem com a cidade e a temperatura obtida.
    """

    res = await consulta_api(cidade)
    return f"Previsão para {cidade}:{res}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

"""Servidor MCP que demonstra o registro e o uso de tools.

As ferramentas meteorológicas consultam a temperatura de uma cidade, enquanto
`Enviar_Convites` demonstra confirmação do usuário e atualização de progresso
durante uma operação assíncrona.
"""

import asyncio

import httpx2
from fastmcp import Context, FastMCP

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

    res = httpx2.get(f"https://wttr.in/{cidade}?format=%t").text
    return f"Previsão para {cidade}:{res}"


@mcp.tool(name="Tempo")
async def tempo(cidade: str) -> str:
    """Consulta o tempo atual de uma cidade."""

    return await consulta_api(cidade)


@mcp.tool(name="Temperatura")
async def temperatura(cidade: str) -> str:
    """Consulta a temperatura atual de uma cidade."""

    return await consulta_api(cidade)


@mcp.tool(name="Enviar_Convites", title="Enviar Convites")
async def enviar_convites(quantidade: int, contexto: Context) -> str:
    """Simula convites após obter confirmação explícita do usuário.

    A ferramenta envia uma atualização de informação e de progresso para cada
    convite. O intervalo entre itens existe para tornar esse fluxo observável
    em clientes MCP durante o workshop.

    Args:
        quantidade: Número de convites a simular.
        contexto: Contexto fornecido pelo FastMCP para elicitação e progresso.

    Returns:
        `Enviado!` quando confirmado ou `Cancelado!` caso contrário.
    """

    autorizado = await contexto.elicit(
        "Confirma o envio?", response_type=bool, response_title="concordo"
    )
    if autorizado.action == "accept":
        for i in range(1, quantidade + 1):
            await asyncio.sleep(5.0)
            await contexto.info(f"Enviado {i}:{quantidade}")
            await contexto.report_progress(i, total=quantidade)
        return "Enviado!"
    else:
        await contexto.warning("Cancelado")
        return "Cancelado!"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

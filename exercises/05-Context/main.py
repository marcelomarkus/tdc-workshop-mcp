"""Servidor MCP dedicado ao uso do contexto durante uma operação.

O exercício usa o `Context` do FastMCP para solicitar confirmação, enviar
mensagens ao cliente e reportar o progresso do envio simulado de convites.
"""

import asyncio
import os

from fastmcp import Context, FastMCP
from fastmcp.server.auth.providers.auth0 import Auth0Provider

auth_provider = Auth0Provider(
    config_url=os.getenv("AUTH_DOMAIN"),
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    base_url="http://127.0.01:8000",
    audience=os.getenv("AUDIENCE"),
)

# Instância do servidor com auth Auth0 tenant
mcp = FastMCP("workshop", version="1.0", instructions="Workshop", auth=auth_provider)


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

"""Servidor MCP completo do workshop com autenticação Auth0.

Este exercício combina resources, tools, prompts e operações com contexto para
demonstrar um servidor protegido por credenciais configuradas no ambiente.
"""

import asyncio
import os

import httpx2
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


@mcp.tool(name="Tempo")
async def tempo(cidade: str) -> str:
    """Consulta o tempo atual de uma cidade."""

    return await previsao(cidade)


@mcp.tool(name="Temperatura")
async def temperatura(cidade: str) -> str:
    """Consulta a temperatura atual de uma cidade."""

    return await previsao(cidade)


@mcp.prompt("exemplo_prompt", title="Exemplo prompt")
async def exemplo_prompt(pergunta: str) -> str:
    """Cria um prompt que orienta a escolha entre as tools meteorológicas.

    Args:
        pergunta: Pergunta do usuário que será incluída nas instruções.

    Returns:
        Instruções textuais para o cliente MCP decidir qual tool invocar.
    """

    return f"""
    Você é o assistente responsavel por decidir qual tool utilizar, sega as REGRAS.

    REGRAS OBRIGATÓRIAS:
    1. Caso {pergunta} for sobre tempo. Você DEVE invocar a tool 'temperatura'.
    2. Caso {pergunta} for sobre temperatura. Você DEVE invocar a tool 'tempo'.

    responda a {pergunta}
    EXECUTE a tool apropriada e siga RIGOROSAMENTE as REGRAS.
    """


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

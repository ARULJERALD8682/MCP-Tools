import os
import sys
from pathlib import Path
from google.cloud import bigquery

from mcp.server.fastmcp import FastMCP  
from mcp.server import Server  
from mcp.server.sse import SseServerTransport  

from starlette.applications import Starlette 
from starlette.routing import Route, Mount  
from starlette.requests import Request  

import uvicorn  
from mcp.server import FastMCP
from dotenv import load_dotenv


load_dotenv()

def get_bq_client():
    client = bigquery.Client()
    return client

try:
    DATASET_NAME = os.getenv("DATASET_NAME")
except:
    sys.exit("Couldn't find any Dataset Name inside the env file")

try :
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
except:
    sys.exit(f"Couldn't find any service account inside {Path.cwd()}")

mcp = FastMCP("Custom_Telementry")

client = get_bq_client()

@mcp.tool(name="get_list_of_tablename", description="Help to get the list of table In the specified Dataset")
async def get_list_of_table() -> list:
    list_table = client.list_tables(dataset=f"{DATASET_NAME}")
    tables = []
    for table in list_table:
        tables.append(table.full_table_id.replace(":","."))
    return tables

@mcp.tool(name="get_table_information", description="Helps to find table information like schema")
async def get(table_id:str):
    schemas = client.get_table(table=table_id)
    return list(schemas.schema)

@mcp.tool(name="excute_qury_and_get_results", description="Helps to Excute the query and get results from Bigquery table")
async def get_results_using_query(query: str,sample:str):
    try:
        jobs = client.query(query)
        jobs.result()
        res = [dict(job) for job in jobs]
        return res
    except  Exception as e:
        print("error occurred:", e)

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """
    Constructs a Starlette app with SSE and message endpoints.

    Args:
        mcp_server (Server): The core MCP server instance.
        debug (bool): Enable debug mode for verbose logs.

    Returns:
        Starlette: The full Starlette app with routes.
    """
 
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        """
        Handles a new SSE client connection and links it to the MCP server.
        """
        print(f"handle_sse ...... {request.scope }'+',\
            {request.receive}'+'\
            {request._send}")

        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,  
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )


    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),        
            Mount("/messages/", app=sse.handle_post_message),  
        ],
    )



if __name__ == "__main__":
  
    mcp_server = mcp._mcp_server  

    import argparse

    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8081, help='Port to listen on')
    args = parser.parse_args()

    starlette_app = create_starlette_app(mcp_server, debug=True)


    uvicorn.run(starlette_app, host=args.host, port=args.port)


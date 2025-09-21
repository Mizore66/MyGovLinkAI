from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import uvicorn
from client import MCPClient
import os

app = FastAPI(title="MCP Client API", description="API wrapper for MCP Client with Bedrock")

# Global client instance
mcp_client = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

@app.on_event("startup")
async def startup_event():
    """Initialize MCP client on startup"""
    global mcp_client
    mcp_client = MCPClient()
    
    # Connect to your MCP server (localhost if on same instance)
    mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
    try:
        await mcp_client.connect_to_server(mcp_server_url)
        print(f"✅ Connected to MCP server: {mcp_server_url}")
    except Exception as e:
        print(f"❌ Failed to connect to MCP server: {e}")
        raise e

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    global mcp_client
    if mcp_client:
        await mcp_client.cleanup()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "healthy", "message": "MCP Client API is running"}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    global mcp_client
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP Client not initialized")
    
    try:
        # Test connection by listing tools
        tools = await mcp_client.list_tools()
        return {
            "status": "healthy",
            "mcp_connected": True,
            "available_tools": len(tools),
            "tools": [{"name": tool.name, "description": tool.description} for tool in tools]
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"MCP connection failed: {str(e)}")

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a query through the MCP client"""
    global mcp_client
    
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP Client not initialized")
    
    try:
        response = await mcp_client.process_query(request.query)
        return QueryResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")

@app.get("/tools")
async def list_available_tools():
    """List all available tools from the MCP server"""
    global mcp_client
    
    if not mcp_client:
        raise HTTPException(status_code=503, detail="MCP Client not initialized")
    
    try:
        tools = await mcp_client.list_tools()
        return {
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
                for tool in tools
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list tools: {str(e)}")

if __name__ == "__main__":
    # For local development
    uvicorn.run(app, host="0.0.0.0", port=8080)
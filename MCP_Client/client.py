import asyncio
import json
import re
from typing import Optional
from contextlib import AsyncExitStack
import aiohttp

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class HTTPMCPTransport:
    """Simple HTTP transport for MCP over HTTP (REST-style)"""
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_tools(self):
        """Get available tools from the server"""
        if not self.session:
            raise RuntimeError("Transport not initialized")
        
        async with self.session.get(f"{self.base_url}/tools") as response:
            if response.status == 200:
                return await response.json()
            else:
                raise Exception(f"HTTP {response.status}: {await response.text()}")
    
    async def call_tool(self, tool_name: str, arguments: dict):
        """Call a specific tool on the server"""
        if not self.session:
            raise RuntimeError("Transport not initialized")
        
        # Server expects arguments nested under "arguments" key
        request_body = {"arguments": arguments}
        
        # Try POST to /tools/{tool_name}
        async with self.session.post(
            f"{self.base_url}/tools/{tool_name}",
            json=request_body,
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_text = await response.text()
                raise Exception(f"HTTP {response.status}: {error_text}")

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.http_transport = None
        self.is_http = False

        # Initialize Bedrock Runtime client with region - this will fail without credentials
        try:
            self.bedrock_client = boto3.client(
                "bedrock-runtime",
                region_name="us-east-1"  # DeepSeek models are available in us-east-1
            )
        except Exception as e:
            self.bedrock_client = None
        
        # DeepSeek R1 model - correct model ID
        self.model_id = "openai.gpt-oss-120b-1:0"

    def clean_response_formatting(self, response: str) -> str:
        """Clean and format the AI response for messaging applications"""
        if not response:
                return response
        
        # Remove any raw JSON objects at the beginning and anywhere in the text
        response = re.sub(r"\{'result':\s*'[^']*'\}", '', response, flags=re.MULTILINE | re.DOTALL)
        response = re.sub(r'\{"result":\s*"[^"]*"\}', '', response, flags=re.MULTILINE | re.DOTALL)
        response = re.sub(r"^\{'result':\s*\".*?\"\}\s*", '', response, flags=re.MULTILINE | re.DOTALL)
        
        # Convert HTML tags to proper formatting
        response = re.sub(r'<br\s*/?>|<br>', '\n', response, flags=re.IGNORECASE)  # Convert <br> to newlines
        response = re.sub(r'<[^>]+>', '', response)  # Remove any other HTML tags
        
        # Convert markdown tables to Field: Value format
        table_pattern = r'\|([^|]+)\|([^|]+)\|[\s\S]*?(?=\n\n|\n[^|]|\Z)'
        
        def convert_table(match):
            lines = match.group(0).split('\n')
            formatted_lines = []
            
            for line in lines:
                if '|' in line and not line.strip().startswith('|---'):
                    cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                    if len(cells) >= 2:
                        field = cells[0].replace('**', '').strip()  # Remove bold from field names
                        value = cells[1].strip()  # Keep bold formatting in values
                        if field and value and field != 'Field' and value != 'Information':
                            formatted_lines.append(f"{field}: {value}")
            
            return '\n'.join(formatted_lines) if formatted_lines else ''
        
        response = re.sub(table_pattern, convert_table, response)
        
        # Remove markdown formatting (but keep bold text)
        # Keep bold text as **text** - this line is commented out to preserve bold formatting
        response = re.sub(r'(?<!\*)\*(?!\*)([^*]+?)(?<!\*)\*(?!\*)', r'\1', response)  # Remove single * (italic) but not **
        response = re.sub(r'`(.*?)`', r'\1', response)        # Remove code formatting
        response = re.sub(r'#{1,6}\s*', '', response)         # Remove headers
        response = re.sub(r'---+', '', response)              # Remove horizontal rules
        response = re.sub(r'^\s*[\*\-\+]\s+', '', response, flags=re.MULTILINE)  # Remove bullet points
        
        # Clean up encoding issues
        replacements = {
            'â¯': ' ', 'â': '-', 'â': "'", 'â': "'", 
            'â': '"', 'â': '"', 'â¦': '...', 'â': '-', 'â': '--',
        }
        for bad_char, good_char in replacements.items():
            response = response.replace(bad_char, good_char)
        
        # Clean up extra whitespace and empty lines
        response = re.sub(r'\n\s*\n\s*\n', '\n\n', response)  # Multiple empty lines
        response = re.sub(r'[ \t]+', ' ', response)           # Multiple spaces
        response = response.strip()
        
        return response

    def format_tool_result(self, tool_name: str, result_content: str, tool_args: dict) -> str:
        """Format tool results in a clean way"""
        try:
            # Try to parse the result as JSON for clean formatting
            if isinstance(result_content, str):
                try:
                    parsed_result = json.loads(result_content)
                    return json.dumps(parsed_result, indent=2)
                except json.JSONDecodeError:
                    return result_content
            else:
                return str(result_content)
            
        except Exception as e:
            return str(result_content)

    def clean_response(self, content: str) -> str:
        """Remove reasoning sections and clean up the response for messaging"""
        if not content:
            return content
            
        # Remove reasoning sections
        lines = content.split('\n')
        cleaned_lines = []
        skip_reasoning = False
        
        for line in lines:
            # Check for reasoning tags or patterns
            if '<reasoning>' in line.lower() or line.strip().startswith('**Reasoning'):
                skip_reasoning = True
                continue
            elif '</reasoning>' in line.lower() or (skip_reasoning and line.strip() == ''):
                skip_reasoning = False
                continue
            elif skip_reasoning:
                continue
                
            cleaned_lines.append(line)
        
        response = '\n'.join(cleaned_lines).strip()
        
        # Apply additional formatting cleanup
        return self.clean_response_formatting(response)

    async def list_tools(self):
        """List available tools (works with both HTTP and stdio)"""
        if self.is_http:
            result = await self.http_transport.get_tools()
            # Convert HTTP response to match stdio format
            class Tool:
                def __init__(self, name, description, inputSchema):
                    self.name = name
                    self.description = description
                    self.inputSchema = inputSchema
            
            tools = []
            if "tools" in result:
                for tool_data in result["tools"]:
                    tools.append(Tool(
                        tool_data["name"],
                        tool_data.get("description", ""),
                        tool_data.get("inputSchema", {})
                    ))
            return tools
        else:
            response = await self.session.list_tools()
            return response.tools
    
    async def call_tool(self, tool_name: str, arguments: dict):
        """Call a tool (works with both HTTP and stdio)"""
        if self.is_http:
            result = await self.http_transport.call_tool(tool_name, arguments)
            # Convert HTTP response to match stdio format
            class ToolResult:
                def __init__(self, content):
                    self.content = content
            
            # Return the result directly as content
            return ToolResult(result)
        else:
            return await self.session.call_tool(tool_name, arguments)

    async def connect_to_server(self, server_path: str):
        """Connect to an MCP server
        
        Args:
            server_path: Path to the server script (.py or .js) or HTTP URL
        """
        # Check if it's an HTTP URL
        if server_path.startswith('http://') or server_path.startswith('https://'):
            self.http_transport = await self.exit_stack.enter_async_context(HTTPMCPTransport(server_path))
            self.is_http = True
            
            # Test connection by getting tools
            try:
                result = await self.http_transport.get_tools()
                return
            except Exception as e:
                raise Exception(f"Failed to connect to HTTP MCP server: {e}")
        
        # Handle local files
        is_python = server_path.endswith('.py')
        is_js = server_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file, or use an HTTP URL")
            
        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_path],
            env=None
        )
        
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
        self.is_http = False
        
        await self.session.initialize()
        
        # List available tools
        tools = await self.list_tools()
        print("\nConnected to server with tools:", [tool.name for tool in tools])

    async def process_query(self, query: str) -> str:
        """Process a query using DeepSeek R1 on Bedrock and available tools"""
        # Add system prompt to guide the model's behavior
        system_prompt = """
        You are a helpful assistant specializing in Malaysian government services and data retrieval.

        When retrieving Saman data or other official records:
        - Always use the appropriate tools rather than generating fake data
        - Present results in a clear, structured format
        - Use proper Malaysian formats (MyKad numbers, phone numbers, etc.)
        - Be accurate and only return actual tool results

        Format responses professionally and clearly. Do note that if the MyKad data is not correct, still use it as a argument to pass
        it into the tools and get appropriate data from the tools. If the users ask for anything related to paying a saman or renewing
        their license, simply call the tool as we dont need their mykad number or any details to provide them with the information
        """

        messages = [
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user",
                "content": query
            }
        ]

        tools = await self.list_tools()
        available_tools = []
        
        # Convert MCP tools to OpenAI-compatible format for DeepSeek
        for tool in tools:
            tool_spec = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            }
            available_tools.append(tool_spec)

        # Format request for OpenAI model on Bedrock (no model parameter needed)
        native_request = {
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        # Add tools if available
        if available_tools:
            native_request["tools"] = available_tools
            native_request["tool_choice"] = "auto"

        try:
            # Call Bedrock
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(native_request)
            )
        except (ClientError, Exception) as e:
            return f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}"

        # Decode the response body
        model_response = json.loads(response["body"].read())
        
        # Process response and handle tool calls (DeepSeek R1 uses OpenAI-compatible format)
        tool_results = []
        final_text = []

        # Handle DeepSeek R1 response format (similar to OpenAI)
        choices = model_response.get("choices", [])
        if not choices:
            return "No response choices received from GPT"

        message = choices[0].get("message", {})
        
        # Check if there are tool calls first
        tool_calls = message.get("tool_calls", [])
        
        # Only add initial content if there are NO tool calls
        # (if there are tool calls, we'll get the final response after tool execution)
        if not tool_calls and "content" in message and message["content"]:
            cleaned_content = self.clean_response(message["content"])
            if cleaned_content:
                final_text.append(cleaned_content)
        for tool_call in tool_calls:
            if tool_call.get("type") == "function":
                function = tool_call.get("function", {})
                tool_name = function.get("name")
                tool_args_str = function.get("arguments", "{}")
                
                try:
                    tool_args = json.loads(tool_args_str)
                except json.JSONDecodeError:
                    tool_args = {}
                
                # Execute tool call
                result = await self.call_tool(tool_name, tool_args)
                tool_results.append({"call": tool_name, "result": result})
                
                # Format the result nicely
                formatted_result = self.format_tool_result(tool_name, str(result.content), tool_args)
                final_text.append(formatted_result)

                # Continue conversation with tool results (send raw result to model)
                messages.append({
                    "role": "assistant",
                    "content": message.get("content"),
                    "tool_calls": tool_calls
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.get("id"),
                    "content": str(result.content)
                })

                # Get next response from OpenAI model
                follow_up_request = {
                    "messages": messages,
                    "max_tokens": 1000,
                    "temperature": 0.7
                }
                
                if available_tools:
                    follow_up_request["tools"] = available_tools
                    follow_up_request["tool_choice"] = "auto"

                try:
                    follow_up_response = self.bedrock_client.invoke_model(
                        modelId=self.model_id,
                        body=json.dumps(follow_up_request)
                    )
                    follow_up_data = json.loads(follow_up_response["body"].read())
                    
                    # Extract text from follow-up response
                    follow_choices = follow_up_data.get("choices", [])
                    if follow_choices:
                        follow_message = follow_choices[0].get("message", {})
                        if follow_message.get("content"):
                            cleaned_content = self.clean_response(follow_message["content"])
                            if cleaned_content:
                                final_text.append(cleaned_content)
                            
                except (ClientError, Exception) as e:
                    final_text.append(f"Error in follow-up response: {e}")

        final_response = "\n".join(final_text) if final_text else "No response received from GPT"
        return self.clean_response_formatting(final_response)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("Type your queries or 'quit' to exit.")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                
                if query.lower() == 'quit':
                    break
                    
                response = await self.process_query(query)
                print(response)
                    
            except Exception as e:
                print(f"Error: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)
        
    client = MCPClient()
    try:

        
        # Then connect to MCP server and start chat
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())

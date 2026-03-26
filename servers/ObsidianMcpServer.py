from helpers.config import get_settings
from mcp_use import MCPClient

class ObsidianMcpServer:
    def __init__(self):
        self.settings = get_settings()
        self.mcp_server = MCPClient({
            "mcpServers":{
                "mcp-obsidian": {
                    "command": "./.venv/Scripts/uvx.exe",
                    "args": [
                    "mcp-obsidian"
                    ],
                    "env": {
                    "OBSIDIAN_API_KEY": self.settings.OBSIDIAN_API_KEY
                    },
                }
            }
        })
        self.session = None
    
    async def create_session(self, server_name:str = "mcp-obsidian"):
        self.session = await self.mcp_server.create_session(server_name = server_name)
    
    async def close_seesion(self, server_name:str = "mcp-obsidian"):
        await self.mcp_server.close_session(server_name=server_name)
        self.session = None
    
    async def obsidian_add_note_async(self, filepath:str, content:str):
        result = None
        try: 
            await self.create_session()
            result = await self.session.call_tool(
            "obsidian_append_content" , 
            {'filepath' : filepath, 'content': content}
            )
            await self.close_seesion()
        except :
            print("couldn't call tool")
        return result
        

    


        
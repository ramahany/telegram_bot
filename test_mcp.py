from llm import ObsidianMcpServer, GroqClient
import asyncio

if __name__ == "__main__":
    test = ObsidianMcpServer() 
    asyncio.run(test.create_session())
    # client = GroqClient()
    # query = "i want to build a ecommerce app for sweatshirts that enables the client to design their own designs using genAI "
    # while True:
    #     asyncio.run(client.responce_agent(query=query))
    #     query = input()
    # # asyncio.run(client.print_tools())


# name='obsidian_append_content' 
# title=None 
# description='Append content to a new or existing file in the vault.' 
# inputSchema={'type': 'object', 
# 'properties': {
# 'filepath': {'type': 'string', 'description': 'Path to the file (relative to vault root)', 'format': 'path'}, 
# 'content': {'type': 'string', 'description': 'Content to append to the file'}}, 
# 'required': ['filepath', 'content']} 
# outputSchema=None icons=None annotations=None meta=None execution=None

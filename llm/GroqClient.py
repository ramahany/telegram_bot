import groq
from helpers.config import get_settings
from helpers.prompts import Prompts
from servers import ObsidianMcpServer
from mcp_use import MCPAgent, MCPClient
from langchain_groq import ChatGroq
from tools.add_obsidian_note_groq import create_obsidian_note

class GroqClient:
    def __init__(self):
        self.settings = get_settings()


        self.client = groq.Client(
            api_key=self.settings.GROQ_API_KEY,
            
            )
        # self.agent = MCPAgent(
        #     llm = ChatGroq(
        #         model="llama-3.1-8b-instant",
        #         api_key=self.settings.GROQ_API_KEY),
        #     client=self.mcp_client,
        #     # disallowed_tools =['obsidian_list_files_in_dir', 'obsidian_list_files_in_vault', 'obsidian_get_file_contents', 'obsidian_simple_search', 'obsidian_patch_content', 'obsidian_delete_file', 'obsidian_complex_search', 'obsidian_batch_get_file_contents', 'obsidian_get_periodic_note', 'obsidian_get_recent_periodic_notes', 'obsidian_get_recent_changes'],
        #     # use_server_manager=True,
        #     max_steps=10,
        #     system_prompt='''You have access to one tool: obsidian_append_content.
        #     Always use the EXACT tool name 'obsidian_append_content' — never rename it.
        #     Always use .md extension for file paths (e.g. 'note.md', not 'note.txt')'''
        #     # system_prompt=Prompts.SYSTEM_PROMPT.value
        
        # )




    async def print_tools(self):
        await self.mcp_client.create_all_sessions()
        session = self.mcp_client.get_session("mcp-obsidian")

        tools = await session.list_tools()
        print("TOOLS ARE :")
        for t in tools : 
            print(t.name)
            # print(t)
            # print('='*20)

        result = await session.call_tool(
            "obsidian_append_content" , 
            {'filepath' : "hello.md", 'content': "hamada hellal"}
        )
        print(result)
        await self.mcp_client.close_all_sessions()

    async def responce_agent(self, query:str):
        result = await self.agent.run(query=query)
        print(result)

    

    def response(self, hist:list, model:str="llama-3.3-70b-versatile"):
        chat_completion = self.client.chat.completions.create(
            messages=[
                        {
                            "role": "system",
                            "content":"" # TODO Create a good system prompt to test the obsidian tool 
                        }
                        ]+ hist,
            tools=[
                    {   
                        "type": "function",
                        "function":{
                            "name":"create_obsidian_note",
                            
                        }
                    }],

            model=model,
            temperature=0.1,
        )

        
        if not chat_completion or not chat_completion.choices or len(chat_completion.choices) == 0 or not chat_completion.choices[0].message :
            return "Client didn't work prop"
        return chat_completion.choices[0].message.content
    


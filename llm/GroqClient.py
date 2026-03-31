import groq
from helpers.config import get_settings
from helpers.prompts import Prompts
from servers import ObsidianMcpServer
from mcp_use import MCPAgent, MCPClient
from langchain_groq import ChatGroq
from tools.add_obsidian_note_groq import create_obsidian_note
import json

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

    
    async def responce_with_local_tools(self, hist:list, model:str="llama-3.3-70b-versatile"):
        available_tools = {
            "create_obsidian_note" : create_obsidian_note
        }

        chat_completion = self.client.chat.completions.create(
                            messages=[
                                        {
                                            "role": "system",
                                            "content":Prompts.SYSTEM_PROMPT.value 
                                        }
                                        ]+ hist,
                            tools=[
                                    {   
                                        "type": "function",
                                        "function":{
                                            "name":"create_obsidian_note",
                                            "description":"Creates obsidian note",
                                            "parameters" : {
                                                "type":"object",
                                                "properties" : {
                                                    "note_title":{
                                                        "type":"string",
                                                        "description" : "The title used for the obsidian note"
                                                    },
                                                    "note_content":{
                                                        "type":"string",
                                                        "description" : "The content stored obsidian note"
                                                    }
                                                },
                                            "required" : ["note_title", "note_content"]
                                            }
                                            
                                        }
                                    }],
                            model=model,
                            temperature=0.1,
                        )
        
        res_msg = chat_completion.choices[0].message
        hist.append(res_msg)
        tool_calls = res_msg.tool_calls
        if tool_calls: 
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_tools.get(function_name, -1)
                if function_to_call == -1 : 
                    hist.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": "invalid function",
                })
                else :
                    print(tool_call.function.arguments)
                    print('_' * 20)
                    function_args = json.loads(tool_call.function.arguments)
                    result = await function_to_call(**function_args)
                    hist.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": str(result),
                })
                hist = await self.responce_with_local_tools(hist)

        return hist
        
    


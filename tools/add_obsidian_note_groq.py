from langchain.tools import tool
from pydantic import BaseModel, Field
from servers.ObsidianMcpServer import ObsidianMcpServer
#create a class schema 
class NoteInputs(BaseModel):
    note_title : str = Field(description="Note title")
    note_content : str =Field(description="content saved in the note")


# @tool("create_obsidian_note", 
#       description="takes note title and note content and uses them to create an obsidian note",
#       args_schema=NoteInputs)
async def create_obsidian_note(note_title:str, note_content:str):
    """Create an obsidian Note"""
    server = ObsidianMcpServer()
    res = None

    try:
        res = await server.obsidian_add_note_async(
            filepath=note_title, 
            content=note_content)
    except Exception as e :
        print(f"Problem Running Tool 'create_obsidian_note' : {e}")

    return res



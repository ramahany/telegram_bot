from mcp_use.agents.managers.base import BaseServerManager
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from servers import ObsidianMcpServer

# define input Class args schema
class NoteInputs(BaseModel):
    note_title : str = Field(description="Note title")
    note_content : str =Field(description="content saved in the note")

# define the tool class
class AddObsidianNote(BaseTool):
    name: str = "add_obsidian_note"
    description: str = "Takes note title along with note content and saves them as obsidian note"
    args_schema : type[BaseModel] = NoteInputs

    def _run(self, note_title:str, note_content:str):
        note_title = note_title+'.md'
        
         

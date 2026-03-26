from pydantic_settings import BaseSettings

class Settings(BaseSettings): 
    BOT_TOKEN : str
    GROQ_API_KEY : str
    GITHUB_TOKEN : str
    HF_TOKEN : str
    NGROK_TOKEN:str
    NOTION_TOKEN:str
    PARALLEL_API_KEY:str
    OBSIDIAN_API_KEY:str

    class Config : 
        env_file = '.env'


def get_settings(): 
    return Settings()
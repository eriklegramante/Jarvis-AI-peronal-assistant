from .system_tools import SystemManager
from .web_tools import WebManager

def get_all_jarvis_tools(username="Root"):
    # Instancia os gerentes
    sys_m = SystemManager(username=username)
    web_m = WebManager()
    
    # Consolida as listas
    all_tools = sys_m.fetch_tools() + web_m.fetch_tools()
    
    return all_tools
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

search = DuckDuckGoSearchRun()

class WebManager:
    """Gerenciador de ferramentas de internet."""
    
    def fetch_tools(self):
        @tool
        def search_web(query: str):
            """Pesquisa na internet por informações em tempo real. 
            Use para notícias, fatos recentes ou dúvidas que não estão na sua memória."""
            return search.run(query)
            
        return [search_web]
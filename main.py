import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from tools import get_all_jarvis_tools
from logs.logger import setup_logger
import time


load_dotenv()


manager = get_all_jarvis_tools(username="Root")
tools_do_jarvis = get_all_jarvis_tools(username="Root") 


llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.3,
    google_api_key=os.getenv("API_KEY_GEMINI")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é o Jarvis, um assistente de IA sofisticado. "
               "Não seja excessivamente formal se o usuário não gostar. "
               "Sempre use as ferramentas para validar dados de sistema."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

try:
    agent = create_tool_calling_agent(llm, tools_do_jarvis, prompt)
    
    debug_status = os.getenv("DEBUG_MODE", "False") == "True"

    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools_do_jarvis, 
        verbose=debug_status, 
        handle_parsing_errors=True
    )
    print(">>> Sistemas inicializados com sucesso, senhor. Aguardando comandos.")
except Exception as e:
    print(f"Erro na inicialização: {e}")

logger = setup_logger()
start_time = time.time()

logger.info("Sistemas inicializados, senhor.")
logger.info("Enviando requisição para o Gemini-3-flash-preview...")
logger.warning("Tentativa de acesso não autorizado detectada.")

end_time = time.time()
duration = end_time - start_time
logger.info(f"Requisição processada em {duration:.2f} segundos.")

if __name__ == "__main__":
    historico = []
    while True:
        try:
            entrada = input("\nComo posso ajudar? ")
            if entrada.lower() in ["sair", "exit"]: break

            resultado = agent_executor.invoke({"input": entrada, "chat_history": historico})
            
            resposta = resultado['output']
            if isinstance(resposta, list):
                resposta = resposta[0].get('text', str(resposta))
            
            print(f"\nJARVIS: {resposta}")
            
        except Exception as e:
            print(f"\n[!] Erro: {e}")
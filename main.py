import os
import time
import threading
import asyncio
from dotenv import load_dotenv

#langchain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#modules imports
from tools import get_all_jarvis_tools
from speech.speaker import JarvisSpeaker
from logs.logger import setup_logger


load_dotenv()
logger = setup_logger()

tools_do_jarvis = get_all_jarvis_tools(username="Root")

llm = ChatGoogleGenerativeAI(
    model="gemini-3-flash-preview",
    temperature=0.3,
    google_api_key=os.getenv("API_KEY_GEMINI")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é o Jarvis, um assistente de IA britânico e sofisticado. "
               "Sempre use as ferramentas para validar dados de sistema ou buscar na web."),
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
    logger.info(">>> Sistemas inicializados com sucesso, senhor.")
except Exception as e:
    logger.error(f"Erro crítico na inicialização: {e}")

# 4. Função Auxiliar para Voz em Background (Não trava o sistema)
def play_voice_background(text):
    """Executa o áudio em uma thread separada para não travar o input do usuário."""
    try:
        speaker = JarvisSpeaker()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(speaker.speak(text))
        loop.close()
    except Exception as e:
        print(f"\n[!] Ered no áudio: {e}")

# 5. Loop Principal
async def main_loop():
    historico = []
    print("\n>>> Jarvis Online. Aguardando comandos, senhor. (CTRL+C para sair)")

    while True:
        try:
            entrada = input("\nSenhor? (Comando): ")
            
            if entrada.lower() in ["sair", "exit", "desligar"]:
                print("Encerrando sistemas...")
                break

            start_time = time.time()

            resultado = agent_executor.invoke({
                "input": entrada, 
                "chat_history": historico 
            })

            duration = time.time() - start_time
            logger.info(f"Requisição processada em {duration:.2f}s")

            resposta = resultado['output']
            if isinstance(resposta, list):
                resposta = resposta[0].get('text', str(resposta))
            
            print(f"\nJARVIS: {resposta}")

            threading.Thread(target=play_voice_background, args=(resposta,), daemon=True).start()

            historico.append(("human", entrada))
            historico.append(("ai", resposta))

        except KeyboardInterrupt:
            print("\nProtocolo de encerramento ativado.")
            break
        except Exception as e:
            logger.error(f"Falha no ciclo: {e}")

if __name__ == "__main__":
    # Garante que o loop assíncrono rode corretamente
    asyncio.run(main_loop())
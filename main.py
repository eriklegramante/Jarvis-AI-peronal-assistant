import os
import time
import threading
import asyncio
from dotenv import load_dotenv
import re
import pygame

#langchain imports
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#modules imports
from tools import get_all_jarvis_tools
from speech.speaker import JarvisSpeaker
from logs.logger import setup_logger
from ui.avatar import JarvisAvatar
from speech.listener import JarvisListener

load_dotenv()
logger = setup_logger()

avatar = JarvisAvatar("ui/assets/jarvis_avatar.png")

listener = JarvisListener(model_size="tiny")  #tiny

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

def chat_thread():
    """O loop de chat agora roda aqui para não travar a interface gráfica."""
    asyncio.run(main_loop()) 

def clean_text_for_speech(text):
    """Remove caracteres de formatação Markdown e símbolos especiais para a narração."""
    text = text.replace("*", "")
    text = text.replace("#", "")
    text = text.replace("`", "")
    text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def play_voice_background(text):
    try:
        avatar.set_talking(True)
        speaker = JarvisSpeaker()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(speaker.speak(text))
        avatar.set_talking(False) 
        loop.close()
    except Exception as e:
        avatar.set_talking(False)
        print(f"\n[!] Erro no áudio/avatar: {e}")

# 5. Loop Principal
async def main_loop():
    historico = []
    print("\n>>> Jarvis Online. Aguardando comandos, senhor. (CTRL+C para sair)")

    while True:
        try:
            entrada = listener.listen()
        
            if not entrada:
                continue # Se não ouviu nada, volta a ouvir

            print(f"VOCÊ: {entrada}")
            
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

            texto_para_voz = clean_text_for_speech(resposta)
            threading.Thread(target=play_voice_background, args=(texto_para_voz,), daemon=True).start()

            historico.append(("human", entrada))
            historico.append(("ai", resposta))

        except KeyboardInterrupt:
            print("\nProtocolo de encerramento ativado.")
            break
        except Exception as e:
            logger.error(f"Falha no ciclo: {e}")

if __name__ == "__main__":
    thread_jarvis = threading.Thread(target=chat_thread, daemon=True)
    thread_jarvis.start()

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        avatar.draw()
        clock.tick(30) 

    pygame.quit()
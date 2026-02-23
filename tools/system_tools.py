from langchain_core.tools import tool
from datetime import datetime
import os

class SystemManager:
    def __init__(self, username="Senhor"):
        self.username = username

    def fetch_tools(self):
        """
        Gera e retorna a lista de ferramentas. 
        Definir as funções aqui dentro permite que elas usem o 'self.username'.
        """
        
        @tool
        def get_personal_info():
            """Gera uma saudação personalizada para o dono do Jarvis."""
            return f"Bem vindo de volta, senhor {self.username}."
        
        @tool
        def check_disk_space():
            """Verifica o espaço em disco disponível."""
            import shutil
            total, used, free = shutil.disk_usage("/")

            print(f"Espaço total: {total // (2**30)} GB")
            print(f"Espaço usado: {used // (2**30)} GB")
            print(f"Espaço livre: {free // (2**30)} GB")
    
        @tool
        def get_date(cidade: str):
            """Retorna a data e hora atual. Útil para quando o usuário pergunta que dia é hoje ou a hora."""
            data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            return f"A data e hora atual (baseada no sistema) para {cidade} é: {data_atual}"

        @tool
        def verification_user(user: str):
            """Verifica se o usuário é autorizado a usar o Jarvis."""
            # Você pode mudar "Root" para o seu nome de usuário
            usuarios_autorizados = ["root", "legramante"] 
            if user.lower() in usuarios_autorizados:
                return f"Usuário {user} verificado. Acesso concedido."
            else:
                return f"Usuário {user} não autorizado. Protocolo de segurança ativado."
            
        @tool
        def list_files(diretorio: str):
            """Lista os arquivos em um diretório específico."""
            try:
                arquivos = os.listdir(diretorio)
                return f"Arquivos em {diretorio}: {', '.join(arquivos)}"
            except Exception as e:
                return f"Erro ao listar arquivos em {diretorio}: {str(e)}"

        @tool
        def get_system_info():
            """Retorna informações básicas do sistema."""
            import platform
            info = {
                "Sistema Operacional": platform.system(),
                "Versão": platform.version(),
                "Arquitetura": platform.architecture()[0],
                "Processador": platform.processor()
            }
            return info
        
        @tool
        def get_date_time():
            """Retorna a data e hora atual do sistema."""
            return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        
        return [
            get_personal_info, 
            check_disk_space, 
            get_date, 
            verification_user, 
            list_files, 
            get_system_info,
            get_date_time
        ]
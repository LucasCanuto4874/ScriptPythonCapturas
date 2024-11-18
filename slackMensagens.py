import slack
from dotenv import load_dotenv, set_key
import os

# Conexão com o Slack
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])


# Mensagem de disco personalizado
def discoUsadoPersonalizado(discoUsado):
       client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de Bytes Enviados! (Alerta Personalizado)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {discoUsado} GB                                                 
""")
       
def discoUsadoSistema(discoUsado): 
    client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de Bytes Enviados! (Alerta de Segurança)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {discoUsado} GB                                                     
""")
    
def memoriaRamUsadaPersonalizada(memoriaUsada):
    client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de RAM! (Alerta Personalizada)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {memoriaUsada} GB                                                    
""")
    
def memoriaRamUsadaSistema(memoriaUsada):
    client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de RAM! (Alerta de Segurança)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {memoriaUsada} GB                                                   
""")
    
def usoDeCpuPersonalizado(usoCpu):
     client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de CPU! (Alerta Personalizado)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {usoCpu}%                                    
""")
     
def usoDeCpuSistema(usoCpu):
    client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de CPU! (Alerta de Segurança)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {usoCpu}%                                                     
""")
     
def frequenciaCpuPersonalizado(frequencia):
    client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de alta frenquência CPU! (Alerta Personalizado)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {frequencia} Ghz                                         
""")
    
def frequenciaCpuSistema(frequencia):
      client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de alta frenquência CPU! (Alerta de Segurança)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {frequencia} MB                                                     
""")
      
def perdaDePacotesPersonalizado(pacotesPerdidos):
    client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de alta perda de pacotes! (Alerta Personalizado)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {pacotesPerdidos} MB                                                     
""")
    
def perdaDePacotesSistema(pacotesPerdidos):
    client.chat_postMessage(channel='#alertas-dashboard-novascan', text= f"""
🚧 *Alerta Disparado de alta perda de pacotes! (Alerta de Segurança)* 🚧
    🚨 Status: Alerta Disparado!
    📊 Valor Capturado: {pacotesPerdidos} MB                                                     
""")
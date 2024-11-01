import banco as bd
import capturasComponente as cp
import dadosComponente as cd
import time as t
from textwrap import dedent
from dotenv import load_dotenv, set_key
import os

load_dotenv()

caminho = ".env"
identificadorMaquina = "CODIGO_MAQUINA"

def main():
    while True:    

        print("Insira suas informações de login")
        email = input("Insira o seu email: ")
        senha = input("Insira a sua senha: ")
        print("Verificando login aguarde!")
        
        idsRetornado = verificaoLogin(email, senha)
        
        # Pegando o id da empresa e o id do usuario logado
        codigoEmpresa = idsRetornado["fkEmpresa"]
        idUsuario = idsRetornado["idUsuario"]
        
        if codigoEmpresa and idUsuario is not None:
            print("Login efetuado com sucesso!")
           
            # Fazer a verificação de se existe uma máquina associada aquela empresa
            while True:
                print("Selecione uma opção:")
                print(dedent("""\
                    1 - Iniciar Sistema
                    2 - Sair
                """))
                
                opcao = input()
                
                if opcao == "1":

                    codigoMaquina = os.getenv(identificadorMaquina)
                    
                    if codigoMaquina is None:
                        print("Máquina não cadastrada, vamos começar o cadastro")
                        cadastrarMaquina(codigoEmpresa, idUsuario)
                    else:
                        print("Máquina já cadastrada no sistema, iniciado a captura de dados")
                        capturaDadosComponentes(codigoMaquina, idUsuario)
                if opcao == "2":
                    print("Saindo do sistema...")
                    break
                
                if opcao != "1" and opcao != "2":
                    print("Opção inválida, tente novamente!")
        else:
            print("Usuário não encontrado, tente novamente!") 
    
            
def cadastrarMaquina(fkEmpresa, idUsuario):
    nomeMaquina = input("Insira o nome da máquina: ")
    codigoEmpresa = fkEmpresa
    
    insertMaquina = bd.insert(f"INSERT INTO dispositivo (nome, fkEmpresa) VALUES ('{nomeMaquina}', {codigoEmpresa})")
    idUltimaMaquina = bd.select(f"SELECT id, nome FROM dispositivo ORDER BY id DESC LIMIT 1")
    insertMaquinaAtividade = bd.insert(f"INSERT INTO historicoAtividade (fkDispositivo, fkAtividade, dataHora) VALUES ('{idUltimaMaquina[0][0]}', 1, '{cp.bootTime()}')")
    
    if insertMaquina > 0 and insertMaquinaAtividade > 0:
        print("Máquina cadastrada com sucesso!")
        print("Começando processo de cadastrar os componentes da máquina...")
        
        # Setando o ID da máquina no arquivo .env (Simulando Session Storage)
        set_key(caminho, identificadorMaquina, str(idUltimaMaquina[0][0]))
        cadastrarComponentes(idUsuario)
    else: 
        print("Erro ao cadastrar a máquina, tente novamente!")
    
    
def cadastrarComponentes(idUsuario):
    idUltimaMaquina = bd.select(f"SELECT id, nome FROM dispositivo ORDER BY id DESC LIMIT 1")
    nomeMaquina = idUltimaMaquina[0][1]
    idMaquina = idUltimaMaquina[0][0]
    print(f"Cadastrando componentes da máquina {nomeMaquina}...")
    
    print("Cadastrando Processador...")
    bd.insert(f"INSERT INTO componente (nome, tipo, fkDispositivo) VALUES ('{cp.nomeCPU()}', 'Processador', {idMaquina})")
    
    print("Cadastrando memória ram...")
    bd.insert(f"INSERT INTO componente (nome, tipo, fkDispositivo) VALUES ('Memória Ram', 'Memória', {idMaquina})")
    
    print("Cadastrando armazenamento... ")
    bd.insert(f"INSERT INTO componente (nome, tipo, fkDispositivo) VALUES ('Memória Massa', 'Armazenamento', {idMaquina})")
    
    print("Componentes registrado com sucesso!, atualize a página da sua dashboard para listar a nova máquina cadastrada")
    
    # Verificando se a placa de rede foi cadastrada no kotlin 
    while(True):    
        print("Buscando a placa de rede do kotlin...")
        ultimoIdPlacaRede = bd.select(f"SELECT id FROM componente WHERE fkDispositivo = {idMaquina} AND tipo = 'Placa de Rede'")
        
        if(len(ultimoIdPlacaRede) <= 0):
            print("Execute o kotlin para capturar a placa de rede")
        else:
            break
        t.sleep(2)
    
    capturaDadosComponentes(idMaquina, idUsuario)


def capturaDadosComponentes(idMaquina, idUsuario):
    print("Iniciando a captura de dados dos componentes...")
    print("Caso deseje encerrar a captura pressione CTRL + C")
    print("Buscando alertas cadastrados do usuário...")
    
    # Parte da procura dos alertas criado pelo usuário
    fkDispositivo = os.getenv('CODIGO_MAQUINA')
    alertasUsuario = bd.select(f"SELECT * FROM alertaUsuario WHERE fkUsuario = {idUsuario} AND fkDispositivo = {fkDispositivo};")

    if(len(alertasUsuario) <= 0):
        print("Cadastre um alerta na sessão 'Alertas Personalizados'")
    else:
        # Listando os alertas encontrados do usuario
        i = 0
        while i < len(alertasUsuario):
            print(dedent(f"""\
                    Alertas encontrados da máquina {alertasUsuario[i][0]}:
                    Mínimo do Intervalo: {alertasUsuario[i][1]},
                    Máximo do Intervalo: {alertasUsuario[i][2]},
                    Tipo do Componente: {alertasUsuario[i][3]},
                """))
            i += 1
            
        print("Começando a captura dos dados...")
    
        # Fazendo a captura de armazenamento e inserindo no banco de dados
        i = 0 
        alerta = 0
        print("Iniciando Captura de dados do armazenamento...")
        while i < len(alertasUsuario):
            
            discoUsado = int(cp.discoUsado())
            discoTotal = int(cp.totalDisco())
            
            cd.capturaArmazenamentoTotal(discoTotal, idMaquina)
            
            if(alertasUsuario[i][3] == "Armazenamento"):
                if(discoUsado < alertasUsuario[i][1]):
                    cd.capturaArmazenamentoUsado(discoUsado, idMaquina, alerta)
            else:
                cd.capturaArmazenamentoUsado(discoUsado, idMaquina, alerta)
            i += 1
        # Capturando a memória RAM total
        print("Capturando a memória RAM total...")
        cd.capturandoMemoriaRamTotal(idMaquina)
        
        print("Iniciando Captura de dados constante da Memória RAM, CPU e Perda de Pacotes...")
        
        while True:
        # Capturando dados constante da memória RAM, CPU e Perda de Pacotes
            alerta = 0
            i = 0
            memoriaUsada = float(cp.memoriaRamUsada())
            usoCpu = float(cp.UsoCpu())
            pacotesPerdido = float(cp.pacotesPerdidos())
            
            if(len(alertasUsuario) > 0):
                
                while i < len(alertasUsuario):
                    while True:
                        if(alertasUsuario[i][3] == "Memória"):
                            if(memoriaUsada <= int(alertasUsuario[i][1]) or memoriaUsada >= int(alertasUsuario[i][2])):
                                print("Alerta disparado de Memória RAM")
                                print("Memória RAM Usada: ", memoriaUsada)
                                cd.inserirMemoriaUsada(memoriaUsada, idMaquina, alerta)
                            else:
                                print("Memória RAM Usada: ", memoriaUsada)
                                alerta = 1
                                cd.inserirMemoriaUsada(memoriaUsada, idMaquina, alerta)
                        else:
                            print("Memória RAM Usada: ", memoriaUsada)
                            cd.inserirMemoriaUsada(memoriaUsada, idMaquina, alerta)
                        
                        # Capturando uso da cpu
                        if(alertasUsuario[i][3] == "Processador"):
                            if(usoCpu <= int(alertasUsuario[i][1]) or usoCpu >= int(alertasUsuario[i][2])):
                                print("Alerta disparado de CPU")
                                print("Uso da CPU: ", usoCpu)
                                cd.capturandoUsoCpu(usoCpu, idMaquina, alerta)
                            else:
                                print("Uso da CPU: ", usoCpu)
                                alerta = 1
                                cd.capturandoUsoCpu(usoCpu, idMaquina, alerta)
                        else:
                            print("Uso da CPU: ", usoCpu)
                            cd.capturandoUsoCpu(usoCpu, idMaquina, alerta)
                        
                        
                        # Capturando perda de pacotes 
                        if(alertasUsuario[i][3] == "Placa de Rede"):
                            if(pacotesPerdido <= int(alertasUsuario[i][1]) or pacotesPerdido >= int(alertasUsuario[i][2])):
                                print("Alerta disparado de Perda de Pacotes")
                                print("Perda de Pacotes: ", pacotesPerdido)
                                cd.capturaPerdaDePacotes(pacotesPerdido, idMaquina, alerta)
                            else:
                                print("Perda de Pacotes: ", pacotesPerdido)
                                alerta = 1
                                cd.capturaPerdaDePacotes(pacotesPerdido, idMaquina, alerta)
                        else:
                            print("Perda de Pacotes: ", pacotesPerdido)
                            cd.capturaPerdaDePacotes(pacotesPerdido, idMaquina, alerta)
                            
                        t.sleep(5)    
                    i += 1
            else:
                print("Memória RAM Usada: ", memoriaUsada)
                print("Uso da CPU: ", usoCpu)
                print("Perda de Pacotes: ", pacotesPerdido)
                cd.inserirMemoriaUsada(memoriaUsada, idMaquina)
            
            t.sleep(5)
    
def verificaoLogin(email, senha):
    listaVerificacao = [email, senha]  
    resultado = bd.select(f"SELECT nome, fkEmpresa, id FROM usuario WHERE email = '{listaVerificacao[0]}' AND senha = '{listaVerificacao[1]}'")
    
    if len(resultado) <= 0:
        return None
    else:
        print(f"Usuário {resultado[0][0]} encontrado")
        idsDoBanco = {
            "fkEmpresa": resultado[0][1],
            "idUsuario": resultado[0][2]
        }
        return idsDoBanco
    
def pularLinha():
    return print("\n" * 50)
    
# Garante que o main será executado primeiro
if __name__ == "__main__":
    main()  
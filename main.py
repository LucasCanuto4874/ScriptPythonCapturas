import slack
import slackMensagens as sm
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
    
    # Listando os alertas encontrados do usuario
    i = 0
    
    if (alertasUsuario is None ):
        print("Nenhum alerta encontrado para a máquina")
        print("Iniciando a captura de dados com alertas seguros")
    else:
        while i < len(alertasUsuario):
            print(dedent(f"""\
                        Alertas encontrados da máquina {alertasUsuario[i][0]}:
                        Mínimo do Intervalo: {alertasUsuario[i][1]},
                        Máximo do Intervalo: {alertasUsuario[i][2]},
                        Tipo do Componente: {alertasUsuario[i][3]},
                        Tipo do Alerta: {alertasUsuario[i][4]}
                    """))
            i += 1
            
    # # ÁREA DE CAPTURA DE ARMAZENAMENTO
    # # Capturando o armazenamento total 
    alerta = 0
    discoTotal = cp.totalDisco()
    cd.capturaArmazenamentoTotal(discoTotal, idMaquina, alerta)
    
    
    
    
    # Capturando o armazenamento usado
    discoUsado = float(cp.discoUsado())
    discoUsadoMaximo = 500
    for armazenamentoAlerta in alertasUsuario:
        if armazenamentoAlerta[3] == "Armazenamento" and armazenamentoAlerta[4] == "Uso Armazenamento(GB)":
            if discoUsado < int(armazenamentoAlerta[1]) and discoUsado > int(armazenamentoAlerta[2]):
                print(f"Armazenamento Capturado {discoUsado} GB")
                print("Alerta de alto uso de armazenamento!!!!!")
                alerta = 1
                # Mandando mensagem para o banco e registrando o dado
                cd.capturaArmazenamentoUsado(discoUsado, idMaquina, alerta)
                
                # Disparando o alerta para o Slack
                sm.discoUsadoPersonalizado(discoUsado)
            else:
                print(f"Armazenamento Capturado {discoUsado} GB")
                alerta = 0
                cd.capturaArmazenamentoUsado(discoUsado, idMaquina, alerta)
                
        # Caso não tenha nehum alerta cadastrado ele sai do loop e começa a usar os alertas "Seguros"
        break
    if discoUsado > discoUsadoMaximo:
        print(f"Armazenamento Capturado {discoUsado} GB")
        print("Alerta de alto uso de armazenamento!!!!!")
        alerta = 1
        # Disparando o alerta para o banco 
        cd.capturaArmazenamentoUsado(discoUsado, idMaquina, alerta)
        
        # Disparando o alerta para o slack
        sm.discoUsadoSistema(discoUsado)
    else: 
        print(f"Armazenamento Capturado {discoUsado} GB")
        alerta = 0
        cd.capturaArmazenamentoUsado(discoUsado, idMaquina, alerta)
        
        
        
        
    # ÁREA DE CAPTURA DE MEMÓRIA RAM
    # Capturando a memória RAM total
    alerta = 0
    memoriaRamTotal = cp.memoriaRamTotal()
    cd.capturandoMemoriaRamTotal(memoriaRamTotal, idMaquina, alerta)
    
    # Capturando os dados constatemente
    while True:
        # Capturando a memória RAM usada
        memoriaUsada = float(cp.memoriaRamUsada())
        ramUsadaMinima = 1
        ramUsadaMaxima = 7
        
        for ramAlerta in alertasUsuario:
            if ramAlerta[3] == "Memória" and ramAlerta[4] == "Uso Memória Ram (GB)":
                if memoriaUsada < int(ramAlerta[1]) and memoriaUsada > int(ramAlerta[2]):
                    print(f"Memória RAM Capturada {memoriaUsada} GB")
                    print("Alerta de alto uso de memória RAM!!!!!")
                    alerta = 1
                    
                    # Disparando o alerta para o banco
                    cd.inserirMemoriaUsada(memoriaUsada, idMaquina, alerta)
                    
                    # Disparando o alerta para o slack
                    sm.memoriaRamUsadaPersonalizada(memoriaUsada)
                else:
                    alerta = 0
                    print(f"Memória RAM Capturada {memoriaUsada} GB")
                    cd.inserirMemoriaUsada(memoriaUsada, idMaquina, alerta)
            # Caso não tenha nehum alerta cadastrado ele sai do loop e começa a usar os alertas "Seguros"
            break
        
        if memoriaUsada < ramUsadaMinima and memoriaUsada > ramUsadaMaxima:
            print(f"Memória RAM Capturada {memoriaUsada} GB")
            print("Alerta de alto uso de memória RAM!!!!!")
            alerta = 1

            # Disparando o alerta para o banco de dados
            cd.inserirMemoriaUsada(memoriaUsada, idMaquina, alerta)
            # Disparando o alerta para o slack 
            sm.memoriaRamUsadaSistema(memoriaUsada)
        else:
            alerta = 0
            print(f"Memória RAM Capturada {memoriaUsada} GB")
            cd.inserirMemoriaUsada(memoriaUsada, idMaquina, alerta)
        
                    
                    
                    
                    
        # ÁREA DE CAPTURA DE CPU
        # Capturando o uso da CPU
        usoCpu = float(cp.UsoCpu())
        usoCpuMinimo = 10
        usoCpuMaximo = 90
        
        for cpuAlerta in alertasUsuario:
            if cpuAlerta[3] == "Processador" and cpuAlerta[4] == "Uso CPU (%)":
                if usoCpu < int(cpuAlerta[1]) and usoCpu > int(cpuAlerta[2]):
                    print(f"Uso da CPU Capturado {usoCpu} %")
                    print("Alerta de alto uso de CPU!!!!!")
                    alerta = 1

                    # Disparando o alerta para o banco de dados
                    cd.capturandoUsoCpu(usoCpu, idMaquina, alerta)
                    
                    # Disparando o alerta para o slack 
                    sm.usoDeCpuPersonalizado(usoCpu)
                    
                    print(f"Alerta disparou {usoCpu}")
                else:
                    alerta = 0
                    print(f"Uso da CPU Capturado {usoCpu} %")
                    cd.capturandoUsoCpu(usoCpu, idMaquina, alerta)
            # Caso não tenha nehum alerta cadastrado ele sai do loop e começa a usar os alertas "Seguros"
            break
        
        if usoCpu < usoCpuMinimo and usoCpu > usoCpuMaximo:
            print(f"Uso da CPU Capturado {usoCpu} %")
            print("Alerta de alto uso de CPU!!!!!")
            alerta = 1
           
            # Disparando o aletta para o banco de dados
            cd.capturandoUsoCpu(usoCpu, idMaquina, alerta)
            
            # Disparando o alerta para o slack 
            sm.usoDeCpuSistema(usoCpu)
            
        else:
            alerta = 0
            print(f"Uso da CPU Capturado {usoCpu} %")
            cd.capturandoUsoCpu(usoCpu, idMaquina, alerta)
                    
                    
        # Capturando frequencia da cpu
        frequencia = float(cp.freqCpu())
        frequenciaMaxima = 3

        for frequenciaCpuAlerta in alertasUsuario:
            if frequenciaCpuAlerta[3] == "Processador" and frequenciaCpuAlerta[4] == "Frequência CPU (Ghz)":
                if frequencia < int(frequenciaCpuAlerta[1]) and frequencia > int(frequenciaCpuAlerta[2]):
                    print(f"Frequência da CPU Capturada {frequencia} MHz")
                    print("Alerta de alta frequência da CPU!!!!!")
                    alerta = 1
                    # Disparando o alerta para o banco de dados
                    cd.capturandoFrequenciaCpu(frequencia, idMaquina, alerta)
                    
                    # Disparando o alerta para o slack
                    sm.frequenciaCpuPersonalizado(frequencia)

                else:
                    alerta = 0
                    print(f"Frequência da CPU Capturada {frequencia} MHz")
                    cd.capturandoFrequenciaCpu(frequencia, idMaquina, alerta)
            # Caso não tenha nehum alerta cadastrado ele sai do loop e começa a usar os alertas "Seguros"
            break
        if frequencia > frequenciaMaxima:
            print(f"Frequência da CPU Capturada {frequencia} MHz")
            print("Alerta de alta frequência da CPU!!!!!")
            alerta = 1
            # Disparando o alerta para o banco de dados
            cd.capturandoFrequenciaCpu(frequencia, idMaquina, alerta)
            
            # Disparando o alerta para o slack
            sm.frequenciaCpuSistema(frequencia)
        else:
            alerta = 0
            print(f"Frequência da CPU Capturada {frequencia} MHz")
            cd.capturandoFrequenciaCpu(frequencia, idMaquina, alerta)
        
    
    
    
    
    
        # ÁREA DE CAPTURA DE PERDA DE PACOTES
        # Capturando a perda de pacotes
        pacotesPerdidos = float(cp.pacotesPerdidos())
        pacotesPerdidosMaximo = 5
        
        for pacotesAlerta in alertasUsuario:
            if pacotesAlerta[3] == "Placa de Rede" and pacotesAlerta[4] == "Perda de Pacote(%)":
                if pacotesPerdidos < int(pacotesAlerta[1]) and pacotesPerdidos > int(pacotesAlerta[2]):
                    print(f"Perda de Pacotes Capturada {pacotesPerdidos} MB")
                    print("Alerta de alta perda de pacotes!!!!!")
                    alerta = 1
                    # Disparando o alerta para o banco de dados
                    cd.capturaPerdaDePacotes(pacotesPerdidos, idMaquina, alerta)
                    
                    # Disparando o alerta para o slack 
                    sm.perdaDePacotesPersonalizado(pacotesPerdidos)
                else:
                    alerta = 0
                    print(f"Perda de Pacotes Capturada {pacotesPerdidos} MB")
                    cd.capturaPerdaDePacotes(pacotesPerdidos, idMaquina, alerta)
            # Caso não tenha nehum alerta cadastrado ele sai do loop e começa a usar os alertas "Seguros"
            break
        if pacotesPerdidos > pacotesPerdidosMaximo:
            print(f"Perda de Pacotes Capturada {pacotesPerdidos} MB")
            print("Alerta de alta perda de pacotes!!!!!")
            alerta = 1
            # Disparando o alerta para o banco de dados
            cd.capturaPerdaDePacotes(pacotesPerdidos, idMaquina, alerta)
            # Disparando o alerta para o slack 
            sm.perdaDePacotesSistema(pacotesPerdidos)
        else: 
            alerta = 0
            print(f"Perda de Pacotes Capturada {pacotesPerdidos} MB")
            cd.capturaPerdaDePacotes(pacotesPerdidos, idMaquina, alerta)
            
        t.sleep(1)
    
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
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
    insertMaquinaAtividade = bd.insert(f"INSERT INTO historicoAtividade (fkDispositivo, fkAtividade, dataHora) VALUES ('{idUltimaMaquina[0][0]}', 1, current_timestamp())")
    
    # Inserindo o bootTime da ultima máquina da empresa
    bd.insert(f"INSERT INTO tempoAtividade (fkDispositivo, bootTime) VALUES ({idUltimaMaquina[0][0]}, '{cp.bootTime()}')")
    
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
    print(f"Resultado da consulta {alertasUsuario}")
    # Listando os alertas encontrados do usuario
    i = 0
    
    if not alertasUsuario:
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
            
    
    discoTotal = cp.totalDisco()
    cd.capturaArmazenamentoTotal(discoTotal, idMaquina, 0)
    
    memoriaRamTotal = cp.memoriaRamTotal()
    cd.capturandoMemoriaRamTotal(memoriaRamTotal, idMaquina, 0)
    
    while True:
        # Dados capturados
        memoriaUsada = float(cp.memoriaRamUsada())
        discoUsado = float(cp.discoUsado())
        usoCpu = float(cp.UsoCpu())
        frequencia = float(cp.freqCpu())
        pacotesPerdidos = float(cp.pacotesPerdidos())

        # Iteração sobre os componentes para capturar os alertas
        componentes = ["Armazenamento", "Memória", "Processador", "Placa de Rede"]
        for componente in componentes:
            alertaEncontrado = False  # Flag para verificar se encontrou um alerta para o componente

            if alertasUsuario:
                for alertaUsuario in alertasUsuario:
                    metrica = alertaUsuario[4]
                    limiteInferior = float(alertaUsuario[1])
                    limiteSuperior = float(alertaUsuario[2])

                    # Verifica o alerta baseado no componente e métrica
                    if componente == alertaUsuario[3] and metrica:
                        alertaEncontrado = True
                        
                        # ARMZENAMENTO
                        if componente == "Armazenamento" and metrica == "Uso Armazenamento(GB)":
                            if discoUsado <= limiteInferior or discoUsado >= limiteSuperior:
                                print("Alerta de alto uso de armazenamento!!!!!")
                                print(f"Armazenamento Capturado {discoUsado} GB")
                                cd.capturaArmazenamentoUsado(discoUsado, idMaquina, 1)
                                sm.discoUsadoPersonalizado(discoUsado)
                            else:
                                print(f"Armazenamento Capturado {discoUsado} GB")
                                cd.capturaArmazenamentoUsado(discoUsado, idMaquina, 0)

    
                        # MEMÓRIA RAM USADA
                        elif componente == "Memória" and metrica == "Uso Memória Ram (GB)":
                            if memoriaUsada <= limiteInferior or memoriaUsada >= limiteSuperior:
                                print("Alerta de alto uso de memória RAM!!!!!")
                                print(f"Memória RAM Capturada {memoriaUsada} GB")
                                cd.inserirMemoriaUsada(memoriaUsada, idMaquina, 1)
                                sm.memoriaRamUsadaPersonalizada(memoriaUsada)
                            else:
                                print(f"Memória RAM Capturada {memoriaUsada} GB")
                                cd.inserirMemoriaUsada(memoriaUsada, idMaquina, 0)



                        # PROCESSADOR (USO DE CPU)
                        elif componente == "Processador" and metrica == "Uso CPU (%)":
                            if usoCpu <= limiteInferior or usoCpu >= limiteSuperior:
                                print("Alerta de alto uso de CPU!!!!!")
                                print(f"Uso da CPU Capturado {usoCpu} %")
                                cd.capturandoUsoCpu(usoCpu, idMaquina, 1)
                                sm.usoDeCpuPersonalizado(usoCpu)
                            else:
                                print(f"Uso da CPU Capturado {usoCpu} %")
                                cd.capturandoUsoCpu(usoCpu, idMaquina, 0)


                        # PROCESSADOR (FREQUÊNCIA)
                        elif componente == "Processador" and metrica == "Frequência CPU (Ghz)":
                            if frequencia <= limiteInferior or frequencia >= limiteSuperior:
                                print("Alerta de alta frequência da CPU!!!!!")
                                print(f"Frequência da CPU Capturada {frequencia} MHz")
                                cd.capturandoFrequenciaCpu(frequencia, idMaquina, 1)
                                sm.frequenciaCpuPersonalizado(frequencia)
                            else:
                                print(f"Frequência da CPU Capturada {frequencia} MHz")
                                cd.capturandoFrequenciaCpu(frequencia, idMaquina, 0)


                        # PLACA DE REDE
                        elif componente == "Placa de Rede" and metrica == "Perda de Pacote(%)":
                            if pacotesPerdidos <= limiteInferior or pacotesPerdidos >= limiteSuperior:
                                print("Alerta de alta perda de pacotes!!!!!")
                                print(f"Perda de Pacotes Capturada {pacotesPerdidos} MB")
                                cd.capturaPerdaDePacotes(pacotesPerdidos, idMaquina, 1)
                                sm.perdaDePacotesPersonalizado(pacotesPerdidos)
                            else:
                                print(f"Perda de Pacotes Capturada {pacotesPerdidos} MB")
                                cd.capturaPerdaDePacotes(pacotesPerdidos, idMaquina, 0)

                        break  # Encerra o loop de alertas assim que um alerta for encontrado

            # Caso não tenha encontrado nenhum alerta específico para o componente, executa o alerta de segurança do sistema
            if not alertaEncontrado:
                print(f"Capturas sem alertas cadastrados para {componente}. Usando alertas de segurança.")
                
                # ALERTAS DE SEGURANÇA DO SISTEMA
                
                ramUsadaMinima = 1
                ramUsadaMaxima = 2
                
                discoUsadoMaximo = 1
                
                usoCpuMinimo = 0
                usoCpuMaximo = 0.5
                
                frequenciaMaxima = 1
                
                pacotesPerdidosMaximo = 1
                
                # ARMAZENAMENTO (ALERTA NÃO CADASTRADO PELO USUÁRIO)
                if componente == "Armazenamento":
                    if discoUsado >= discoUsadoMaximo:
                        print("Alerta de alto uso de Armazenamento!!!!!")
                        print(f"Armazenamento capturada {discoUsado}")
                        cd.capturaArmazenamentoUsado(discoUsado, idMaquina, 1)
                        sm.discoUsadoSistema(discoUsado)
                    else: 
                        print(f"Armazenamento capturada {discoUsado}")
                        cd.capturaArmazenamentoUsado(discoUsado, idMaquina, 0)

                # MEMÓRIA (ALERTA NÃO CADASTRADO PELO USUÁRIO)
                elif componente == "Memória":
                    if memoriaUsada <= ramUsadaMinima or memoriaUsada >= ramUsadaMaxima:
                        print("Alerta de alto uso de Memória Ram!!!!!")
                        print(f"Memória Ram capturada {memoriaUsada}")
                        cd.inserirMemoriaUsada(memoriaUsada, idMaquina, 1)
                        sm.memoriaRamUsadaSistema(memoriaUsada)
                    else:
                        print(f"Memória Ram capturada {memoriaUsada}")
                        cd.inserirMemoriaUsada(memoriaUsada, idMaquina, 0)


                # PROCESSADOR (ALERTA NÃO CADASTRADO PELO USUÁRIO)
                elif componente == "Processador":
                    if usoCpu <= usoCpuMinimo or usoCpu >= usoCpuMaximo:
                        print("Alerta de alto uso de CPU!!!!!")
                        print(f"Uso de CPU capturado {usoCpu}")
                        cd.capturandoUsoCpu(usoCpu, idMaquina, 1)
                        sm.usoDeCpuSistema(usoCpu)
                    else:
                        print(f"Uso de CPU capturado {usoCpu}")
                        cd.capturandoUsoCpu(usoCpu, idMaquina, 0)

                    if frequencia >= frequenciaMaxima:
                        print("Alerta de alto uso de frequência da CPU!!!!!")
                        print(f"Frequência da CPU capturada {frequencia}")
                        cd.capturandoFrequenciaCpu(frequencia, idMaquina, 1)
                        sm.frequenciaCpuSistema(frequencia)
                    else:
                        print(f"Frequência da CPU capturada {frequencia}")
                        cd.capturandoFrequenciaCpu(frequencia, idMaquina, 0)

                # PLACA DE REDE (ALERTA NÃO CADASTRADO PELO USUÁRIO)
                elif componente == "Placa de Rede":
                    if pacotesPerdidos >= pacotesPerdidosMaximo:
                        print("Alerta de alta perda de pacote!!!!!")
                        print(f"Perda de pacotes capturado {pacotesPerdidos}")
                        cd.capturaPerdaDePacotes(pacotesPerdidos, idMaquina, 1)
                        sm.perdaDePacotesSistema(pacotesPerdidos)
                    else:
                        print(f"Perda de pacotes capturado {pacotesPerdidos}")
                        cd.capturaPerdaDePacotes(pacotesPerdidos, idMaquina, 0)

        # Atraso entre iterações
        t.sleep(2)

    
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
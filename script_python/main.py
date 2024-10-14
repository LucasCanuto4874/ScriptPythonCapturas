import banco as bd
import capturasComponente as cp
import dadosComponente as cd
import time as t
from textwrap import dedent
from dotenv import load_dotenv, set_key
import os

load_dotenv()

caminho = "./script_python/.env"
identificadorMaquina = "CODIGO_MAQUINA"

def main():
    while True:    

        print("Insira suas informações de login")
        email = input("Insira o seu email: ")
        senha = input("Insira a sua senha: ")
        print("Verificando login aguarde!")
        
        codigoEmpresa = verificaoLogin(email, senha)
    
        if codigoEmpresa is not None:
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
                        cadastrarMaquina(codigoEmpresa)
                    else:
                        print("Máquina já cadastrada no sistema, iniciado a captura de dados")
                        capturaDadosComponentes(codigoMaquina)
                if opcao == "2":
                    print("Saindo do sistema...")
                    break
                
                if opcao != "1" and opcao != "2":
                    print("Opção inválida, tente novamente!")
        else:
            print("Usuário não encontrado, tente novamente!") 
    
            
def cadastrarMaquina(fkEmpresa):
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
        cadastrarComponentes()
    
    
def cadastrarComponentes():
    idUltimaMaquina = bd.select(f"SELECT id, nome FROM dispositivo ORDER BY id DESC LIMIT 1")
    nomeMaquina = idUltimaMaquina[0][1]
    idMaquina = idUltimaMaquina[0][0]
    print(f"Cadastrando componentes da máquina {nomeMaquina}...")
    
    print("Cadastrando Processador...")
    bd.insert(f"INSERT INTO componentes (nome, tipo, qtdNucleos, fkDispositivo) VALUES ('{cp.nomeCPU()}', 'Processador', {cp.qtdNucleos()}, {idMaquina})")
    
    print("Cadastrando memória ram...")
    bd.insert(f"INSERT INTO componentes (nome, tipo, memTotal, fkDispositivo) VALUES ('Memória Ram', 'Memória', {cp.memoriaRamTotal()}, {idMaquina})")
    
    print("Cadastrando armazenamento... ")
    bd.insert(f"INSERT INTO componentes (nome, tipo, armazTotal, fkDispositivo) VALUES ('Memória Massa', 'Armazenamento', {cp.totalDisco()}, {idMaquina})")
    
    print("Componentes registrado com sucesso!, atualize a página da sua dashboard para listar a nova máquina cadastrada")
    
    capturaDadosComponentes(idMaquina)


def capturaDadosComponentes(idMaquina):
    print("Iniciando a captura de dados dos componentes...")
    print("Caso deseje encerrar a captura pressione CTRL + C")

    print("Começando a captura dos dados...")
    
    # Parte da captura de dados dos componentes
    # Capturando armazenamento
    print("Iniciando Captura de dados do armazenamento...")
    cd.capturaArmazenamento(idMaquina)
    
    print("Iniciando Captura de dados constante da Memória RAM, CPU e Perda de Pacotes...")
    
    while True:
    # Capturando dados constante da memória RAM, CPU e Perda de Pacotes
        memoria = cd.capturaMemoria(idMaquina)
        cpu = cd.capturandoCpu(idMaquina)
        # perdaPacote = cd.capturaPerdaDePacotes(idMaquina)

        print("Memória RAM Usada: ", memoria[0])
        print("Memória RAM Livre: ", memoria[1])
        print("Média de Uso da CPU: ", cpu[0])
        print("Frequencia do Processador: ", cpu[1])
        # print("Perda de Pacotes: ", perdaPacote)
        
        t.sleep(1)
    
def verificaoLogin(email, senha):
    listaVerificacao = [email, senha]  
    resultado = bd.select(f"SELECT nome, fkEmpresa FROM usuario WHERE email = '{listaVerificacao[0]}' AND senha = '{listaVerificacao[1]}'")
    
    if len(resultado) <= 0:
        return None
    else:
        print(f"Usuário {resultado[0][0]} encontrado")
        fkEmpresa = resultado[0][1]
        return fkEmpresa
    
def pularLinha():
    return print("\n" * 50)
    
# Garante que o main será executado primeiro
if __name__ == "__main__":
    main()  
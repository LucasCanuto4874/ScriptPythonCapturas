import banco as bd
import capturasComponente as cp
import time as t

# Capturando dados de média de uso da CPU
def capturandoCpu(idMaquina):   
    idUltimaCpu = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Processador'")
    mediaUsoCpu = cp.mediaUsoCpu()
    frequencia = cp.freqCpu()
    
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao) VALUES ('{mediaUsoCpu}', current_timestamp(), {idUltimaCpu[0][0]}, {idMaquina}, 'Média de Uso da CPU' );")
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao) VALUES ('{frequencia}', current_timestamp(), {idUltimaCpu[0][0]}, {idMaquina}, 'Frequencia do processador' );")
    
    return mediaUsoCpu, frequencia
    
# Capturando dados da memória RAM usada e Livre
def capturaMemoria(idMaquina):
    idUltimaMemoria = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Memória'")   
    memoriaUsada = cp.memoriaRamUsada()
    memoriaLivre = cp.memoriaRamLivre()
    
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao) VALUES ('{memoriaUsada}', current_timestamp(), {idUltimaMemoria[0][0]}, {idMaquina}, 'Uso de Memória RAM');")
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao) VALUES ('{memoriaLivre}', current_timestamp(), {idUltimaMemoria[0][0]}, {idMaquina}, 'Memória RAM Livre');")
    
    return memoriaUsada, memoriaLivre
        
# Capturando dados de disco usado e livre 
def capturaArmazenamento(idMaquina):
    idUltimoArmazenamento = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Armazenamento'")
    
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao) VALUES ('{cp.discoUsado()}', current_timestamp(), {idUltimoArmazenamento[0][0]}, {idMaquina}, 'Uso de Armazenamento');")
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao) VALUES ('{cp.discoLivre()}', current_timestamp(), {idUltimoArmazenamento[0][0]}, {idMaquina}, 'Armazenamento Livre');")
    
# Capturando dados de perda de pacote na rede
def capturaPerdaDePacotes(idMaquina):
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao)  VALUES ('{cp.pacotesPerdidos()}', current_timestamp(), null, {idMaquina}, 'Perda de Pacotes');")
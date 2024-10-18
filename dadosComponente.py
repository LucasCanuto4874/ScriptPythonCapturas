import banco as bd
import capturasComponente as cp

# Capturando dados de média de uso da CPU
def capturandoCpu(idMaquina):   
    idUltimaCpu = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Processador'")
    usoCpu = cp.UsoCpu()
    frequencia = cp.freqCpu()
    
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao) VALUES ('{usoCpu}', current_timestamp(), {idUltimaCpu[0][0]}, {idMaquina}, 'Uso da CPU' );")
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao) VALUES ('{frequencia}', current_timestamp(), {idUltimaCpu[0][0]}, {idMaquina}, 'Frequencia do processador' );")
    
    return usoCpu, frequencia
    
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
    idUltimaPlacaRede = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Placa de Rede'")
    pacotesPerdidos = cp.pacotesPerdidos()
    bd.insert(f"INSERT INTO log (valor, dataHora, fkComponente, fkDispositivo, descricao)  VALUES ('{pacotesPerdidos}', current_timestamp(), {idUltimaPlacaRede[0][0]}, {idMaquina}, 'Perda de Pacotes');")
    
    return pacotesPerdidos
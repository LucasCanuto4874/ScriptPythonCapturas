import banco as bd
import capturasComponente as cp

# Capturando dados de média de uso da CPU
def capturandoCpu(idMaquina):   
    idUltimaCpu = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Processador'")
    usoCpu = cp.UsoCpu()
    frequencia = cp.freqCpu()
    
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{usoCpu}', '%', current_timestamp(), 'Uso da CPU', {idUltimaCpu[0][0]}, {idMaquina});")
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{frequencia}', 'Ghz', current_timestamp(), 'Frequencia do processador', {idUltimaCpu[0][0]}, {idMaquina});")
    
    return usoCpu, frequencia
    
# Capturando dados da memória RAM usada e Livre
def capturaMemoria(idMaquina):
    idUltimaMemoria = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Memória'")   
    memoriaUsada = cp.memoriaRamUsada()
    memoriaLivre = cp.memoriaRamLivre()
    
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{memoriaUsada}', 'GB', current_timestamp(), 'Uso de Memória RAM', {idUltimaMemoria[0][0]}, {idMaquina});")
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{memoriaLivre}', 'GB', current_timestamp(), 'Memória RAM Livre', {idUltimaMemoria[0][0]}, {idMaquina});")
    
    return memoriaUsada, memoriaLivre, 

def capturandoMemoriaRamTotal(idMaquina):
    idUltimaMemoria = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Memória'")
    memoriaRamTotal = cp.memoriaRamTotal()
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{memoriaRamTotal}', 'GB', current_timestamp(), 'Memória RAM Total', {idUltimaMemoria[0][0]}, {idMaquina});")
    
    return memoriaRamTotal
        
# Capturando dados de disco usado e livre 
def capturaArmazenamento(idMaquina):
    idUltimoArmazenamento = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Armazenamento'")
    
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{cp.discoUsado()}', 'GB', current_timestamp(), 'Uso de Armazenamento', {idUltimoArmazenamento[0][0]}, {idMaquina});")
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{cp.discoLivre()}', 'GB', current_timestamp(), 'Armazenamento Livre', {idUltimoArmazenamento[0][0]}, {idMaquina});")
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{cp.totalDisco()}', 'GB', current_timestamp(), 'Armazenamento Total', {idUltimoArmazenamento[0][0]}, {idMaquina});")
    
# Capturando dados de perda de pacote na rede
def capturaPerdaDePacotes(idMaquina):
    idUltimaPlacaRede = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Placa de Rede'")
    pacotesPerdidos = cp.pacotesPerdidos()
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo)  VALUES ('{pacotesPerdidos}', 'MB', current_timestamdp(), 'Perda de Pacotes', {idUltimaPlacaRede[0][0]}, {idMaquina});")
    
    return pacotesPerdidos
import banco as bd
import capturasComponente as cp

# Capturando dados de média de uso da CPU
def capturandoUsoCpu(usoCpu, idMaquina, alerta):   
    idUltimaCpu = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Processador'")
    
    if(alerta == 1):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{usoCpu}', '%', current_timestamp(), 'Uso da CPU', {idUltimaCpu[0][0]}, {idMaquina});")
    else:
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{usoCpu}', '%', current_timestamp(), 'Uso da CPU', {idUltimaCpu[0][0]}, {idMaquina});")

def capturandoFrequenciaCpu(frequencia, idMaquina, alerta):
    idUltimaCpu = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Processador'")
    
    if(alerta == 1):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{frequencia}', 'Ghz', current_timestamp(), 'Frequencia do processador', {idUltimaCpu[0][0]}, {idMaquina});")
    else: 
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{frequencia}', 'Ghz', current_timestamp(), 'Alerta: Alta Frequencia do processador', {idUltimaCpu[0][0]}, {idMaquina});")
    
# Capturando dados da memória RAM usada e Livre
def inserirMemoriaUsada(memoriaUsada, idMaquina, alerta):
    idUltimaMemoria = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Memória'")   
    
    if(alerta == 1):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{memoriaUsada}', 'GB', current_timestamp(), 'Uso de Memória RAM', {idUltimaMemoria[0][0]}, {idMaquina});")
    else:
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{memoriaUsada}', 'GB', current_timestamp(), 'Alerta: Uso Alto de Memória RAM', {idUltimaMemoria[0][0]}, {idMaquina});")

def capturaMemoriaLivre(memoriaLivre, idMaquina):
    idUltimaMemoria = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Memória'")   
    
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{memoriaLivre}', 'GB', current_timestamp(), 'Memória RAM Livre', {idUltimaMemoria[0][0]}, {idMaquina});")


def capturandoMemoriaRamTotal(idMaquina):
    idUltimaMemoria = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Memória'")
    memoriaRamTotal = cp.memoriaRamTotal()
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{memoriaRamTotal}', 'GB', current_timestamp(), 'Memória RAM Total', {idUltimaMemoria[0][0]}, {idMaquina});")
    
    return memoriaRamTotal
        
# Capturando dados de disco usado e livre 
def capturaArmazenamentoUsado(discoUsado, idMaquina, alerta):
    idUltimoArmazenamento = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Armazenamento'")
    if(alerta == 1):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{discoUsado}', 'GB', current_timestamp(), 'Uso de Armazenamento', {idUltimoArmazenamento[0][0]}, {idMaquina});")
    else:
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{discoUsado}', 'GB', current_timestamp(), 'Alerta: Alto uso de armazenamento', {idUltimoArmazenamento[0][0]}, {idMaquina});")
        
def capturaArmazenamentoLivre(idMaquina):
    idUltimoArmazenamento = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Armazenamento'")
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{cp.discoLivre()}', 'GB', current_timestamp(), 'Armazenamento Livre', {idUltimoArmazenamento[0][0]}, {idMaquina});")

def capturaArmazenamentoTotal(discoTotal, idMaquina):
    idUltimoArmazenamento = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Armazenamento'")
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo) VALUES ('{discoTotal}', 'GB', current_timestamp(), 'Armazenamento Total', {idUltimoArmazenamento[0][0]}, {idMaquina});")
    
    
# Capturando dados de perda de pacote na rede
def capturaPerdaDePacotes(pacotesPerdidos, idMaquina, alerta):
    idUltimaPlacaRede = bd.select("SELECT id FROM ultimoComponente WHERE tipo = 'Placa de Rede'")
    if(alerta == 1):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo)  VALUES ('{pacotesPerdidos}', 'MB', current_timestamp(), 'Perda de Pacotes', {idUltimaPlacaRede[0][0]}, {idMaquina});")
    else:
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, fkComponente, fkDispositivo)  VALUES ('{pacotesPerdidos}', 'MB', current_timestamp(), 'Alerta: Alta Perda de Pacotes', {idUltimaPlacaRede[0][0]}, {idMaquina});")
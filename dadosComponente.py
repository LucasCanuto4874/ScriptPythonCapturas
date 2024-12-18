import banco as bd
import capturasComponente as cp

# Capturando dados de média de uso da CPU
def capturandoUsoCpu(usoCpu, idMaquina, alerta):   
    idUltimaCpu = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Processador' AND fkDispositivo = {idMaquina}")
    
    if(alerta == 0):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{usoCpu}', '%', current_timestamp(), 'Uso da CPU', {alerta}, {idUltimaCpu[0][0]}, {idMaquina});")
    else:
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{usoCpu}', '%', current_timestamp(), 'Alerta: Alto uso da CPU!!', {alerta}, {idUltimaCpu[0][0]}, {idMaquina});")

def capturandoFrequenciaCpu(frequencia, idMaquina, alerta):
    idUltimaCpu = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Processador' AND fkDispositivo = {idMaquina}")
    
    if(alerta == 0):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{frequencia}', 'Ghz', current_timestamp(), 'Frequência do processador', {alerta}, {idUltimaCpu[0][0]}, {idMaquina});")
    else: 
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{frequencia}', 'Ghz', current_timestamp(), 'Alerta: Alta Frequência do processador', {alerta}, {idUltimaCpu[0][0]}, {idMaquina});")

def caputrandoNuceloCPU(nucleoCPU, idMaquina, alerta):
    idUltimaCpu = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Processador' AND fkDispositivo = {idMaquina}")
    return bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{nucleoCPU}', 'Qtd', current_timestamp(), 'Núcleos CPU', {alerta}, {idUltimaCpu[0][0]}, {idMaquina});")
        
# Capturando dados da memória RAM usada e Livre
def inserirMemoriaUsada(memoriaUsada, idMaquina, alerta):
    idUltimaMemoria = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Memória' AND fkDispositivo = {idMaquina}")   
    
    if(alerta == 0):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{memoriaUsada}', 'GB', current_timestamp(), 'Uso de Memória RAM', {alerta}, {idUltimaMemoria[0][0]}, {idMaquina});")
    else:
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{memoriaUsada}', 'GB', current_timestamp(), 'Alerta: Uso Alto de Memória RAM!!', {alerta}, {idUltimaMemoria[0][0]}, {idMaquina});")

def capturandoMemoriaRamTotal(memoriaRamTotal, idMaquina, alerta):
    idUltimaMemoria = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Memória' AND fkDispositivo = {idMaquina}")
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{memoriaRamTotal}', 'GB', current_timestamp(), 'Memória RAM Total', {alerta}, {idUltimaMemoria[0][0]}, {idMaquina});")

def capturandoMemoriaRamPorcentagem(memoriaRamTotal, idMaquina, alerta):
    idUltimaMemoria = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Memória' AND fkDispositivo = {idMaquina}")
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{memoriaRamTotal}', '%', current_timestamp(), 'Porcentagem Memória Ram', {alerta}, {idUltimaMemoria[0][0]}, {idMaquina});")
        
# Capturando dados de disco usado e livre 
def capturaArmazenamentoUsado(discoUsado, idMaquina, alerta):
    idUltimoArmazenamento = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Armazenamento' AND fkDispositivo = {idMaquina}")
    if(alerta == 0):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{discoUsado}', 'GB', current_timestamp(), 'Uso de Armazenamento', {alerta}, {idUltimoArmazenamento[0][0]}, {idMaquina});")
    else:
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{discoUsado}', 'GB', current_timestamp(), 'Alerta: Alto uso de armazenamento', {alerta}, {idUltimoArmazenamento[0][0]}, {idMaquina});")
        
def capturaArmazenamentoTotal(discoTotal, idMaquina, alerta):
    idUltimoArmazenamento = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Armazenamento' AND fkDispositivo = {idMaquina}")
 
    bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo) VALUES ('{discoTotal}', 'GB', current_timestamp(), 'Armazenamento Total', {alerta}, {idUltimoArmazenamento[0][0]}, {idMaquina});")
    
    
# Capturando dados de perda de pacote na rede
def capturaPerdaDePacotes(pacotesPerdidos, idMaquina, alerta):
    idUltimaPlacaRede = bd.select(f"SELECT id FROM ultimoComponente WHERE tipo = 'Placa de Rede' AND fkDispositivo = {idMaquina}")
    if(alerta == 0):
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo)  VALUES ('{pacotesPerdidos}', 'MB', current_timestamp(), 'Perda de Pacotes', {alerta}, {idUltimaPlacaRede[0][0]}, {idMaquina});")
    else:
        bd.insert(f"INSERT INTO log (valor, unidadeDeMedida, dataHora, descricao, eAlerta, fkComponente, fkDispositivo)  VALUES ('{pacotesPerdidos}', 'MB', current_timestamp(), 'Alerta: Alta Perda de Pacotes', {alerta}, {idUltimaPlacaRede[0][0]}, {idMaquina});")
        
    
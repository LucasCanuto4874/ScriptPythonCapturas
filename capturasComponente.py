import psutil as ps 
import cpuinfo as cp
import datetime as dt


# Capturas de processador
def nomeCPU():
    nome = cp.get_cpu_info()
    return nome["brand_raw"]

def UsoCpu():
    uso = ps.cpu_percent(interval=0.1)
    return uso

def freqCpu():
    frequencia = ps.cpu_freq().current
    return f"{frequencia / 1000:.2f}"

def qtdNucleos():
    return ps.cpu_count()

# Capturando memória RAM
def memoriaRamTotal():
    total = ps.virtual_memory().total
    
    return f"{total / (1024 ** 3):.2}" 

def memoriaRamUsada():
    total = ps.virtual_memory().used
    
    return f"{total / (1024 ** 3):.2}" 

def memoriaRamLivre():
    total = ps.virtual_memory().free
    
    return f"{total / (1024 ** 3):.2}" 

# Capturando dados de armazenamento 
def totalDisco():
    total = ps.disk_usage("/").total 
    return f"{total / (1024**3):.0f}"

def discoUsado():
    total = ps.disk_usage("/").used 
    return f"{total / (1024**3):.0f}"

def discoLivre():
    total = ps.disk_usage("/").free 
    return f"{total / (1024**3):.0f}"


#Capturando pacotes perdidos da rede 
def pacotesPerdidos():
    pacotesTotal = 0
    pacotesPerdidos = 0
    perdaPorcentagem = 0

    i = 0
    while i < 5:
        rede = ps.net_io_counters()
        #  pacotes recebidos que foram perdidos
        errin = rede.errin
        #  pacotes enviados que foram perdidos
        errout = rede.errout
        pacotesEnviado = rede.packets_sent
        pacotesRecebido = rede.packets_recv
     
        pacotesTotal += pacotesEnviado + pacotesRecebido
        pacotesPerdidos += errin + errout
     
        i += 1
     
    if pacotesPerdidos > 0:    
        perdaPorcentagem = (pacotesPerdidos / pacotesTotal) * 100 
    else:
        perdaPorcentagem = 0

    return "{:.2f}".format(perdaPorcentagem)

# Capturando o tempo de boot 
def bootTime():
    boot = ps.boot_time()
    tempoConvertido = dt.datetime.fromtimestamp(boot)
    formatado = tempoConvertido.strftime("%Y/%m/%d %H:%M:%S")
    return formatado



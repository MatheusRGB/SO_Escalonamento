import os, csv

def isNumber(value):
    try:
        float(value)
    except ValueError:
        return False
    return True

def getCSVData(file):
    if os.path.exists(file):
        data = []
        with open(file) as file:
            reader = csv.reader(file)
            filter = []
            for row in reader:
                for col in row:
                    if isNumber(col):
                        filter.append(int(col))
                data.append(filter)
                filter = []
            return data
    return False

def tempoEspera(data,newData):
    filter = getDatatime(data)
    aux, count = 0, 0
    for vet in data:
        if count == 0:
            aux = vet[0]
        else:
            aux = filter[count-1]-vet[0]
        newData.append(aux)
        count = count+1

def tempoVida(data,newData):
    filter = getDatatime(data)
    aux, count = 0, 0
    for vet in data:
        aux = filter[count]-vet[0]
        count = count+1
        newData.append(aux)

def media(data):
    aux = 0
    for i in data:
        aux = aux+i
    aux = aux/len(data)
    return aux

def getDatatime(data):
    filter = []
    aux = 0
    for vet in data:
        aux = aux+vet[1]
        filter.append(aux)
    return filter

def fcfs(data):
    vida = []
    espera = []
    tempoVida(data,vida)
    tempoEspera(data,espera)
    print(media(vida))
    print(media(espera))
    runtimeDiagram(data,data,False)

def sjf(data):
    vida = []
    espera = []
    filter = []
    result = []
    duracao,inicio,time,count = 0,0,0,0
    #Verifica de dois em dois processos qual é o menor
    for vet in data:
        filter.append(vet)
        if len(filter) > 1:
            for a in filter:
                if count == 0:
                    inicio = a[0]
                    duracao = a[1]
                    time = count
                else:
                    #Caso o inicio dos dois processos da fila sejam igauis
                    if inicio == a[0] and duracao > a[1]:
                        duracao = a[1]
                        time = count
                    else:
                        #Demais casos pega o menor da fila
                        if duracao > a[1]:
                            duracao = a[1]
                            time = count
                count = count+1
            result.append(filter[time])
            count = 0
            filter.pop(time)
    result.append(filter[0])
    tempoVida(result,vida)
    tempoEspera(result,espera)
    print(media(vida))
    print(media(espera))
    runtimeDiagram(result,data,False)

def updateorder(data,vector,qtd, time):
    for i in range(qtd, len(data)):
        if data[i][0] <= time:
            vector.append(i)
    if time > 0:        
        last = vector[0]
        vector.pop(0)
        vector.append(last)
    return vector

    
def rrquantum(data,q):
    #Inicialização dos vetores e variaveis
    result = []
    filter = []
    order = []
    process = []
    life_time = []
    wait_time = []
    is_alive = []
    execution = []
    max = len(data)
    clock = 0

    #Preenchimento dos vetores com 0
    for i in range(max):
        wait_time.append(0)  
        life_time.append(0) 
        is_alive.append(0) 
        process.append(data[i][1])

    #Percorre os processos
    for i in range(100):
        #atualiza a ordem de processos a serem executados
        order = updateorder(data,order, len(order), clock)
        select = order[0]

        #Verifica se o processos ainda nao foi finalizado e realiza seu processamento
        if is_alive[select] == 0:
            #Caso seja a ultima execução desse processo
            if process[select] <= 2:
                time = process[select]
                process[select] = process[select] - process[select]

                for j in range(max):
                    if j != select and is_alive[j] == 0:
                        wait_time[j] = wait_time[j] + time
                
                execution.append(select)
                clock = clock + time  

                is_alive[select] = -1
                life_time[select] = clock             
            #Caso o processo nao finalize apos o processamento
            else:
                process[select] = process[select] - q

                for j in range(max):
                    if j != select and is_alive[j] == 0:
                        wait_time[j] = wait_time[j] + q
                execution.append(select)       

                clock = clock + q

                if process[select] == 0:
                    is_alive[select] = -1 
                    life_time[select] = clock       
                
    #Calcula o tempo de espera e tempo de vida
    for i in range(max):
        wait_time[i] = wait_time[i] - data[i][0]
        life_time[i] = life_time[i] - data[i][0]

    print(media(life_time))
    print(media(wait_time))

    #transforma a ordem de execução, no vetor que sera utilizado como entrada para calcular a media de tempo de vida e espera
    for i in execution:
        newData = tableCopy(data)
        count = 0
        #Caso exita um processo repetido ele tirar adicinar um contador na variavel exec
        for obj in filter:
            if obj["pos"] == i:
                count = count+1
        aux = {
            "pos":i,
            "exec":count
        }
        filter.append(aux)
        #Conforme o exec for maior menor é o valor da duração(para previnir caso o a duração seja menor que 2 não inserir 2 o restante que falta)
        if q*count == 0 and newData[i][1] >= q:
            newData[i][1] = q
        else:
            a = data[i][1]
            newData[i][1] = a-q*count
            if newData[i][1] > q:
                newData[i][1] = q
        result.append(newData[i])

    runtimeDiagram(result,False,execution)

def tableCopy(data):
    newData = []
    for row in range(len(data)):
        filter = []
        for col in data[row]:
            filter.append(col)
        newData.append(filter)
    return newData

def runtimeDiagram(data,oldData,position):
    aux = ""
    count,size,tempo,index = 0,0,0,0
    filter = []
    #Cria a primeira linha onde exibe o tempo de execução dos processos
    for vet in data:
        size = size+int(vet[1])
        teste = []
        filter.append(teste)

    for i in range(size):
        if len(str(i)) > 1:
            aux = aux+" T"+str(i)+" "
        else:
            aux = aux+"  T"+str(i)+" "
    print("Processo  "+aux)
    #Adiciona espaços ou - ou ### no diagrama
    for vet in filter:
        for i in range(tempo):
            vet.append("   ")
        for i in range(data[index][1]):
            vet.append("###")
        if len(vet) < size:
            for j in range(size-len(vet)):
                vet.append("---")
        tempo = tempo+data[index][1]
        index = index+1
    #Exibe o grafico com os espaços necessarios e a string completa de cada processo
    index = 0
    for i in range(len(data)):
        if position:
            print(str(position[i]+1)+"        ",end="")
        else:
            for vet in oldData:
                index = index+1
                if vet == data[i]:
                    print(str(index)+"        ",end="")
                    index = 0
                    break
        string = ""
        for s in filter[i]:
            string = string+"  "+str(s)
        print(string)

result = getCSVData("teste.csv")

print("-------------")
fcfs(result)
print("-------------")
sjf(result)
print("-------------")
rrquantum(result,2)
print("-------------")

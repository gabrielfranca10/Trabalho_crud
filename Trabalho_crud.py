import os
os.system('cls')

def salvar_treino(treino):
    with open("treinos.txt", "a") as file:
        file.write(f"{treino['Data']},{treino['Distância']},{treino['Tempo']},{treino['Localização']},{treino['Clima']}\n")

def carregar_treinos():
    treinos = []
    try:
        with open("treinos.txt", "r") as file:
            for linha in file:
                data, distancia, tempo, localizacao, clima = linha.strip().split(",")
                treinos.append({
                    "Data": data,
                    "Distância": float(distancia),
                    "Tempo": int(tempo),
                    "Localização": localizacao,
                    "Clima": clima
                })
    except FileNotFoundError:
        print("Arquivo de treinos não encontrado. Um novo será criado ao adicionar dados.")
    except ValueError:
        print("Erro ao processar dados do treino. Verifique o formato do arquivo.")
    return treinos

def adicionar_treino():
    try:
        data = input("Digite a data (DD/MM/AAAA): ")
        distancia = float(input("Digite a distância em km: "))
        tempo = int(input("Digite o tempo em minutos: "))
        localizacao = input("Digite a localização: ")
        clima = input("Digite as condições climáticas: ")

        treino = {
            "Data": data,
            "Distância": distancia,
            "Tempo": tempo,
            "Localização": localizacao,
            "Clima": clima
        }
        salvar_treino(treino)
        print("Treino registrado com sucesso!")
    except ValueError as e:
        print(f"Erro: {e}. Insira um número válido para distância e tempo.")

def visualizar_treinos():
    treinos = carregar_treinos()
    if not treinos:
        print("Nenhum treino registrado ainda.")
    else:
        localizacoes = {}
        for treino in treinos:
            if treino["Localização"] not in localizacoes:
                localizacoes[treino["Localização"]] = []
            localizacoes[treino["Localização"]].append(treino)

        for localizacao, treinos_local in localizacoes.items():
            print(f"\nLocalização: {localizacao}")
            for treino in treinos_local:
                print(f"  Data: {treino['Data']}, Distância: {treino['Distância']} km, Tempo: {treino['Tempo']} min, Clima: {treino['Clima']}")

def atualizar_treino():
    data = input("Digite a data do treino que deseja atualizar (DD/MM/AAAA): ")
    treinos = carregar_treinos()
    encontrado = False
    for treino in treinos:
        if treino["Data"] == data:
            try:
                treino["Distância"] = float(input("Nova distância em km: "))
                treino["Tempo"] = int(input("Novo tempo em minutos: "))
                treino["Localização"] = input("Nova localização: ")
                treino["Clima"] = input("Novas condições climáticas: ")
                encontrado = True
                break
            except ValueError:
                print("Erro: Insira um número válido para distância e tempo.")
                return
    if encontrado:
        with open("treinos.txt", "w") as file:
            for t in treinos:
                file.write(f"{t['Data']},{t['Distância']},{t['Tempo']},{t['Localização']},{t['Clima']}\n")
        print("Treino atualizado com sucesso!")
    else:
        print("Treino não encontrado.")

def excluir_treino():
    data = input("Digite a data do treino que deseja excluir (DD/MM/AAAA): ")
    treinos = carregar_treinos()
    treinos = [treino for treino in treinos if treino["Data"] != data]
    
    if len(treinos) < len(carregar_treinos()):
        with open("treinos.txt", "w") as file:
            for treino in treinos:
                file.write(f"{treino['Data']},{treino['Distância']},{treino['Tempo']},{treino['Localização']},{treino['Clima']}\n")
        print("Treino excluído com sucesso!")
    else:
        print("Treino não encontrado.")

def filtrar_por_distancia():
    try:
        distancia_min = float(input("Digite a distância mínima (km): "))
        distancia_max = float(input("Digite a distância máxima (km): "))
        treinos = carregar_treinos()
        filtrados = [treino for treino in treinos if distancia_min <= treino["Distância"] <= distancia_max]
        if filtrados:
            for treino in filtrados:
                print(f"Data: {treino['Data']}, Distância: {treino['Distância']} km, Tempo: {treino['Tempo']} min")
        else:
            print("Nenhum treino encontrado nesse intervalo.")
    except ValueError:
        print("Erro: Insira um número válido para distância. Certifique-se de usar apenas números")


def filtrar_por_tempo():
    try:
        tempo_min = int(input("Digite o tempo mínimo (min): "))
        tempo_max = int(input("Digite o tempo máximo (min): "))

        if tempo_min < 0 or tempo_max < 0:
            print("Erro: O tempo não pode ser negativo.")
            return

        treinos = carregar_treinos()
        filtrados = [treino for treino in treinos if tempo_min <= treino["Tempo"] <= tempo_max]

        if filtrados:
            print(f"\n{len(filtrados)} treino(s) encontrado(s):")
            for treino in filtrados:
                print(f"Data: {treino['Data']}, Distância: {treino['Distância']} km, Tempo: {treino['Tempo']} min")
        else:
            print("Nenhum treino encontrado nesse intervalo de tempo.")

    except ValueError:
        print("Erro: Insira um número válido para tempo.")

def calcular_media():
    treinos = carregar_treinos()

    if not treinos:
        print("Nenhum treino registrado para calcular a média.")
        return

    total_distancia = 0  
    total_tempo = 0  
    total_pace = 0  
    num_treinos = len(treinos)  

    
    for treino in treinos:
        total_distancia += treino["Distância"]
        total_tempo += treino["Tempo"]

        if treino["Distância"] > 0:
            pace = treino["Tempo"] / treino["Distância"]
        else:
            pace = 0

        total_pace += pace

    media_distancia = total_distancia / num_treinos
    media_tempo = total_tempo / num_treinos
    media_pace = total_pace / num_treinos

    print(f"Média de distância: {media_distancia:.2f} km")
    print(f"Média de tempo: {media_tempo:.2f} min")
    print(f"Média de pace: {media_pace:.2f} min/km")

def definir_meta():
    tipo = input("Digite o tipo de meta (distância/tempo): ").strip().lower()
    if tipo != "distancia" and tipo != "tempo":
        print('Opção inválida')
        return
    valor = input("Digite o valor da meta: ")
    meta = f"{tipo},{valor}\n"
    with open("metas.txt", "w") as file:
        file.write(meta)
    print("Meta definida com sucesso!")

def verificar_meta():
    try:
        with open("metas.txt", "r") as file:
            tipo, valor = file.readline().strip().split(",")
            valor = float(valor) if tipo == "distancia" else int(valor)

        treinos = carregar_treinos()
        tipo = tipo.lower()
        if tipo == "distancia":
            total = sum(treino["Distância"] for treino in treinos)
        else: 
            total = sum(treino["Tempo"] for treino in treinos)

        if total >= valor:
            print("Meta atingida!")
        else:
            print(f"Ainda faltam {valor - total:.2f} para atingir a meta.")
    except FileNotFoundError:
        print("Nenhuma meta definida.")
    except ValueError:
        print("Erro ao verificar a meta. Verifique o formato do arquivo de metas.")

def sugerir_treino():
    treinos = carregar_treinos()
    if treinos:
        treino = treinos[len(treinos) // 2]
        print(f"Sugestão de treino - Distância: {treino['Distância']} km, Tempo: {treino['Tempo']} min")
    else:
        print("Nenhum treino disponível para sugestão.")

def menu():
    while True:
        print("\n----- Sistema de Gerenciamento de Treinos -----")
        print("1. Adicionar treino")
        print("2. Visualizar treinos")
        print("3. Atualizar treino")
        print("4. Excluir treino")
        print("5. Filtrar por distância")
        print("6. Filtrar por tempo")
        print("7. Calcular média de distância e tempo")
        print("8. Definir meta")
        print("9. Verificar meta")
        print("10. Sugerir treino aleatório")
        print("0. Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_treino()
        elif opcao == "2":
            visualizar_treinos()
        elif opcao == "3":
            atualizar_treino()
        elif opcao == "4":
            excluir_treino()
        elif opcao == "5":
            filtrar_por_distancia()
        elif opcao == "6":
            filtrar_por_tempo()
        elif opcao == "7":
            calcular_media()
        elif opcao == "8":
            definir_meta()
        elif opcao == "9":
            verificar_meta()
        elif opcao == "10":
            sugerir_treino()
        elif opcao == "0":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")
menu()
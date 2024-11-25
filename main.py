import customtkinter as ctk
import requests
from tkinter import *
from PIL import Image  

# Configuração inicial do customtkinter
ctk.set_appearance_mode("dark")  # Tema escuro
ctk.set_default_color_theme("blue")  # Tema azul

# Lista de criptomoedas configuradas
CRIPTO_CONFIGURADAS = ["bitcoin", "ethereum", "cardano"]

# Função para buscar cotações
def atualizar_cotacoes():
    try:
        # Converte a lista de criptos em uma string separada por vírgulas
        criptos = ",".join(CRIPTO_CONFIGURADAS)
        
        # URL da API
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={criptos}&vs_currencies=usd"
        response = requests.get(url)
        dados = response.json()
        
        # Atualizar resultados
        resultados = []
        for cripto, valores in dados.items():
            price = valores.get("usd", "N/A")
            resultados.append(f"{cripto.capitalize()}: ${price}")
        
        label_resultado.configure(text="\n".join(resultados))
    except Exception as e:
        label_resultado.configure(text="Erro ao buscar cotações")
        print(f"Erro: {e}")

# Função para adicionar uma nova criptomoeda à lista configurada
def adicionar_cripto():
    nova_cripto = entrada_cripto.get().lower().strip()  # Obtém a entrada do usuário
    if nova_cripto and nova_cripto not in CRIPTO_CONFIGURADAS:
        CRIPTO_CONFIGURADAS.append(nova_cripto)  # Adiciona a criptomoeda à lista
        entrada_cripto.delete(0, END)  # Limpa o campo de entrada
        atualizar_cotacoes()  # Atualiza as cotações
    else:
        label_resultado.configure(text="Criptomoeda já adicionada ou entrada inválida!")

# Criação da interface gráfica
janela = ctk.CTk()
janela.title("Cotações de Criptomoedas")
janela.geometry("700x500")
janela.resizable(False, False)

# Carregar imagem com PIL e usar CTkImage
try:
    img_pillow = Image.open("cripto.png")  # Certifique-se de que o caminho para a imagem está correto
    img = ctk.CTkImage(light_image=img_pillow, dark_image=img_pillow, size=(250, 250))  # Redimensionar a imagem
    label_img = ctk.CTkLabel(janela, image=img, text="")
    label_img.place(x=5, y=65)
except Exception as e:
    print(f"Erro ao carregar imagem: {e}")

# Frame para exibir as cotações


# Título
label_titulo = ctk.CTkLabel(master=janela, text="Cotações de Criptomoedas", font=("Arial", 20, "bold"))
label_titulo.pack(pady=20)

label_resultado = ctk.CTkLabel(master=janela, text="", font=("Arial", 16), justify="left")
label_resultado.pack(pady=50, padx=50)

# Entrada para adicionar novas criptomoedas
entrada_cripto = ctk.CTkEntry(janela, width=300, placeholder_text="Digite o nome da criptomoeda")
entrada_cripto.place(relx=0.5, rely=0.75, anchor="center", )

botao_adicionar = ctk.CTkButton(
    master=janela, text="Adicionar Criptomoeda", command=adicionar_cripto
)
botao_adicionar.place(relx=0.5, rely=0.82, anchor="center")

# Botão de Atualizar
botao_atualizar = ctk.CTkButton(master=janela, text="Atualizar Cotações", command=atualizar_cotacoes)
botao_atualizar.place(relx=0.5, rely=0.89, anchor="center")

# Rodapé
label_rodape = ctk.CTkLabel(master=janela, text="Powered by Bernardo Martins", font=("Arial", 12))
label_rodape.place(relx=0.5, rely=0.95, anchor="center")

# Atualiza automaticamente ao iniciar
atualizar_cotacoes()

# Iniciar a interface gráfica
janela.mainloop()

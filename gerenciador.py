import tkinter as tk
from tkinter import messagebox
from urllib.parse import urlparse
import subprocess
import os

def descobrir_estrategia(url):
    dominio = urlparse(url).netloc.lower()
    # Lojas pesadas -> Playwright
    if any(loja in dominio for loja in ["amazon", "a.co", "mercadolivre", "magazineluiza"]):
        return "avancado"
    return "nao-avancado"

def processar_link():
    url = entrada_url.get().strip()
    
    if not url:
        messagebox.showwarning("Aviso", "Por favor, cole um link válido!")
        return
        
    estrategia = descobrir_estrategia(url)
    janela.destroy()
    
    print(f"\n==================================================")
    print(f"⚙️ ENVIANDO LINK PARA O MONITOR {estrategia.upper()}...")
    print(f"==================================================\n")

    # 💡 REPASSE DINÂMICO: Passamos a 'url' como o próximo item da lista no subprocess.run
    if estrategia == "avancado":
        arquivo = "monitor-avancado.py"
    else:
        arquivo = "monitor-nao-avancado.py"

    if os.path.exists(arquivo):
        subprocess.run(["python", arquivo, url])
    else:
        print(f"❌ Erro: O arquivo '{arquivo}' não foi encontrado nesta pasta.")

# --- INTERFACE TKINTER ---
janela = tk.Tk()
janela.title("Busca Preço - Orquestrador")
janela.geometry("550x200")
janela.configure(bg="#2c3e50")

rotulo = tk.Label(janela, text="Cole o link do produto abaixo para iniciar:", font=("Arial", 11, "bold"), bg="#2c3e50", fg="#ecf0f1")
rotulo.pack(pady=20)

entrada_url = tk.Entry(janela, width=60, font=("Arial", 10))
entrada_url.pack(pady=5)
entrada_url.focus()

botao = tk.Button(janela, text="Analisar Preço 🚀", command=processar_link, font=("Arial", 10, "bold"), bg="#27ae60", fg="white", width=20, height=2)
botao.pack(pady=20)

janela.mainloop()
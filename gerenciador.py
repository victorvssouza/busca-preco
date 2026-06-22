import tkinter as tk
from tkinter import messagebox
from urllib.parse import urlparse, quote
import subprocess
import os
import json

LOJAS_ALVO = ["amazon", "mercadolivre", "magazineluiza"]

def descubrir_estrategia(url):
    dominio = urlparse(url).netloc.lower()
    if any(loja in dominio for loja in ["amazon", "a.co", "mercadolivre", "magazineluiza"]):
        return "avancado"
    return "nao-avancado"

def processar_link():
    url = entrada_url.get().strip()
    if not url:
        messagebox.showwarning("Aviso", "Por favor, cole um link válido!")
        return
        
    estrategia = descubrir_estrategia(url)
    janela.destroy()
    
    if os.path.exists("compartilhado.json"):
        os.remove("compartilhado.json")
    
    print(f"\n==================================================")
    print(f"[ETAPA 1] EXTRAINDO PRODUTO DO LINK ORIGINAL...")
    print(f"==================================================\n")

    arquivo = "monitor-avancado.py" if estrategia == "avancado" else "monitor-nao-avancado.py"

    if os.path.exists(arquivo):
        subprocess.run(["python", arquivo, url])
    else:
        print(f"❌ Erro Crítico: O arquivo '{arquivo}' não foi encontrado.")
        return

    if not os.path.exists("compartilhado.json"):
        print("❌ Erro: O monitor não conseguiu extrair ou salvar os dados do link de origem.")
        return

    with open("compartilhado.json", "r", encoding="utf-8") as f:
        dados_origem = json.load(f)
        
    titulo = dados_origem["produto"]
    preco_origem = dados_origem["preco"]
    loja_origem = dados_origem["loja_origem"]
    
    # Filtro inteligente de palavras irrelevantes
    palavras = titulo.split()
    palavras_filtradas = [p for p in palavras if p.lower() not in ["fone", "de", "ouvido", "para", "com", "jogos", "relogio", "masculino", "hd", "smart"]]
    
    if len(palavras_filtradas) >= 2:
        termo_busca = " ".join(palavras_filtradas[:3])
    else:
        termo_busca = " ".join(palavras[:4])
        
    termo_busca = termo_busca.replace(",", "").replace("-", "").replace(":", "").strip()
    termo_codificado = quote(termo_busca)

    print(f"\n==================================================")
    print(f"[ETAPA 2] INICIANDO BUSCA CRUZADA AUTOMÁTICA")
    print(f"Termo Gerado para Pesquisa: '{termo_busca}'")
    print(f"==================================================\n")

    ranking_precos = [{"loja": loja_origem.upper(), "preco": preco_origem, "tipo": "Link Fornecido"}]

    for loja in LOJAS_ALVO:
        if loja == loja_origem:
            continue
            
        print(f"🔍 Varrendo marketplace: {loja.upper()}...")
        
        if loja == "amazon":
            url_busca = f"https://www.amazon.com.br/s?k={termo_codificado}"
        elif loja == "mercadolivre":
            url_busca = f"https://lista.mercadolivre.com.br/{termo_codificado.replace('%20', '-')}"
        elif loja == "magazineluiza":
            url_busca = f"https://www.magazineluiza.com.br/busca/{termo_codificado}/"

        if os.path.exists("compartilhado.json"): 
            os.remove("compartilhado.json")

        subprocess.run(["python", "monitor-avancado.py", url_busca])

        if os.path.exists("compartilhado.json"):
            with open("compartilhado.json", "r", encoding="utf-8") as f:
                dados_busca = json.load(f)
            ranking_precos.append({"loja": loja.upper(), "preco": dados_busca["preco"], "tipo": "Pesquisa Automática"})
        else:
            print(f"⚠️ Aviso: Não foi possível capturar resultados na busca da {loja.upper()}")

    ranking_ordenado = sorted(ranking_precos, key=lambda x: x["preco"])

    print(f"\n==================================================")
    print(f"🏆 RANKING COMPARATIVO FINAL (Menor Preço -> Maior)")
    print(f"==================================================")
    for posicao, item in enumerate(ranking_ordenado, start=1):
        print(f"{posicao}º Lugar - {item['loja']}: R$ {item['preco']:.2f} ({item['tipo']})")
    print(f"==================================================\n")

janela = tk.Tk()
janela.title("Busca Preço - Comparador de Marketplaces")
janela.geometry("550x200")
janela.configure(bg="#2c3e50")

rotulo = tk.Label(janela, text="Cole o link do produto abaixo para iniciar o monitoramento:", font=("Arial", 11, "bold"), bg="#2c3e50", fg="#ecf0f1")
rotulo.pack(pady=20)
entrada_url = tk.Entry(janela, width=60, font=("Arial", 10))
entrada_url.pack(pady=5)
entrada_url.focus()

botao = tk.Button(janela, text="Comparar Preços 🚀", command=processar_link, font=("Arial", 10, "bold"), bg="#e67e22", fg="white", width=20, height=2)
botao.pack(pady=20)

janela.mainloop()
import requests
from bs4 import BeautifulSoup
import json
import sys # 💡 Importante para receber o link do gerenciador

if len(sys.argv) > 1:
    URL = sys.argv[1]
else:
    URL = "https://www.millenamoveiseeletro.com.br/colchao/..."

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}

def extrair_dados_produto():
    print("Acessando o site via método rápido...")
    resposta = requests.get(URL, headers=HEADERS)
    
    if resposta.status_code == 200:
        sopa = BeautifulSoup(resposta.text, "html.parser")
        script_dados = sopa.find("script", type="application/ld+json")
        
        if script_dados:
            try:
                dados_json = json.loads(script_dados.string)
                nome_produto = dados_json.get("name")
                ofertas = dados_json.get("offers", {})
                preco_puro = ofertas.get("price")
                
                if nome_produto and preco_puro:
                    preco_decimal = float(preco_puro)
                    print("\n🎉 PRODUTO ENCONTRADO COM SUCESSO!")
                    print(f"Produto: {nome_produto}")
                    print(f"Preço: R$ {preco_decimal:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
                    return
            except Exception:
                pass
        
        print("\n❌ Não foi possível extrair dados estruturados deste link leve.")
    else:
        print(f"\n❌ Erro de status: {resposta.status_code}")

if __name__ == "__main__":
    extrair_dados_produto()
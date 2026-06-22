import asyncio
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from mapeamento import CONFIG_LOJAS

# 💡 A LINHA QUE FALTAVA PARA CORRIGIR O ERRO:
from playwright.async_api import async_playwright

# Importando o mapa do seu arquivo mapeamento.py
from mapeamento import CONFIG_LOJAS

URL = "https://www.amazon.com.br/TAT2500BK-00-Bluetooth-Cancelamento-Microfone/dp/B0FVGQ8DD4/?_encoding=UTF8&pd_rd_w=txKaM&content-id=amzn1.sym.9d4cd3f8-955c-4000-9b8a-43f9dce62737%3Aamzn1.symc.050ea944-f1cf-4610-b462-3b604f2f4082&pf_rd_p=9d4cd3f8-955c-4000-9b8a-43f9dce62737&pf_rd_r=W0M0150S5A3QGCAF9G74&pd_rd_wg=2bc2K&pd_rd_r=67ef76ec-791f-4658-861c-58fed2b3f495&ref_=pd_hp_d_btf_ci_mcx_mr_ca_id_hp_d"

def descobrir_loja(url):
    dominio = urlparse(url).netloc.lower()
    if "amazon" in dominio or "a.co" in dominio: return "amazon"
    if "mercadolivre" in dominio: return "mercadolivre"
    if "magazineluiza" in dominio: return "magazineluiza"
    return None

# ⚡ MÉTODO RÁPIDO: Tenta extrair dados via JSON estruturado (Sem abrir navegador)
def tentar_metodo_rapido(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        resposta = requests.get(url, headers=headers, timeout=10)
        if resposta.status_code == 200:
            sopa = BeautifulSoup(resposta.text, "html.parser")
            script_dados = sopa.find("script", type="application/ld+json")
            if script_dados:
                dados_json = json.loads(script_dados.string)
                # Aceita dicionários simples ou listas de JSONs estruturados
                if isinstance(dados_json, list): dados_json = dados_json[0]
                
                nome = dados_json.get("name")
                ofertas = dados_json.get("offers", {})
                preco = ofertas.get("price") if not isinstance(ofertas, list) else ofertas[0].get("price")
                
                if nome and preco:
                    return {"nome": nome, "preco": float(preco), "metodo": "JSON-LD (Rápido)"}
    except Exception:
        pass
    return None

# 🤖 MÉTODO AVANÇADO: Abre o navegador oculto ou visível caso o rápido falhe
async def tentar_metodo_avancado(url, loja):
    async with async_playwright() as p:
        navegador = await p.chromium.launch(
            headless=False, 
            args=["--disable-blink-features=AutomationControlled", "--disable-infobars"]
        )
        contexto = await navigator.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="pt-BR",
            timezone_id="America/Sao_Paulo"
        )
        pagina = await contexto.new_page()
        await pagina.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        await pagina.goto(url, wait_until="domcontentloaded")
        await asyncio.sleep(6) # 6 segundos igual ao seu avançado
        html = await pagina.content()
        await navegador.close()
        
        sopa = BeautifulSoup(html, "html.parser")
        regras = CONFIG_LOJAS[loja]
        
        tag_titulo = sopa.find(**regras["tag_titulo"])
        tag_preco = sopa.find(**regras["tag_preco"])
        
        if tag_titulo and tag_preco:
            nome = tag_titulo.get_text().strip()
            preco_bruto = tag_preco.get("content") if tag_preco.has_attr("content") else tag_preco.get_text()
            
            # Limpeza cirúrgica do preço
            preco_limpo = preco_bruto.replace("R$", "").replace(".", "").replace(",", ".").strip()
            
            # 💡 A CORREÇÃO AQUI: Se for Amazon, isola o primeiro bloco de texto antes dos espaços/quebras de linha
            if loja == "amazon":
                preco_limpo = preco_limpo.split()[0]
                
            return {"nome": nome, "preco": float(preco_limpo), "metodo": "Playwright (HTML Dinâmico)"}
    return None

async def rodar_monitor():
    loja = descobrir_loja(URL)
    if not loja:
        print("❌ Loja não suportada.")
        return

    print(f"🚀 Iniciando monitoramento para: {loja.upper()}")
    
    # Executa a tentativa rápida primeiro
    print("⏳ Tentando extração rápida por API invisível/JSON...")
    resultado = tentar_metodo_rapido(URL)
    
    # Se falhar, aciona o Plano B automaticamente
    if not resultado:
        print("⚠️ Método rápido bloqueado ou indisponível. Acionando navegador camuflado...")
        resultado = await tentar_metodo_avancado(URL, loja)
        
    if resultado:
        print(f"\n🎉 PRODUTO EXTRAÍDO VIA: {resultado['metodo']}")
        print(f"Produto: {resultado['nome'][:60]}...")
        print(f"Preço: R$ {resultado['preco']:.2f}")
    else:
        print("\n❌ Falha crítica: Nenhum dos métodos conseguiu furar o bloqueio do site.")

if __name__ == "__main__":
    asyncio.run(rodar_monitor())
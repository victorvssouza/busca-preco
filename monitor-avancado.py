import asyncio
import sys  # 💡 Biblioteca nativa necessária para ler o link enviado
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from mapeamento import CONFIG_LOJAS

# 💡 CAPTURA DINÂMICA: Verifica se o gerenciador enviou um link. 
# Se não enviou (você rodou direto o monitor), usa o link padrão de teste abaixo.
if len(sys.argv) > 1:
    URL = sys.argv[1]
else:
    URL = "https://www.amazon.com.br/TAT2500BK-00-Bluetooth-Cancelamento-Microfone/dp/B0FVGQ8DD4/"

def descobrir_loja(url):
    dominio = urlparse(url).netloc.lower()
    if "amazon" in dominio or "a.co" in dominio:
        return "amazon"
    if "mercadolivre" in dominio:
        return "mercadolivre"
    if "magazineluiza" in dominio:
        return "magazineluiza"
    return None

async def rodar_monitor():
    loja_detectada = descobrir_loja(URL)
    if not loja_detectada:
        print("❌ Loja não suportada ou não identificada no link.")
        return

    print(f"Iniciando navegador... 🤖 Modo Correto Ativado: {loja_detectada.upper()}")
    
    async with async_playwright() as p:
        navegador = await p.chromium.launch(
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--disable-infobars"]
        )
        
        contexto = await navegador.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="pt-BR",
            timezone_id="America/Sao_Paulo"
        )
        pagina = await contexto.new_page()
        await pagina.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print(f"Acessando a página da {loja_detectada.upper()}...")
        await pagina.goto(URL, wait_until="domcontentloaded")
        
        print("Aguardando estabilização da página (6 segundos)...")
        await asyncio.sleep(6) 
        
        html = await pagina.content()
        await navegador.close()
        
        sopa = BeautifulSoup(html, "html.parser")
        regras = CONFIG_LOJAS[loja_detectada]
        
        tag_titulo = sopa.find(**regras["tag_titulo"])
        tag_preco = sopa.find(**regras["tag_preco"])
        
        if tag_titulo and tag_preco:
            nome = tag_titulo.get_text().strip()
            preco_bruto = tag_preco.get("content") if tag_preco.has_attr("content") else tag_preco.get_text()
            preco_limpo = preco_bruto.replace("R$", "").replace(".", "").replace(",", ".").strip()
            
            # Ajuste extra para a Amazon caso venha fragmentado
            if loja_detectada == "amazon":
                preco_limpo = preco_limpo.split()[0]
            
            print(f"\n🎉 [{loja_detectada.upper()}] PRODUTO ENCONTRADO!")
            print(f"Produto: {nome[:70]}...")
            print(f"Preço: R$ {float(preco_limpo):.2f}".replace(".", ","))
        else:
            print(f"\n❌ Falha ao extrair dados da {loja_detectada.upper()}.")

if __name__ == "__main__":
    asyncio.run(rodar_monitor())
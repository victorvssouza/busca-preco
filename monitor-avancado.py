import asyncio
import sys
import json
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from mapeamento import CONFIG_LOJAS

if len(sys.argv) > 1:
    URL = sys.argv[1]
else:
    URL = "https://www.amazon.com.br/TAT2500BK-00-Bluetooth-Cancelamento-Microfone/dp/B0FVGQ8DD4/"

def descubrir_loja(url):
    dominio = urlparse(url).netloc.lower()
    # 💡 CORREÇÃO ULTRA ESTRITA: Remove o 'www.' e verifica exatamente quem é o dono do site
    dominio_limpo = dominio.replace("www.", "")
    
    if "amazon.com.br" in dominio_limpo or "a.co" in dominio_limpo:
        return "amazon"
    if "mercadolivre.com.br" in dominio_limpo:
        return "mercadolivre"
    if "magazineluiza.com.br" in dominio_limpo:
        return "magazineluiza"
    return None

async def rodar_monitor():
    loja_detectada = descubrir_loja(URL)
    if not loja_detectada:
        print(f"❌ Loja não suportada ou não identificada no link. Dominio lido: {urlparse(URL).netloc}")
        return

    print(f"Iniciando navegador... 🤖 Modo Correto Ativado: {loja_detectada.upper()}")
    
    # Identifica se é uma página de pesquisa baseada na URL
    eh_pagina_busca = "/s?" in URL or "lista.mercadolivre" in URL or "/busca/" in URL
    
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
        
        print(f"Acessando a página... Aguarde carregar.")
        
        try:
            await pagina.goto(URL, wait_until="networkidle", timeout=25000)
        except:
            pass
            
        await asyncio.sleep(4) 
        html = await pagina.content()
        await navegador.close()
        
        sopa = BeautifulSoup(html, "html.parser")
        regras = CONFIG_LOJAS[loja_detectada]
        
        # 💡 DINÂMICA DE SELEÇÃO: Escolhe as chaves certas do mapa se for busca ou produto único
        if eh_pagina_busca:
            tag_titulo = sopa.find(**regras["tag_titulo_busca"])
            tag_preco = sopa.find(**regras["tag_preco_busca"])
        else:
            tag_titulo = sopa.find(**regras["tag_titulo"])
            tag_preco = sopa.find(**regras["tag_preco"])
            
        # Fallback de emergência genérico caso as tags principais falhem
        if not tag_preco:
            tag_preco = sopa.find("span", class_="andes-money-amount__fraction") or sopa.find("span", class_="a-price-whole")
            tag_titulo = sopa.find("h2") or sopa.find("h3")
        
        if tag_titulo and tag_preco:
            nome = tag_titulo.get_text().strip()
            preco_bruto = tag_preco.get("content") if tag_preco.has_attr("content") else tag_preco.get_text()
            
            # Limpeza cirúrgica de caracteres de moeda e espaços
            preco_limpo = preco_bruto.replace("R$", "").replace("a partir de", "").replace(".", "").replace(",", ".").strip()
            preco_limpo = preco_limpo.split()[0] if preco_limpo else "0"
            
            # Correção de múltiplos pontos decimais em milhares
            if preco_limpo.count(".") > 1:
                preco_limpo = preco_limpo.replace(".", "", preco_limpo.count(".") - 1)
            
            try:
                preco_final = float(preco_limpo)
                print(f"\n🎉 [{loja_detectada.upper()}] DADO CAPTURADO!")
                print(f"Item: {nome[:60]}...")
                print(f"Preço: R$ {preco_final:.2f}".replace(".", ","))
                
                dados = {
                    "loja_origem": loja_detectada,
                    "produto": nome,
                    "preco": preco_final
                }
                with open("compartilhado.json", "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=4, ensure_ascii=False)
            except Exception as e:
                print(f"❌ Erro ao converter preço limpo '{preco_limpo}': {e}")
        else:
            print(f"\n❌ Falha ao extrair dados. Seletores não correspondidos nesta página.")

if __name__ == "__main__":
    asyncio.run(rodar_monitor())
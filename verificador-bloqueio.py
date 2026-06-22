import requests

URL = "https://www.casasbahia.com.br/smart-tv-4k-50-lg-ultra-hd-50ua8550psa-com-processador-a7-gen8-ai-otimizador-de-jogos-wi-fi-bluetooth-webos-25-e-controle-smart-magic/p/55069668?vtr_id=indicados_com_base_nas_suas_visitas&vtr_name=indicados+com+base+nas+suas+visitas"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive"
}

print("Tentando acessar e salvar a página...")
resposta = requests.get(URL, headers=HEADERS)

# Salva o resultado em um arquivo para a gente analisar
with open("pagina.html", "w", encoding="utf-8") as f:
    f.write(resposta.text)

print("Pronto! O arquivo 'pagina.html' foi criado na sua pasta. Dê uma olhada nele no VS Code.")
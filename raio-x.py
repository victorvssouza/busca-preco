from bs4 import BeautifulSoup

print("Fazendo o Raio-X do arquivo 'pagina.html'...")

with open("pagina.html", "r", encoding="utf-8") as f:
    conteudo = f.read()

sopa = BeautifulSoup(conteudo, "html.parser")

# Busca o título da aba do navegador
titulo_aba = sopa.title.string if sopa.title else "Sem título de aba"
print(f"\n📌 Título da aba do navegador: {titulo_aba}")

print("\n📌 Começo do texto visível da página (Primeiros 300 caracteres):")
texto_limpo = sopa.get_text().strip()
# Remove espaços excessivos para ficar legível
texto_resumido = " ".join(texto_limpo.split())[:300]
print(texto_resumido if texto_resumido else "[Página totalmente vazia de texto]")
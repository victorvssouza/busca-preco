# 🎯 Busca Preço - Orquestrador Multimarketplace

Este é um sistema modular em Python projetado para monitorar e extrair preços de produtos em diferentes e-commerces (como Amazon e Mercado Livre). O projeto utiliza uma arquitetura inteligente que separa a interface de usuário, a lógica de descoberta, as regras de extração de dados e as estratégias antibot.

---

## 🏗️ Arquitetura e Fluxo do Projeto

O projeto foi desenhado seguindo as melhores práticas de engenharia de software, utilizando o princípio da responsabilidade única. Em vez de um único script massivo, o sistema é orquestrado por um maestro que delega tarefas para scripts especialistas.

### 🗺️ Mapa de Comunicação entre os Componentes

1. **`gerenciador.py` (O Maestro):** Abre a interface gráfica (Tkinter), recebe a URL do usuário, limpa o domínio e decide qual motor deve ser acionado com base no nível de proteção do site.
2. **`mapeamento.py` (A Fonte de Verdade):** Um dicionário centralizado que guarda os seletores HTML (`id`, `class`, `itemprop`) de cada marketplace. Se um site mudar de layout, apenas este arquivo é alterado.
3. **`monitor-avancado.py` (O Tanque de Guerra):** Acionado para lojas complexas (Amazon, Mercado Livre). Abre um navegador real via **Playwright**, injeta camuflagem JavaScript na raiz do browser para burlar bloqueios (como erro 403/telas de login) e usa as regras do `mapeamento.py` + `BeautifulSoup` para capturar o preço.
4. **`monitor-nao-avancado.py` (O Motor Rápido):** Acionado para links que não possuem travas pesadas. Utiliza requisições diretas via `requests` e faz a extração ultrarápida via dados estruturados **JSON-LD** (`application/ld+json`).
5. **`verificador.py` & `raio-x.py` (O Laboratório):** Ferramentas de diagnóstico offline para baixar páginas locais e testar seletores sem bombardear os servidores dos marketplaces.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.13**
* **Playwright** (Automação e emulação de navegador real)
* **BeautifulSoup4** (Parsing e extração de dados do HTML)
* **Requests** (Requisições HTTP leves)
* **Tkinter** (Interface gráfica nativa do Windows)
* **JSON & Urllib** (Tratamento de dados estruturados e análise de URLs)

---

## 📁 Estrutura de Arquivos

```text
Busca Preço/
│
├── gerenciador.py          # Interface Gráfica e Orquestrador principal
├── mapeamento.py           # Dicionário central de seletores das lojas
├── monitor-avancado.py     # Motor Playwright + BeautifulSoup (Lojas complexas)
├── monitor-nao-avancado.py  # Motor Requests + JSON-LD (Lojas leves)
│
├── verificador.py          # Ferramenta de laboratório: Baixa HTML
├── raio-x.py               # Ferramenta de laboratório: Analisa HTML offline
│
├── .gitignore              # Ignora arquivos locais (como pagina.html e caches)
└── README.md               # Documentação do projeto
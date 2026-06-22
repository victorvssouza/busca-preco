# mapeamento.py
CONFIG_LOJAS = {
    "amazon": {
        "tag_titulo": {"id": "productTitle"},
        "tag_preco": {"name": "span", "class_": "a-price-whole"},
        "tag_titulo_busca": {"name": "span", "class_": "a-size-medium a-color-base a-text-normal"},
        "tag_preco_busca": {"name": "span", "class_": "a-price-whole"}
    },
    "mercadolivre": {
        "tag_titulo": {"name": "h1", "class_": "ui-pdp-title"},
        "tag_preco": {"name": "meta", "itemprop": "price"},
        # 💡 Garante que pegará o título e preço do PRIMEIRO card real de produto na busca:
        "tag_titulo_busca": {"name": "h2", "class_": "poly-box poly-component__title"},
        "tag_preco_busca": {"name": "span", "class_": "poly-price__current"}
    },
    "magazineluiza": {
        "tag_titulo": {"name": "h1", "data-testid": "heading-product-title"},
        "tag_preco": {"name": "p", "data-testid": "price-value"},
        # 💡 Seletores para a página de listagem da Magalu:
        "tag_titulo_busca": {"name": "h3", "data-testid": "product-title"},
        "tag_preco_busca": {"name": "p", "data-testid": "price-value"}
    }
}
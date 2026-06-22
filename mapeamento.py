# 🗺️ O MAPA DOS MARKETPLACES (Corrigido e sem o operador 'or')
CONFIG_LOJAS = {
    "amazon": {
        "tag_titulo": {"id": "productTitle"},
        "tag_preco": {"name": "span", "class_": "a-price-whole"}
    },
    "mercadolivre": {
        "tag_titulo": {"name": "h1", "class_": "ui-pdp-title"},
        "tag_preco": {"name": "meta", "itemprop": "price"}
    },
    "magazineluiza": {
        "tag_titulo": {"name": "h1", "data-testid": "heading-product-title"},
        "tag_preco": {"name": "p", "data-testid": "price-value"}
    }
}
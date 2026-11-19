"""
Run the graphrag enhanced vector search pipeline by connecting the individual processing steps.
"""

from search_products import search_products

question = input("Describe your application: ").strip()

products = search_products(question)

for product in products:
    print(
        f"{product['item_number']} | "
        f"{product['designation']} | "
        f"Score: {product['score']:.3f}"
    )

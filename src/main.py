"""
Run the graphrag enhanced vector search pipeline by connecting the individual processing steps.
"""

from search_products import search_products
from retrieve_technical_data import retrieve_technical_data

question = input("Describe your application: ").strip()

products = search_products(question)
technical_data = retrieve_technical_data(products)

for result in technical_data:
    print(result)
    print()
    
    
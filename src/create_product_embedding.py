"""
Generate and store embeddings for product nodes directly in Neo4j
"""

# Access environment variables
import os

# Load .env settings
from dotenv import load_dotenv
load_dotenv(".env")

# Connection to neo4j
from neo4j import GraphDatabase

# Python framework for embeddings
from sentence_transformers import SentenceTransformer

# Pretrained model that turns each product's text into 384 numbers.
MODEL = "all-MiniLM-L6-v2"


# ---------------------------------------------------------------------------
# Cypher queries to read products, store embeddings and create the vector index
# ---------------------------------------------------------------------------

# Read the fields used to generate the embeddings
READ_PRODUCTS_QUERY = """
MATCH (product:Product)
RETURN product.item_number AS item_number,
       product.designation AS designation,
       product.long_description AS long_description,
       product.applications AS applications,
       product.features AS features
"""

# Match each product by item number and save its embedding.
# UNWIND turns the Python list into one Cypher row per product.
STORE_EMBEDDINGS_QUERY = """
UNWIND $products AS row
MATCH (product:Product {item_number: row.item_number})
CALL db.create.setNodeVectorProperty(product, 'embedding', row.embedding)
"""

# Index the embedding so Neo4j can find similar products.
# The index uses cosine similarity and expects 384 numbers per embedding.
CREATE_INDEX_QUERY = """
CREATE VECTOR INDEX product_embeddings IF NOT EXISTS
FOR (product:Product)
ON (product.embedding)
OPTIONS {
    indexConfig: {
        `vector.dimensions`: 384,
        `vector.similarity_function`: 'cosine'
    }
}
"""


# ---------------------------------------------------------------------------
# Function to generate and store product embeddings
# ---------------------------------------------------------------------------

def create_product_embeddings():
    database = os.environ["NEO4J_DATABASE"]

    with GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(
            os.environ["NEO4J_USERNAME"],
            os.environ["NEO4J_PASSWORD"],
        ),
    ) as driver:
        driver.verify_connectivity()

        products, _, _ = driver.execute_query(
            READ_PRODUCTS_QUERY,
            database_=database,
        )

        if not products:
            raise ValueError("No Product nodes found")

        model = SentenceTransformer(MODEL)
        products_with_embeddings = []

        for product in products:
            applications = " ".join(product["applications"] or [])
            features = " ".join(product["features"] or [])

            text = "\n".join([
                product["designation"] or "",
                product["long_description"] or "",
                f"Applications: {applications}",
                f"Features: {features}",
            ])

            products_with_embeddings.append({
                "item_number": product["item_number"],
                "embedding": model.encode(text).tolist(),
            })

        driver.execute_query(
            STORE_EMBEDDINGS_QUERY,
            parameters_={"products": products_with_embeddings},
            database_=database,
        )

        driver.execute_query(CREATE_INDEX_QUERY, database_=database)

    print(f"Generated embeddings for {len(products_with_embeddings)} products.")


if __name__ == "__main__":
    create_product_embeddings()
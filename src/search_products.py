"""
Retrieve relevant product nodes from Neo4j using vector similarity search.
"""

# Access environment variables
import os

# Load .env settings
from dotenv import load_dotenv
load_dotenv(".env")

# Connection to Neo4j
from neo4j import GraphDatabase

# Python framework for embeddings
from sentence_transformers import SentenceTransformer

# Use the same pretrained model used for the product embeddings.
MODEL = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL)


# ---------------------------------------------------------------------------
# Search for relevant product nodes
# ---------------------------------------------------------------------------

def search_products(question, top_k=10):

    # Create query embedding
    question_embedding = model.encode(question, convert_to_numpy=True)

    # Query Neo4j vector index
    # First part is the vector search from Neo4j documentation
    # Second part retrieves the properties needed for this project
    cypher = """
    CALL db.index.vector.queryNodes(
        'product_embeddings',
        $top_k,
        $question_embedding
    )
    YIELD node, score

    RETURN
        node.item_number AS item_number,
        node.designation AS designation,
        labels(node) AS type,
        score
    ORDER BY score DESC
    """

    # Connect to Neo4j and execute query
    with GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(
            os.environ["NEO4J_USERNAME"],
            os.environ["NEO4J_PASSWORD"],
        ),
    ) as driver:

        records, _, _ = driver.execute_query(
            cypher,
            top_k=top_k,
            question_embedding=question_embedding.tolist(),
            database_=os.environ["NEO4J_DATABASE"],
        )

    # Return relevant products
    return [record.data() for record in records]
"""
For each product found by vector search, retrieve technical data from Neo4j.
Follows up to two outgoing relationships.
"""

# Access environment variables
import os

# Load .env settings
from dotenv import load_dotenv
load_dotenv(".env")

# Connection to Neo4j
from neo4j import GraphDatabase


# ---------------------------------------------------------------------------
# Query to retrieve product properties and follow relationships
# ---------------------------------------------------------------------------

TECHNICAL_DATA_QUERY = """
UNWIND $products AS result
MATCH (product:Product {item_number: result.item_number})

RETURN
    result.score AS score,
    labels(product) AS type,
    product {.*, embedding: null} AS product,

    [(product)-[relationship]->(related) |
        {
            relationship: type(relationship),
            relationship_properties: properties(relationship),
            type: labels(related),
            properties: related {.*, embedding: null},

            related_nodes: [
                (related)-[next_relationship]->(next_node) |
                {
                    relationship: type(next_relationship),
                    relationship_properties: properties(next_relationship),
                    type: labels(next_node),
                    properties: next_node {.*, embedding: null}
                }
            ]
        }
    ] AS related_nodes

ORDER BY score DESC
"""


# ---------------------------------------------------------------------------
# Retrieve technical data for the products returned by vector search
# ---------------------------------------------------------------------------

def retrieve_technical_data(products):
    # An empty search result produces an empty technical result.
    if not products:
        return []

    with GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(
            os.environ["NEO4J_USERNAME"],
            os.environ["NEO4J_PASSWORD"],
        ),
    ) as driver:
        records, _, _ = driver.execute_query(
            TECHNICAL_DATA_QUERY,
            parameters_={"products": products},
            database_=os.environ["NEO4J_DATABASE"],
        )

    return [record.data() for record in records]
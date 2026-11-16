"""
Import descriptive data from an Excel file into existing Neo4j product nodes using Cypher queries.
"""

# Access environment variables
import os

# Use Pandas to read Excel
import pandas as pd

# Load .env settings
from dotenv import load_dotenv
load_dotenv(".env")

# Connection to neo4j
from neo4j import GraphDatabase


EXCEL_FILE = "data/Descriptive_Data.xlsx"


# ---------------------------------------------------------------------------
# Queries to import data from the different tables in the Excel
# ---------------------------------------------------------------------------

CHANNEL_QUERY = """
MATCH (channel:Channel {item_number: $item_number})
SET channel:Product
SET channel.long_description = $long_description,
    channel.features = $features,
    channel.applications = $applications
"""

CONNECTOR_QUERY = """
MATCH (connector:Connector {item_number: $item_number})
SET connector:Product
SET connector.long_description = $long_description,
    connector.features = $features,
    connector.applications = $applications
"""


# ---------------------------------------------------------------------------
# Functions that map table rows to query parameters
# ---------------------------------------------------------------------------

def import_channels(driver, table):
    for _, row in table.iterrows():
        item_number = int(row["Item number"])
        features = []
        applications = []

        # Read features and applications from 1 to 5
        for number in range(1, 6):
            feature = row[f"Feature {number}"]
            if pd.notna(feature):
                features.append(feature)

            application = row[f"Application {number}"]
            if pd.notna(application):
                applications.append(application)

        driver.execute_query(
            CHANNEL_QUERY,
            parameters_={
                "item_number": item_number,
                "long_description": row["Long description"],
                "features": features,
                "applications": applications,
            },
            database_=os.environ["NEO4J_DATABASE"],
        )


def import_connectors(driver, table):
    for _, row in table.iterrows():
        item_number = int(row["Item number"])
        features = []
        applications = []

        # Read features and applications from 1 to 5
        for number in range(1, 6):
            feature = row[f"Feature {number}"]
            if pd.notna(feature):
                features.append(feature)

            application = row[f"Application {number}"]
            if pd.notna(application):
                applications.append(application)

        driver.execute_query(
            CONNECTOR_QUERY,
            parameters_={
                "item_number": item_number,
                "long_description": row["Long description"],
                "features": features,
                "applications": applications,
            },
            database_=os.environ["NEO4J_DATABASE"],
        )
        
        
# ---------------------------------------------------------------------------
# Function that imports tables using one shared driver
# ---------------------------------------------------------------------------

def import_descriptive_data():
    tables = pd.read_excel(EXCEL_FILE, sheet_name=None)

    with GraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(
            os.environ["NEO4J_USERNAME"],
            os.environ["NEO4J_PASSWORD"],
        ),
    ) as driver:
        driver.verify_connectivity()

        import_channels(driver, tables["MT Channels"])
        import_connectors(driver, tables["MT Connectors"])

    print("Data imported into Neo4j!")

if __name__ == "__main__":
    import_descriptive_data()
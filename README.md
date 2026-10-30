# graphrag-enhanced-vector-search-from-scratch

This project focuses on learning how GraphRAG works using vector search as the retrieval method, by building the complete pipeline from scratch in Python.

It intentionally avoids higher level frameworks, so each step can be implemented and understood independently.

As a practical use case, the project uses descriptive Hilti product data stored in a Neo4j knowledge graph. Users describe their intended application in natural language, and the app recommends relevant products. Vector search identifies products whose descriptions and application information match the user’s needs.

Unlike the Text2Cypher project, which used structured technical data to answer questions about specific properties and relationships, this project requires more descriptive data. Product descriptions, features, and applications provide the semantic context needed to match an application to relevant products.

## Project Goal

The goal is to gain hands-on experience with the main components of a GraphRAG system using vector search:

- Structured data and graph schema preparation
- Data import into Neo4j
- Embedding generation and vector index creation for nodes
- User application embedding
- Vector similarity search
- LLM generation of product recommendations based on the retrieved data
- Evaluation against a golden set
- UI development with Streamlit

## Technology Stack

| Area                   | Technology                 |
| ---------------------- | -------------------------- |
| Programming language   | Python                     |
| Structured data source | Excel                      |
| Graph schema           | JSON                       |
| Excel processing       | pandas with openpyxl       |
| Graph database         | Neo4j                      |
| Query language         | Cypher                     |
| Embedding generation   | Sentence Transformers      |
| Embedding model        | all-MiniLM-L6-v2           |
| Vector index           | Neo4j vector index         |
| Retrieval method       | Vector similarity search  |
| LLM                    | Qwen3 4B via Ollama        |
| UI                     | Streamlit                  |

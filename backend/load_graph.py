import pandas as pd
from neo4j import GraphDatabase

print("1. Starting...")

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "welcometocit"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

print("2. Connected to Neo4j")

df = pd.read_csv("data/processed/transactions_processed.csv").head(5000)

print("3. CSV loaded")
print("Rows:", len(df))

with driver.session() as session:
    print("4. Clearing graph...")
    session.run("MATCH (n) DETACH DELETE n")

    print("5. Inserting data...")

    for i, (_, row) in enumerate(df.iterrows()):
        sender = str(row["Account"])
        receiver = str(row["Account.1"])
        amount = float(row["Amount Paid"])

        session.run("""
        MERGE (s:Account {id:$sender})
        MERGE (r:Account {id:$receiver})
        MERGE (s)-[:TRANSFERRED {amount:$amount}]->(r)
        """,
        sender=sender,
        receiver=receiver,
        amount=amount)

        if i % 1000 == 0:
            print(f"Inserted {i} rows")

print("Graph loaded successfully!")
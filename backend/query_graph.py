from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "welcometocit"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

with driver.session() as session:

    result = session.run("""
    MATCH (a:Account)-[t:TRANSFERRED]->(b:Account)
    RETURN
        a.id AS Sender,
        b.id AS Receiver,
        t.amount AS Amount
    ORDER BY Amount DESC
    LIMIT 10
    """)

    print("\nTop 10 Highest Transactions\n")

    for record in result:
        print(f"Sender   : {record['Sender']}")
        print(f"Receiver : {record['Receiver']}")
        print(f"Amount   : {record['Amount']}")
        print("-" * 40)

driver.close()
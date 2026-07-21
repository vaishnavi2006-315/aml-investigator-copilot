from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "welcometocit"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

with driver.session() as session:

    result = session.run("""
    MATCH (a:Account)-[t:TRANSFERRED]->()
    RETURN
        a.id AS Account,
        COUNT(t) AS Transactions,
        SUM(t.amount) AS TotalTransferred
    ORDER BY TotalTransferred DESC
    LIMIT 20
    """)

    print("\nTop 20 High-Risk Accounts\n")

    for record in result:
        print(f"Account      : {record['Account']}")
        print(f"Transactions : {record['Transactions']}")
        print(f"Total Amount : {record['TotalTransferred']:.2f}")
        print("-" * 40)

driver.close()
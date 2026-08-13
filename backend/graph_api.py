from fastapi import APIRouter
from neo4j import GraphDatabase

URI = "bolt://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "welcometocit"

driver = GraphDatabase.driver(
    URI,
    auth=(USER, PASSWORD)
)

router = APIRouter()


@router.get("/graph/{account_id}")
def get_graph(account_id: str):

    with driver.session() as session:

        result = session.run("""
            MATCH path =
            (a:Account {id: $account_id})
            -[:TRANSFERRED*1..3]->
            (b:Account)

            UNWIND nodes(path) AS n
            UNWIND relationships(path) AS r

            RETURN
                collect(DISTINCT n.id) AS nodes,
                collect(DISTINCT {
                    source: startNode(r).id,
                    target: endNode(r).id,
                    amount: r.amount
                }) AS relationships
        """, account_id=account_id)

        record = result.single()

        if not record:
            return {
                "nodes": [],
                "relationships": []
            }

        return {
            "nodes": record["nodes"],
            "relationships": record["relationships"]
        }
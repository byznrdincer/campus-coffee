import uuid
from datetime import datetime
from azure.cosmos import CosmosClient
import os
from dotenv import load_dotenv

load_dotenv()

client = CosmosClient(os.getenv("COSMOS_ENDPOINT"), os.getenv("COSMOS_KEY"))
database = client.get_database_client(os.getenv("COSMOS_DATABASE"))
container = database.get_container_client(os.getenv("COSMOS_CONTAINER"))

def create_order(student_name, items, note=""):
    order = {
        "id": str(uuid.uuid4()),
        "student_name": student_name,
        "items": items,
        "note": note,
        "status": "bekliyor",
        "created_at": datetime.now().isoformat()
    }
    container.create_item(order)
    return order

def get_all_orders():
    orders = list(container.query_items(
        query="SELECT * FROM c ORDER BY c.created_at DESC",
        enable_cross_partition_query=True
    ))
    return orders

def update_order_status(order_id, status):
    items = list(container.query_items(
        query=f"SELECT * FROM c WHERE c.id = '{order_id}'",
        enable_cross_partition_query=True
    ))
    if items:
        item = items[0]
        item["status"] = status
        container.replace_item(item=item["id"], body=item)

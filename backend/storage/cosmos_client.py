import os
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

load_dotenv()

client = CosmosClient(
   os.environ["COSMOS_DB_ENDPOINT"],
   credential=os.environ["COSMOS_DB_KEY"]
)

database = client.get_database_client(os.environ["COSMOS_DB_DATABASE"])
container = database.get_container_client(os.environ["COSMOS_DB_CONTAINER"])

def save_workflow_state(workflow_state: dict):
   container.upsert_item(workflow_state)

def get_workflow_state(workflow_id: str):
   query = f"SELECT * FROM c WHERE c.workflowId = '{workflow_id}'"
   items = list(container.query_items(query=query, enable_cross_partition_query=True))
   return items[0] if items else None
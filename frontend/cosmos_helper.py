"""
Cosmos DB Helper Module
Provides functions to save and retrieve workflow state for the Multi-Agent Automation Engine.
"""

from azure.cosmos import CosmosClient, exceptions
import time


class CosmosHelper:
    """Helper class for Cosmos DB operations on workflow state."""

    def __init__(self, endpoint: str, key: str, database_name: str, container_name: str):
        """
        Initialize Cosmos DB helper.

        Args:
            endpoint: Cosmos DB endpoint URL
            key: Cosmos DB primary key
            database_name: Database name (e.g., 'agent-memory-db')
            container_name: Container name (e.g., 'agent-state')
        """
        self.client = CosmosClient(endpoint, credential=key)
        self.database = self.client.get_database_client(database_name)
        self.container = self.database.get_container_client(container_name)

    def _retry_operation(self, operation, max_retries=3):
        """
        Retry an operation with exponential backoff.

        Args:
            operation: Function to retry
            max_retries: Maximum number of retry attempts

        Returns:
            Result of the operation
        """
        for attempt in range(max_retries):
            try:
                return operation()
            except exceptions.CosmosHttpResponseError as e:
                if e.status_code == 429 and attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Rate limited. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    raise
        return None

    def save_workflow_state(self, workflow_state: dict) -> str:
        """
        Save or update workflow state in Cosmos DB.

        Args:
            workflow_state: Workflow state dict (must include 'id' and 'workflowId')

        Returns:
            str: ID of the upserted item
        """
        def upsert():
            result = self.container.upsert_item(body=workflow_state)
            return result["id"]

        try:
            return self._retry_operation(upsert)
        except exceptions.CosmosHttpResponseError as e:
            print(f"Error saving workflow state: {e.message}")
            return None
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return None

    def get_workflow_state(self, workflow_id: str) -> dict:
        """
        Retrieve a workflow state by workflow ID.

        Args:
            workflow_id: The workflow ID to look up

        Returns:
            dict: Workflow state document, or None if not found
        """
        try:
            query = f"SELECT * FROM c WHERE c.workflowId = '{workflow_id}'"
            items = list(
                self.container.query_items(
                    query=query, enable_cross_partition_query=True
                )
            )
            return items[0] if items else None
        except Exception as e:
            print(f"Error retrieving workflow state: {str(e)}")
            return None

    def get_all_workflows(self, limit: int = 50) -> list:
        """
        Retrieve all workflow states, ordered by timestamp (newest first).

        Args:
            limit: Maximum number of workflows to retrieve

        Returns:
            list: List of workflow state dicts
        """
        try:
            query = f"SELECT TOP {limit} * FROM c ORDER BY c.timestamp DESC"
            items = list(
                self.container.query_items(
                    query=query, enable_cross_partition_query=True
                )
            )
            return items
        except Exception as e:
            print(f"Error retrieving workflow history: {str(e)}")
            return []

    def delete_workflow(self, workflow_id: str) -> bool:
        """
        Delete a workflow state by ID.

        Args:
            workflow_id: The workflow ID to delete

        Returns:
            bool: True if deleted, False otherwise
        """
        try:
            self.container.delete_item(item=workflow_id, partition_key=workflow_id)
            return True
        except exceptions.CosmosResourceNotFoundError:
            return False
        except Exception as e:
            print(f"Error deleting workflow: {str(e)}")
            return False

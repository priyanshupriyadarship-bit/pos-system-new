cat > backend/integrations/notion.py << 'NOTION'
from typing import Dict, Any
from notion_client import Client
from config.settings import Config
from loguru import logger

class NotionIntegration:
    """
    Integration with Notion API for databases, pages, etc.
    """
    
    def __init__(self):
        self.client = Client(auth=Config.NOTION_API_KEY)

    def add_to_database(self, database_id: str, properties: Dict) -> Dict:
        """Add a new row to a Notion database."""
        try:
            response = self.client.pages.create(
                parent={"database_id": database_id},
                properties=properties
            )
            return {"success": True, "page_id": response['id']}
        except Exception as e:
            logger.error(f"Notion add failed: {e}")
            return {"success": False, "message": str(e)}

    def query_database(self, database_id: str, filter: Dict = None) -> List[Dict]:
        """Query a Notion database."""
        try:
            response = self.client.databases.query(
                database_id=database_id,
                filter=filter or {}
            )
            return [page['properties'] for page in response['results']]
        except Exception as e:
            logger.error(f"Notion query failed: {e}")
            return []

    def create_page(self, parent_page_id: str, title: str, content: str) -> Dict:
        """Create a new Notion page."""
        try:
            response = self.client.pages.create(
                parent={"page_id": parent_page_id},
                properties={"title": {"title": [{"text": {"content": title}}]}},
                children=[{"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"type": "text", "text": {"content": content}}]}}}
            )
            return {"success": True, "page_id": response['id']}
        except Exception as e:
            logger.error(f"Notion page create failed: {e}")
            return {"success": False, "message": str(e)}
NOTION
echo "✓ Created backend/integrations/notion.py"
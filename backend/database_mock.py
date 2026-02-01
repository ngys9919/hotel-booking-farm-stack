"""
Mock database for demonstration when MongoDB is not available.
This allows the application to run without a real MongoDB connection.
"""
from typing import List, Dict, Any
from datetime import datetime
from bson import ObjectId


class MockCollection:
    """Mock MongoDB collection"""
    
    def __init__(self):
        self.data: List[Dict[str, Any]] = []
        self.counter = 1
    
    async def insert_one(self, document: Dict[str, Any]):
        """Insert a document"""
        doc = document.copy()
        doc['_id'] = ObjectId()
        self.data.append(doc)
        
        class InsertResult:
            def __init__(self, inserted_id):
                self.inserted_id = inserted_id
        
        return InsertResult(doc['_id'])
    
    async def insert_many(self, documents: List[Dict[str, Any]]):
        """Insert multiple documents"""
        for doc in documents:
            await self.insert_one(doc)
    
    async def find_one(self, query: Dict[str, Any]):
        """Find one document"""
        for doc in self.data:
            if self._match(doc, query):
                return doc
        return None
    
    def find(self, query: Dict[str, Any] = None):
        """Find documents"""
        return MockCursor(self.data, query or {})
    
    async def count_documents(self, query: Dict[str, Any]):
        """Count documents"""
        count = 0
        for doc in self.data:
            if self._match(doc, query):
                count += 1
        return count
    
    def _match(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        """Check if document matches query"""
        if not query:
            return True
        
        for key, value in query.items():
            if key == '_id':
                if isinstance(value, dict):
                    continue
                if str(doc.get(key)) != str(value):
                    return False
            elif isinstance(value, dict):
                # Handle regex queries
                if '$regex' in value:
                    import re
                    pattern = value['$regex']
                    options = value.get('$options', '')
                    flags = re.IGNORECASE if 'i' in options else 0
                    if not re.search(pattern, str(doc.get(key, '')), flags):
                        return False
            elif doc.get(key) != value:
                return False
        return True


class MockCursor:
    """Mock MongoDB cursor"""
    
    def __init__(self, data: List[Dict[str, Any]], query: Dict[str, Any]):
        self.data = data
        self.query = query
        self.sort_field = None
        self.sort_order = 1
    
    def sort(self, field: str, order: int = 1):
        """Sort results"""
        self.sort_field = field
        self.sort_order = order
        return self
    
    def __aiter__(self):
        """Async iterator"""
        return self
    
    async def __anext__(self):
        """Async next"""
        if not hasattr(self, '_iter'):
            results = []
            for doc in self.data:
                if self._match(doc, self.query):
                    results.append(doc)
            
            if self.sort_field:
                results.sort(
                    key=lambda x: x.get(self.sort_field, ''),
                    reverse=(self.sort_order == -1)
                )
            
            self._iter = iter(results)
        
        try:
            return next(self._iter)
        except StopIteration:
            raise StopAsyncIteration
    
    def _match(self, doc: Dict[str, Any], query: Dict[str, Any]) -> bool:
        """Check if document matches query"""
        if not query:
            return True
        
        for key, value in query.items():
            if key == '_id':
                if isinstance(value, dict):
                    continue
                if str(doc.get(key)) != str(value):
                    return False
            elif isinstance(value, dict):
                # Handle regex queries
                if '$regex' in value:
                    import re
                    pattern = value['$regex']
                    options = value.get('$options', '')
                    flags = re.IGNORECASE if 'i' in options else 0
                    if not re.search(pattern, str(doc.get(key, '')), flags):
                        return False
            elif doc.get(key) != value:
                return False
        return True


class MockDatabase:
    """Mock MongoDB database"""
    
    def __init__(self):
        self.collections = {}
    
    def get_collection(self, name: str):
        """Get or create collection"""
        if name not in self.collections:
            self.collections[name] = MockCollection()
        return self.collections[name]


class MockClient:
    """Mock MongoDB client"""
    
    def __init__(self, *args, **kwargs):
        self.databases = {}
    
    def __getitem__(self, name: str):
        """Get database"""
        if name not in self.databases:
            self.databases[name] = MockDatabase()
        return self.databases[name]
    
    @property
    def admin(self):
        """Admin database"""
        class Admin:
            async def command(self, cmd):
                return {'ok': 1}
        return Admin()
    
    def close(self):
        """Close connection"""
        pass

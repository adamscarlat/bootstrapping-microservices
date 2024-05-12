import asyncio


class MockCollectionItems:
  def __init__(self, items) -> None:
    self.items = items

  async def to_list(self, length):
    await asyncio.sleep(0.1)
    return self.items

class MockCollection:
  def __init__(self, items) -> None:
    self.items = MockCollectionItems(items)

  def find(self, fields, projection):
    return self.items

class MockDbClient:
  def __init__(self, mock_collections_map) -> None:
    self.mock_collections_map = mock_collections_map

  def get_collection(self, collection_name):
    return self.mock_collections_map[collection_name]
export const mongo_uri = 'mongodb://admin:pass@localhost:4000';
export const dbName = 'video-streaming';
export const db_fixture_path = "tests/db-fixture/videos.json"

export const getDbCollection = async (client, dbName, collectionName) => {
  await client.connect();
  const db = client.db(dbName);
  const collection = db.collection(collectionName);

  return collection
}
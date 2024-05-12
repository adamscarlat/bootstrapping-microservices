import {dbName, getDbCollection, mongo_uri} from "./helpers"

const { MongoClient } = require('mongodb');

const teardown = async () => {
  console.log('deleting test database...');

  const client = new MongoClient(mongo_uri, { useNewUrlParser: true, useUnifiedTopology: true });
  try {
    const collection = await getDbCollection(client, dbName, "videos")
    await collection.drop()
  } catch (error) {
    console.error('Error saving data:', error);
  } finally {
    await client.close();
  }
}

export default teardown
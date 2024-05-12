import {getDbCollection, mongo_uri, dbName, db_fixture_path} from "./helpers"

const { MongoClient } = require('mongodb');
const fs = require('fs').promises;

const globalSetup = async() => {
  console.log('creating new database...');

  const data_raw = await fs.readFile(db_fixture_path, 'utf8');
  const data = JSON.parse(data_raw);

  const client = new MongoClient(mongo_uri, { useNewUrlParser: true, useUnifiedTopology: true });
  try {
    const collection = await getDbCollection(client, dbName, "videos")
    await collection.drop();
    await collection.insertMany(data);
    console.log('Data saved successfully.');

  } catch (error) {
    console.error('Error saving data:', error);
  } finally {
    await client.close();
  }
}

export default globalSetup;
from pymongo import MongoClient

def save_to_mongodb(data, collection_name, topic, keyword, start_date_str, uri):
    """
    Saves a DataFrame to a specified MongoDB collection.

    Args:
        data (pd.DataFrame): The DataFrame containing the data to be saved.
        collection_name (str): The name of the MongoDB collection where data will be stored.
        topic (str): The topic related to the data, used to form the database name.
        keyword (str): The keyword related to the data, used to form the database name.
        start_date_str (str): The start date of the data in 'YYYY-MM-DD' format, added to the data as a field.
        uri (str): The MongoDB connection URI.

    Returns:
        None: Returns None if there is an error during the operation.
    """
    try:
        # Add the search date to the data
        data["search_date"] = start_date_str

        # Convert the DataFrame to a list of dictionaries, where each dictionary represents a record
        records = data.to_dict(orient='records')

        # Connect to the MongoDB database using the provided URI
        client = MongoClient(uri)

        # Clean up the topic and keyword to remove spaces and convert them to lowercase
        topic_clean = topic.replace(' ', '').lower()
        keyword_clean = keyword.replace(' ', '').lower()

        # Select the database based on the cleaned topic and keyword
        db = client[f"{topic_clean}-{keyword_clean}"]

        # Select the collection within the chosen database
        collection = db[collection_name]

        # Insert the records into the specified collection
        collection.insert_many(records)

        # Close the connection to the MongoDB server
        client.close()

    except Exception as e:
        # Log the error if needed
        # print(f"Error: {e}")
        return None

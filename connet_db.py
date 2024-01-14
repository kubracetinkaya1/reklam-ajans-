import pymongo


class ConnectDatabase:
    def __init__(self):
        self._host = "localhost"
        self._port = 27017
        self._database = "Ajans"
        self._connection = None
        self._collection = None

    def connect_db(self, collection):
        self._connection = pymongo.MongoClient(self._host, self._port)
        database = self._connection[self._database]
        self._collection = database[collection]

    def login(self,data):
        self.connect_db("login")
        user = self._collection.find_one(data)
        return user

    def get_single_data(self, oyuncu):
        self.connect_db("info")
        data = self._collection.find_one({'oyuncu': oyuncu})
        return data

    def add_info(self, oyuncu_data):
        self.connect_db("info")
        document = self._collection.insert_one(oyuncu_data)
        return document.inserted_id

    def search_info(self, data):
        # Connect to the database
        self.connect_db("info")
        query = {}
        if data["oyuncu"]:

            query["oyuncu"] = {"$regex": f".*{data['oyuncu']}.*", "$options": "i"}

            if data['boy']:
                query["boy"] = {"$regex": f".*{data['boy']}.*", "$options": "i"}
            if data['yas']:
                query["yas"] = {"$regex": f".*{data['yas']}.*", "$options": "i"}
            if data['deneyim']:
                query["deneyim"] = {"$regex": f".*{data['deneyim']}.*", "$options": "i"}


        if query:
            # Koşullarla bilgi aramak için bir MongoDB sorgusu oluştur
            results = self._collection.find(query)
            return list(results)
        else:
            # Tüm bilgiyi aramak için bir MongoDB sorgusu oluştur
            results = self._collection.find()
            return list(results)
        
    
    def delete_info(self, oyuncu):
        self.connect_db("info")
        try:
            document = self._collection.delete_one({'oyuncu':oyuncu })
            print(document)
            return document.acknowledged
        except Exception as E:
            self._connection.rollback()
            return E
        finally:
            self._connection.close()

    def update_info(self, data):
        self.connect_db("info")
        print(data)
        try:
            document = self._collection.update_one({'oyuncu': data['oyuncu']},
                                                   {"$set": data}, upsert=True)
            return document.acknowledged
        except Exception as E:
            self._connection.rollback()
            return E
        finally:
            self._connection.close()
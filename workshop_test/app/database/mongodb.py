from fastapi.param_functions import Query
import pymongo

from model.library import createLibraryModel, updateLibraryModel


class MongoDB:
    def __init__(self, host, port, user, password, auth_db, db, collection):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.auth_db = auth_db
        self.db = db
        self.collection = collection
        self.connection = None

    def _connect(self):
        client = pymongo.MongoClient(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            authSource=self.auth_db,
            authMechanism="SCRAM-SHA-1",
        )
        db = client[self.db]
        self.connection = db[self.collection]

    def find(self, sort_by, order):
        mongo_results = self.connection.find({}) 
        if sort_by is not None and order is not None:
            mongo_results.sort(sort_by, self._get_sort_by(order))

        return list(mongo_results)

    def _get_sort_by(self, sort: str) -> int:
        return pymongo.DESCENDING if sort == "desc" else pymongo.ASCENDING

    def find_one(self, id):
        return self.connection.find_one({"_id": id})

    def create(self, library: createLibraryModel):
        library_dict = library.dict(exclude_unset=True)

        insert_dict = {**library_dict, "_id": library_dict["id"]} #การกีดกันการ coppy / address ใหม่ตลอดเวลาคืออันเก่าจะไม่สามารถใช้งานได้

        inserted_result = self.connection.insert_one(insert_dict)
        library_id = str(inserted_result.inserted_id)

        return library_id

    def update(self, library_id, update_library: updateLibraryModel):
        query = {"id": library_id}
        update_data = {"$set": update_library.dict(exclude_unset=True)}
        updated_result = self.connection.update_one(query, update_data)
            
        return [library_id, updated_result.modified_count]

    def delete(self, library_id):
        deleted_result = self.connection.delete_one({"id": library_id})
        return [library_id, deleted_result.deleted_count]

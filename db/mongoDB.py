from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import msgspec



class LeafNode(msgspec.Struct):
    art: str
    name: str
    description: str
    image_path: str
    type_additional: str
    name_additional: str
    children: list["LeafNode"] = []


LeafNode.__annotations__["children"] = list[LeafNode]

class RootNode(msgspec.Struct):
    type: int
    product_code: int
    place: int
    art: str
    name: str
    description: str
    image_path: str
    children: list[LeafNode]



class Database():
    def __init__(self):
        try:
            self.client = MongoClient("mongodb://localhost:27017/")
            self.client.admin.command('ping')
            self.db =  self.client["testDB"]
        except ConnectionFailure as e:
            print(f"Ошибка подключения: {e}")


        
        
    def insert_test_data(self):
        self.deleteAll()
        
        items = [172,169,173]
    
        for item in items:
            data = RootNode(
                type=item,
                product_code=1122,
                place=629,
                art=f"PIR_{item}",
                name=f"{item}",
                description=f"description for {item}",
                image_path="image.png",
                children=[
                    LeafNode(
                        art=f"PIR_1_{item}",
                        name=f"1_{item}",
                        description=f"desc for child 1 of {item}",
                        image_path="image.png",
                        type_additional="some type_additional",
                        name_additional="some name_additional",
                        children=[
                            LeafNode(
                                art=f"PIR_1_1_{item}",
                                name=f"1_1_{item}",
                                description=f"desc for child 1 of {item}",
                                image_path="image.png",
                                type_additional="some type_additional",
                                name_additional="some name_additional"
                            ),
                            LeafNode(
                                art=f"PIR_1_2_{item}",
                                name=f"1_2_{item}",
                                description=f"desc for child 1 of {item}",
                                image_path="image.png",
                                type_additional="some type_additional",
                                name_additional="some name_additional"
                            )
                        ]
                    ),
                    LeafNode(
                        art=f"PIR_2_{item}",
                        name=f"2_{item}",
                        description=f"desc for child 2 of {item}",
                        image_path="image.png",
                        type_additional="some type_additional",
                        name_additional="some name_additional"
                    ),
                    LeafNode(
                        art=f"PIR_3_{item}",
                        name=f"3_{item}",
                        description=f"desc for child 3 of {item}",
                        image_path="image.png",
                        type_additional="some type_additional",
                        name_additional="some name_additional"
                    )
                ]
            )

            new_item = msgspec.to_builtins(data)
            self.db["drones"].insert_one(new_item)
            
        
        
    def insert_parent(self, type: int, prod_code: int, place:int,  art: str, name: str, desc: str):
        """
        desc = description
        type_ad = type_additional
        name_ad = name_additional
        """
        new_drone = {
            "type": type,
            "product_code": prod_code,
            "place": place,
            "art": art,
            "name": name,
            "description": desc
        }
        collection = self.db["drones"]
        collection.insert_one(new_drone)
        
        
    def insert(self, art: str, name: str, desc: str, type_ad: str, name_ad: str):
        """
        desc = description
        type_ad = type_additional
        name_ad = name_additional
        """
        new_drone = {
            "art": art,
            "name": name,
            "description": desc,
            "type_additional": type_ad,
            "name_additional": name_ad,
        }
        self.db["drones"].insert_one(new_drone)
        
    def deleteAll(self):
        self.db["drones"].delete_many({})
                
        
    def get_all(self):
        collection = self.db["drones"]
        return collection.find()
    
    def get_firsts(self):
        collection = self.db["drones"]
        return collection.find({}, {
            "children": 0,
        })
    
    def get_by_art(self, art: str):
        collection = self.db["drones"]
        return collection.find_one({
            "art": f"{art}"
        })
       
        
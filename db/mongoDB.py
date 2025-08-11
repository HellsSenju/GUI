from pymongo import MongoClient

class Database():
    def __init__(self):
        self.client = MongoClient("localhost", 27017)
        self.db =  self.client["testDB"]
        
        
    def insert_test_data(self):
        self.deleteAll()
        
        items = [172,169,173]
    
        for item in items:
            new_item = {
                "type": item,
                "product_code": 1122,
                "place": 629,
                "art": f"PIR_{item}",
                "name": f"{item}",
                "description": f"description for {item}",
                "image_path": "image.png",                
                "children": [
                    {
                        "art": f"PIR_1_{item}",
                        "name": f"1_{item}",
                        "description": f"desc for child 1 of {item}",
                        "image_path": "image.png",                
                        "type_additional": "some type_additional",
                        "name_additional": "some name_additional",
                    },
                    {
                        "art": f"PIR_2_{item}",
                        "name": f"2_{item}",
                        "description": f"desc for child 2 of {item}",
                        "image_path": "image.png",                
                        "type_additional": "some type_additional",
                        "name_additional": "some name_additional",
                    },
                    {
                        "art": f"PIR_3_{item}",
                        "name": f"3_{item}",
                        "description": f"desc for child 3 of {item}",
                        "image_path": "image.png",                
                        "type_additional": "some type_additional",
                        "name_additional": "some name_additional",
                    },
                ]
            }
            
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
       
        

from typing import Optional

level = 0 

def recursion()-> Optional[str]:
    if level == 0:
        return
    


def create(deep_level: int):
    tree = {}
    parents = [172,169,173]
    
    for parent in parents:
        p = {
            "type": parent,
            "art": "PIR...",
            "name": f"name for {parent}",
            "description": f"description for {parent}",
            "product_code": 1122,
            "place": 629
        }
        
        level = deep_level
        ch = recursion()
        
    
    
    
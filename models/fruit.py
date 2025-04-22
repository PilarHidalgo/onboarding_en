class Fruit:
    def __init__(self, id=None, name="", price=0.0, quantity=0, category=""):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            price=data.get("price", 0.0),
            quantity=data.get("quantity", 0),
            category=data.get("category", "")
        )
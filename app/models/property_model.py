class Property():
    next_property_id = 1

    def __init__(self, owner_id) -> None:
        self.id = Property.next_property_id
        Property.next_property_id+=1
        self.owner_id = owner_id
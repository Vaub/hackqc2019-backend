import uuid


class Organization:

    @staticmethod
    def create_new(data):
        return Organization(
            **data,
            reference=str(uuid.uuid4())
        )

    @staticmethod
    def from_json(data):
        return Organization(**data)

    def __init__(self, reference, name, description, position, address, services):
        self.reference = reference
        self.name = name
        self.description = description
        self.position = position
        self.address = address
        self.services = services

    def as_json(self):
        return self.__dict__

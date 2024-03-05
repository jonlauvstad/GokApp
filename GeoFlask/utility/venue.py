class Venue:

    def __init__(self, id, name, description, locationId, streetAddress, postCode, city, capacity, locationName, link=None, links=None):
        self.id = id
        self.name = name
        self.description = description
        self.locationId = locationId
        self.streetAddress = streetAddress
        self.postCode = postCode
        self.city = city
        self.capacity = capacity
        self.locationName = locationName
        self.link = link
        self.links = links or {}

        # Example of an additional convenience property
        self.address = f"{streetAddress}, {postCode} {city}"

    def __str__(self):
        return f"Venue(name={self.name}, capacity={self.capacity}, address={self.address})"

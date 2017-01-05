from store.templates import store_obj

def pet_obj(pet):
    return {
      "id":             pet.external_id,
      "name":           pet.name,
      "species":        pet.species,
      "breed":          pet.breed,
      "age":            pet.age,
      "store":          store_obj(pet.store),
      "price":          str(pet.price),
      "received_date":  str(pet.received_date.isoformat()[:19]) +"Z",
      "links": [
        { "rel": "self", "href": "/pets/" + pet.external_id }
      ]
    }

def pets_obj(pets):
    pets_obj = []
    for pet in pets.items:
        pets_obj.append(pet_obj(pet))
    return pets_obj

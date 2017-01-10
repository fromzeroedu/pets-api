from store.templates import store_obj

def pet_obj(pet, nostore=False):
    pet_obj = {
      "id":             pet.external_id,
      "name":           pet.name,
      "species":        pet.species,
      "breed":          pet.breed,
      "age":            pet.age,
      "price":          str(pet.price),
      "received_date":  str(pet.received_date.isoformat()[:19]) +"Z",
      "links": [
        { "rel": "self", "href": "/pets/" + pet.external_id }
      ]
    }
    if not nostore:
        pet_obj["store"] = store_obj(pet.store)
    return pet_obj

def pets_obj(pets, nostore=False):
    pets_obj = []
    for pet in pets.items:
        pets_obj.append(pet_obj(pet, nostore))
    return pets_obj

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "species": {"type": "string"},
        "breed": {"type": "string"},
        "age": {"type": "number"},
        "store": {"type": "string"},
        "price": {"type": "string"},
        "received_date": {"type": "string", "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"},
    },
    "required": ["name", "species", "breed", "age", "store", "price", "received_date"]
}

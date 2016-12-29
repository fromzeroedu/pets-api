from jsonschema import validate

schema = {
    "type": "object",
    "properties": {
        "price": {"type": "number"},
        "name": {"type": "string"},
        "external_id": {"type": "string",
                "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"}
    },
    "required": ["price", "name"]
}
validate({"price": 32, "external_id": "c3ae497c-5b6d-4acb-ae77-60caeaaae815"}, schema)

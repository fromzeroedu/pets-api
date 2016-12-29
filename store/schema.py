schema = {
    "type": "object",
    "properties": {
        "neighborhood":   {"type": "string"},
        "street_address": {"type": "string"},
        "city":           {"type": "string"},
        "state":          {"type": "string", "pattern": "^[A-Z]{2}$"},
        "zip":            {"type": "string", "pattern": "^[0-9]{5}$"},
        "phone":          {"type": "string", "pattern": "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"},
    },
    "required": ["neighborhood", "street_address", "city", "state", "zip", "phone"]
}

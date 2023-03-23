user_schema = {
    "type": "object",
    "properties": {
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["email", "firstName", "lastName"]
}

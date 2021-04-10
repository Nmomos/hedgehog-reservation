CREATE_HEDGEHOG_QUERY = """
    INSERT INTO hedgehogs (name, description, age, color_type, owner)
    VALUES (:name, :description, :age, :color_type, :owner)
    RETURNING id, name, description, age, color_type, owner, created_at, updated_at;
"""

GET_HEDGEHOG_BY_ID_QUERY = """
    SELECT id, name, description, age, color_type, owner, created_at, updated_at
    FROM hedgehogs
    WHERE id = :id;
"""

LIST_ALL_USER_HEDGEHOGS_QUERY = """
    SELECT id, name, description, age, color_type, owner, created_at, updated_at
    FROM hedgehogs
    WHERE owner = :owner;
"""

UPDATE_HEDGEHOG_BY_ID_QUERY = """
    UPDATE hedgehogs
    SET name          = :name,
        description   = :description,
        age           = :age,
        color_type    = :color_type
    WHERE id = :id
    RETURNING id, name, description, age, color_type, owner, created_at, updated_at;
"""

DELETE_HEDGEHOG_BY_ID_QUERY = """
    DELETE FROM hedgehogs
    WHERE id = :id
    RETURNING id;
"""

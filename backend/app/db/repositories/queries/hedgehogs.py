CREATE_HEDGEHOG_QUERY = '''
    INSERT INTO hedgehogs (name, description, age, color_type)
    VALUES (:name, :description, :age, :color_type)
    RETURNING id, name, description, age, color_type;
'''
GET_HEDGEHOG_BY_ID_QUERY = '''
    SELECT id, name, description, age, color_type
    FROM hedgehogs
    WHERE id = :id;
'''
GET_ALL_HEDGEHOGS_QUERY = '''
    SELECT id, name, description, age, color_type
    FROM hedgehogs;
'''
UPDATE_HEDGEHOG_BY_ID_QUERY = '''
    UPDATE hedgehogs
    SET name          = :name,
        description   = :description,
        age           = :age,
        color_type = :color_type
    WHERE id = :id
    RETURNING id, name, description, age, color_type;
'''
DELETE_HEDGEHOG_BY_ID_QUERY = '''
    DELETE FROM hedgehogs
    WHERE id = :id
    RETURNING id;
'''

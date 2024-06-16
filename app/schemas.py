from marshmallow import Schema, fields, validate

class IngredientSchema(Schema):
    ingredients = fields.List(fields.String(), required=True, validate=validate.Length(min=1))

ingredient_schema = IngredientSchema()
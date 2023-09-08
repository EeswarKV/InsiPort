from marshmallow import Schema, fields, validate

class AddCustomerSchema(Schema):
    name = fields.Str(required = True, validate = validate.Length(min=1, max=15))
    email = fields.Email(required = True)
    given_name = fields.Str(required = True, validate = validate.Length(min=1, max=15))
    family_name = fields.Str(required = True, validate = validate.Length(min=1, max=15))
    nickname = fields.Str(required = True, validate = validate.Length(min=1, max=8))
    username = fields.Str(required = True, validate = validate.Length(min=1, max=15))
    password = fields.Str(validate = validate.Length(min=6, max=15))
    age = fields.Int(validate = validate.Range(min=15, max=100))
    phone_number = fields.Str(required = True, validate = validate.Length(min=10, max=12))

class UpdateUserInfoSchema(Schema):
    user_id = fields.Str(required = True, validate = validate.Length(min=1, max=18))
    email = fields.Email()
    name = fields.Str(validate = validate.Length(min=1, max=15))
    phone_number = fields.Str(validate = validate.Length(min=10, max=12))

class UpdateUserPasswordSchema(Schema):
    user_id = fields.Str(required = True, validate = validate.Length(min=1, max=18))
    old_password = fields.Str(validate = validate.Length(min=6, max=15))
    new_password = fields.Str(validate = validate.Length(min=6, max=15))
    confirm_password = fields.Str(validate = validate.Length(min=6, max=15))
    
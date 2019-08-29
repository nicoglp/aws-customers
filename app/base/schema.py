from marshmallow import Schema, fields


class ModelSchema(Schema):
    id = fields.Str(attribute="id")
    createdAt = fields.Decimal(attribute="created_at", as_string=True)
    updatedAt = fields.Decimal(attribute="updated_at", as_string=True)


class PaginationSchema(Schema):
    pageNumber = fields.Integer(attribute='page')
    pageSize = fields.Integer(attribute='per_page')
    totalPages = fields.Integer(attribute='pages')
    totalItems = fields.Integer(attribute='total')


pagination_schema = PaginationSchema()

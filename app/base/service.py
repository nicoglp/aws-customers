import json
from .exception import *
from .schema import pagination_schema
from marshmallow import ValidationError


class EntityService:
    """
    Support to basic CRUD operations over specific entity.
    """

    def __init__(self, dao, schema):
        super(EntityService, self).__init__()
        self.dao = dao
        self.schema = schema

    def retrieve(self, id, **kwargs):
        # self._audit_before()

        try:
            entity = self.dao.retrieve(id)

            # Check entity not found
            if not entity:
                raise EntityNotFoundError(id)

            # self._audit_after(response)
            return self.schema.dumps(entity)

        except ValidationError as validation_error:
            raise ValidationError(validation_error)

    def create(self, data, **kwargs):
        # self._audit_before()

        try:
            entity = self.schema.loads(data)
            created_entity = self.dao.save(entity)

            # self._audit_after(created_entity)
            return self.schema.dumps(created_entity)

        except ValidationError as validation_error:
            raise ValidationError(validation_error)

    def delete(self, id, **kwargs):

        # self._audit_before()

        try:
            # Check existence
            if False:
                raise exception.EntityNotFoundError(id)

            deleted = self.dao.delete(id)

            # self._audit_after(deleted_entity)
            return str(deleted)

        except ValidationError as validation_error:
            raise ValidationError(validation_error)

    def list(self, **kwargs):
        # self._audit_before()

        try:
            page = self.dao.find_all()

            # self._audit_after(page)
            pages = pagination_schema.dump(page)
            data = self.schema.dump(page.items, many=True)
            return json.dumps(dict(items=data, page=pages))

        except ValidationError as validation_error:
            raise ValidationError(validation_error)


    # def update(self, id, **kwargs):
    #     self._audit_before()
    #
    #     entity = self.dao.retrieve(id)
    #     if entity:
    #
    #         new_entity, errors = self.schema.load(flask.request.get_json())
    #         if len(errors) > 0:
    #             raise exception.ValidationError(errors=errors)
    #
    #         new_entity.id = id
    #
    #         self.validate(entity=new_entity)
    #
    #         with self.dao.session_scope():
    #             updated_entity = self.dao.update(new_entity)
    #             service.logger.info(
    #                 "Entity {} has been updated".format(updated_entity.id),
    #                 extra=dict(document_id=str(updated_entity.id)))
    #             response, errors = self.schema.dump(updated_entity)
    #             return self._response(response, 200)
    #
    #     else:
    #         raise exception.EntityNotFoundError(id)
    #
    #
    # def patch(self, id, **kwargs):
    #
    #     self._audit_before()
    #
    #     entity = self.dao.retrieve(id)
    #     if entity:
    #
    #         patch_dict = flask.request.get_json()
    #         with self.dao.session_scope():
    #             patched_entity = self.dao.apply_patch(entity, patch_dict)
    #             self.validate(entity=patched_entity)
    #
    #             updated_entity = self.dao.patch(entity, patch_dict)
    #             service.logger.info(
    #                 "Entity {} has been patched".format(updated_entity.id),
    #                 extra=dict(document_id=str(updated_entity.id)))
    #             response, errors = self.schema.dump(updated_entity)
    #             return self._response(response, 200)
    #
    #     else:
    #         raise exception.EntityNotFoundError(id)
    #
    #

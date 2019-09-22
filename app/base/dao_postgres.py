from contextlib import contextmanager
import logging
import uuid
from datetime import datetime
from ..base import model

log = logging.getLogger('PostgresDAO')
from .. import logger


class PostgresDAO:
    """
    Implement basic functionality for SQL DAOs as CRUD and transactions management.
    For transactions : http://docs.sqlalchemy.org/en/rel_0_8/orm/session.html#session-faq-whentocreate
    """

    def __init__(self, schema, mapped_class, session):
        super(PostgresDAO, self).__init__()
        self.schema = schema
        self.mapped_class = mapped_class
        self.session = session

    def find_all(self, page=1, per_page=10):
        items = self.session.query(self.mapped_class).limit(per_page).offset((page - 1) * per_page).all()
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = self.session.query(self.mapped_class).count()
        return model.Pagination(page, per_page, total, items)

    def save(self, entity):
        self.session.add(entity)
        self.session.flush()
        return entity

    def retrieve(self, id):
        return self.session.query(self.mapped_class).get(id)

    def delete(self, id):
        entity = self.retrieve(id)
        self.session.delete(entity)
        self.session.flush()
        return True



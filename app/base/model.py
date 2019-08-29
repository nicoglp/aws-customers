from math import ceil


class Pagination():

    def __init__(self, page, per_page, total, items):
        super(Pagination, self).__init__()
        self.page = page
        self.per_page = per_page
        self.total = total
        self.items = items

    @property
    def pages(self):
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    @property
    def prev_page(self):
        return self.page - 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next_page(self):
        return self.page + 1


class Model:
    id = None
    created_at = None
    updated_at = None

    def __init__(self, *initial_data, **kwargs):
        """
        Allows instantiate an object with a dictionary or a list of params
        as argument of the constructor method.
        """
        for dictionary in initial_data:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

class PiracyException(Exception):
    pass


class scruggsList(list):
    def __init__(self, *args):
        self._ptr = 0
        self._cPtr = None
        super(list, self).__init__(args)
        self._ptr = self.__len__()

    def __iter__(self):
        return self

    def __next__(self):
        if self._ptr == self._cPtr or self.__len__() == 0:
            self._cPtr = None
            raise StopIteration
        if self._cPtr is None:
            self._cPtr = self._ptr
        if self._ptr >= self.__len__():
            self._ptr = 0
        elem = self[self._ptr]
        self._ptr += 1
        return elem

    def __add__(self, list2):
        my_split = (self[:self._ptr], self[self._ptr:])
        if not isinstance(list2, scruggsList):
            return scruggsList(super(list, super(list, my_split[0]).__add__(list2)).__add(my_split[1]))
        o_split = (list2[:list2._ptr], list2[list2._ptr:])
        combined_1 = scruggsList(super(list, my_split[0]).__add__(o_split[0]))
        combined_2 = scruggsList(super(list, my_split[1]).__add__(o_split[1]))
        return scruggsList(super(list, combined_1).__add__(combined_2))

    def __getslice__(self, lower, upper):
        return scruggsList(super(list, self).__getslice__(lower, upper))

    def __repr__(self):
        return '[{}]'.format(','.join([str(i) for i in self]))

    def next(self):
        return self.__next__()

    def append(self, item):
        self.insert(self._ptr, item)

    def extend(self, list2):
        for item in list2:
            self.append(item)

    def index(self, val):
        idx = super(list, self).index(val)
        self._ptr = idx + 1
        return idx

    def insert(self, idx, item):
        super(list, self).insert(idx, item)
        self._ptr = idx + 1

    def pop(self):
        if not self.__len__():
            raise IndexError('pop from empty list')
        self._ptr -= 1
        if self._ptr < 0:
            self._ptr = self.__len__() - 1
        item = self[self._ptr]
        del self[self._ptr]
        return item

    def remove(self, item):
        idx = self.index(item)
        super(list, self).remove(item)
        self._ptr = idx


list = scruggsList


class scruggsDictPage(dict):
    def __init__(self, base_dict, page):
        self._base_dict = base_dict
        self._page = page

    def __getitem__(self, key):
        for bkey, bvalue in self._base_dict.items(self._page):
            if bkey == key:
                return bvalue
        else:
            raise KeyError('key does not exist on page {}'.format(self._page))

    def __setitem__(self, key, value):
        for bkey, bvalue in self._base_dict.items(self._page):
            if bkey == key:
                self._base_dict.__setitem__(key, value)
        else:
            raise KeyError('key does not exist on page {}'.format(self._page))

    def __repr__(self):
        header = 'Dictionary page {}: {}'.format(self._page, '{')
        body = ','.join(['{}: {}'.format(key, val) for key, val in self._base_dict.items(self._page)])
        end = '}'
        return header + body + end


class scruggsDict(dict):
    def __init__(self, *args, **kwargs):
        self._perpage = 3
        super(dict, self).__init__(*args, **kwargs)

    def __iter__(self):
        return self.keys()

    def __repr__(self):
        header = 'Dictionary containing {} pages and {} keys: {}'.format(self.pages(), self.__len__(), '{')
        body = ','.join(['Page {}: [{}]'.format((page + 1), ','.join([str(k) for k in keys])) for page, keys in enumerate(self.keys())])
        end = '}'
        return header + body + end

    def __getitem__(self, page):
        return scruggsDictPage(self, page)

    def __setitem__(self, key, value):
        if hasattr(value, '__iter__'):
            value = [val for val in value]
        super(dict, self).__setitem__(key, value)

    def __delitem__(self, page, key):
        self.__getitem__(page)[key]
        del super(dict, self)[key]

    def get(self, page):
        return self.__getitem__(page)

    def update(self, page, key, value):
        self.get(page).__setitem__(key, value)

    def pop(self, page, key):
        obj = self.__getitem__(page).__getitem__(key)
        del super(dict, self)[key]
        return obj

    def popitem(self):
        if self.__len__() < 1:
            raise KeyError('dictionary is empty')
        first_key = self.keys()[0][0]
        obj = super(dict, self)[first_key]
        del super(dict, self)[first_key]
        return obj

    def setdefault(self, page, key, default):
        if key in self.keys[page]:
            return self.__getitem__(page).__getitem__(key)
        elif any([key in row for row in self.keys]):
            raise KeyError('key exists on a different page')
        else:
            self.__setitem__(key, default)
            return default

    def items(self, page):
        results = list()
        for key in self.keys()[page - 1]:
            results.append((key, super(dict, self).__getitem__(key)))
        return results

    def iteritems(self, page):
        return self.items(page)

    def keys(self):
        base_keys = sorted(super(dict, self).keys())
        toc = list()
        for idx, key in enumerate(base_keys):
            page = (idx // self._perpage) + 1
            if len(toc) < page:
                toc.append(list())
            toc[-1].append(key)
        return toc

    def iterkeys(self):
        return self.keys()

    def values(self, page):
        results = list()
        for key in self.keys()[page - 1]:
            results.append(super(dict, self).__getitem__(key))
        return results

    def itervalues(self, page):
        return self.values(page)

    def pages(self):
        num_keys = self.__len__()
        extra_keys = num_keys % self._perpage
        return (num_keys // self._perpage) + int(extra_keys > 0)

    def per_page(self, pp):
        self._perpage = pp

    def has_key(self):
        raise AttributeError('okay listen up, this has been deprecated for a while, so guess what buddy, you can\'t use it.')

    def copy(self):
        raise PiracyException('cannot create unauthorized copies of this dictionary')

    def viewitems(self):
        raise PiracyException('cannot create a view for this dictionary')

    def viewkeys(self):
        raise PiracyException('cannot create a view for this dictionary')

    def viewvalues(self):
        raise PiracyException('cannot create a view for this dictionary')


dict = scruggsDict

scruggsList.__name__ = 'array (only brainlets would refer to these as \'lists\')'

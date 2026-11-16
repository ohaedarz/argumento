import pytest

from argumento.namespace_dict import NamespaceDict


def test_set_get_simple():
    ns_dict = NamespaceDict()
    ns_dict['item'] = 1
    assert ns_dict['item'] == 1
    assert ns_dict.item == 1


def test_init_from_dict():
    ns_dict = NamespaceDict({'item1': 1,
                             'item2': 2,
                             'item3': {
                                 'subitem31': {'subitem311': 311, 'subitem312': 312},
                                 'subitem32': {'subitem321': 321, 'subitem322': 322}}})
    assert ns_dict['item1'] == 1
    assert ns_dict['item2'] == 2
    assert ns_dict.item1 == 1
    assert ns_dict.item2 == 2

    assert ns_dict['item3']['subitem31']['subitem311'] == 311
    assert ns_dict['item3']['subitem31']['subitem312'] == 312
    assert ns_dict['item3']['subitem32']['subitem321'] == 321
    assert ns_dict['item3']['subitem32']['subitem322'] == 322
    #
    assert ns_dict.item3['subitem31']['subitem311'] == 311
    assert ns_dict.item3['subitem31']['subitem312'] == 312
    assert ns_dict.item3['subitem32']['subitem321'] == 321
    assert ns_dict.item3['subitem32']['subitem322'] == 322
    #
    assert ns_dict.item3.subitem31['subitem311'] == 311
    assert ns_dict.item3.subitem31['subitem312'] == 312
    assert ns_dict.item3.subitem32['subitem321'] == 321
    assert ns_dict.item3.subitem32['subitem322'] == 322
    #
    assert ns_dict.item3.subitem31.subitem311 == 311
    assert ns_dict.item3.subitem31.subitem312 == 312
    assert ns_dict.item3.subitem32.subitem321 == 321
    assert ns_dict.item3.subitem32.subitem322 == 322

def test_set_recursive():
    ns_dict = NamespaceDict()
    ns_dict['item1.subitem1'] = 11
    assert ns_dict.item1.subitem1 == 11
    assert ns_dict['item1.subitem1'] == 11

    ns_dict['item1']['subitem2'] = 12
    assert ns_dict['item1']['subitem2'] == 12
    assert ns_dict['item1.subitem2'] == 12
    assert ns_dict.item1.subitem2 == 12

    with pytest.raises(TypeError):
        ns_dict['item2']['subitem2'] = 22

    ns_dict['item2'] = {'subitem2': 22}
    assert ns_dict['item2']['subitem2'] == 22
    assert ns_dict['item2.subitem2'] == 22
    assert ns_dict.item2.subitem2 == 22

    ns_dict['item3'] = {'subitem31': {'subitem311': 311, 'subitem312': 312},
                        'subitem32': {'subitem321': 321, 'subitem322': 322}}
    assert ns_dict['item3']['subitem31']['subitem311'] == 311
    assert ns_dict['item3']['subitem31']['subitem312'] == 312
    assert ns_dict['item3']['subitem32']['subitem321'] == 321
    assert ns_dict['item3']['subitem32']['subitem322'] == 322
    #
    assert ns_dict.item3['subitem31']['subitem311'] == 311
    assert ns_dict.item3['subitem31']['subitem312'] == 312
    assert ns_dict.item3['subitem32']['subitem321'] == 321
    assert ns_dict.item3['subitem32']['subitem322'] == 322
    #
    assert ns_dict.item3.subitem31['subitem311'] == 311
    assert ns_dict.item3.subitem31['subitem312'] == 312
    assert ns_dict.item3.subitem32['subitem321'] == 321
    assert ns_dict.item3.subitem32['subitem322'] == 322
    #
    assert ns_dict.item3.subitem31.subitem311 == 311
    assert ns_dict.item3.subitem31.subitem312 == 312
    assert ns_dict.item3.subitem32.subitem321 == 321
    assert ns_dict.item3.subitem32.subitem322 == 322


def test_setitem_existing_nested_preserves_siblings():
    """Setting a new sibling key under an existing nested NamespaceDict must
    not clobber the keys that were already there."""
    ns_dict = NamespaceDict()
    ns_dict['item1'] = {'subitem1': {'deep': 11}}
    ns_dict['item1.subitem2'] = 12
    assert ns_dict.item1.subitem1.deep == 11
    assert ns_dict.item1.subitem2 == 12
    # deep: add a key under an existing nested branch (parent already exists)
    ns_dict['item1.subitem1.nested'] = 99
    assert ns_dict.item1.subitem1.nested == 99
    assert ns_dict.item1.subitem2 == 12


def test_setitem_overwrite_leaf():
    ns_dict = NamespaceDict()
    ns_dict['a.b'] = 1
    ns_dict['a.b'] = 2
    assert ns_dict['a.b'] == 2
    assert ns_dict.a.b == 2


def test_delitem_and_delattr():
    ns_dict = NamespaceDict()
    ns_dict['item'] = 1
    assert ns_dict['item'] == 1
    del ns_dict['item']
    assert 'item' not in ns_dict
    ns_dict['other'] = 2
    del ns_dict.other
    assert 'other' not in ns_dict


def test_getitem_missing_returns_none():
    ns_dict = NamespaceDict()
    assert ns_dict['missing'] is None
    assert 'missing' not in ns_dict


def test_getitem_partial_dot_path_missing():
    ns_dict = NamespaceDict()
    ns_dict['item1'] = 1  # leaf, not a mapping
    # 'item1.subitem' -> self.get('item1') is 1, then 1.get('subitem') -> None
    assert ns_dict['item1.subitem'] is None


def test_getitem_always_returns_namespacedict():
    """A stored mapping must always come back as a NamespaceDict, never a
    plain dict, no matter how it was assigned."""
    ns_dict = NamespaceDict()

    # assigned as a raw dict
    ns_dict['a'] = {'x': 1}
    assert isinstance(ns_dict['a'], NamespaceDict)

    # nested raw dict inside
    ns_dict['b'] = {'c': {'d': 1}}
    assert isinstance(ns_dict['b'], NamespaceDict)
    assert isinstance(ns_dict['b']['c'], NamespaceDict)

    # a raw dict swapped in over an existing leaf
    ns_dict['e'] = 5
    ns_dict['e'] = {'f': 2}
    assert isinstance(ns_dict['e'], NamespaceDict)

    # every level supports attribute access
    assert ns_dict.b.c.d == 1


def test_getitem_wraps_list_items():
    ns_dict = NamespaceDict({'ports': [{'host': '1.1.1.1', 'port': 1},
                                       {'host': '2.2.2.2', 'port': 2}]})
    assert isinstance(ns_dict['ports'][0], NamespaceDict)
    assert ns_dict.ports[0].host == '1.1.1.1'
    assert ns_dict.ports[1].port == 2


def test_getitem_read_does_not_create_missing_key():
    """A pure read of a missing key must not pollute the dict."""
    ns_dict = NamespaceDict()
    _ = ns_dict['ghost']
    assert 'ghost' not in ns_dict
    assert list(ns_dict.keys()) == []


def test_attr_assignment_auto_creates():
    ns_dict = NamespaceDict()
    ns_dict.a.b = 1
    assert ns_dict.a.b == 1
    assert isinstance(ns_dict.a, NamespaceDict)
    ns_dict.a.c = 2
    assert ns_dict.a.b == 1
    assert ns_dict.a.c == 2

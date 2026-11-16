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
    assert ns_dict['item'] is None
    ns_dict['other'] = 2
    del ns_dict.other
    assert ns_dict.other is None


def test_getitem_missing_returns_none():
    ns_dict = NamespaceDict()
    assert ns_dict['missing'] is None
    assert ns_dict.missing is None


def test_getitem_partial_dot_path_missing():
    ns_dict = NamespaceDict()
    ns_dict['item1'] = 1  # leaf, not a mapping
    # 'item1.subitem' -> self.get('item1') is 1, then 1.get('subitem') -> None
    assert ns_dict['item1.subitem'] is None

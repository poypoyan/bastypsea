# Distributed under the MIT software license. See the accompanying
# file LICENSE or https://opensource.org/license/mit/.

from bastypsea import bastypsea


def test_UnitTest():
    outputs0 = bastypsea('./testdata/UnitTest.cls', 'Account', 'Delete')
    outputs1 = bastypsea('./testdata/UnitTest.cls', 'Account', 'Delete', False)
    assert len(outputs0) == 0
    assert len(outputs1) == 1


def test_SimpleDML():
    expected = [{'init_line_n': 10, 'line_n': 21, 'pline': '        daTabAse.INseRTiMmEDiatE(y, false);'},
                {'init_line_n': 9, 'line_n': 21, 'pline': ' insErT X;'}]
    outputs = bastypsea('./testdata/SimpleDML.cls', 'Contact', 'Insert')

    assert len(outputs) == 2
    for i in outputs:
        assert i in expected


def test_SimpleDML2():
    expected = [{'init_line_n': 23, 'line_n': 23, 'pline': '        DeLeTE [SELECT Id FROM  Contact LIMIT 5];'},
                {'init_line_n': 24, 'line_n': 24, 'pline': '        database.deleteAsync([SELECT Id FROM Contact LIMIT 5]);'}]
    outputs = bastypsea('./testdata/SimpleDML.cls', 'Contact', 'Delete')

    assert len(outputs) == 2
    for i in outputs:
        assert i in expected


def test_ComplexTypes():
    expected = [{'init_line_n': 17, 'line_n': 27, 'pline': '        UPSERT x.cuteAcc;'},
                {'init_line_n': 19, 'line_n': 28, 'pline': '        Database.upsert( testMap, true );'},
                {'init_line_n': 9, 'line_n': 29, 'pline': '        UPSERT y;'},
                {'init_line_n': 22, 'line_n': 30, 'pline': '        upsert z;'}]

    outputs = bastypsea('./testdata/ComplexTypes.cls', 'Opportunity', 'Upsert')

    assert len(outputs) == 4
    for i in outputs:
        assert i in expected

def test_ObjectNamesSubString():
    outputs = bastypsea('./testdata/ObjectNamesSubString.cls', 'Obj__c', 'Update')

    assert len(outputs) == 0

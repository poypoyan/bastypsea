# Distributed under the MIT software license. See the accompanying
# file LICENSE or https://opensource.org/license/mit/.

from bastypsea import bastypsea


def test_UnitTest():
    outputs0 = bastypsea('./testdata/UnitTest.cls', 'Account', 'Delete')
    outputs1 = bastypsea('./testdata/UnitTest.cls', 'Account', 'Delete', False)
    assert len(outputs0) == 0
    assert len(outputs1) == 1


def test_SimpleDML():
    expected = [{'init_line_n': 10, 'line_n': 16, 'pline': '        daTabAse.INseRTiMmEDiatE(y, false);'},
                {'init_line_n': 9, 'line_n': 16, 'pline': ' insErT x;'}]
    outputs = bastypsea('./testdata/SimpleDML.cls', 'Contact', 'Insert')

    assert len(outputs) == 2
    for i in outputs:
        assert i in expected


def test_ComplexTypes():
    expected = [{'init_line_n': 17, 'line_n': 24, 'pline': '        UPSERT x.cuteAcc;'},
                {'init_line_n': 18, 'line_n': 25, 'pline': '        Database.upsert( mapX2Y.keys(), true );'},
                {'init_line_n': 9, 'line_n': 26, 'pline': '        UPSERT y;'}]

    outputs = bastypsea('./testdata/ComplexTypes.cls', 'Opportunity', 'Upsert')

    assert len(outputs) == 3
    for i in outputs:
        assert i in expected

from bastypsea import bastypsea


def test_UnitTest():
    with open('./testdata/UnitTest.cls', 'r', encoding='utf-8') as fp:
        outputs0 = bastypsea(fp, 'Account', 'Delete')
        outputs1 = bastypsea(fp, 'Account', 'Delete', False)
    assert len(outputs0) == 0
    assert len(outputs1) == 1


def test_SimpleDML():
    expected = [{'init_line_n': 10, 'line_n': 16, 'pline': '        daTabAse.INseRTiMmEDiatE(y, false);'},
                {'init_line_n': 9, 'line_n': 16, 'pline': ' insErT x;'}]
    with open('./testdata/SimpleDML.cls', 'r', encoding='utf-8') as fp:
        outputs = bastypsea(fp, 'Contact', 'Insert')

    assert len(outputs) == 2
    for i in outputs:
        assert i in expected


def test_ComplexTypes():
    expected = [{'init_line_n': 16, 'line_n': 24, 'pline': '        UPSERT x.cuteAcc;'},
                {'init_line_n': 17, 'line_n': 25, 'pline': '        Database.upsert(mapX2Y.keys(), true);'}]

    with open('./testdata/ComplexTypes.cls', 'r', encoding='utf-8') as fp:
        outputs = bastypsea(fp, 'Opportunity', 'Upsert')

    assert len(outputs) == 2
    for i in outputs:
        assert i in expected

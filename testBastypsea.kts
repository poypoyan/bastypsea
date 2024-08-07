/*
Test bastypsea Kotlin.
Run command: kotlin -cp bastypsea.jar testBastypsea.kts

Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.
*/
import org.bastypsea.btsRun
import org.bastypsea.OutputEntry
import kotlin.io.path.Path

// poor man's testing
class AssertException(): Exception("Assertion failed.")

fun testUnitTest() {
    val outputs0 = btsRun(Path("./testdata/UnitTest.cls"), "Account", "Delete")
    val outputs1 = btsRun(Path("./testdata/UnitTest.cls"), "Account", "Delete", false)

    if (!(outputs0.size == 0)) throw AssertException()
    if (!(outputs1.size == 1)) throw AssertException()
}

fun testSimpleDML() {
    val expected = arrayOf<OutputEntry>(
        OutputEntry(10, 16, "daTabAse.INseRTiMmEDiatE(y, false);"),
        OutputEntry(9, 16, "insErT x;"),
    )
    val outputs = btsRun(Path("./testdata/SimpleDML.cls"), "Contact", "Insert")

    if (!(outputs.size == 2)) throw AssertException()
    for (i in outputs) {
        if(!(i in expected)) throw AssertException()
    }
}

fun testSimpleDML2() {
    val expected = arrayOf<OutputEntry>(
        OutputEntry(18, 18, "DeLeTE [SELECT Id FROM  Contact LIMIT 5];"),
        OutputEntry(19, 19, "database.deleteAsync([SELECT Id FROM Contact LIMIT 5]);"),
    )
    val outputs = btsRun(Path("./testdata/SimpleDML.cls"), "Contact", "Delete")

    if (!(outputs.size == 2)) throw AssertException()
    for (i in outputs) {
        if(!(i in expected)) throw AssertException()
    }
}

fun testComplexTypes() {
    val expected = arrayOf<OutputEntry>(
        OutputEntry(17, 27, "UPSERT x.cuteAcc;"),
        OutputEntry(19, 28, "Database.upsert( testMap, true );"),
        OutputEntry(9, 29, "UPSERT y;"),
        OutputEntry(22, 30, "upsert z;"),
    )
    val outputs = btsRun(Path("./testdata/ComplexTypes.cls"), "Opportunity", "Upsert")

    if (!(outputs.size == 4)) throw AssertException()
    for (i in outputs) {
        if(!(i in expected)) throw AssertException()
    }
}

fun testObjectNamesSubString() {
    val outputs = btsRun(Path("./testdata/ObjectNamesSubString.cls"), "Obj__c", "Update")

    if (!(outputs.size == 0)) throw AssertException()
}

testUnitTest()
testSimpleDML()
testSimpleDML2()
testComplexTypes()
testObjectNamesSubString()

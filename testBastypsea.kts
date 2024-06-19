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

fun testComplexTypes() {
    val expected = arrayOf<OutputEntry>(
        OutputEntry(17, 24, "UPSERT x.cuteAcc;"),
        OutputEntry(18, 25, "Database.upsert( mapX2Y.keys(), true );"),
        OutputEntry(9, 26, "UPSERT y;"),
    )
    val outputs = btsRun(Path("./testdata/ComplexTypes.cls"), "Opportunity", "Upsert")

    if (!(outputs.size == 3)) throw AssertException()
    for (i in outputs) {
        if(!(i in expected)) throw AssertException()
    }
}

testUnitTest()
testSimpleDML()
testComplexTypes()

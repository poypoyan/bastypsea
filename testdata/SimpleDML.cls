/*
These test data are not assumed to work--just to be Apex-like.

Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.
*/

public class SimpleDML extends ParentClass {
    public void method0(Contact x) {
        Contact y = new Contact(
            FirstName = 'Bob',
            LastName = 'the Builder'
        );

        // INSERT x; <-- this may trick parser
        daTabAse.INseRTiMmEDiatE(y, false); insErT x;
    }
}

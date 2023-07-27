/*
These test data are not assumed to work, but just to be Apex-like.

Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.
*/

public class ComplexTypes {
    public class SampleClass {
        public Boolean isCute {get; set;}
        public Account cuteAcc {get; set;}
        public Opportunity cuteOpp {get; set;}
    }

    public void method0(Id w, SampleClass x) {
        Map<Account, Opportunity> mapX2Y = new Map<Account, Opportunity>();
        mapX2Y.put(x.cuteAcc, x.cuteOpp);

        // false positives are allowed
        /*
        // <-- this may trick parser --> } Database.upsert(x); 
        */
        UPSERT x.cuteAcc;
        Database.upsert(mapX2Y.keys(), true);
    }
}

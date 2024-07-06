/*
These test data are not assumed to work, but just to be Apex-like.

Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.
*/

public class ComplexTypes {
    private SampleClass y;

    public class SampleClass {
        public Boolean isCute {get; set;}
        public Account cuteAcc {get; set;}
        public Opportunity cuteOpp {get; set;}
    }

    public void method0(SampleClass x, Id w) {
        // for maps, only values are captured
        Map<String, Opportunity> testMap = new Map<String, Opportunity>();
        mapX2Y.put(x.cuteAcc, x.cuteOpp);

        Opportunity[] z = new Opportunity[]{};

        /*
        // <-- this may trick parser --> } Database.upsert(x); 
        */
        UPSERT x.cuteAcc;   // false positives are allowed
        Database.upsert( testMap, true );
        UPSERT y;
        upsert z;
    }
}

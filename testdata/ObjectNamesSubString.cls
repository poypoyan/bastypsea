/*
These test data are not assumed to work, but just to be Apex-like.

Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.
*/

public class ObjectNamesSubString {
    public void method0() {
        Obj__c x = new Obj__c();
        LongerName_Obj__c y = new LongerName_Obj__c();
        Obj__c_Spec__c z = new Obj__c_Spec__c();

        UPDATE y; UPDATE z;
    }
}

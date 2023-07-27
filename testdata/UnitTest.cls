/*
These test data are not assumed to work, but just to be Apex-like.

Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.
*/

@isTest
public class UnitTest {
    @isTest static void method0() {
        Test.startTest();
        Account x = [SELECT Id, Name FROM Account WHERE (NOT Name LIKE '%Critical%') LIMIT 1];
        DELETE x;        
        Test.stopTest();
    }
}

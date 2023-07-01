# bastypsea
Basic Type Search for Apex language

This is for use in Salesforce Apex code debugging/investigation.
Given an SObject and a DML operation, this tool finds lines in Apex code
where there is a DML operation for a variable of type _that SObject_.
By default, this ignores test classes.

This is written to be easy to modify for other purposes, and to be
understood for porting to other languages.

**Limitations:**
1) Cannot detect multiline variable declarations and actions
   (e.g. when data type and variable name are in different lines).
   Why would you even do that?
2) There are no further checks for variable declarations of more
   complex data type like Maps, Inner Classes, etc.
   Hence, misses are possible for this.
3) Scope of variable declarations and actions are not considered
   (e.g. the action is inside which method).
   Hence, false positives are possible for this.

## License
Distributed under the MIT software license. See the accompanying file LICENSE or https://opensource.org/license/mit/.

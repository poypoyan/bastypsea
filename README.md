# bastypsea
Basic Type Search for Apex language

This is for use in Salesforce Apex code debugging/investigation.
Given an SObject and a database action, this tool finds lines in Apex code
where there is a database action for a variable of type "that SObject".
By default, this ignores test classes.

This is written to be easy to modify for other purposes, and to be
easily understood for porting to other languages.

**Instruction for Python prototype:**
1) Download the whole Apex codebase of your project.
2) Download the source code (zip or tarball, whatever's more familiar to you) in [Releases](../../releases).
3) Extract bastypsea.py.
4) Edit the Python script here:
```Python
my_obj = 'Contact'   # the SObject
my_act = 'Insert'   # the database action
my_path = r'./testdata/*.cls'   # the directory path to Apex classes
```
Note: the use of wildcard `*` to get all files is **required**.

You may disable ignoring test classes (thus also search to those)
by appending `False` as argument to the `bastypsea()` call:
```Python
outputs = bastypsea(file_name, my_obj, my_act, False)
```
5) Just run Python in terminal: `python bastypsea.py` (Windows)
or `python3 bastypsea.py` (Linux).

**Instruction for JAR file:**
1) Download the whole Apex codebase of your project.
2) Download the JAR file in [Releases](../../releases).
3) Just run `java -jar bastypsea.jar` to display usage.

**Limitations:**
1) Cannot detect multiline variable declarations and database actions
   (e.g. when data type and variable name are in different lines).
   Hence, misses are possible for this. *But why would you even do that?*
2) There are no further checks for variable declarations of more complex
   data types like Inner Classes, Maps, etc.
   Hence, false positives are possible for this.
3) Scope of variable declarations and actions are not considered
   (e.g. the action is inside which method).
   Hence, false positives are possible for this.
4) For all database actions, it is assumed that only one variable is inputted.
   Hence, misses are possible for this.

## License
Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.

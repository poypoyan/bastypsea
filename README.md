# bastypsea
Basic Type Search for Apex language

This is for use in Salesforce Apex code debugging/investigation/refactoring.

Do you want to find lines in your codebase (stored in your local env) wherein
an `Opportunity` is Inserted? Updated? Deleted? If yes, then this tool is for you!

In general, given an SObject and a database action, this tool finds lines in Apex classes
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

Here's a sample output:
```
$ java -jar bastypsea.jar Contact Insert ./testdata/
------
ini N: ./testdata/SimpleDML.cls:10
act N: ./testdata/SimpleDML.cls:16
act L: daTabAse.INseRTiMmEDiatE(y, false);
------
ini N: ./testdata/SimpleDML.cls:9
act N: ./testdata/SimpleDML.cls:16
act L: insErT x;
------
```
Where `ini N` is the line number where initialization of variable occurs, `act N` is the line number where the database action occurs, and `act L` is the actual line of `act N`.

The outputs of JAR file are designed so that paths are clickable in VS Code terminals. This leads us to...

**Adding JAR file to VS Code Terminal PATH environment variable:**

Copy the bastypsea.jar to a directory path, then [add that path to VS Code Terminal PATH](AddDirpath.md).

**Limitations:**
1) Cannot detect multiline variable declarations and database actions
   (e.g. when data type and variable name are in different lines).
   Hence, misses are possible for this. *But why would you even do that?*
2) Cannot detect the SObject as the type of *Map keys*.
   Hence, misses are possible for this. Again, *why oh why?*
3) There are no further checks for variable declarations of more complex
   data types like Inner Classes, Maps, etc.
   Hence, false positives are possible for this.
4) Scope of variable declarations and actions are not considered
   (e.g. the action is inside which method).
   Hence, false positives are possible for this.

## License
Distributed under the MIT software license. See the accompanying
file LICENSE or https://opensource.org/license/mit/.
## Adding File Path to a VSCode Terminal Environment Variable

1. Run VS Code/Codium.
2. Go to File Menu > Preference > Settings, or just press `Ctrl + ,`.
3. Search for `terminal.integrated.env.`. There should be three results, one each for Windows, Linux, and OS X. Then click the "Edit in settings.json" inside any of the three.
4. The settings.json opens with the following data added inside or focused on:
```JavaScript
    "terminal.integrated.env.<your os>": {
        ...
    },
```
Then add a new environment variable:
- For Linux and OS X, just add "bastypsea" key, and insert the **absolute** file path, like this:
```JavaScript
    "terminal.integrated.env.<your os>": {
        "bastypsea": "/home/SamplePC/Documents/MyDir/bastypsea.jar"
        ...
    },
```
- For Windows, just add "bastypsea" key, and insert the **absolute** file path such that backslashes are doubled to escape it, like this:
```JavaScript
    "terminal.integrated.env.<your os>": {
        "bastypsea": "C:\\Users\\SamplePC\\Documents\\MyDir\\bastypsea.jar"
        ...
    },
```
5. Save the settings.json.
6. Spin up a new terminal by going to Terminal Menu > New Terminal, or just press `` Ctrl + Shift + ` ``. That terminal should have the new environment variable.
7. To run the JAR: `java -jar $bastypsea ...` for Linux and OS X, and `java -jar ${env:bastypsea} ...` for Windows.
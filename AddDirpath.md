## Adding Directory Path to VSCode Terminal PATH Environment Variable

1. Run VS Code/Codium.
2. Go to File Menu > Preference > Settings, or just press `Ctrl + ,`.
3. Search for `terminal.integrated.env.`. There should be three results, one each for Windows, Linux, and OS X. Then click the "Edit in settings.json" inside any of the three.
4. The settings.json opens with the following data added inside or focused on:
```JavaScript
    "terminal.integrated.env.<your os>": {
        ...
    },
```
Then add or edit the "PATH" key:
- For Linux and OS X, just add "PATH" key if not exists, or append to its value the **absolute** path for your directory, like this:
```JavaScript
    "terminal.integrated.env.<your os>": {
        "PATH": "${env:PATH}:/home/SamplePC/Documents/MyDir"
        ...
    },
```
- For Windows, just add "PATH" key if not exists, or append to its value the **absolute** path for your directory such that backslashes are doubled to escape it, like this:
```JavaScript
    "terminal.integrated.env.<your os>": {
        "PATH": "${env:PATH};C:\\Users\\SamplePC\\Documents\\MyDir"
        ...
    },
```
5. Save the settings.json.
6. Spin up a new terminal by going to Terminal Menu > New Terminal, or just press `` Ctrl + Shift + ` ``. That terminal should have the updated PATH environment variable.
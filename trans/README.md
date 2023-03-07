Simple command line translator, based on DeepL's free API, no need to fill in API Key or anything like that.

### demo
![demo](./gif/demo.gif)

### install dependencies
```bash
pip install requests
pip install prompt_toolkit
```

### usage
```bash
chmod +x ./trans # give `trans` script executable privileges
./trans
```
Press `<C-d>` or `<C-c>` to exit.

### configuration
No configuration files. Please change the source code directly.

### input syntax
+ Enter the sentence to be translated directly.
+ `<LANG1> => <LANG2>` sets the source and target language. The source language will be set to `<LANG1>` and the target language will be set to `<LANG2>`. `<LANG1>` can be empty to indicate that the source language is automatically detected.
    + Spaces are not required. That's means `en => zh` and `en=>zh` are the same thing.
+ `<LANG1> => <LANG2>: <SENTENCE>` specifies the source language as `<LANG1>` and the target language as `<LANG2>` to translate `<SENTENCE>`. This approach does not change the default language settings. `<LANG1>` can be empty to indicate automatic detection.
    + Spaces are not required.

### acknowledgements
+ OwO-Network/DeepLX

### license
WTFPL

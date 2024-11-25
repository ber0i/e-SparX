# e-SparX - Python Package

In this directory, run the following line to install the package into your Python environment:

```bash
pip install .
```

> Currently, it is recommended to use Python 3.12 or lower!

## User Config

This tool can be configured using a global `config.json` file. The location of the configuration file changes depending on your operating system. The file is created, when you import the package the first time.

- MacOS: `$HOME/.config/esparx/config.json` (`$HOME` refers to your home directory: `Users/<username>`)
- Linux: `$XDG_CONFIG_HOME/esparx/config.json` (Defaults to `$HOME/.config/esparx/config.json`, `$HOME` refers to your home directory: `home/<username>`)
- Windows: `\Users\<username>\AppData\Local\esparx\esparx\config.json`

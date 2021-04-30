# 
🇸🇪 Släpp

Tool for quick tagging and deploying releases to Git. Släpp automatically generates and pushes CHANGELOG file to your repo, based on your commit history.

### Installation
```bash
pip install slapp
```

### Quick start
1. Init slapp config
```bash
slapp init
```
2. Edit slapp.yml file if needed
3. Do some stuff in your repo and commit it with * 
```bash
git add . && git commit -m "* Added some cool features!"
```
4. Generate release tag and build auto-changelog in one command!
```bash
slapp release
```

### Release

Only [Semantic Versioning](https://semver.org) is supported, versions have to be without prefixes or postfixes. 

Advanced usage of `release` command:
```bash
slapp release [OPTIONS] [MANUAL_VERSION]

Arguments:
  [MANUAL_VERSION]  Manually added version name

Options:
  -t, --type TEXT   Release type: major, minor, patch  [default: minor]
  --dry / --no-dry  Do not perform any actions with git repo  [default: False]
  --help            Show this message and exit.
```

### Versions

You can view all versions in repo by `versions` command:
```bash
slapp versions [OPTIONS]

Options:
  -l, --last INTEGER  Show only last N versions.
  -r, --reverse       Order versions by ascending.  [default: False]
```
For example, you want to see the earliest three versions:
```shell
slapp versions -r -l 3
```

### Add randomly generated namings

You can randomly name your releases from list or several lists of words.
Just add _random_names_ option to your config file:
```yaml
. . .
random_names:
- [ Aggressive, Brave, Calm ]
- ['Dog', 'Cow', 'Cat'] 
```

Släpp will automatically generate a release name for you by mixing words from given lists. For example: 
`0.1.0 Brave Cat` 

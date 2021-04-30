# Släpp

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

### Advanced usage
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
You can view this help by:
```bash
slapp release --help
```

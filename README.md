# Släpp

Tool for quick taggin and deploying releases to Git. Släpp automatically generates and pushes CHANGELOG file to your repo, based on your commit history.

### Installation
```bash
pip install slapp
```

### Usage
- init slapp config
```bash
slapp init
```
- edit slapp.yml file if needed
- do some stuff in your repo and commit it with * 
```bash
git add . && git commit -m "* Added some cool features!"
```
- release tag and build auto-changelog in one command
```bash
slapp release v0.1
```


# A430Py

A simulator and Gymnasium environment for **A430** aircraft.

## Install

### From source

```bash
git clone https://github.com/GongXudong/a430py
```

or

```bash
git clone https://www.gitlink.org.cn/gongxudong/a430py
```

### From PyPI

```bash
# use pip
pip install a430py

# use uv
uv add a430py
```

## Develop

### Prepare python environment

```bash
cd a430py
uv sync
```

### Pre-commit

```bash
# Install pre-commit
pre-commit install

# Run
pre-commit run --all-files  # run all hooks on all files
pre-commit run <HOOK_ID> --all-files # run one hook on all files
pre-commit run --files <PATH_TO_FILE>  # run all hooks on a file
pre-commit run <HOOK_ID> --files <PATH_TO_FILE> # run one hook on a file

# Commit
git add .
git commit -m <MESSAGE>

# Commit without hooks
git commit -m <MESSAGE> --no-verify

# update pre-commit hook
pre-commit autoupdate
```

### Build

```bash
uv build
```

### Publish

```bash
# publish to PyPI
uv publish

# publish to test.pypi
uv publish --index testpypi

# test publish
uv run --with a430py==0.1.3 -i https://test.pypi.org/simple/ --no-project -- python -c "import a430py;import gymnasium as gym;env=gym.make('A430Gym
-v0');print(env.reset())"
```

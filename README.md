# drivehound

## install

```sh
git clone https://github.com/mewmix/drivehound && cd drivehound
pip install .
```

## usage

run interactive recovery tool:

```sh
drivehound-recover
```

or import and use as a library:

```python
from drivehound import Hound
hound = Hound()
hound.recover_files(drive="/dev/sda")
```

## testing

```sh
pytest
```

## features

- signature-based carving
- cross-platform (linux, mac, windows)
- pure python, no dependencies


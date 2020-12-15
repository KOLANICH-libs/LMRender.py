LMRender.py [![Unlicensed work](https://raw.githubusercontent.com/unlicense/unlicense.org/master/static/favicon.png)](https://unlicense.org/)
===========
~~[wheel (GitLab)](https://gitlab.com/KOLANICH-libs/LMRender.py/-/jobs/artifacts/master/raw/dist/LMRender-0.CI-py3-none-any.whl?job=build)~~
[wheel (GHA via `nightly.link`)](https://nightly.link/KOLANICH-libs/LMRender.py/workflows/CI/master/LMRender-0.CI-py3-none-any.whl)
~~![GitLab Build Status](https://gitlab.com/KOLANICH-libs/LMRender.py/badges/master/pipeline.svg)~~
~~![GitLab Coverage](https://gitlab.com/KOLANICH-libs/LMRender.py/badges/master/coverage.svg)~~
[![GitHub Actions](https://github.com/KOLANICH-libs/LMRender.py/workflows/CI/badge.svg)](https://github.com/KOLANICH-libs/LMRender.py/actions/)
[![Libraries.io Status](https://img.shields.io/librariesio/github/KOLANICH-libs/LMRender.py.svg)](https://libraries.io/github/KOLANICH-libs/LMRender.py)
[![Code style: antiflash](https://img.shields.io/badge/code%20style-antiflash-FFF.svg)](https://github.com/KOLANICH-tools/antiflash.py)

A library to render lightweight markup languages into each other. The main purpose is rendering ReadMe files, mainly - into a terminal using ANSI escape sequencies.

## Goals

1. It is designed to be smol.

2. It is designed to allow a user to specify what he wants to get, not how exactly to do it.

3. It is designed to be moderately tweakable. An integrator can avoid using the unneeded backends, rebalance the priorities of the existing ones, and add own backends by just constructing an own instance of `Renderer`. A more careful tweaking of backend priorities can be done by subclassing the `Renderer` and redefining the method building the adjacency matrix.

4. Since is designed to require no mandatory dependencies, it is also designed to help projects integrating that lib to provide useful hints to end users about what packages they should install to get the needed functionality. (Currently this feature was broken when I was refactoring my lib).

5. It provides a function (`SupportedFormat.fromFileName`) to guess which source format is stored within a file by its extension.

## How to use

Basically the pipeline for working with my lib is the following:

```python
from LMRender import SupportedFormat as SF, DEFAULT_RENDERER

srcFileName: PurePath = getTheSourceFileName()  # integrator's
src: str = getTheSource(srcFileName)  # integrator's
targetFormat: SF = getTargetFormat()  # integrator's
fmt: SF = SF.fromFileName(srcFileName)
depsToInstall: typing.Iterable[str] = DEFAULT_RENDERER.isSourceUnavailable(fmt)
printMessageToAUserIfNeeded(depsToInstall)  # integrator's
rendered: str = DEFAULT_RENDERER.render(src, fmt, targetFormat)
displayRenderedToUser(rendered)  # integrator's
```

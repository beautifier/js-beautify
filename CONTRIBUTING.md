# Contributing
TODO - How to contribute


# Folders 
## js
## python
## web


# Branches
We use the `master` branch as the primrary development branch.  

## Releases
Each platform has a branch that tracks to the latest release of that platform.

* `python-stable`
* `node-stable`
* `gh-pages`

## Functional Parity
Keeping the platforms in some semblance of functional parity is one of the key features of this project.  As such, there branches for the last time synchronization occured and when it stablized. 

* `sync`
* `sync-stable` 

## Attic
This project has been around for a while.  While some parts have improved significantly over time, others fell
into disrepair and were mothballed.

### PHP
There is a out-of-date version of the beautifier available on branch `attic-php`.  If you're interested
in using it feel free. If you plan to enhance it, please consider joining this project, and updating this
version to match current functionality.

### Other Languages
Versions of the beautifier adapted to other languages are at least two years out-of-date and are
available on branch `attic-other`.  Take a look and feel free to resurrect them, but know it's pretty
dusty back there.

### Generic Eval Unpacker
The `attic-genericeval` branch includes an unpacker that call `eval` on whatever source is passed to it. 
Useful when working with source that unpacks itself when eval is called on it, but also unsafe.  We keep
it on this separate branch to keep it from hurting the other children. 


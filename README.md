# Hydrangea-Screen-Monitor

A homebrew package for safely monitoring remote screens.

## Install

This tool is temperarily not accepted by homebrew, so you can install it by brew tap

```bash
brew tap Zeyu-Xie/homebrew-core
```

then install it by brew

```bash
brew install hydrangea-screen-monitor
```

## Run

Use password to run the script

```bash
hydrangea-screen-monitor -p [password] [server] [screen ID]
```

or use SSH key to run the script

```bash
hydrangea-screen-monitor -k [private key path] [server] [screen ID]
```

You can also see the file version

```bash
hydrangea-screen-monitor -v
```

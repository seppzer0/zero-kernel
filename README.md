# zero-kernel

An advanced Android kernel builder with assets collection and Kali NetHunter support.

## Contents

- [zero-kernel](#zero-kernel)
  - [Contents](#contents)
  - [**Important**](#important)
  - [Description](#description)
  - [Kernel Features](#kernel-features)
  - [Supported Devices \& ROMs](#supported-devices--roms)
  - [Prerequisites](#prerequisites)
  - [Examples](#examples)
  - [See also](#see-also)
  - [Credits](#credits)

## **Important**

> [!IMPORTANT]
> **\- DISCLAIMER \-**
>
> **This kernel is made for educational purposes only.**
>
> **I am not responsible for anything that may or may not happen to your device by installing any custom ROMs, kernels and/or any other forms of software.**
>
> **Anything you do with this kernel and your device you do at your own risk. By using it, you take the responsibility upon yourself and in case of any issue you are not to blame me or other related contributors.**

> [!NOTE]
> \- ROM artifacts in releases \-
>
> The contents of each release include ROM builds compatible with corresponding kernel builds. These ROM files are **unmodified and mirrored from official sources**.
>
>This can be verified via the checksums, which should be identical to the ones presented on the ROM project's official web page.
>
>You can always download the same ROM file from official sources if you'd like. The mirroring in this repository is only done due to the fact that some ROM projects remove their older builds once they become too outdated.

## Description

The codebase of this project is an extensive build wrapper automating the entire Android kernel build process, starting from kernel source collection and ending with artifact packaging.

The key goal is to modify the kernel in such a way that enables unique features of [Kali NetHunter](https://www.kali.org/docs/nethunter) — a ROM layer designed to add extended functionality for penetration testing in a mobile form factor.

The architecture of this wrapper is ~~trying to be~~ as modular as possible, making it a little easier to add support for new devices.

## Kernel Features

The kernel has the following features:

- Kali NetHunter support;
- RTL8812/21AU + RTL8814AU + RTL8187 Wi-Fi drivers;
- packet injection support for internal Wi-Fi chipset;
- optional KernelSU support (v0.9.5, max compatible version for non-GKI kernels).

## Supported Devices & ROMs

<details>
<summary>OnePlus 5/T</summary>

- 4.4 Linux kernel version:
  - LineageOS;
  - ParanoidAndroid;
  - x_kernel supported (universal)`*`.

- 4.14 Linux kernel version:
  - ParanoidAndroid (unofficial & testing);
  - x-ft_kernel supported (universal)`**`.

`*` -- this is mostly relevant to ROMs based on LineageOS; however, technically speaking, this includes ParanoidAndroid as well, which makes x_kernel-based builds universal.

`**` -- this, **in theory**, is relevant to all 4.14-based ROMs for this device in existence.

</details>

## Usage

The custom build wrapper (aka "zkb") consists of 2 core components and 3 primary commands:

Components:

- kernel_builder ;
- assets_collector.

Commands:

- kernel ;
- assets ;
- bundle.

## Prerequisites

**It is highly recommended to use `docker` option to run this tool.** For that you need Docker Engine or Docker Desktop, depending on your OS.

> [!WARNING]
> Because of how *specific* Linux kernel source is, building it on Windows even with Docker (using WSL2 back-end) might be [challenging](https://stackoverflow.com/questions/76754956/how-to-clone-the-linux-kernel-repository-to-my-machine-i-keep-geting-errors).

To run this tool in a `local` environment, you will need:

- a Debian-based Linux distribution (other distribution families are untested);
- a few [packages](Dockerfile#L15) installed in your system;
- a configured Python environment with Python 3.12+.

```sh
# install uv version from project file
python3 -m pip install uv==$(cat ./uv-version.txt | tr -d ' \n')

# make zkb/ internal imports visible to itself
export PYTHONPATH=$(pwd)

# prepare and activate environment
uv sync --frozen
source .venv/bin/activate
```

Once you are finished working with the project, don't forget to disable the virtual environment (venv) via simple `deactivate`.

## Examples

Here are some examples of commands:

**(Recommended)** Build kernel and collect ROM via Docker:

```sh
uv run zkb bundle --build-env=docker --base=los --codename=dumpling --lkv=4.4 --package-type=slim
```

Build kernel locally:

```sh
uv run zkb kernel --build-env=local --base=los --codename=dumpling --lkv=4.4
```

Collect all of the assets locally:

```sh
uv run zkb assets --build-env=local --base=los --codename=dumpling --package-type=full
```

## See also

- [FAQ](docs/FAQ.md);
- [TODO List](docs/TODO.md);
- [Kernel Flashing Instructions](docs/FLASHING.md).

## Credits

- [kali-nethunter-kernel](https://gitlab.com/kalilinux/nethunter/build-scripts/kali-nethunter-kernel) : Official kernel patches from Kali NetHunter project.

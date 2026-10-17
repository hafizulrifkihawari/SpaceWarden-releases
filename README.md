# SpaceWarden

**Tidy Mac. Zero snooping.**

**Website: [hafizulrifkihawari.github.io/SpaceWarden-releases](https://hafizulrifkihawari.github.io/SpaceWarden-releases/)**

SpaceWarden shows what fills your Mac and helps you free up space, safely and privately.
This repository holds the downloads and the update information. The source code is private.

## Download

Get the latest disk image from [Releases](../../releases/latest).

1. Download `SpaceWarden.dmg`.
2. Open it, then drag SpaceWarden to the Applications folder.
3. Open SpaceWarden from Applications.

### Update to a new version

1. In SpaceWarden, select **SpaceWarden → Check for Updates…**.
2. If a new version is available, select **Download from GitHub**.
3. Quit SpaceWarden.
4. Open the new disk image, drag SpaceWarden to Applications, then select **Replace**.

Your settings and Full Disk Access stay.

## How you know a download is real

- Each disk image is signed with the developer's Developer ID and notarized by Apple. macOS
  checks both when you open it.
- `update.json` in this repository has an Ed25519 signature. SpaceWarden checks the signature
  before it shows a new version. A changed file shows no download link.
- SpaceWarden never downloads or installs an update by itself. You choose when to update.

## Privacy

SpaceWarden works offline. It connects to the internet only when you select Check for Updates.
Then it reads `update.json` from this repository and sends no information about you or your
files. It never accepts connections. Your file names, sizes and contents stay on your Mac.

Passwords, keys and private messages are never scanned or read.

## Requirements

macOS 15 Sequoia or later.

## Support

SpaceWarden is free, with every feature. If it freed space for you, you can support its work on
[Ko-fi](https://ko-fi.com/psi404). A tip gives no extra features.

Found a bug or have an idea? Open an [issue](../../issues).

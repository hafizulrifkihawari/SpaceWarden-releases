# SpaceWarden

**Tidy Mac. Zero snooping.**

**Website: [hafizulrifkihawari.github.io/SpaceWarden-releases](https://hafizulrifkihawari.github.io/SpaceWarden-releases/)**

SpaceWarden shows what fills your Mac and helps you free up space, safely and privately.
This repository holds the downloads and the update information. The source code is private.

## Download

> **Beta.** SpaceWarden is an early beta. It is not signed and notarized through Apple's
> Developer ID system yet, so macOS shows a security warning. If you downloaded the app from
> the official GitHub release, you can review the warning and use **System Settings → Privacy
> & Security → Open Anyway** to run it. Never turn off Gatekeeper.

Get the latest disk image from [Releases](../../releases/latest).

1. Download `SpaceWarden.dmg`.
2. Check the file. In Terminal, run `shasum -a 256 ~/Downloads/SpaceWarden.dmg`. The result
   must match the checksum on the release page (also in `SpaceWarden.dmg.sha256`). If it does
   not match, delete the file.
3. Open the disk image, then drag SpaceWarden to the Applications folder.
4. Open SpaceWarden from Applications. macOS shows a warning. Click **Done**.
5. Open **System Settings → Privacy & Security**, then click **Open Anyway** next to the
   SpaceWarden message. Enter your password.
6. Click **Full Scan**.

In the beta, macOS forgets Full Disk Access after each update. If you use it, turn it on again.

Full Disk Access is optional. Without it, the scan skips iCloud Drive, cloud storage, the data
of other apps and the Trash. To count them too, turn it on in **Settings → Privacy**.

### Update to a new version

1. In SpaceWarden, select **SpaceWarden → Check for Updates…**.
2. If a new version is available, select **Download from GitHub**.
3. Quit SpaceWarden.
4. Open the new disk image, drag SpaceWarden to Applications, then select **Replace**.

Your settings stay. SpaceWarden never downloads or installs an update by
itself. You choose when to update.

## Privacy

SpaceWarden works offline. It connects to the internet only when you select Check for Updates.
Then it reads `update.json` from this repository and sends no information about you or your
files. It never accepts connections. Your file names, sizes and contents stay on your Mac.

Passwords, keys and private messages are never scanned or read.

Read the full [Security & Privacy](https://hafizulrifkihawari.github.io/SpaceWarden-releases/security.html)
page: what the app reads and stores, the macOS permissions, and the checksum steps.

## Requirements

macOS 15 Sequoia or later.

## Support

SpaceWarden is free, with every feature. If it freed space for you, you can support its work on
[Ko-fi](https://ko-fi.com/psi404). A tip gives no extra features.

Found a bug or have an idea? Open an [issue](../../issues).

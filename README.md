# SpaceWarden

**Tidy Mac. Zero snooping.**

**Website: [hafizulrifkihawari.github.io/SpaceWarden-releases](https://hafizulrifkihawari.github.io/SpaceWarden-releases/)**

SpaceWarden shows what fills your Mac and helps you free up space, safely and privately.
This repository holds the downloads and the update information. The source code is private.

## Download

Get the latest disk image from [Releases](../../releases/latest).

1. Download `SpaceWarden.dmg`.
2. Check the file. In Terminal, run `shasum -a 256 ~/Downloads/SpaceWarden.dmg`. The result
   must match the checksum on the release page (also in `SpaceWarden.dmg.sha256`). If it does
   not match, delete the file.
3. Open the disk image, then drag SpaceWarden to the Applications folder.
4. Open SpaceWarden from Applications. If macOS shows a warning, click **Done**.
5. Then open **System Settings → Privacy & Security**, and click **Open Anyway** next to the
   SpaceWarden message. Enter your password.
6. Click **Full Scan**.

macOS can forget Full Disk Access after an update. If you use it, check it after an update.

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

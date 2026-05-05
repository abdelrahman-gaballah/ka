# Beginner Examples for Ka

This guide provides simple, real-world examples for beginners who are new to Linux or Ka.

## Table of Contents

1. [First Steps](#first-steps)
2. [Checking Your System](#checking-your-system)
3. [Working with Files](#working-with-files)
4. [Internet and Networking](#internet-and-networking)
5. [Managing Your Computer](#managing-your-computer)
6. [Everyday Tasks](#everyday-tasks)
7. [Common Problems and Solutions](#common-problems-and-solutions)

## First Steps

### Check if Ka is Installed

```bash
ka version
```

Expected output:
```
Ka version 0.1.0
```

### See All Available Commands

```bash
ka help
```

This shows all commands you can use, organized by category.

### Get Help for a Specific Command

```bash
ka help space
```

## Checking Your System

### How Much Free Space Do I Have?

```bash
ka space
```

This shows your hard drive space. Example output:
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       256G  120G  136G  47% /
```

### How Much RAM Is Being Used?

```bash
ka ram
```

Shows your memory usage. Example output:
```
              total        used        free      shared  buff/cache
Mem:           15Gi       4.2Gi       8.1Gi       234Mi       3.8Gi
Swap:         2.0Gi       0.0Ki       2.0Gi
```

### Is My Battery Running Out?

```bash
ka battery
```

Shows battery percentage and remaining time.

### How Long Has My Computer Been On?

```bash
ka uptime
```

Shows how long since last restart.

### What Operating System Am I Using?

```bash
ka os
```

Shows your Linux distribution name.

## Working with Files

### See What Files Are in a Folder

```bash
ka list
```

Shows all files and folders in your current location.

### See Files in a Different Folder

```bash
ka list Documents/
```

### Create a New Folder

```bash
ka create folder my_project
```

### Create an Empty File

```bash
ka create file notes.txt
```

### Copy a File

```bash
ka copy notes.txt my_project/
```

### Move a File

```bash
ka move notes.txt my_project/notes_backup.txt
```

### Rename a File

```bash
ka rename old_name.txt new_name.txt
```

### Delete a File

```bash
ka delete unwanted.txt
```

Ka will ask: `rm: remove regular file 'unwanted.txt'?` Type `y` and press Enter.

### Delete a Folder

```bash
ka delete folder old_folder/
```

### Find a File You Lost

```bash
ka find myfile.txt
```

This searches for `myfile.txt` in your current folder and all subfolders.

### Open a Folder in File Manager

```bash
ka open folder Downloads/
```

Opens your file manager showing the Downloads folder.

## Internet and Networking

### What Is My IP Address?

```bash
ka ip
```

Shows your local IP address.

### What Is My Public IP Address?

```bash
ka ip public
```

Shows the IP address the internet sees.

### Available WiFi Networks

```bash
ka wifi
```

Lists all WiFi networks near you.

### Connect to WiFi

```bash
ka wifi connect MyNetworkName MyPassword123
```

Replace `MyNetworkName` and `MyPassword123` with your actual WiFi credentials.

### Test If a Website Is Online

```bash
ka ping google.com
```

Sends 4 test packets to google.com. If you see replies, the website is online.

### Download a File from the Internet

```bash
ka download https://example.com/file.zip
```

Downloads the file to your current folder.

## Managing Your Computer

### Lock Your Screen

```bash
ka lock
```

Locks your screen without turning off the computer.

### Turn Off Your Computer

```bash
ka shutdown
```

Shuts down immediately. Make sure you saved your work!

### Restart Your Computer

```bash
ka restart
```

Reboots your computer.

### Put Computer to Sleep

```bash
ka suspend
```

Puts your computer into sleep mode.

### Update Your System

```bash
ka update
```

Updates all software on your computer. May ask for your password.

### Clean Up Unused Files

```bash
ka clean
```

Removes old package files to free up space.

## Everyday Tasks

### See Your To-Do List

```bash
ka todo
```

Shows your saved tasks.

### Add a Task to Your To-Do List

```bash
ka todo add "Buy groceries"
```

### Remove a Task

```bash
ka todo remove "Buy groceries"
```

### Take a Screenshot

```bash
ka screenshot
```

Opens an interactive screenshot tool.

### Take a Full Screen Screenshot

```bash
ka screenshot full
```

Takes a screenshot of your entire screen immediately.

### Set a Timer for 5 Minutes

```bash
ka timer minutes 5
```

You'll hear a sound when time is up.

### Set a Timer for 30 Seconds

```bash
ka timer 30
```

### Clear Terminal Screen

```bash
ka clear
```

Removes all previous text from your terminal.

### Check Weather

```bash
ka weather Cairo
```

Replace `Cairo` with your city name.

## Common Problems and Solutions

### Problem: `ka: command not found`

**Solution:** Ka is not installed. Run:

```bash
cd ka
./scripts/install.sh
```

### Problem: `Permission denied`

**Solution:** Some commands need administrator privileges. Try:

```bash
sudo ka update
```

Enter your password when prompted.

### Problem: I typed `ka space` but nothing happened

**Solution:** Check that Ka is working:

```bash
ka version
```

If you see version info, Ka is installed. Try restarting your terminal.

### Problem: `Command 'space' not found`

**Solution:** Make sure you typed `ka space`, not just `space`.

```bash
# Correct
ka space

# Wrong
space
```

### Problem: WiFi commands not working

**Solution:** Network Manager might not be installed. For Linux Mint, install it:

```bash
sudo apt install network-manager
```

### Problem: Volume commands don't work

**Solution:** PulseAudio might not be installed. Install it:

```bash
sudo apt install pulseaudio-utils
```

### Problem: I accidentally deleted a file

**Important:** Deleted files cannot be easily recovered. Always double-check before confirming deletion.

## Tips for Beginners

1. **Start simple** - Try `ka space`, `ka ram`, `ka list` first
2. **Use `ka help` often** - It shows all available commands
3. **Be careful with delete** - Always read the confirmation message
4. **Make backups** - Save important files before trying new commands
5. **Ask for help** - Search online or ask a friend if stuck

## Next Steps

After mastering these basics:

- Read the [Usage Guide](../usage.md) for more detailed instructions
- Explore [Advanced Examples](advanced.md) for more complex tasks
- Learn about [Custom Commands](../languages.md#customization) to create your own shortcuts

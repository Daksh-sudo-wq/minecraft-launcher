# Advanced Minecraft Launcher

A comprehensive Python-based Minecraft launcher with modern GUI support for offline/online play, mod management, resource pack management, and multiplayer server support.

## Features

✅ **Account Management**
- Offline account support (no login required)
- Microsoft account authentication
- Username customization

✅ **Mod Management**
- Import .jar mod files easily
- Enable/disable mods toggle
- View installed mods list
- Direct mods folder access

✅ **Resource Pack Management**
- Import .zip resource packs
- Enable/disable resource packs toggle
- Support for both .zip and folder formats
- Direct resourcepacks folder access

✅ **Multiplayer Server Support**
- Join any Minecraft server
- Custom server IP and port configuration
- Server configuration saved to launcher config

✅ **Version Management**
- Support for multiple Minecraft versions
- Latest release and snapshot versions
- Auto-detection of installed versions
- Version refresh capability

✅ **Performance Control**
- Configurable RAM allocation (1-16GB)
- JVM argument optimization

✅ **Modern User Interface**
- Dark theme UI
- Tabbed interface
- Real-time game status updates
- File management integration

## Installation

### Prerequisites
- Python 3.8 or higher
- Java Development Kit (JDK) or Java Runtime Environment (JRE)
- Minecraft (must be installed through official launcher at least once)
- Linux/macOS/Windows

### Setup Steps on Linux

1. **Clone/Download the Project**
```bash
cd ~/project/minecraft1
```

2. **Create Virtual Environment** (if not already done)
```bash
python3 -m venv ../.venv
source ../.venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install customtkinter minecraft-launcher-lib requests Pillow
```

4. **Run the Launcher**
```bash
python minecraft_launcher.py
```

Or use the provided run script:
```bash
bash run_launcher.sh  # Linux/macOS
# or
python minecraft_launcher.py
```
## installation guid on windows
1. **Download Python**
2. Go to the official - [python](https://www.python.org/downloads/)

3. **Create Virtual Environment (if not already done)**
 ```bash
 ..\\.venv\\Scripts\\activate
   ```

6.**Install Dependencies
 Open your Windows Command Prompt (cmd) and run:
```bash
   pip install customtkinter minecraft-launcher-lib requests Pillow
 ```

**Configure Java**
Ensure you have the appropriate Java version installed for your target Minecraft version (e.g., Java 8 for Minecraft 1.12.2 or below; Java 17/21 for modern versions).


**Run the Launcher**
Double-click the minecraft_launcher.py script inside your project folder, or run it through the Command Prompt:
```bash
python minecraft_launcher.py
```

## 🖥️ How to Create a Clickable Desktop Shortcut (No Terminal Required)
Opening a terminal every time to play a game is a hassle. Use these setups to create a standard, single-click application shortcut that completely hides the background terminal window.

**🐧 For Linux: Create a .desktop Launcher**
Open your terminal and create a new desktop entry file:
```bash
nano ~/.local/share/applications/minecraft_launcher.desktop
```
Paste the following configuration (make sure to replace YOUR_USERNAME with your actual Linux account username):
```bash
[Desktop Entry]
Type=Application
Version=1.0
Name=Minecraft Launcher Pro
Comment=Launch Custom Minecraft Client
Exec=/home/YOUR_USERNAME/project/minecraft1/../.venv/bin/python3 /home/YOUR_USERNAME/project/minecraft1/minecraft_launcher.py
Path=/home/YOUR_USERNAME/project/minecraft1/
Icon=gamepad
Terminal=false
Categories=Game;
```
Note: Setting Terminal=false is what keeps the terminal screen hidden.

Save and close the file (Ctrl+O, Enter, Ctrl+X). The launcher will now seamlessly show up in your system's application menu/drawer!


**For Windows: Create a No-Console VBS Shortcut**
Standard Windows batch (.bat) files still flash a black command prompt window briefly. To launch the code 100% silently, you can use a tiny script shortcut:

The folder containing your minecraft_launcher.py file, create a new text file and name it Launch.vbs (make sure to remove the .txt extension)

Open it in Notepad and paste the following lines:
```bash
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe minecraft_launcher.py", 0, False
```
Note: Using pythonw.exe running under mode 0 runs the game completely hidden in the background

Right-click your new Launch.vbs file ➡️ Show more options (if on Win 11) ➡️ Send to ➡️ Desktop (create shortcut).

Go to your desktop, right-click the new shortcut, select Properties, click Change Icon, and pick a cool gaming icon! Now, you just double-click that desktop icon to jump straight into the launcher.


### 🎮 Launcher Tab
1. **Select Account Type**: Choose between "offline" or "microsoft"
2. **Enter Username**: Your Minecraft username (for offline mode)
3. **Select Version**: Choose which Minecraft version to launch
4. **Allocate RAM**: Set memory (4GB recommended minimum)
5. **Enter Server** (Optional): For multiplayer, enter `server.ip:port`
6. **Click "LAUNCH GAME"**: Start playing!

### 📦 Mods Tab
1. Click **"➕ Add Mod"** to import a .jar file
2. Mods will be copied to `~/.minecraft/mods/`
3. Toggle **"Enable Mods"** to turn mods on/off
4. Select a mod and click **"❌ Remove Mod"** to delete
5. Click **"📁 Open Mods Folder"** to manage files directly

### 🎨 Resource Packs Tab
1. Click **"➕ Add Resource Pack"** to import .zip files
2. Resource packs are stored in `~/.minecraft/resourcepacks/`
3. Toggle **"Enable Resource Packs"** to activate
4. Select and click **"❌ Remove Resource Pack"** to delete
5. Supports both .zip files and folder formats

### ⚙️ Settings Tab
- View launcher information
- Access Minecraft directory
- Reset all settings to defaults

### ℹ️ Info Tab
- Complete help documentation
- Troubleshooting guide
- Feature overview

## Configuration

Settings are automatically saved to `launcher_config.json`:

```json
{
    "username": "YourUsername",
    "account_type": "offline",
    "version": "latest-release",
    "ram": 4,
    "mods_enabled": true,
    "resource_packs_enabled": true,
    "server_ip": "play.example.com:25565",
    "server_port": 25565
}
```

You can manually edit this file, but it's recommended to use the GUI.

## Directory Structure

```
~/.minecraft/
├── versions/           # Minecraft versions
├── mods/              # Mod files (.jar)
└── resourcepacks/     # Resource packs (.zip or folders)
```

Current working directory:
```
minecraft1/
├── minecraft_launcher.py    # Main launcher script
├── launcher_config.json     # Configuration (auto-created)
├── README.md               # This file
└── run_launcher.sh         # Convenience run script
```

## Troubleshooting

### Game Won't Launch
- **Check Java**: Ensure Java is installed: `java -version`
- **Check Minecraft**: Launch official Minecraft launcher once first
- **Check Version**: Ensure version is installed in `~/.minecraft/versions/`

### Mods Don't Load
- Verify mod .jar files are in `~/.minecraft/mods/`
- Ensure mods match your Minecraft version
- Toggle "Enable Mods" off and on
- Check mod compatibility

### Resource Packs Not Working
- Verify .zip file format is correct
- Check that .zip contains `pack.mcmeta` file
- Try placing resource pack in folder format
- Ensure format matches your MC version

### Server Won't Connect
- Format: `server.ip:port` (example: `play.mc.com:25565`)
- Verify server is online
- Check firewall/network settings
- Port 25565 is default for Minecraft

### Python Module Errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Verify virtual environment is activated
- Check Python version: `python --version` (need 3.8+)

## Advanced Features

### Command Line Launch
```bash
python minecraft_launcher.py --version 1.20.1 --username Player --ram 6 --server play.example.com:25565
```

### Manual Configuration
Edit `launcher_config.json` directly for advanced settings:
```json
{
    "username": "YourUsername",
    "version": "1.20.1",
    "ram": 8,
    "server_ip": "your-server.com:25565"
}
```

### Custom Mods Folder
You can symlink external mod folders:
```bash
ln -s /path/to/your/mods ~/.minecraft/mods
```

## System Requirements

- **OS**: Windows 10/11, macOS 10.13+, Linux (Ubuntu 18.04+, Fedora, etc.)
- **RAM**: Minimum 2GB free (4GB+ recommended with mods)
- **Disk**: 2GB minimum for Minecraft + mods
- **Java**: Java 8 or higher
- **Python**: Python 3.8+

## Performance Tips

1. **RAM Allocation**: 
   - Vanilla: 2-4GB
   - With Mods: 4-8GB
   - Heavy Mods: 8-16GB

2. **Optimization**:
   - Use OptiFine mod for better performance
   - Remove unused mods
   - Update Java to latest version

3. **Server Connection**:
   - Use LAN IP for local servers
   - Use full domain for remote servers
   - Check port forwarding if hosting

## Support & Issues

### Common Errors

| Error | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'minecraft_launcher_lib'` | Run: `pip install minecraft-launcher-lib` |
| `Java not found` | Install Java from java.com or use package manager |
| `Connection refused on server` | Verify server IP/port and firewall settings |
| `GUI doesn't appear` | Ensure display server is running (Linux X11/Wayland) |

## License

This launcher is provided as-is for personal use. Minecraft is copyright Mojang Studios.

## Version History

- **v2.0** (2026-06-04)
  - Complete rewrite with modern GUI
  - Added tabbed interface
  - Mod and resource pack management
  - Multiplayer server support
  - Configuration persistence

- **v1.0** - Initial console-based launcher

## Contributing

To improve this launcher:
1. Test all features thoroughly
2. Report bugs with reproduction steps
3. Suggest features via documentation

---

**Enjoy Minecraft!** 🎮

For more information about Minecraft mods, visit:
- [Curseforge](https://www.curseforge.com/minecraft)
- [Modrinth](https://modrinth.com/)
- [Planet Minecraft](https://www.planetminecraft.com/)

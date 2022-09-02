# plasmac2
A Plasma add-on for Axis configs using  LinuxCNC master branch. (v2.9)

## Installation
### Requirements for using plasmac2 are:
  * A working version of LinuxCNC Master branch (V2.9)
  * A working QtPlasmaC configuration
  * git
  * python3-git

### To install git, from a terminal enter:  
```console
sudo apt install git
```

### To install python3-git, from a terminal enter:  
```console
sudo apt install python3-git
```

### To install plasmac2, from a terminal enter:  
```console
git clone https://github.com/phillc54/plasmac2 ~/linuxcnc/plasmac2
python3 ~/linuxcnc/plasmac2/source/setup.py
```
From the setup application click **Install**  
When the installation is complete then either a migration or simulator creation may be done.
  * click **Migration** to create a new plasmac2 config based on an existing QtPlasmaC config.
  * click **Simulation** to create a new plasmac2 simulator config.

### To update plasmac2 there are two options:

From the plasmac2 GUI:  
click **Help** then click **Update**

From a terminal:
```console
cd ~/plasmac2
git pull
```

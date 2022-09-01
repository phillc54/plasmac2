# PlasmaC2
A Plasma add-on for Axis configs using  LinuxCNC master branch. (v2.9)

## Installation
### Requirements for using PlasmaC2 are:
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

### To install PlasmaC2, from a terminal enter:  
```console
git clone https://github.com/phillc54/PlasmaC2 ~/linuxcnc/PlasmaC2
python3 ~/linuxcnc/PlasmaC2/plasmac2/setup.py
```
From the setup application click **Install**  
When the installation is complete then either a migration or simulator creation may be done.
  * click **Migration** to create a new PlasmaC2 config based on an existing QtPlasmaC config.
  * click **Simulation** to create a new PlasmaC2 simulator config.

### To update PlasmaC2 there are two options:

From the PlasmaC2 GUI:  
click **Help** then click **Update**

From a terminal:
```console
cd ~/PlasmaC2
git pull
```

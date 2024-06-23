# Vector Blender Animation
Blender scenes and addon to animate custom animations for Vector.

## About The Addon
Vector Animation addon let you import decompiled animation bin from the game into Blender, and export animation into .bindec to compile and use in-game.
This project also includes rig and sample scene.

## Getting Started
This project required Vectorier Unity Editor to work along with - [Download Vectorier Unity Editor project](https://github.com/DoritoTheChips/Vectorier-Unity-Editor/archive/refs/heads/main.zip)


### Addon Installation
![image](https://github.com/FlipThoseTitle/Vector-Animator/assets/115728514/b78f665b-a5ae-4663-b26a-65ca138ac3e6)

**It is recommended to use blender 4.0+**
To install the VectorAnimation addon:
 * Go into the blender preferences, by clicking on Main Header>Edit>Preferences
 * Go to the 'Add-ons' category, and click on 'Install' to install a new addon.
 * Choose VectorAnimation.py on where you've it downloaded.
 * Search in your blender plugins and enable VectorAnimation in your addons preferences.

The Vector Animation panel should appear now. If not, press N to view the side panel. There should be two options for exporting and importing.

## Usage
Project includes 2 rig, sample animation and fbx file.
 * Vector Rig with armature (main one for animating and export)
 * Vector rig with node only (only for importing animation)
 * Vector node fbx
 * 1 Custom Animation (Backslide)

![image](https://github.com/FlipThoseTitle/Vector-Animator/assets/115728514/cc387d4e-d0e7-4cd6-8cc2-fc59cb2bd56d)

### Exporting & Importing
**Exporting:**
 * After you've installed the addon, simply open the main rig to start animating. Once you're done, you can export into .bindec and compile the bindec in Unity using Vectorier.

**Importing:**
 * It is recommended to use Vector Rig Node Only version.
 * To import animation, you have to decompile .bin using Vectorier first. The project should also comes with the decompiled vector animation dz folder.
 * Click import animation, you can now choose the .bindec you've decompiled to import the animation into blender.

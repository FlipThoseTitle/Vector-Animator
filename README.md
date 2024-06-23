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
Project includes 2 rig, sample animation, fbx file and necessary decompiled dz folder.
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

# Setting up
Setting up your animation to work in-game, requires many step to follow through. This will be a tutorial on how you can add your animation into the game.

### Dzip
In order to actually use it in-game, you'll have to add your own animation into "animations.dz". To do this, required a lot of steps. The project should already included the pre-configured dzip folder, ready to use.

### Adding Animation:
1. Copy every .bin from decompiled animation folder to input folder.
2. After compiling your animation in Unity, copy your .bin animation into the input folder.
3. Run _quickstart.bat_ to start comprsesing it into ".dz". After it's finished, there should be a new dz file in the output folder. Rename the dz to "animations.dz"
4. Copy the animations.dz to your Vector directory (Don't forget to make a backup of the original file.

# Trick Animation
Creating trick animation is a bit more complicated than cutscene animation due to numerous steps.

### Configuring Moves_new.xml
In your Vector directory, there should be a Move_news.xml, we need to configure the xml in order for the animation to work.
1. Open your Move_news.xml with notepad or other text editor programs (Notepad++ recommended)
2. Go into ReactionGroups > ReactionGroup Name="TrickGroup", you should see a list of animation configuration.
3. Add your own config
   ```xml
   example: <BackslideStart FirstFrame = "1" Priority = "10" OnEndTrigger="1" TriggerName="TriggerBackslide"/>
   ```
4. Scroll down to Moves section, you should see many animation configuration here. Find a space for you to write and add a new config.
   ```xml
   For the trick, please add any ID for it to work as a trick. ItemName should be TRICK_yourtrickname. Endframe is where your frame ends.
   example:
   <BackslideStart ID="200" ItemName="TRICK_BACKSLIDE" Type="3" Loop="0" VelocityX="0" VelocityY="0" DeltaDetectorH="20" DeltaDetectorV="40"
	FileName="backslide.bin" MidFrames="2" FirstFrame="0" EndFrame="51" PivotNode="DetectorH" Priority="2">
	  <Interval Start = "2" End = "48" Safe="1">
	    <OnEnd>
          <Reactions>
            <RunForward FirstFrame = "1" Priority = "1"/>
          </Reactions>
        </OnEnd>
	  </Interval>
	</BackslideStart>
   ```
   
### Configuring Objects.xml
After finishing up the Move_news.xml, we're going to add a new config to the Objects.xml
1. Go to your Vectorier project folder and follow the path, "\Assets\XML\dzip\level_xml". In the level_xml folder, open up the objects.xml with notepad or text editor.
2. Enter a new line and add your own config
   ```xml
   ItemName should be the same from your moves_new
   example:
   <Object Name="TriggerBackslide" Label="Trigger">
      <Content>
        <Area Name="TriggerBackslide" X="0" Y="0" Width="150" Height="200" Type="Trick" ItemName="TRICK_BACKSLIDE" Score="100"/>
      </Content>
    </Object>
   ```
### Adding trick images
Before you can test your animation in-game, you have to add trick images first. We are going to modify _"track_content_universal"_ and _"GUI_2048_1536"_. The project should also includes the decompiled folder required to do all these step.

**Track Content Universal:**
1. Copy every file from track_content_universal folder into dzip input folder.
2. Put your custom trick image or copy existing one, rename it to "TRACK_TRICK_yourtrickname" (eg. TRACK_TRICK_BACKSLIDE)
3. Run quickstart.bat and your output folder should have a new dz file, rename it to "track_content_universal" and copy it to your Vector directory.

**GUI_2048_1536:**
1. Copy every file from GUI_2048_1536 folder into dzip input folder.
2. Put your custom trick shop image or copy existing one, rename it to "SHOP_TRICK_yourtrickname" (eg. SHOP_TRICK_BACKSLIDE)
3. Run quickstart.bat and your output folder should have a new dz file, rename it to "GUI_2048_1536" and copy it to your Vector directory.

### Configuring common_xml
After adding trick images, we're going to add a new config to the common_xml
1. Copy every file in the common_xml folder into your dzip input folder.
2. Open up Shop_payed.xml with notepad or text editor program.
3. Add a new line under Shop > Group Name="TRICK", and then add a new config
   ```xml
   Note: Setting the item price to 0 will make you automatically obtain it, without having to purchase.
   example:
   <Item Price="2600" Name="TRICK_BACKSLIDE" ShopImage="SHOP_TRICK_BACKSLIDE" TrackImage="TRACK_TRICK_BACKSLIDE"/>
   ```
After that, we're going to modify localization_all.xml
1. Open up localization_all.xml with notepad or text editor program.
2. Scroll down until you see trick section such as Downtown tricks, Construction tricks
3. You can either make a new section or add into existing section (This doesn't affect where it would appear, it's just organizing the xml to be easy on eyes.)
4. Add a new config, this will be the trick name that appears in-game.
   ```xml
   example:
   <item_TRICK_BACKSLIDE eng="Sprint to Backslide"/>
   ```
After everything is done, run quickstart.bat and rename the dz file in the output folder to "common_xml", and copy the file to your Vector directory.

To add a trick trigger in Unity scene, add any tricks prefab and rename the prefab to your trick name from objects.xml (eg. TriggerBackslide) and buildmap. You can now test out the trick that you've made in your own map.

This should concludes everything for the trick animation.

# Cutscene Animation
Creating cutscene animation is easier, since you don't have to config many files in the game.

### Configuring Moves_new.xml
1. Open your Move_news.xml with notepad or other text editor programs (Notepad++ recommended)
2. Scroll down to Moves section, you should see many animation configuration here. Find a space for you to write and add a new config.
   ```xml
   example:
    <CS02DownTownHelpBotPart1 ID="0" Type="1" 
    FileName="cs02_helpbot_part1.bin" MidFrames="2" FirstFrame="0" EndFrame="41" PivotNode="DetectorH" Priority="2">
      <Interval Start = "0" End = "41" Safe="1"/>
    </CS02DownTownHelpBotPart1>
   ```
### Adding animation event trigger in Unity scene.
Instead of adding config to objects.xml, we're going to add a more customizable trigger inside our Unity scene.
1. Add a new trigger sprite from textures folder and name it anything you want.
2. Set the gameobject tag to "Trigger"
3. Add a new component under the gameobject called "TriggerSettings" (Add Component > Vectorier > Trigger Settings)
4. In the inspector panel, you should see content textbox. Add the following config to the textbox area.
   ```xml
   example:
   <Init>
              <SetVariable Name="$Active" Value="1"/>
              <SetVariable Name="$AI" Value="0"/>
              <SetVariable Name="$Node" Value="DetectorH"/>
              <SetVariable Name="AnimName" Value="CS02DownTownHelpBotPart1"/>
              <SetVariable Name="AnimFrame" Value="1"/>
              <SetVariable Name="Reversed" Value="0"/>
            	<SetVariable Name="Flag1" Value="0"/>
            </Init>
            <Template Name="ForcedAnimation"/>
   ```
5. Buildmap and test the animation in-game. Where the animation will trigger depends on your trigger sprite size.

This should concludes the tutorial on how to add your own animation into vector, Have fun animating!
Note: Rig may not the best, as I have never rig in blender before. Feel free to improve upon it.

![image](https://github.com/FlipThoseTitle/Vector-Animator/assets/115728514/8c058df8-da9d-43d7-b11e-40b22fd22022)

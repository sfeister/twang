# Building the Instrument Hardware

By Dr. Scott Feister

Updated March 2, 2025

In this guide, I will skim over the steps of setting up your hardware. The target audience is a middle school student or teacher. Prior to beginning this guide, you should have read the guide on Laser Safety.

## Example circuit layouts

* For a ten-string laser harp, you could build the circuits shown in [the Harp circuit diagram](https://github.com/sfeister/twang/raw/master/diagrams/HarpCircuitDiagram.pdf).

* For a six-string laser guitar with five unique chords, you could build the circuits shown in [the Guitar circuit diagram](https://github.com/sfeister/twang/raw/master/diagrams/GuitarCircuitDiagram.pdf).

## 3D print your phototransistor and laser mounts

##### Note:

If you are using LEDs rather than lasers for your light source, you will want to design your own LED holders or buy them online! You can still print the Tinkercad objects below to get the phototransistor holders.

##### Parts needed:

* 3D printer
* Black PLA printer filament

##### Instructions:

The link below on Tinkercad is for a set of ten laser holders and light catchers that I designed -- mounts for the lasers and phototransistors that you can use in your laser instrument. It took about 10 hours on our printer. 3D print in *black* PLA with 100% infill and 0.15 mm resolution, or as close to this as you can.

https://www.tinkercad.com/things/kMZ0uLT9j7g 

## Design and build your instrument shell

##### Parts needed:

- Maker lab
- Creativity

##### Instructions

This is the fun part! You can design and build whatever form factor you'd like for an instrument -- a guitar, a banjo, a harp, a piano, something we've never thought of! Discuss your ideas with your teacher and use the tools of a Maker Lab (e.g. a CNC wood router, saws, 3D printer, etc.) to create your own special instrument shell.

Here are some factors to consider during your design and construction of your instrument shell:

* Make sure to leave enough space for the Pi Pico and your wiring.

* Put appropriately-sized holes in where you want to mount your buttons.

* If you are going to use lasers, make sure to carefully follow the design suggestions in the [Laser Safety Guide](Safety.md), especially designing in physical safeguards as discussed in that guide. However, **do not install any lasers or phototransistors yet** (this will be covered in a future section of this guide.)

* You can use your light holders and light catchers that you 3D printed to get a sense of how much space they'll take up, but **don't glue your holders/catchers yet**.

## Mount your buttons

##### Parts needed:

* Arcade-style momentary pushbuttons to act as chord buttons (if desired)

##### Instructions:

If you are going to be panel-mounting your chord buttons, go ahead and mount them now! However, you don't need to connect these into a circuit yet.

## Assemble your light catchers

##### Parts needed (for each string):

- One HW5P-1 phototransistor (or similar; e.g. [from Adafruit](https://www.adafruit.com/product/2831))

- One 3D-printed phototransistor holder (You 3D printed ten of them above)

- One 3D-printed barrel (You 3D printed ten of them above)

##### Additional parts needed:

- Hammer + tissue paper (or rubber mallet)

##### At the end of this section you should:

- Have all of your phototransistors fully-enclosed into their fully-hammered- together 3D-printed mounts. (See example image of [constructed catchers](img/constructedcatchers.JPG).)

##### Instructions:

1. Check the quality of your barrel. Hold it up to the light so that you can see that light is getting through the central hole. Scrape out the central hole with a wire/paper-clip as needed to clear out the extra PLA filament that may have accumulated in the hole. (See example image of a [clean barrel](img/cleanbarrel.JPG).)

2. Push the phototransistor into the mount so that the two wires poke out the back. You may wish to close one eye while doing this to improve your ability to get the metal leads through the two holes.

3. Once you've pushed it in by hand and both wires are popping out the back, ram the phototransistor the rest of the way in, e.g. with a cue tip, to make it flush with the bottom.

4. Bend down the two phototransistor lead wires down that are now popping out the back of your plastic holder.

5. By hand, push the 3D printed barrel piece onto the phototransistor holder as far as you can. It should now be covering up the phototransistor, and the only path for light to get to the phototransistor is through the central hole. In my case, pushing the barrel fully into place took a lot of force and finger strength.

6. Hammer the barrel the rest of the way into place. That is, flip the phototransistor holder + barrel, which are now combined, and place barrel face-down on a table. Put some tissue paper over the bent-down leads (to protect them) and then hammer until the barrel is in as far as it will go.

## Align and glue your light sources and light catchers

##### Note:

If you are using lasers rather than LEDs as your light source, adult supervision at your table is required for the entirety of this section. Also, you must read the [Laser Safety Guide](Safety.md) before proceeeding.

This section is kind of tricky but is essential to the functionality of your light instrument! You may wish to have help from someone who has done the alignment before, to show you the ropes.

##### Parts needed (for each string):

- One LED or laser, depending on your design (e.g. this 3V, 5 mW red dot laser from [Amazon](https://www.amazon.com/Ferwooh-20PCS-Copper-semiconductor-Diameter/dp/B0CYZ9G969)
- One LED holder or laser holder (e.g. 3D printed in the earlier step) 
- One fully assembled light catcher (from the prior step)

##### Additional parts needed:

- Hot glue
- Your instrument shell
- Multimeter

##### Instructions

[REMINDER: This section is discussed at length in the [Laser Safety Guide](Safety.md)! If you are using lasers, read that guide completely before proceeding.]

[NOTE: If you are using lasers, they should not be powered on yet.]

1. On your instrument shell, carefully measure and mark  where your light catchers and light sources should go.

2. Carefully align and hot-glue your light catcher in place. Press firmly to keep the base flush with the instrument surface, and carefully aim the barrel towards the location of its light source. Use only as much hot glue as needed -- avoid giant globs of glue that the light catcher will "float on". Hot glue dries in seconds, so here are the goals to keep in mind in the moments where you place the light catcher: (1) Ensure that the base is secured to the instrument shell, (2) ensure the barrel is level with the instrument surface, and (3) ensure the barrel is aimed towards the spot where the light source will be placed. 

3. Mount your LED or laser into the LED holder or laser holder.

4. If you are using a laser:
   
   1. Before powering the laser: Mount the laser in its holder, place the mounted laser on the mark you made earlier, and aim it generally towards the wall.
   
   2. After ensuring safety per the guide, and with direct adult approval and management, connect the laser directly to a 5V power supply.
   
   3. Aim the laser towards its light catcher.
   
   4. Carefully rotate the laser **within** its mount such so that its aim is **vertically** level with the light catcher.
   
   5. Once you're happy with the vertical alignment, rotate the **mount itself** so that the center of the beam hits the center of the barrel of the light catcher.
   
   6. Once you are confident that the beam is hitting the barrel hole dead-center, glue it into place. You will almost certainly need to do a quick re-alignment of the mount itself in the seconds while the glue dries. Hold it for about twenty seconds before letting go, because even slight movement of the laser while drying will result in misalignment.

5. If you are using an LED:
   
   1. Mount the LED in its holder.
   
   2. Aim the LED in the direction of your light catcher.
   
   3. Glue or otherwise mount the LED into place.

6. Hook up a multimeter to each phototransistor (make sure + goes to the long lead!), and set it to measure the effective resistance. You may wish to make a table to record the "resistance when blocked" and "resistance when unblocked" for each phototransistor. This will be a good record to keep for future troubleshooting with your teacher. When lasers/LEDs are blocked by your finger, each phototransistor should have an effective resistance of at least five times greater than 6.8 kiloOhms (e.g., I measured about 600 kiloOhms). When the laser is shining  unblocked, each should have an effective resistance of at least five times less than 6.8 kiloOhm (e.g., I measured about 100 Ohms). This will ensure a clean on/off digital signal, when paired with a 5 V power supply and a 6.8 kiloOhm resistor in a later step.

## Gather your parts for the circuits

##### Parts needed:

- Your Pi Pico

- Your instrument shell with light catchers, light sources, and buttons already securely mounted (see prior steps)

- For each string, one 6.8-kiloOhm resistor (e.g. if you have six strings, need six resistors)

- Female-to-male jumper wires, if you're going to use breadboards (e.g. [from Adafruit](https://www.adafruit.com/product/826))

- Spare wire, breadboards

- Soldering station

#### Instructions

[Pi Pico Pin Diagram](https://www.raspberrypi.com/documentation/microcontrollers/pico-series.html#pinout-and-design-files-3)

Make, solder, connect, breadboard, etc. all the circuits:

* For a ten-string laser harp, you could build the circuits shown in [the Harp circuit diagram](https://github.com/sfeister/twang/raw/master/diagrams/HarpCircuitDiagram.pdf).

* For a six-string laser guitar with five unique chords, you could build the circuits shown in [the Guitar circuit diagram](https://github.com/sfeister/twang/raw/master/diagrams/GuitarCircuitDiagram.pdf).

Don't hesitate to ask for help on this section!
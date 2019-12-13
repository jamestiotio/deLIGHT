# deLIGHT
**SUTD 2019 03.007 Introduction to Design Project**

_Theme: At Play 2.0_

19F07 Group 1 Team Members:
- [James Raphael Tiovalen](https://github.com/jamestiotio) (Team Coordinator & Project Manager)
- [Sharmayne Lim Zhiyu](https://github.com/sl194) (Creative Director & Lead Artist)
- [Velusamy Sathiakumar Ragul Balaji](https://github.com/ragulbalaji) (Software Specialist & Technical Advisor)
- [Mun Jern Wei Ivan](https://github.com/monkeychimpanzee) (Project Advisor & Lead Actor)
- Kenneth Chin Choon Hean (Chief Mechanical & Electrical Engineer)

Since GitHub limits single file size to 100 MB, the project video could not be uploaded/committed to GitHub. Instead, it is available on YouTube [here](https://youtu.be/HanKIdMyvy4).

## Problem Statement

Unsupervised children playing with lighters leads to grave consequences (supported by statistics of burns and deaths worldwide). Additionally, lighters which have run out of fuel are rendered useless in situations whereby lighter refills and charging points are unavailable. Our solution prevents children from activating the lighter when they come into contact with it as it has a fingerprint lock that only registered fingerprints are able to unlock. Also, when our lighter has run out of fuel, there is an option to recharge it by winding it. At the same time, our lighter allows children to have fun by playing video games on it or winding it.

## Product Description

The key highlighted features of our product are:

1. **Fingerprint Sensor**

This capacitive sensor allows us to capture, collect, store and sense fingerprint patterns. This feature is used to restrict access to the lighter.

2. **M5Stick-C**

This is the big boi that does most of the work. This mini IoT core device is based on the ESP32 chip and is equipped with common features, such as Wi-Fi, Bluetooth, LCD Display, LED, Button, Buzzer, IR Transmitter, Battery and Six-Axis MPU. This allows us to do some cool, unconventional integrations of certain systems that only involve light processing power to the lighter. Such an example would be the simple game feature that would run when an unauthorised fingerprint is detected. Note that the fingerprint detection callback still runs asynchronously while the game is running. The game that we currently implement is a simple low-level adaptation of Flappy Bird with balloons as obstacles. Of course, given more time and effort, more intricate games could potentially be written (although care needs to be taken regarding memory usage and the fact that it is very troublesome to write the graphics and physics drivers from scratch).

3. **Plasma Lighter**

Instead of using gas fuel, we utilise a more sustainable, reusable and rechargeable energy source such as a battery. A possible case illustration of its sustainability is that this would reduce the amount of plastic unintentionally consumed by animals like birds. The battery could be charged either through the USB port or by using the hand crank.

4. **Speaker**

Our product is also equipped with a piezoelectric speaker that provides auditory feedback to convey messages or to reinforce certain actions that the user had done.

5. **Hand Crank**

The lighter is equipped with a detachable hand crank that could be wound to provide more energy through its charging circuit.

## Design Requirements & Choices

1. Our product needs to be tightly linked to a specific object taken from a preselected list of suggested, well-designed objects. Our object of focus was the Zippo lighter.

2. We only had a budget of SGD$500 and thus, we sourced for cheap PLA material to construct the lighter's casing and we also sourced for relatively cheaper alternatives of fingerprint sensors and IoT processors.

3. We chose a winding method instead of a shaking mechanism since, by performing some rough preliminary estimations and calculations, we found that winding would provide more energy to the battery (or the device) than shaking.

4. Limitations of our product are mainly centered around energy efficiency, ease of use and ergonomics:

    - The concern over the energy efficiency of the hand crank is relevant to our project. Conversion from mechanical to electrical energy is usually not very efficient since a lot of energy is wasted as heat and sound.

    - Another plausible and reasonable concern is that users would find it a hassle to have to unlock a mere lighter with their fingerprint every time they want to use it. Thus, we tried to implement the Wi-Fi verification method as well as a proof of concept in order to make it slightly easier for users to use the lighter.

    - Finally, the overall size of the lighter is larger than the usual lighter. This is due to the slightly bulky structure of the M5Stick-C. On the other hand, the M5Stick-C is jam-packed with plenty of features in such a tight space that the temptation to include everything in such an Apple-like compact design is quite high.
    
5. Our design focus is on rapid prototyping, as well as iterative development and feature testing. Therefore, our code currently should only be used during development and not in a production-level environment.

## Acknowledgements

Credits to [Prof. Arlindo Silva](https://epd.sutd.edu.sg/people/faculty/arlindo-silva) and [Prof. Daniel Joseph Whittaker](https://asd.sutd.edu.sg/people/faculty/daniel-joseph-whittaker) as our cohort instructors who guided us through every single step of this journey!

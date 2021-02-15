# FuzzyLogicController
Developed a fuzzy logic controller to dynamically adjust applied voltage to maintain water level stayed at a desired level inside a leaking tank. The project contains two parts with different parameters. Please refer resources for details.

## Problem Identification
![alt text](https://github.com/damien2012eng/FuzzyLogicController/blob/main/Resource/Images/Problem.JPG?raw=true)
Let's denote variables first: V applied voltage to the pump. H Water height in the tank. R the radius of the tank. Both a and b are constant parameters related to flow rate.

## Methodology

The approach to solving this assignment is followed by the steps below.
● Create fuzzy variables
● Create three fuzzy logic membership functions
● Define fuzzy rules that applied on the membership functions
● Create an ODE function using the provided differential equation.
● Apply initial values to compute the initial voltage by using the predefined fuzzy logic
● Compute the new height/height change using the current-voltage.
● Run a for-loop for several iterations of the last two steps.

## Results
### membership function
![alt text](https://github.com/damien2012eng/FuzzyLogicController/blob/main/Resource/Images/MembershipFunctionP1.JPG?raw=true)
### Water height and applied voltage (Part 1)
![alt text](https://github.com/damien2012eng/FuzzyLogicController/blob/main/Resource/Images/ResultsP1.JPG?raw=true)
### Water height and applied voltage (Part 2)
![alt text](https://github.com/damien2012eng/FuzzyLogicController/blob/main/Resource/Images/ResultsP2.JPG?raw=true)

## Observation
A universal approach is provided to handle both part 1 and Part 2 with different parameters. The fuzzy logic controller adjust the voltage changing ratio(v/s) and acceleration rate (r/s^2) instead of the voltage to control the applied voltage. As shown in the results section, water height oscillates around the targeted height, while the applied voltage oscillates as well to dynamically adjust the water height. 

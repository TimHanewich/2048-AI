## Exlaining the folders
- **models** - First implementation. Development ended on this commit *3cbd1287113f01dc7fc61f25e0850c716140733d*
- **models2** - Added more hidden layers, started new model from scratch.

## Structure 1 Tests
- 2023-01-29 04-35-08.354122
    - Avg Max Value: 94.72  
    - Avg Concentration: 17.55
- 2023-01-29 04-45-13.728451
    - Avg Max Value: 125.44  
    - Avg Concentration: 20.365
- 2023-01-29 21-26-03.641107
    - Avg Max Value: 124.16  
    - Avg Concentration: 23.3
- 2023-01-30 03-18-12.587640
    - Avg Max Value: 163.84  
    - Avg Concentration: 26.55
- 2023-01-30 13-56-54.905192
    - Avg Max Value: 181.76
    - Avg Concentration: 28.305
- 2023-01-31 04-08-31.118039
    - Avg Max Value: 126.72
    - Avg Concentration: 24.215

## Structure 2
I'm adding significantly more hidden neurons to a model and training from there. 

I halted it's training on January 31, 2023 @ 11:43 PM. It clearly is not working.

### Tests
- 2023-01-31 04-46-14.085862 (start/after only 1 training)
    - Avg Max Value: 105.4
    - Avg Concentration: 19.24375
- 2023-01-31 05-06-47.336688
    - Avg Max Value: 113.6
    - Avg Concentration: 21.1109375
- 2023-01-31 13-44-33.655633
    - Avg Max Value: 104.4
    - Avg Concentration: 16.6125
- 2023-01-31 15-45-44.891697
    - Avg Max Value: 82.4
    - Avg Concentration: 17.421875
- 2023-01-31 18-45-10.140012
    - Avg Max Value: 108.4
    - Avg Concentration: 18.45
- 2023-02-01 04-26-09.856992
    - Avg Max Value: 104.8
    - Avg Concentration: 18.059375

## models4
This uses a different learning method. This plays X number of games side by side. Then selects the game that worked out the best. Then trains the neural network on every decision that was made during that game.

**I did notice a critical error in my code around 9:50 AM EST on February 3, 2023. I was declaring the list properties of classes outside of the __init__ which is they they were building up so many child elements (shared amongst all instances of the class). I corrected it and continued on. Any model after 2023-02-03 12-41-39.969567 is trained using the new version**

### Tests
- 2023-02-01 20-06-10.626808
    - Avg Max Value: 128.4
    - Avg Concentration: 18.5890625
- 2023-02-01 23-52-37.388295
    - Avg Max Value: 135.2
    - Avg Concentration: 19.7078125
- 2023-02-02 02-46-35.077023
    - Avg Max Value: 125.8
    - Avg Concentration: 18.215625
- 2023-02-02 12-39-01.253694
    - Avg Max Value: 114.8
    - Avg Concentration: 17.4875
- 2023-02-02 12-39-01.253694
    - Avg Max Value: 126.8
    - Avg Concentration: 17.9609375
- 2023-02-02 16-42-30.178057
    - Avg Max Value: 136.0
    - Avg Concentration: 19.3109375
- 2023-02-03 04-19-27.234289
    - Avg Max Value: 167.0
    - Avg Concentration: 22.625
- 2023-02-03 12-41-39.969567
    - Avg Max Value: 148.8
    - Avg Concentration: 21.196875
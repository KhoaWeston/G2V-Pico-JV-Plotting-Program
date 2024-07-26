# G2V-Pico-JV-Plotting-Program
 This program plots the raw data from the University of Toledo's G2V Pico's JV measurement device for solar cell characterization. Given the voltage and current density readings, the program will plot a number of curves, as well as include the sample's PCE, FF, Voc, Jsc, temperature coefficients, etc. 

![QE Example Plot](https://github.com/KhoaWeston/QE-Plotting-Program/blob/master/QE%20Example%20Plots.png)

## How to Build
1. Clone the repository
2. Open the project folder using your personal Python IDE
3. Run the following commands in the terminal:
```
pip install matplotlib
```
```
pip install numpy
```

## How to Use
1. Specify the directory where your data is stored in the 'directory' variable.
2. Change the 'sample_ID' variables to correspond with your personal file naming convention.
3. Run the program.

## Result
- A new folder will be created within the specified directory named 'Plots'
- Within the new folder, you will get a couple of plots:
  * QE curve for each file
  * Plot of both subcell's QE curves
- Displayed will be the sample's Jsc in both AM1.5G and AM0, Jsc mismatch in both spectra, and subcell band gap. 

## References
 

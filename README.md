# G2V-Pico-JV-Plotting-Program
 This program plots the raw data from the University of Toledo's G2V Pico's JV measurement device for solar cell characterization. Given the voltage and current density readings, the program will plot a number of curves, as well as include the sample's PCE, FF, Voc, Jsc, temperature coefficients, etc. 

![JV Example Plot](https://github.com/KhoaWeston/QE-Plotting-Program/blob/master/JV%20Example%20Plots.png)

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
2. Change the `get_names` function to correspond with your personal file naming convention.
3. Run the program.

## Result
- A new folder will be created within the specified directory named 'Plots'
- Within the new folder, you will get several plots:
  * Individual JV curves for each data file 
  * All JV curves at a given temperature at different spectra stacked on one another
  * All JV curves at a given solar spectra at different temperatures stacked on one another
  * PCE, Jsc, Voc, and FF vs solar spectra at a given temperature with one showing the points connected and the other with a line of best fit
  * PCE, Jsc, Voc, and FF vs temperature at a given solar spectrum with one showing the points connected and the other with a line of best fit
- Displayed will also be the temperature coefficients and estimated air mass coefficients 

## References
 

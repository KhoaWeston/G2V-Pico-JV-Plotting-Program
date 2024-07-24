from matplotlib import pyplot as plt
import numpy as np
import os
import itertools
import re


# Program variable initializations
meas_name = {
        'batch_name': '',
        'sample_num': '',
        'cell_num': '',
        'spectra_name': '',
        'temp_num': 0,
    }
legend_list = []
spectra_list = []
temp_list = []
PCE_list = []
Voc_list = []
Jsc_list = []
FF_list = []
numbers = re.compile(r'(\d+)')


def main():
    directory = 'C:/Users/khoaw/OneDrive/Personal Documents/UT - REU/Data/New Pico JV Data/07242024'  # TO CHANGE
    if not os.path.exists(directory + '/Plots'):
        os.makedirs(directory + '/Plots')

    plot_ind_JV(directory)
    print("Individuals plotted")
    plot_stack_JV_spectra(directory)
    print("Temp-stacked per spectra plotted")
    plot_stack_JV_temp(directory)
    print("Spectra-stacked per temp plotted")


# Sets sample name and measurement conditions (MAY HAVE TO CHANGE)
def get_names(file_name, flag):
    sample_IDs = file_name[0].split('_')
    meas_name['temp_num'] = int(sample_IDs[4][:len(sample_IDs[4])-1]) if flag \
        else int(file_name[1][:len(file_name[1])-5])
    meas_name['batch_name'] = sample_IDs[1]
    meas_name['sample_num'] = sample_IDs[2]
    meas_name['cell_num'] = sample_IDs[3]
    meas_name['spectra_name'] = file_name[1][:len(file_name[1])-4] if flag else sample_IDs[4]


def plot_ind_JV(directory):
    clear_vars()
    for files in os.listdir(directory):
        if files.endswith('Summary.txt') or files == 'Plots':
            continue

        # Get names from file name
        file_name = files.split('-')
        get_names(file_name, False)

        # Get voltage and current density readings from file
        volt_list, curr_dens_list = unpack_file(directory, files)

        # Get useful parameters
        Jmin, Jmax, Jsc, Voc, FF, PCE = run_calculations(volt_list, curr_dens_list)

        # Plot the data
        plt.plot(volt_list, curr_dens_list, color='b', linestyle='-', marker='.')

        # Add labels to the plot
        plt.title('JV of {} Sample {} Cell {} at {} at {}C'.format(meas_name['batch_name'], meas_name['sample_num'],
                                                                   meas_name['cell_num'], meas_name['spectra_name'],
                                                                   meas_name['temp_num']))
        plt.xlabel('Voltage, V [V]')
        plt.ylabel('Current Density, J [mA/cm{}]'.format(get_super('2')))

        # Add text to the plot
        space = np.linspace((Jmin + Jmax) / 2, Jmin, num=4)
        plt.text(0, space[0], 'PCE = {:.2f} %'.format(PCE * 100), fontsize=10)
        plt.text(0, space[1], 'FF = {:.2f} %'.format(FF * 100), fontsize=10)
        plt.text(0, space[2], 'Jsc = {:.2f} mA/cm{}'.format(Jsc, get_super('2')), fontsize=10)
        plt.text(0, space[3], 'Voc = {:.2f} V'.format(Voc), fontsize=10)

        # Save the plot
        plt.savefig(directory+'/Plots/'+files[:len(files) - 4]+'.png', bbox_inches='tight')

        # Clear the plot
        plt.clf()


def plot_stack_JV_spectra(directory):
    # Store list of different plot styles
    color = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y', 'k'))
    line_style = itertools.cycle(('-', ':', '--', '-.'))

    # Initialize variables
    last_file = ''
    clear_vars()

    for i, files in enumerate(sorted(os.listdir(directory), key=numericalSort)):
        if files.endswith('Summary.txt') or files == 'Plots':
            continue

        # If new sample, plot parameters vs temperature and clear program variables
        file_name = files.split('-')
        if i != 1 and file_name[0] != last_file:
            plot_param_vs_ind(temp_list, [], directory, last_file, 'spectra', True)
            plot_param_vs_ind(temp_list, [], directory, last_file, 'spectra', False)

            clear_vars()

        # Get voltage and current density readings from file
        volt_list, curr_dens_list = unpack_file(directory, files)

        # Get useful parameters
        Jmin, Jmax, Jsc, Voc, FF, PCE = run_calculations(volt_list, curr_dens_list)

        # Get measurement names from file name
        get_names(file_name, False)

        # Add parameters to lists
        temp_list.append(meas_name['temp_num'])
        PCE_list.append(PCE)
        Voc_list.append(Voc)
        Jsc_list.append(Jsc)
        FF_list.append(FF)

        # Plot the data
        plt.plot(volt_list, curr_dens_list, color=next(color), linestyle=next(line_style))

        # Add labels to the plot
        plt.title('JV of {} Sample {} Cell {} at {}'.format(meas_name['batch_name'], meas_name['sample_num'],
                                                            meas_name['cell_num'], meas_name['spectra_name']))
        plt.xlabel('Voltage, V [V]')
        plt.ylabel('Current Density, J [mA/cm{}]'.format(get_super('2')))
        plt.ylim(bottom=0)

        # Add temperature to legend
        legend_list.append(str(meas_name['temp_num']) + 'C')
        plt.legend(legend_list, loc='lower left')

        # Save the plot
        plt.savefig(directory + '/Plots/' + files[:len(files) - 8] + '.png', bbox_inches='tight')

        # Remember last file name
        last_file = file_name[0]

        # Swap spectra and temperature in file name
        new_file = "SS_{}_{}_{}_{}C-{}.txt".format(meas_name['batch_name'], meas_name['sample_num'],
                                                   meas_name['cell_num'], str(int(meas_name['temp_num'])),
                                                   meas_name['spectra_name'])
        os.rename(os.path.join(directory, files), os.path.join(directory, new_file))

    # Plot last sample
    plot_param_vs_ind(temp_list, [], directory, last_file, 'spectra', True)
    plot_param_vs_ind(temp_list, [], directory, last_file, 'spectra', False)

    plt.clf()


def plot_stack_JV_temp(directory):
    # Store list of different plot styles
    color = itertools.cycle(('b', 'g', 'r', 'c', 'm', 'y', 'k'))
    line_style = itertools.cycle(('-', ':', '--', '-.'))

    # Initialize variables
    last_file = ''
    clear_vars()

    for i, files in enumerate(sorted(os.listdir(directory), key=numericalSort)):
        if files.endswith('Summary.txt') or files == 'Plots':
            continue

        # If new sample, plot parameters vs spectra and clear lists
        file_name = files.split('-')
        if i != 1 and file_name[0] != last_file:
            x_list = np.arange(len(spectra_list))
            plot_param_vs_ind(x_list, spectra_list, directory, last_file, 'temp', True)
            plot_param_vs_ind(x_list, spectra_list, directory, last_file, 'temp', False)

            clear_vars()

        # Get voltage and current density readings from file
        volt_list, curr_dens_list = unpack_file(directory, files)

        # Get useful parameters
        Jmin, Jmax, Jsc, Voc, FF, PCE = run_calculations(volt_list, curr_dens_list)

        # Get measurement names from file name
        get_names(file_name, True)

        # Add parameters to lists
        spectra_list.append(meas_name['spectra_name'])
        PCE_list.append(PCE)
        Voc_list.append(Voc)
        Jsc_list.append(Jsc)
        FF_list.append(FF)

        # Plot the data
        plt.plot(volt_list, curr_dens_list, color=next(color), linestyle=next(line_style))

        # Add labels to the plot
        plt.title('JV of {} Sample {} Cell {} at {}C'.format(meas_name['batch_name'], meas_name['sample_num'],
                                                             meas_name['cell_num'], meas_name['temp_num']))
        plt.xlabel('Voltage, V [V]')
        plt.ylabel('Current Density, J [mA/cm{}]'.format(get_super('2')))
        plt.ylim(bottom=0)

        # Add spectra to legend
        legend_list.append(meas_name['spectra_name'])
        plt.legend(legend_list, loc='upper right')

        # Save the plot
        plt.savefig(directory + '/Plots/' + files[:len(files) - len(meas_name['spectra_name']) - 5] + '.png',
                    bbox_inches='tight')

        # Remember last file name
        last_file = file_name[0]

        # Swap temperature and spectra in file name
        new_file = "SS_{}_{}_{}_{}-{}C.txt".format(meas_name['batch_name'], meas_name['sample_num'],
                                                   meas_name['cell_num'], meas_name['spectra_name'],
                                                   str(int(meas_name['temp_num'])))
        os.rename(os.path.join(directory, files), os.path.join(directory, new_file))

    # Plot parameters vs spectra for last sample
    x_list = np.arange(len(spectra_list))
    plot_param_vs_ind(x_list, spectra_list, directory, last_file, 'temp', True)
    plot_param_vs_ind(x_list, spectra_list, directory, last_file, 'temp', False)

    plt.clf()


def plot_param_vs_ind(x_list, x_axe_labs, directory, last_file, plt_type, flag):
    plt.clf()
    fig, ax = plt.subplots(figsize=(12, 4.8) if plt_type == 'temp' else (6.4, 4.8))
    fig.subplots_adjust(right=0.75)

    # Create new y-axes
    twin1 = ax.twinx()
    twin2 = ax.twinx()
    twin3 = ax.twinx()

    # Move extra y-axis spines to the right
    twin2.spines.right.set_position(("axes", 1.2 if plt_type == 'spectra' else 1.1))
    twin3.spines.right.set_position(("axes", 1.4 if plt_type == 'spectra' else 1.2))

    # Plot points with temperature coefficients in the label
    p1, = ax.plot(x_list, PCE_list, label="PCE ({:.4f} %/C)".format(np.polyfit(x_list, PCE_list, 1)[0]),
                  marker='.', linestyle='' if flag else '-', color='r')
    p2, = twin1.plot(x_list, Voc_list, label="Voc ({:.4f} V/C)".format(np.polyfit(x_list, Voc_list, 1)[0]),
                     marker='.', linestyle='' if flag else '-', color='b')
    p3, = twin2.plot(x_list, Jsc_list, label="Jsc ({:.4f} mA/cm{}/C)".format(np.polyfit(x_list, Jsc_list, 1)[0],
                                                                             get_super('2')),
                     marker='.', linestyle='' if flag else '-', color='y')
    p4, = twin3.plot(x_list, FF_list, label="FF ({:.4f} %/C)".format(np.polyfit(x_list, FF_list, 1)[0]),
                     marker='.', linestyle='' if flag else '-', color='c')

    # Plot lines of best fit
    if flag:
        ax.plot(np.unique(x_list), np.poly1d(np.polyfit(x_list, PCE_list, 1))(np.unique(x_list)), color='r')
        twin1.plot(np.unique(x_list), np.poly1d(np.polyfit(x_list, Voc_list, 1))(np.unique(x_list)), color='b')
        twin2.plot(np.unique(x_list), np.poly1d(np.polyfit(x_list, Jsc_list, 1))(np.unique(x_list)), color='y')
        twin3.plot(np.unique(x_list), np.poly1d(np.polyfit(x_list, FF_list, 1))(np.unique(x_list)), color='c')

    # Add titles to axes
    ax.set(xlabel='Spectra' if plt_type == 'temp' else 'Temperature [C]', ylabel="PCE [%]")
    twin1.set(ylabel="Voc [V]")
    twin2.set(ylabel="Jsc [mA/cm{}]".format(get_super('2')))
    twin3.set(ylabel="FF [%]")

    # Set color of axis titles
    ax.yaxis.label.set_color(p1.get_color())
    twin1.yaxis.label.set_color(p2.get_color())
    twin2.yaxis.label.set_color(p3.get_color())
    twin3.yaxis.label.set_color(p4.get_color())

    # Set color of axis labels
    ax.tick_params(axis='y', colors=p1.get_color())
    twin1.tick_params(axis='y', colors=p2.get_color())
    twin2.tick_params(axis='y', colors=p3.get_color())
    twin3.tick_params(axis='y', colors=p4.get_color())

    # Add labels to the title and axes
    if plt_type == 'spectra':
        plt.title('PCE, Voc, Jsc, and FF of {} Sample {} Cell {} at {} at Varying Temperature'.format(
            meas_name['batch_name'], meas_name['sample_num'], meas_name['cell_num'], meas_name['spectra_name']))
    else:
        plt.title('PCE, Voc, Jsc, and FF of {} Sample {} Cell {} at {}C at Varying Spectra'.format(
            meas_name['batch_name'], meas_name['sample_num'], meas_name['cell_num'], meas_name['temp_num']))
        plt.xticks(x_list, x_axe_labs)

    # Add legend to graph of plot labels
    twin3.legend(handles=[p1, p2, p3, p4], loc='lower left')

    # Save the figure
    plt.savefig(directory+'/Plots/'+last_file+'_trends_{}.png'.format('best' if flag else 'conn'), bbox_inches='tight')

    # Close the figure
    plt.close(fig)


def clear_vars():
    plt.clf()
    legend_list.clear()
    temp_list.clear()
    spectra_list.clear()
    PCE_list.clear()
    Voc_list.clear()
    Jsc_list.clear()
    FF_list.clear()


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def unpack_file(directory, files):
    # Find number of columns
    with open(os.path.join(directory, files)) as f:
        f.readline()
        ncols = len(f.readline().split('\t'))

    # Unpack PV Measurement Inc. file data
    arr = np.loadtxt(os.path.join(directory, files), delimiter='\t', skiprows=1, unpack=True,
                     usecols=range(1, ncols), max_rows=2)
    volt_list = [i[0] for i in arr]
    curr_dens_list = [i[1] for i in arr]

    return volt_list, curr_dens_list


def run_calculations(volts, curr_dens):
    # Variable Initializations
    Jsc1 = [-999, 0]
    Jsc2 = [999, 1]
    Voc1 = [0, 999]
    Voc2 = [1, -999]
    Pmp = -999
    Jmin = 999
    Jmax = -999

    # Find specific parameters
    for volt, curr in zip(volts, curr_dens):
        if 0 > volt > Jsc1[0]:
            Jsc1 = volt, curr
        if Jsc2[0] > volt > 0:
            Jsc2 = volt, curr
        if Voc1[1] > curr > 0:
            Voc1 = volt, curr
        if 0 > curr > Voc2[1]:
            Voc2 = volt, curr
        if (volt * curr) > Pmp:
            Pmp = volt * curr
        if curr < Jmin:
            Jmin = curr
        if curr > Jmax:
            Jmax = curr

    # Calculate Jsc
    m_i = (Jsc2[1] - Jsc1[1]) / (Jsc2[0] - Jsc1[0])
    Jsc = Jsc1[1] - m_i * Jsc1[0]

    # Calculate Voc
    m = (Voc2[1] - Voc1[1]) / (Voc2[0] - Voc1[0])
    Voc = (m * Voc1[0] - Voc1[1]) / m

    # Calculate FF
    FF = (Pmp * 0.075) / (Voc * Jsc * 0.075)

    # Calculate PCE
    PCE = (Voc * (Jsc * 0.075) / 1000 * FF) / 0.0075

    return Jmin, Jmax, Jsc, Voc, FF, PCE


def get_super(x):
    normal = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+-=()"
    super_s = "ᴬᴮᶜᴰᴱᶠᴳᴴᴵᴶᴷᴸᴹᴺᴼᴾQᴿˢᵀᵁⱽᵂˣʸᶻᵃᵇᶜᵈᵉᶠᵍʰᶦʲᵏˡᵐⁿᵒᵖ۹ʳˢᵗᵘᵛʷˣʸᶻ⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"
    res = x.maketrans(''.join(normal), ''.join(super_s))
    return x.translate(res)


if __name__ == "__main__":
    main()

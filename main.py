import xlrd
import matplotlib.pyplot as plot
import lmfit

# the population being modeled
population = 329500000
# the number of days a person is infectious
infectious_period = 14

# filepath - the filepath of the .xls file
filepath = "daily_case_data.xls"
# sheetnum - which sheet of the .xls file the data is on
sheetnum = 0
# column - which column contains the data
column = 2
# max_row - the largest row with the data in it
max_row = 634
# min_row - the smallest row with the data in it
min_row = 4
# step - the number of rows between each data point plus one.
# ex: if the desired data was on every other row step would be -2
step = -1

# gets the new daily cases from a single column of a .xls file and transfers them to the list daily_cases[]
# returns the daily-cases[] list, a list of the data gathered with the earliest date at index 0
def get_real_data_xls():
    book = xlrd.open_workbook_xls(filepath)
    sheet = book.sheet_by_index(sheetnum)

    daily_cases = []
    for row in range(max_row-1, min_row, -1):
        daily_cases.append(int(sheet.cell_value(row, column)))
    return daily_cases


# uses a list of new daily cases to create a list for the daily S, I, and R
# daily cases - a list of new daily cases
# returns S - a list of individuals susceptible per day
# returns I - a list of individuals infected per day
# returns R - a list of individuals that are immune per day
def create_real_SIR(daily_cases=get_real_data_xls()):

    S = [population-daily_cases[0]]
    I = [daily_cases[0]]
    R = [0]

    for day in range(1, len(daily_cases)):
        # the number of people that have recovered on day day
        new_recovered = 0
        # the number of new people infected today
        new_cases = daily_cases[day]

        if day > infectious_period:
            new_recovered = daily_cases[day - infectious_period]

        S.append(S[-1] - new_cases)
        I.append(I[-1] + new_cases - new_recovered)
        R.append(R[-1] + new_recovered)
    return S, I, R


# graphs SIR data
def graph_SIR(S, I, R):
    x = range(len(S))
    plot.plot(x, S, label="S")
    plot.plot(x, I, label="I")
    plot.plot(x, R, label="R")

    plot.xlabel("day")
    plot.ylabel("people")
    plot.legend()
    plot.show()


# graphs the percentage of the population infected
def graph_percent_I(I):
    x = range(len(I))
    y = []

    for value in I:
        y.append((value/population)*100)

    plot.xlabel("day")
    plot.ylabel("%I")
    plot.plot(x, y)
    plot.show()


# helper function to plot the data of an SIR model
def generate_graphs(sir=create_real_SIR()):
    S, I, R = sir
    graph_SIR(S, I, R)
    graph_percent_I(I)


# uses lmfit to find the best fit SIR model by finding the constants that minimize the square of the differance
# between the infection rate of the real data and the model
def minimize_square_diff():

    params = lmfit.Parameters()
    params.add("b", value=0.000000005, min=0, max=1)
    params.add("k", value=0.5, min=0, max=1)

    minner = lmfit.Minimizer(generate_constants, params)
    result = minner.minimize()
    lmfit.report_fit(result)


# generates the lists that minimize_square_diff tries to minimize
def generate_constants(params):
    Sr, Ir, Rr = create_real_SIR(get_real_data_xls())
    b = params["b"]
    rt = params["k"]

    Sm, Im, Rm = create_model_SIR(b, rt, len(Ir))

    dif = []
    for day in range(len(Ir)):
        dif.append(Ir[day]-Im[day])

    return dif


# Creates a hypothetical SIR model
# b and rt are constants for an SIR model
# sim length is the number of days you want to run the simulation for
# returns S - a list of individuals susceptible per day
# returns I - a list of individuals infected per day
# returns R - a list of individuals that are immune per day
def create_model_SIR(b, k, sim_length):

    # the number of people that are infected on day 0
    initial_infected = 534962

    I = [initial_infected]
    S = [population-I[0]]
    R = [0]

    for day in range(1, sim_length):
        S.append(S[-1] - b * (S[-1] * I[-1]))
        I.append(I[-1] + b * S[-2] * I[-1] - k * I[-1])
        R.append(R[-1] + k * I[-2])

    return S, I, R


# creates a graph with two SIR models on it
def graph_SIR_together(S1, I1, R1, S2, I2, R2):
    x = range(len(S1))
    plot.plot(x, S1, label="S real")
    plot.plot(x, I1, label="I real")
    plot.plot(x, R1, label="R real")

    x = range(len(S2))
    plot.plot(x, S2, label="S model")
    plot.plot(x, I2, label="I model")
    plot.plot(x, R2, label="R model")

    plot.ylabel("people")
    plot.xlabel("day")
    plot.legend()
    plot.show()


# creates a graph of the %I of two different models
def graph_percent_I_together(I1, I2):

    # plot the real %I
    x = range(len(I1))
    y = []
    for value in I1:
        y.append((value/population)*100)
    plot.plot(x, y, label="%I real")

    # Graph the calculated %I
    x = range(len(I2))
    y = []
    for value in I2:
        y.append((value/population)*100)
    plot.plot(x, y, label="%I model")

    plot.xlabel("day")
    plot.ylabel("%I")
    plot.legend()
    plot.show()


# helper function to graph 2 models together
def graph_together(sir1, sir2):
    S1, I1, R1 = sir1
    S2, I2, R2 = sir2
    graph_SIR_together(S1, I1, R1, S2, I2, R2)
    graph_percent_I_together(I1, I2)


generate_graphs(create_real_SIR(get_real_data_xls()))

max_row = 424
min_row = 134
# minimize_square_diff()
graph_together(create_real_SIR(get_real_data_xls()), create_model_SIR(b=0.00000000068574, k=0.19980995, sim_length=300))

# max_row = 375
# graph_together(create_real_SIR(get_real_data_xls()), create_model_SIR(b=0.0000000010923, rt=0.31305816, sim_length=175))

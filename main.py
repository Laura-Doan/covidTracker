import xlrd
import matplotlib.pyplot as graph


# gets the new daily cases from a single column of a .xls file and transfers them to the list daily_cases[]
# filepath - the filepath of the .xls file
# sheetnum - which sheet of the .xls file the data is on
# column - which column contains the data
# max_row - the largest row with the data in it
# min_row - the smallest row with the data in it
# step - the number of rows between each data point plus one. if the oldest value is at the bottom of the sheet this value will be negative
    # ex: if the desired data was on every other row step would be (-)2
# returns the daily-cases[] list, a list of the data gathered with the earliest date at index 0
def get_real_data_xls(filepath="daily_case_data.xls", sheetnum=0, column=2, max_row=659, min_row=2, step=-1):
    book = xlrd.open_workbook_xls(filepath)
    sheet = book.sheet_by_index(sheetnum)

    daily_cases = []
    for row in range(max_row-1, min_row, step):
        daily_cases.append(int(sheet.cell_value(row, column)))
    return daily_cases


# uses a list of new daily cases to create a list for the daily S, I, and R
# daily cases - a list of new daily cases
# population - the population the daily_cases data is taken from
# returns S - a list of individuals susceptible per day
# returns I - a list of individuals infected per day
# returns R - a list of individuals that are immune per day
def create_real_SIR(daily_cases=get_real_data_xls(), population=329500000):
    # the number of days a person is considered infectious
    infectious_period = 14

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
    graph.plot(x, S, label="S")
    graph.plot(x, I, label="I")
    graph.plot(x, R, label="R")

    graph.legend()
    graph.show()


# graphs the percentage of the population infected
def graph_percent_I(I, population=329500000):
    x = range(len(I))
    y = []

    for value in I:
        y.append((value/population)*100)

    graph.plot(x, y)
    graph.show()


# helper function to graph the data
# Gets data from create real SIR() and sends it to the graph_SIR function
def generate_graphs(sir = create_real_SIR()):
    S, I, R = sir
    graph_SIR(S, I, R)

    graph_percent_I(I)


# Creates a hypothetical SIR model
# returns S - a list of individuals susceptible per day
# returns I - a list of individuals infected per day
# returns R - a list of individuals that are immune per day
def create_hypothetical_SIR(population=329500000):
    # the number of days you want to run the simulation for
    sim_length = 700

    # the number of people that are infected on day 0
    initial_infected = 10

    I = [initial_infected/population]
    S = [1]
    R = [0]

    b = 1/2
    k = 1/14
    for day in range(1, sim_length):
        S.append(S[-1]-b*(S[-1]*I[-1]))
        I.append(I[-1] + b*S[-2]*I[-1]-k*I[-1])
        R.append(R[-1] + k*I[-2])

    for day in range(sim_length):
        S[day] = S[day]*population
        I[day] = I[day]*population
        R[day] = R[day]*population

    return S, I, R


generate_graphs(create_hypothetical_SIR())
generate_graphs()

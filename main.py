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
    # the number of days a person is considered immune after recovery, set equal to len(daily_cases) for indefinite period
    immune_period = 180

    S = [population-daily_cases[0]]
    I = [daily_cases[0]]
    R = [0]

    for day in range(1, len(daily_cases)):
        # the number of people that have recovered on day day
        recovered_today = 0
        # the number of people that have become infectious again on day day
        susceptible_today = 0

        if day > infectious_period:
            recovered_today = daily_cases[day-infectious_period]
        if day > immune_period + infectious_period:
            susceptible_today = daily_cases[day - (infectious_period + immune_period)]

        S.append(S[-1] + susceptible_today - daily_cases[day])
        I.append(I[-1] + daily_cases[0] - recovered_today)
        R.append(R[-1] + recovered_today - susceptible_today)
    return S, I, R


# graphs SIR data
def graph_SIR(S, I, R):
    y = range(len(S))
    graph.plot(y, S)
    graph.show()


# helper function to graph the real-world data
# Gets data from create real SIR() and sends it to the graph_SIR function
def real_world_graph(sir = create_real_SIR()):
    S, I, R = sir
    graph_SIR(S, I, R)


real_world_graph()

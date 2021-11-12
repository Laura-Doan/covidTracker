import xlrd
import matplotlib


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

get_real_data_xls()
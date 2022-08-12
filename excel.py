import xlrd
import sql


def set_rows_excel_into_sql(database_name, excel_file_location, sheetname, excel_start_row, sql_table):
    # open excel sheet
    wb = xlrd.open_workbook(excel_file_location)
    sheet = wb.sheet_by_name(sheetname)
    # create rows based on the amount of rows used in excel
    for r in range(excel_start_row, sheet.nrows):
        query = "INSERT INTO %s (id) VALUES ('%s')" % (
            sql_table, r - (excel_start_row-1))
        sql.execute_query(database_name, query)

    print(f'created {r} rows.')


def update_excel_sql(database_name, excel_file_location, sheetname, excel_start_row, excel_column, sql_column_name, sql_table):
    # open excel sheet
    wb = xlrd.open_workbook(excel_file_location)
    sheet = wb.sheet_by_name(sheetname)
    for r in range(excel_start_row, sheet.nrows):
        q = sheet.cell(r, excel_column)
        if q.ctype == 0:  # * https://pythonhosted.org/xlrd3/cell.html for looking up cell type number values
            excel_last_row = r
            break
        if q.ctype == 0:
            break
        else:
            excel_last_row = sheet.nrows
    # insert every excel value into table
    for r in range(excel_start_row, excel_last_row):
        excel_data = sheet.cell(r, excel_column).value
        query = "UPDATE %s SET %s = '%s' WHERE id = %s" % (
            sql_table, sql_column_name, excel_data, r - (excel_start_row-1))
        sql.execute_query(database_name, query)
    print(f'Updated {r} rows.')

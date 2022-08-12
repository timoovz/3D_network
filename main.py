import excel
import setup as sp
import functions as hp

# fourth version for implementing sqlite


def main():
    hp.create_table(sp.database_name, sp.sql_table, sp.column_names)
    hp.truncate_table(sp.database_name, sp.sql_table)

    excel.set_rows_excel_into_sql(sp.database_name,
                                  sp.excel_file_location, sp.sheetname, 2, sp.sql_table)
    excel.update_excel_sql(sp.database_name, sp.excel_file_location, sp.sheetname,
                           2, 1, sp.column_names["nodenames"], sp.sql_table)
    excel.update_excel_sql(sp.database_name, sp.excel_file_location, sp.sheetname,
                           2, 4, sp.column_names["group_names"], sp.sql_table)
    excel.update_excel_sql(sp.database_name, sp.excel_file_location, sp.sheetname,
                           2, 7, sp.column_names["edges_sources_names"], sp.sql_table)
    excel.update_excel_sql(sp.database_name, sp.excel_file_location, sp.sheetname,
                           2, 10, sp.column_names["edges_targets_names"], sp.sql_table)

    hp.create_numeric_node_group(sp.database_name,
                                 sp.sql_table, sp.column_names["groups_numerics"], sp.column_names["group_names"])

    hp.create_edges(sp.database_name, sp.sql_table, sp.column_names["edges_sources_names"], sp.column_names["edges_targets_names"],
                    sp.column_names["nodenames"], sp.column_names["edges_sources_numerics"], sp.column_names["edges_targets_numerics"])

    hp.create_3d_network_graph(sp.database_name, sp.sql_table, sp.column_names["nodenames"], sp.column_names["groups_numerics"], sp.column_names["edges_sources_numerics"],
                               sp.column_names["edges_targets_numerics"], sp.color["textcolor"], sp.color["linecolor"], sp.color["backgroundcolor"])


if __name__ == '__main__':
    main()

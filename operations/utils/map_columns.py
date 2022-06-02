def map_columns(df, column_maps):
    """
        Maps the column names between extract source and load target.
        Renames data table column names.
        Parameters:
            df: pandas.DataFrame.
            column_maps: ColumnMap object list.
    """
    rename_col_dict = {}
    mapped_load_column_names = []
    
    for obj in column_maps:
        e_col = obj.extract_column
        l_col = obj.load_column
        rename_col_dict[e_col.column_name] = l_col.column_name
        mapped_load_column_names.append(l_col.column_name)

    if len(rename_col_dict) > 0:
        df.rename(columns=rename_col_dict, inplace=True)

    return df

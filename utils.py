import pandas as pd
import json

def process_file(filepath, id_column, date_of_birth_column, columns_to_check_for_total, columns_for_rule_fixing, columns_to_copy_from_last_total, priority_vals):
    df = pd.read_excel(filepath)

    df[date_of_birth_column] = df[date_of_birth_column].dt.strftime("%d/%m/%Y")
    df[id_column].ffill(inplace=True)

    # convert all columns which are not ints to string (SHOULD CHECK FOR FLOAT AS WELL)
    df = df.astype({column : "string" for column, dtype in zip(df.columns, df.dtypes) if not 'int' in str(dtype)})

    df[columns_to_check_for_total] = df[columns_to_check_for_total].fillna('')
    
    counts = df.groupby(id_column).size() # get the frequencies of each client ID

    # we are only concerned about the duplicates i.e. users that have multiple entries
    duplicates = counts[counts > 1]

    for curr_client_id in duplicates.index.to_list():
        curr_client_df = df[df[id_column] == curr_client_id]

        totals_rows = pd.DataFrame()
        for column in columns_to_check_for_total:
            curr_totals_rows = curr_client_df[curr_client_df[column].str.contains("Total")]

            # ARE THEY SORTED AS THEY SHOULD BE HERE OR WE'RE NOT GETTING THE CORRECT LAST TOTALS ROW??

            # This is to fix: FutureWarning: The behavior of DataFrame concatenation with empty or all-NA entries is deprecated.
            # In a future version, this will no longer exclude empty or all-NA columns when determining the result dtypes.
            # To retain the old behavior, exclude the relevant entries before the concat operation.
            if curr_totals_rows.empty:
                continue
            elif totals_rows.empty:
                totals_rows = curr_totals_rows
            else:
                totals_rows = pd.concat([totals_rows, curr_totals_rows])

        non_total_rows = curr_client_df.loc[list(set(curr_client_df.index) - set(totals_rows.index))]

        for column in columns_for_rule_fixing:
            values = non_total_rows[column].to_list()

            final_val = None

            for comp in priority_vals:
                containing_values = list(filter(lambda val: comp in val, values))
                if len(containing_values) > 0:
                    final_val = containing_values[0]
                    break

            if final_val is not None:
                df.loc[curr_client_df.index[0], column] = final_val
            else:
                df.loc[curr_client_df.index[0], column] = ''

        index_of_last_totals_row = max(list(totals_rows.index))

        df.loc[curr_client_df.index[0], columns_to_copy_from_last_total] = df.loc[index_of_last_totals_row, columns_to_copy_from_last_total]

        df.drop(curr_client_df.index[1:], inplace=True)

    return df

def read_defaults():
    deserialised = None
    
    try:
        with open("defaults.json", "r") as f:
            deserialised = json.load(f)
    except:
        return [None, None, [], [], [], []]

    return list(deserialised.values())
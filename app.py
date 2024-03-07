import streamlit as st
import pandas as pd

def load_data(file):
    # Load the Excel file attempting to use the first row as headers
    df = pd.read_excel(file, engine='openpyxl')
    return df

def sum_values(df, row_name, column_name_or_index):
    # Check if DataFrame has column headers
    if isinstance(column_name_or_index, int):
        # DataFrame without named columns, using index to locate the row
        row = df[df.iloc[:, column_name_or_index] == row_name]
    else:
        # DataFrame with named columns
        row = df[df[column_name_or_index] == row_name]

    # Determine the starting column index for summing
    start_col_index = df.columns.get_loc(column_name_or_index) + 1 if isinstance(column_name_or_index, str) else column_name_or_index + 1

    # Sum values to the right of the row name
    sum_val = row.iloc[:, start_col_index:].sum(axis=1)
    return sum_val.values[0] if not sum_val.empty else "No data found"

st.title('Sum Values to the Right of a Row Name')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = load_data(uploaded_file)
    if not df.empty:
        # Dynamically adjust based on whether the DataFrame has named columns
        if 'I' in df.columns:
            column_name_or_index = 'I'
            row_names = df['I'].unique()
        else:
            # Assuming column 'I' corresponds to the 9th column (index 8)
            column_name_or_index = 8
            row_names = df.iloc[:, 8].unique()

        selected_row_name = st.selectbox('Select Row Name', row_names)
        if st.button('Sum Values'):
            result = sum_values(df, selected_row_name, column_name_or_index)
            st.write(f'Sum of values to the right of {selected_row_name}: {result}')

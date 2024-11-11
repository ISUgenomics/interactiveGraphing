import io
import os
import base64
import json
import pandas as pd
from dash import dcc, no_update
from sigloo.apps.src.params.defaults import default_headers

# Generic functions

# Function to check if the first row is likely a header
def is_first_row_header(df):
    return df.iloc[0].apply(lambda x: isinstance(x, str)).all()     # if the first row contains non-numeric values

# Create a dataframe from user-uploaded file of a specific format 
def decode_base64(filename, string):
    try:
        decoded = base64.b64decode(string)
        format = os.path.splitext(filename)[1].upper()

        if filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), header=None)
        elif filename.endswith(('.tsv', '.paf')):
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')), sep='\t', header=None)
        elif filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(io.BytesIO(decoded), header=None)
        elif filename.endswith('.json'):
            decoded = base64.b64decode(string.encode('ascii')).decode('ascii')
            df = pd.read_json(decoded, orient='index')

        # Check if the first row is a header
        if is_first_row_header(df):
            df.columns = df.iloc[0]                             # use the first row as header
            df = df[1:].reset_index(drop=True)                  # remove the header row from data
        else:
            num_columns = len(df.columns)
            if not format or format not in default_headers:     # generate generic header
                header = [f'column_{i+1}' for i in range(len(df.columns))]
            else:                                               # apply default headers if format is known
                header = default_headers[format]
                if num_columns > len(header):
                    extra_headers = [f'extra_col_{i}' for i in range(len(header) + 1, num_columns + 1)]
                    header = header + extra_headers
            df.columns = header
        
        df[df.select_dtypes(include=['number']).columns] = df.select_dtypes(include=['number']).apply(pd.to_numeric)

        return df
    except Exception as e:
        print(f"File {filename} can NOT be decoded! \nError: {e}")
        return None


# [PART 1/2 Dataframe save/download] Manage different file formats
def get_format_functions(df, to_format, filename):
    format_functions = {
        'csv': {'method': df.to_csv, 'is_binary': False, 'filename': f"{filename}.csv", 'download_params': {'index': False}},
        'excel': {'method': df.to_excel, 'is_binary': True, 'filename': f"{filename}.xlsx", 'download_params': {'sheet_name': f"{filename}", 'index': False}},
        'txt': {'method': df.to_csv, 'is_binary': False, 'filename': f"{filename}.txt", 'download_params': {'sep': '\t', 'index': False}},
        'json': {'method': df.to_json, 'is_binary': False, 'filename': f"{filename}.json", 'download_params': {'index': True}},
        'markdown': {'method': df.to_markdown, 'is_binary': False, 'filename': f"{filename}.md", 'download_params': {'index': False}},
        'html': {'method': df.to_html, 'is_binary': False, 'filename': f"{filename}.html", 'download_params': {'index': False}},
        'pickle': {'method': df.to_pickle, 'is_binary': True,  'filename': f"{filename}.pkl", 'download_params': {}},
        'feather': {'method': lambda f, **kwargs: df.reset_index().to_feather(f, **kwargs), 'is_binary': True, 'filename': f"{filename}.feather", 'download_params': {}},
        'stata': {'method': df.to_stata, 'is_binary': True, 'filename': f"{filename}.dta", 'download_params': {}},
    }
    return format_functions.get(to_format)


# [PART 2/2 Dataframe save/download] Save dataframe to the selected path or download from a buffer
def export_df(df, to_format, filename, storage=None, custom=None, download=False):
    if storage or custom or download:
        format_info = get_format_functions(df, to_format, filename)
        export_method = format_info['method']
        is_binary = format_info['is_binary']
        outfile = format_info['filename']
        params = format_info['download_params']
        # Handle dataframe save with 'storage' and 'custom' options
        for path in [storage, custom]:
            if path:
                mode = 'wb' if is_binary else 'w'
                try:
                    os.makedirs(path, exist_ok=True)
                    file_path = os.path.join(path, outfile)
                    if is_binary:
                        with open(file_path, mode) as f:
                            export_method(f, **params)
                    else:
                        with open(file_path, mode, newline='', encoding='utf-8') as f:
                            export_method(f, **params)
                    print("File(s) successfully saved!")
                except Exception as e:
                    print(f"Error writing file {file_path}: {e}")
        # Handle dataframe 'download' option
        if download:
            if to_format == 'feather':
                buffer = io.BytesIO()
                export_method(buffer)
                buffer.seek(0)
                return dcc.send_bytes(buffer.getvalue(), outfile)
            elif to_format in ['markdown']:
                content_string = export_method(**params)
                return dict(content=content_string, filename=outfile)
            else:
                return dcc.send_data_frame(export_method, outfile, **params)            
    else:
        return no_update                                                            ######## Validate it !!!
    

# Helper function to format numbers with k, M, B
def format_length(length):
    if length >= 1_000_000_000:
        return f"{length / 1_000_000_000:.2f}B"
    elif length >= 1_000_000:
        return f"{length / 1_000_000:.2f}M"
    elif length >= 1_000:
        return f"{length / 1_000:.2f}k"
    else:
        return str(length)
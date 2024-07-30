import pandas as pd
import os
import argparse

def process_paf_file(file_path, separator, quality_cutoff, min_block_length=None, min_matching_bases=None, check_strand=False):
    # Extract query and target names from the file name
    base_name = os.path.basename(file_path)
    query, target = base_name.split('.')[0].split('_')
    
    # Load the PAF file with the specified separator
    paf = pd.read_csv(file_path, sep=separator, header=None)
    
    # Define PAF columns based on minimap2 output structure
    paf_columns = [
        'query_name', 'query_length', 'query_start', 'query_end', 'target_strand',
        'target_name', 'target_length', 'target_start', 'target_end',
        'num_matching', 'alignment_block_length', 'mapping_quality'
    ]
    paf.columns = paf_columns + list(paf.columns[len(paf_columns):])
    
    # Filter for high-quality alignments
    high_quality_alignments = paf[paf['mapping_quality'] > quality_cutoff].copy()
    
    # Optional: Filter based on alignment block length
    if min_block_length is not None:
        high_quality_alignments = high_quality_alignments[high_quality_alignments['alignment_block_length'] > min_block_length].copy()
    
    # Optional: Filter based on number of matching bases
    if min_matching_bases is not None:
        high_quality_alignments = high_quality_alignments[high_quality_alignments['num_matching'] > min_matching_bases].copy()
    
    # Optional: Check for same strand orientation
    if check_strand:
        high_quality_alignments = high_quality_alignments[high_quality_alignments['target_strand'] == '+'].copy()
    
    # Tag the data with query and target information
    high_quality_alignments.loc[:, 'query'] = query
    high_quality_alignments.loc[:, 'target'] = target
    
    return high_quality_alignments, query, target

def main(input_path, separator, quality_cutoff, output_path, min_block_length, min_matching_bases, check_strand, consider_strand):
    # Check if the input path is a file or directory
    if os.path.isfile(input_path):
        files_to_process = [input_path]
    else:
        files_to_process = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith('.paf')]
    
    dataframes = {}
    queries = set()
    targets = set()
    
    for file_path in files_to_process:
        print(f"Processing {file_path}")
        high_quality_alignments, query, target = process_paf_file(file_path, separator, quality_cutoff, min_block_length, min_matching_bases, check_strand)
        dataframes[f"{query}_{target}"] = high_quality_alignments
        queries.add(query)
        targets.add(target)
    
    if len(queries) != 1:
        raise ValueError("Multiple queries detected. Ensure all PAF files have the same query genome.")
    
    query_name = queries.pop()
    target_names = list(targets)
    
    # Find common synteny
    common_synteny = None
    
    # Merge alignments on query coordinates
    for i, target in enumerate(target_names):
        df = dataframes[f"{query_name}_{target}"]
        suffix = f"_{target}"
        if common_synteny is None:
            common_synteny = df.rename(columns={
                'target_name': f'target_name{suffix}',
                'target_length': f'target_length{suffix}',
                'target_start': f'target_start{suffix}',
                'target_end': f'target_end{suffix}',
                'target_strand': f'target_strand{suffix}'
            })
        else:
            df = df.rename(columns={
                'target_name': f'target_name{suffix}',
                'target_length': f'target_length{suffix}',
                'target_start': f'target_start{suffix}',
                'target_end': f'target_end{suffix}',
                'target_strand': f'target_strand{suffix}'
            })
            common_synteny = pd.merge(common_synteny, df, on=['query_name', 'query_start', 'query_end'], suffixes=("", suffix))
    
    # Select only the useful columns for synteny visualization
    useful_columns = ['query_name', 'query_length', 'query_start', 'query_end']
    for target in target_names:
        useful_columns.extend([
            f'target_name_{target}', f'target_length_{target}', f'target_start_{target}', f'target_end_{target}', f'target_strand_{target}'
        ])
    
    common_synteny = common_synteny[useful_columns]
    
    # Rename columns to more meaningful names
    column_rename = {
        'query_name': query_name,
        'query_length': f'{query_name}_length',
        'query_start': f'{query_name}_start',
        'query_end': f'{query_name}_end'
    }
    
    for target in target_names:
        column_rename.update({
            f'target_name_{target}': target,
            f'target_length_{target}': f'{target}_length',
            f'target_start_{target}': f'{target}_start',
            f'target_end_{target}': f'{target}_end',
            f'target_strand_{target}': f'{target}_strand'
        })
    
    common_synteny = common_synteny.rename(columns=column_rename)
    
    # Keep only the simpler columns for synteny visualization
    columns_to_keep = [query_name, f'{query_name}_length', f'{query_name}_start', f'{query_name}_end']
    for target in target_names:
        columns_to_keep.extend([target, f'{target}_length', f'{target}_start', f'{target}_end', f'{target}_strand'])
    
    common_synteny = common_synteny[columns_to_keep]
    
    # Optionally filter by strand orientation
    if consider_strand:
        common_synteny = common_synteny[common_synteny.apply(lambda row: all(row[f'{target}_strand'] == row[f'{target_names[0]}_strand'] for target in target_names), axis=1)]
    
    # Determine default output file name
    if len(files_to_process) == 1:
        base_name = os.path.basename(files_to_process[0]).split('.')[0]
        default_output_file = f"synteny_{base_name}.csv"
    else:
        default_output_file = f"synteny_{query_name}_all.csv"
    
    if output_path == '.':
        output_file = default_output_file
    else:
        output_file = output_path
    
    common_synteny.to_csv(output_file, sep=separator, index=False)
    
    print(f"Syntenic blocks have been saved to '{output_file}'")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PAF files for synteny analysis.")
    parser.add_argument("-i", "--input", required=True, help="Input path to process (folder or single file).")
    parser.add_argument("-s", "--separator", default='\t', help="Data separator for the PAF file (default: tab).")
    parser.add_argument("-q", "--quality", type=int, default=50, help="Quality cutoff for filtering alignments (default: >50).")
    parser.add_argument("-o", "--output", default='.', help="Output path for the syntenic blocks file (default: current path or generated file name).")
    parser.add_argument("--min_block_length", type=int, help="Minimum alignment block length for filtering (optional).")
    parser.add_argument("--min_matching_bases", type=int, help="Minimum number of matching bases for filtering (optional).")
    parser.add_argument("--check_strand", action='store_true', help="Check for same strand orientation in alignments (optional).")
    parser.add_argument("--consider_strand", action='store_true', help="Consider strand orientation in synteny analysis (optional).")
    
    args = parser.parse_args()
    main(args.input, args.separator, args.quality, args.output, args.min_block_length, args.min_matching_bases, args.check_strand, args.consider_strand)


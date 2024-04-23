Purpose:
This is a benchmarking tool intended for the nf-core/circrna pipeline ( https://github.com/nf-core/circrna.git ).
This benchmarking is done by comparing the predicted circRNA-content of poly-A selected (which should not have circRNA at all),
and not poly-A Selected material for the same sample.


Configuration

The script accepts several command-line arguments to customize the processing of circRNA data. Below are the options available:

    --tool_list:
        Description: Comma-separated list of directory basenames for circRNA discovery.
        Default: circexplorer2, circrna_finder, dcc, find_circ, segemehl
        Type: String
        Usage: --tool_list tool1,tool2,tool3

    --tools_dir:
        Description: Directory containing the circrna_discovery directory.
        Default: /nfs/data3/CIRCEST/runs/benchmarking/results/circrna_discovery
        Type: String
        Usage: --tools_dir path/to/tools

    --out_dir:
        Description: Path where benchmarking results will be stored.
        Default: /nfs/data3/CIRCEST/runs/benchmarking/benchmarking_results
        Type: String
        Usage: --out_dir path/to/output

    --trimgalore_dir:
        Description: Path to directory containing trimgalore reports.
        Default: /nfs/data3/CIRCEST/runs/benchmarking/results/trimgalore
        Type: String
        Usage: --trimgalore_dir path/to/trimgalore

    --sample_fields:
        Description: Comma-separated indices of the underscore-separated filename that define sample affiliation.
        Default: 0,1
        Type: String
        Usage: --sample_fields indices

    --type_field:
        Description: Index of the underscore-separated filename that defines RNA type.
        Default: 4
        Type: Integer
        Usage: --type_field index

    --module:
        Description: Specifies the modules to execute; '0' for creating stats, '1' for creating plots.
        Default: 01
        Type: String
        Usage: --module 0 or --module 1

Running the Script

To run the script, navigate to the directory containing the script and execute it with the desired parameters. Example command:

python script_name.py --tool_list find_circ,segemehl --tools_dir /path/to/tools --out_dir /path/to/output

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


Output:
1   mRNA_basepairs: Written basepairs used for circRNA-detection
2   tRNA_basepairs	Written basepairs used for circRNA-detection
3    mRNA_total:	Total circRNAs detected
4    mRNA_total_normalized	Total circRNAs detected divided by mRNA_basepairs and multiplied by 0.00000005
5    tRNA_total:	    Total circRNAs detected
6    tRNA_total_normalized:	Total circRNAs detected divided by tRNA_basepairs and multiplied by 0.00000005
7    total_proportions:	mRNA_total/tRNA_total
8    total_proportions_normalized:	mRNA_total_normalized/tRNA_total_normalized
9    overlap_count:	Total count of overlaps between mRNA and tRNA in this sample
10    jaccard_index:    overlap_count/mRNA_total + tRNA_total - overlap_count
11    mRNA_overlap_percentage	overlap_count / mRNA_total
12    mRNA_overlap_percentage_normalized	mRNA_overlap_percentage / mRNA_total
13    tRNA_overlap_percentage	overlap_count / tRNA_total
14    tRNA_overlap_percentage_normalized	tRNA_overlap_percentage / tRNA_total


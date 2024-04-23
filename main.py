from __future__ import print_function
import utils
import os
import argparse

if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--tool_list',
                        default='circexplorer2,circrna_finder,dcc,find_circ,segemehl',
                        type=str, nargs='+', help='Comma-separated list of tools')

    parser.add_argument('--tools_dir',
                        default='/nfs/data3/CIRCEST/runs/benchmarking/results/circrna_discovery', type=str,
                        help='Directory with the different tool directories')
    parser.add_argument('--out_dir',
                        default=r'/nfs/data3/CIRCEST/runs/benchmarking/benchmarking_results',
                        type=str, help='Path to benchmarking results')
    parser.add_argument('--trimgalore_dir',
                        default='/nfs/data3/CIRCEST/runs/benchmarking/results/trimgalore',
                        type=str, help='path to directory with trimgalore reports')
    parser.add_argument('--sample_fields',
                        default='0,1',
                        type=str,
                        help='comma separated field indicees of the "_" separeted filename, that define sample affiliation')

    parser.add_argument('--type_field',
                        default='4',
                        type=int,
                        help='field indice of the "_" separeted filename, that defines rna type')

    parser.add_argument('--module',
                        default='01',
                        type=str, help='0 = create stats, 1 = create plots')
    args = parser.parse_args()


    def main():
        sample_fields = str(args.sample_fields).split(',')
        sample_fields.sort()
        tool_out_path = os.path.abspath(args.tools_dir)
        trimgalore_path = os.path.abspath(args.trimgalore_dir)
        out_path = os.path.abspath(args.out_dir)
        tool_list = str(args.tool_list).strip().split(',')
        utils.create_out_directory(out_path, tool_list, args.module)

        # stat computation:
        if '0' in args.module:
            print(args.tool_list)
            for tool in args.tool_list:
                print(tool)
                filenames = utils.list_directories(os.path.join(args.tools_dir, tool))
                filenames.sort()
                written_basepairs_map = utils.get_written_basepair_map(filenames, args.trimgalore_dir)

                sample_id = ''  # field 0,1
                type = ''  # field 4 (3 after compression)
                samples = {}  # 1. Sample_name, 2. m/tRNA, 3.filelist
                types = {}
                types['mRNA'] = []
                types['tRNA'] = []
                for file in filenames:
                    file_id = str(file).split('_')
                    sample_name = ''
                    for f in sample_fields: sample_name += '_' + file_id[f]
                    sample_name = sample_name[1:]
                    file_id = [sample_name, file_id[args.type_field]]  # sample + type extracted

                    # if no list there create one to allow append
                    if not (file_id[0] in samples.keys()): samples[file_id[0]] = {}
                    if not (file_id[1] in samples[file_id[0]].keys()): samples[file_id[0]][file_id[1]] = []
                    samples[file_id[0]][file_id[1]].append(file)
                    types[file_id[1]].append(file)

                print('Data read')

                os.chdir(args.tools_dir + tool)
                # get Summed array
                # type
                types, types_tRNA_length, types_mRNA_length = utils.get_summed_location_and_length(types,
                                                                                                   written_basepairs_map)
                # sample

                sample_basepairs_dict = {}
                for sample in sorted(samples.keys()):
                    sample_basepairs_dict[sample] = {}
                    os.chdir(args.tools_dir + tool)
                    samples[sample], sample_basepairs_dict[sample]['tRNA'], sample_basepairs_dict[sample]['mRNA'] \
                        = utils.get_summed_location_and_length(samples[sample], written_basepairs_map)
                    utils.compute_stats(tool, sample, samples[sample], sample_basepairs_dict[sample]['mRNA'],
                                        sample_basepairs_dict[sample]['tRNA'], out_path + '/sample_stats')
                    print(sample + '\tfinished')
                utils.compute_stats(tool, tool, types, types_mRNA_length, types_tRNA_length, out_path + '/tool_stats')
                print('tool_stats finished')




    """
0    #	circexplorer2
1   mRNA_basepairs	188217468380
2   tRNA_basepairs	200589554830
3    mRNA_total	2217
4    mRNA_total_normalized	0.235578559108
5    tRNA_total	208969
6    tRNA_total_normalized	20.8354817056
7    total_proportions	0.0106092291201
8    total_proportions_normalized	0.011306604879
9    overlap_count	0
10    jaccard_index	0
11    mRNA_overlap_percentage	0
12    mRNA_overlap_percentage_normalized	0
13    tRNA_overlap_percentage	0
14    tRNA_overlap_percentage_normalized	0
    """

    main()
    print('execution finished')

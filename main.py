from __future__ import print_function
import utils
import os
import argparse

#TODO: samples don't get saved coorectly

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

    parser.add_argument('--module',
                        default='01',
                        type=str, help='0 = create stats, 1 = create plots')
    args = parser.parse_args()


    def main():
        tool_out_path = os.path.abspath(args.tools_dir)
        trimgalore_path = os.path.abspath(args.trimgalore_dir)
        out_path = os.path.abspath(args.out_dir)
        tool_list = str(args.tool_list).strip().split(',')
        utils.create_out_directory(out_path, tool_list, args.module)

        for tool in tool_list:
            filenames = utils.list_directories(args.tools_dir + tool)
            filenames.sort()
            written_basepairs_map = utils.get_written_basepair_map(filenames, args.trimgalore_dir)

            sample_id = ''  # field 0,1
            type = ''  # field 4 (3 after compression)
            samples = {}  # 1. Sample_name, 2. m/tRNA, 3.filelist
            types = {}
            types['mRNA'] = []
            types['tRNA'] = []
            for file in filenames:
                print(file)
                file_id = str(file).split('_')
                file_id[0] = file_id[0] + '_' + file_id[1]
                file_id = [file_id[0], file_id[4]]  # sample + type extracted
                print(file_id)
                # if no list there create one to allow append
                if not (file_id[0] in samples): samples[file_id[0]] = {}
                if not (file_id[1] in samples[file_id[0]]): samples[file_id[0]][file_id[1]] = []
                list(samples[file_id[0]][file_id[1]]).append(file)
                types[file_id[1]].append(file)

                os.chdir(args.tools_dir + tool)
                # get Summed array
                # type
                types, types_tRNA_length, types_mRNA_length = utils.get_summed_location_and_length(types,
                                                                                                   written_basepairs_map)
                # sample
                try :
                    for sample in samples.keys():
                        print(sample.keys())
                except:
                    print(sample)

                sample_basepairs_dict = {}
                for sample in samples.keys():
                    sample_basepairs_dict[sample] = {}
                    samples[sample], sample_basepairs_dict[sample]['tRNA'], sample_basepairs_dict[sample]['mRNA'] \
                        = utils.get_summed_location_and_length(samples[sample], written_basepairs_map)
                    utils.compute_stats(tool, sample, samples[sample], sample_basepairs_dict[sample]['mRNA'],
                                        sample_basepairs_dict[sample]['tRNA'], out_path + '/samplestats')
                utils.compute_stats(tool, tool, types, types_mRNA_length, types_tRNA_length, out_path + '/toolstats')


    # utils.tool_comparison(args.tool_list, filepath_list, out, args.work_dir, args.trimgalore)

    # for i in filenames: bed_filenames.append('{}/{}.annotation.bed'.format(i, i))

    main()
    print('execution finished')

from __future__ import print_function
import utils
import os
import argparse

if __name__ == "__main__":
    # Arguments
    parser = argparse.ArgumentParser(description='Process some paths and a tool list.')
    parser.add_argument('--work_dir', default='../results/circrna_discovery/',
                        type=str, help='Working directory path')
    parser.add_argument('--tool_list',
                        default=['circexplorer2', 'circrna_finder', 'ciriquant', 'dcc', 'find_circ', 'segemehl'],
                        type=str, nargs='+', help='List of tools')
    parser.add_argument('--out', default=r'../benchmarking_results.txt',
                        type=str, help='Path to benchmarking results')
    parser.add_argument('--trimgalore', default='../trimgalore',
                        type=str, help='path to directory with trimgalore reports')
    args = parser.parse_args()


    def main():
        out = os.path.abspath(args.out)
        utils.create_out_directory(out)
        os.chdir(args.work_dir)

        # searching for files and write names to list (sort by tool) (handle intermediates) ( code for what to compare?)
        filesID_list = [s for s in utils.list_directories(args.tool_list[0]) if "intermediates" not in s]
        filepath_list = []
        for i in filesID_list: filepath_list.append('{}/{}.annotation.bed'.format(i, i))

        utils.tool_comparison(args.tool_list, filepath_list, out, args.work_dir, args.trimgalore)
        print('execution finished')


    main()

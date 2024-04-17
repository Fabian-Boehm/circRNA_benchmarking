import os


def get_overlaps(array1, array2):
    overlaps = []
    for one in array1:
        for two in array2:
            # check chromosome and strand
            if one[0] == two[0] and one[5] == two[5]:
                # Corrected check for overlapping positions
                # Overlap occurs if one starts before two ends, and one ends after two starts
                if (one[1] > two[1] and one[2] < two[1]) or (one[1] > two[2] and one[2] < two[2]):
                    overlaps.append([one[0], one[3], one[1], one[2], two[1], two[2]])
    return overlaps


def write_stats(tool, filename_m, filename_t, tRNArray_len, mRNArray_len, overlaps, result_path,
                mRNAlen, tRNAlen):
    with open(result_path, 'a') as file:
        file.write('#\t{}\t{}\t{}\n'
                   'mRNA total:\t{}\n'
                   'tRNA total:\t{}\n'
                   'mRNA/tRNA proportions:\t{:.3f}\n'
                   'Overlaps total:\t{}\n'
                   'Overlaps percentile tRNA:\t{:.3f}%\n'
                   'Overlaps percentile mRNA:\t{:.3f}%\n'

                   'Filelength Proportion(mRNA/tRNA):\t{}\n'
                   'Filelength Proportion(tRNA/mRNA):\t{}\n'
                   'mRNA filelength:\t{}\n'
                   'tRNA filelength:\t{}\n'
                   'mRNA/tRNA normalized proportions:\t{:.3f}\n'

                   'Overlaps normalized percentile tRNA:\t{:.3f}%\n'
                   'Overlaps normalized percentile mRNA:\t{:.3f}%\n'

            .format(
            tool, filename_m, filename_t,

            mRNArray_len,
            tRNArray_len,
            round(mRNArray_len / float(tRNArray_len), 3),
            len(overlaps),
            round(len(overlaps) / float(tRNArray_len), 3),
            round(len(overlaps) / float(mRNArray_len), 3),

            round(mRNAlen / tRNAlen, 3),
            round(tRNAlen / mRNAlen, 3),
            mRNAlen,
            tRNAlen,
            round(mRNArray_len * round(tRNAlen / mRNAlen, 3) / float(tRNArray_len), 3),
            round(len(overlaps) / float(tRNArray_len) * round(tRNAlen / mRNAlen, 3), 3),
            round(len(overlaps) / float(mRNArray_len) * round(mRNAlen / mRNAlen, 3), 3)
        )
        )


def read_file_to_array(file_path):
    array = []
    with open(file_path, 'r') as file:
        for line in file:
            array.append(line.split('\t'))
    return array


def extract_column(array, column_index):
    return [row[column_index] for row in array]


def list_directories(path):
    # List comprehension to get all directories at the given path
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
    return directories


def prune_annotationBED(array):
    strand = []
    for l in array:
        strand.append(l[5])
    i = 0
    while i < len(array):
        array[i] = array[i][:3] + [strand[i]]
        i += 1
    return array


def tool_comparison(tools, files, out_path, work_dir, trimgalore_dir):
    for tool in tools:

        i = 0
        while i + 1 < len(files):
            os.chdir(trimgalore_dir)
            mRNAlen = get_written_Basepairs(files[i])
            tRNAlen = get_written_Basepairs(files[i + 1])

            os.chdir('{}/{}'.format(work_dir, tool))
            mRNArray = read_file_to_array(files[i])
            tRNArray = read_file_to_array(files[i + 1])
            overlaps = get_overlaps(mRNArray, tRNArray)
            write_stats(
                tool,
                files[i].split("/", 1)[0],
                files[i + 1].split("/", 1)[0],
                len(tRNArray), len(mRNArray),
                overlaps,
                out_path,
                mRNAlen,
                tRNAlen
            )
            i += 2


def get_stat_from_stats(statfile_array, statnumber):
    out = []
    while statnumber < len(statfile_array):
        out.append(statfile_array[statnumber])
        statnumber += 8
    return out


def create_out_directory(directory_path, tool_list):
    try:
        os.makedirs(directory_path)
        os.chdir(directory_path)
        os.makedirs('./samples')
    except OSError as e:
        pass


def get_written_basepair(name):
    filepath = name + '.fastq.gz_trimming_report.txt'
    with open(filepath, 'r') as file:
        for i, line in enumerate(file):
            if i == 31:  # Since line numbering starts from 0
                parts = line.split()
                number = parts[3].replace(',', '')  # Remove commas for numerical processing
                return int(number)


def get_written_basepair_map(filenames, trimgalore_path):
    os.chdir(trimgalore_path)
    written_basepairs = {}
    for name in filenames: written_basepairs[name] = get_written_basepair(name)
    return written_basepairs

def get_summed_location_and_length(hashpair, written_basepairs):
    def process_rna_type(rna_type):
        rna_list = []
        rna_length = 0
        for name in dict(hashpair)[rna_type]:
            rna_list += read_file_to_array('{}/{}.annotation.bed'.format(name, name))
            rna_length += written_basepairs[name]
        hashpair[rna_type] = rna_list
        return rna_length

    tRNA_length = process_rna_type('tRNA')
    mRNA_length = process_rna_type('mRNA')
    return hashpair, tRNA_length, mRNA_length


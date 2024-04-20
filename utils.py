import os
import re

# factor to make more beautiful numbers for normalized values
import traceback

normalisation_factor = 0.25


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


def read_file_to_array(file_path):
    array = []
    with open(file_path, 'r') as file:
        for line in file:
            array.append(line.split('\t'))
    return array


def extract_column(array, column_index):
    return [row[column_index] for row in array]

def list_directories(path):
    # Ensure the path ends with a slash
    path = path.rstrip('/') + '/'
    # List comprehension to get all directories at the given path
    directories = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    # Create a new list to store directories with matching .annotation.bed files
    valid_directories = []
    for directory in directories:
        annotation_file = '{}{}/{}.annotation.bed'.format(path, directory, directory)
        if os.path.exists(annotation_file):
            valid_directories.append(directory)
        else:
            print
            '{}\t.bed file does not exist'.format(path + directory)
    return valid_directories


def prune_annotationBED(array):
    strand = []
    for l in array:
        strand.append(l[5])
    i = 0
    while i < len(array):
        array[i] = array[i][:3] + [strand[i]]
        i += 1
    return array


def get_stat_from_stats(statfile_array, statnumber):
    out = []
    while statnumber < len(statfile_array):
        out.append(statfile_array[statnumber])
        statnumber += 8
    return out


def create_out_directory(directory_path, tool_list, modules):
    try:
        os.makedirs(directory_path)
        os.chdir(directory_path)
        if '0' in modules:
            os.makedirs('./toolstats')
            os.makedirs('./samplestats')
        if '1' in modules:
            os.makedirs('./tool_plots')
            os.makedirs('./sample_plots')
            os.chdir('./sample_plots')
            os.makedirs('./total')
            for tool in tool_list: os.makedirs('./' + tool)
    except OSError as e:
        traceback.print_exc()


def get_written_basepair_map(filenames, trimgalore_path):
    def get_written_basepair(name):
        out = 0
        extra = ''
        pattern = r'(_R\d_\d{3})'
        name = re.split(pattern, name, 1)
        if (len(name) > 1): extra = name[1]
        pattern = r'(_L\d{3})'
        name = re.split(pattern, name[0], 1)
        name = name[0] + name[1] + extra

        filepath = trimgalore_path + name + '_1.fastq.gz_trimming_report.txt'
        with open(filepath, 'r') as file:
            for i, line in enumerate(file):
                if i == 32:  # Since line numbering starts from 0
                    parts = line.split()
                    number = parts[3].replace(',', '')  # Remove commas for numerical processing
                    out += int(number)
        filepath = trimgalore_path + name + '_2.fastq.gz_trimming_report.txt'
        with open(filepath, 'r') as file:
            for i, line in enumerate(file):
                if i == 32:  # Since line numbering starts from 0
                    parts = line.split()
                    number = parts[3].replace(',', '')  # Remove commas for numerical processing
                    out += int(number)
        return out

    os.chdir(trimgalore_path)
    written_basepairs = {}
    for name in filenames: written_basepairs[name] = get_written_basepair(name)
    return written_basepairs


def get_summed_location_and_length(hashpair, written_basepairs):
    def process_rna_type(rna_type):
        rna_list = []
        rna_length = 0
        for name in dict(hashpair)[rna_type]:
            print(os.getcwd()+'/{}/{}.annotation.bed'.format(name, name))
            rna_list += read_file_to_array(os.getcwd()+'/{}/{}.annotation.bed'.format(name, name))
            rna_length += written_basepairs[name]
        hashpair[rna_type] = rna_list
        return rna_length

    # check legal
    if not (hashpair.keys() == ['tRNA', 'mRNA']):
        print(hashpair.keys())
        return None, 0, 0

    tRNA_length = process_rna_type('tRNA')
    mRNA_length = process_rna_type('mRNA')
    return hashpair, tRNA_length, mRNA_length


def compute_stats(tool_name, sample_name, sample, mRNA_basepairs, tRNA_basepairs, directory):
    os.chdir(directory)
    sample;
    mRNA_basepairs;
    tRNA_basepairs;

    mRNA_total = len(sample['mRNA'])
    tRNA_total = len(sample['tRNA'])
    overlap_count = len(get_overlaps(sample['mRNA'], sample['tRNA']))

    print(overlap_count)
    print(mRNA_total)

    mRNA_overlap_percentage = overlap_count / mRNA_total
    tRNA_overlap_percentage = overlap_count / tRNA_total

    mRNA_total_normalized = mRNA_total / normalisation_factor * mRNA_basepairs  # overlap coefficient
    tRNA_total_normalized = tRNA_total / normalisation_factor * tRNA_basepairs
    mRNA_overlap_percentage_normalized = mRNA_overlap_percentage / mRNA_total  # normalized overlap coeficcient
    tRNA_overlap_percentage_normalized = tRNA_overlap_percentage / tRNA_total

    union = mRNA_total + tRNA_total - overlap_count  # not a stat
    jaccard_index = overlap_count / union if union != 0 else 0

    # filewriting

    with open(directory + '/' + tool_name + '.txt', 'a') as statfile:
        statfile.write(
            '#\t{}\n'
            'mRNA_basepairs\t{}\n'
            'tRNA_basepairs\t{}]\n'
            'mRNA_total\t{}\n'
            'mRNA_total_normalized\t{}\n'
            'tRNA_total\t{}\n'
            'tRNA_total_normalized\t{}\n'
            'overlap_count\t{}\n'
            'jaccard_index\t{}\n'
            'mRNA_overlap_percentage\t{}\n'
            'mRNA_overlap_percentage_normalized\t{}\n'
            'tRNA_overlap_percentage\t{}\n'
            'tRNA_overlap_percentage_normalized\t{}\n'
                .format(
                sample_name,
                mRNA_basepairs,
                tRNA_basepairs,
                mRNA_total,
                mRNA_total_normalized,
                tRNA_total,
                tRNA_total_normalized,
                overlap_count,
                jaccard_index,
                mRNA_overlap_percentage,
                mRNA_overlap_percentage_normalized,
                tRNA_overlap_percentage,
                tRNA_overlap_percentage_normalized
            )
        )

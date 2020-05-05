# This parser requires a file and returns a Seq.

from Bio import SeqIO
import sys


def main(argv):
    file_name = argv[1]
    file_format = file_name.split('.')[-1]

    # Handle clustal_num file format as clustal format
    if file_format.__contains__('_'):
        file_format = file_format.split('_')[0]

    sequences = []

    for seq_record in SeqIO.parse(file_name, file_format):
        sequences.append({
            'id': seq_record.id,
            'seq': seq_record.seq,
            'seq_length': len(seq_record)
        })

    return sequences


main(sys.argv)

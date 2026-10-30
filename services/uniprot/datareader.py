from pathlib import Path

import pyfastx

FASTA_PATH = Path(__file__).parent / "data" / "uniprot.fasta"


def get_fastx():
    fasta_data = {}

    for record in pyfastx.Fasta(str(FASTA_PATH)):
        uniprot_id = record.name.split("|")[1]
        fasta_data[uniprot_id] = record.seq

    return fasta_data

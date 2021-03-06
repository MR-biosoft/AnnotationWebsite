from Bio.Blast import NCBIWWW, NCBIXML
import numpy as np


def launch_blast(
    sequence,
    program="blastn",
    database="nr",
    e_value_threshold=10,
    word_size=None,
    megablast=False,
):

    word_size = word_size or 10

    blast_output = NCBIWWW.qblast(
        program=program,
        database=database,
        sequence=sequence,
        format_type="XML",
        descriptions=0,
        alignments=100,
        expect=e_value_threshold,
        hitlist_size=100,
        megablast=megablast,
        word_size=word_size,
    )
    blast_entries = NCBIXML.read(blast_output)
    blast_entry_list = []
    for entry in blast_entries.alignments:
        entry_dict = {}
        title = entry.title.split("|")
        entry_dict["gi"] = title[1]
        entry_dict["gb_emb"] = title[3]
        hsps = entry.hsps[0]
        entry_dict["score"] = hsps.score
        entry_dict["bits"] = hsps.bits
        entry_dict["e_value"] = -round(np.log10(hsps.expect), 4)
        entry_dict["identities"] = hsps.identities
        entry_dict["gaps"] = hsps.gaps
        entry_dict["coverage"] = hsps.align_length
        blast_entry_list.append(entry_dict)
    return blast_entry_list


blast_hits = [
    {
        "gi": "1845299776",
        "gb_emb": "CP053597.1",
        "score": 2463.0,
        "bits": 4549.42,
        "e_value": 0.0,
        "identities": 2463,
        "gaps": 0,
        "coverage": 2463,
    },
    {
        "gi": "1845295615",
        "gb_emb": "CP053603.1",
        "score": 2463.0,
        "bits": 4549.42,
        "e_value": 0.0,
        "identities": 2463,
        "gaps": 0,
        "coverage": 2463,
    },
    {
        "gi": "1845291569",
        "gb_emb": "CP053595.1",
        "score": 2463.0,
        "bits": 4549.42,
        "e_value": 0.0,
        "identities": 2463,
        "gaps": 0,
        "coverage": 2463,
    },
]

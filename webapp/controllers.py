from flask import request, render_template, jsonify, flash
from .models import *
import sys
from Bio.SeqUtils import ProtParamData
from Bio.SeqUtils import IsoelectricPoint
from Bio.Seq import Seq
from Bio.Data import IUPACData
from Bio.SeqUtils import molecular_weight

def flash_errors(form):
    """Generate flashes for errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


# e.g. only peptools

class PepTool:
    def __init__(self, prot_sequence, monoisotopic=False):
        if prot_sequence.islower():
            self.sequence = Seq(prot_sequence.upper())
        else:
            self.sequence = Seq(prot_sequence)
        self.amino_acids_content = None
        self.amino_percent = None
        self.length = len(self.sequence)
        self.monoisotopic = monoisotopic



    def molecular_weight(self):
        return molecular_weight(
            self.sequence, seq_type="protein", monoisotopic=self.monoisotopic
        )

    def amino_count(self):
        if self.amino_acids_content is None:
            prot_dic = {k: 0 for k in IUPACData.protein_letters}
            for aa in prot_dic:
                prot_dic[aa] = self.sequence.count(aa)

            self.amino_acids_content = prot_dic

        return self.amino_acids_content

    def get_amino_percent(self):
        if self.amino_percent is None:
            aa_counts = self.amino_count()

            percentages = {}
            for aa in aa_counts:
                percentages[aa] = aa_counts[aa] / float(self.length)

            self.amino_percent = percentages

        return self.amino_percent

    def isoelectric_point(self):
        aa_content = self.amino_count()

        ie_point = IsoelectricPoint.IsoelectricPoint(self.sequence, aa_content)
        return ie_point.pi()

    def charge_at_pH(self, pH):
        aa_content = self.amino_count()
        charge = IsoelectricPoint.IsoelectricPoint(self.sequence, aa_content)
        return charge.charge_at_pH(pH)
    
    def molar_extinction_coefficient(self):
        num_aa = self.amino_count()
        mec_reduced = num_aa["W"] * 5500 + num_aa["Y"] * 1490
        mec_cystines = mec_reduced + (num_aa["C"] // 2) * 125
        return (mec_reduced, mec_cystines)
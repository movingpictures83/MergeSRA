# Objective:
#   To merge SRA runs to individuals

import os
import pandas as pd

import PyPluMA
import PyIO

def combine_mate(prefix, samples_dir, run, out_dir, sra_dict):
    # prefix is either "_1.fastq" or "_2.fastq"; Actually it's affix but whatever
    m_path = os.path.join(samples_dir, run + prefix)
    combined_path = os.path.join(out_dir, sra_dict[run] + prefix)
    if os.path.exists(m_path):
        print(m_path)
        with open(m_path, 'r') as m1:
            with open(combined_path, 'a') as out:
                for line in m1.readlines():
                    out.write(line)
        #os.remove(m_path)




class MergeSRAPlugin:
 def input(self, inputfile):
   self.parameters = PyIO.readParameters(inputfile)

 def run(self):
     pass

 def output(self, outputfile):
     batch = self.parameters["batch"]#"1"
     samples_dir = PyPluMA.prefix()+"/"+self.parameters["samples_dir"]#"../../Raymond/samples/FASTQ/"
     out_dir = outputfile#"RaymondCombined/"
     metadata_file = PyPluMA.prefix()+"/"+self.parameters["metadata_file"]#"SraRunTable.csv"
     sra_list_file = PyPluMA.prefix()+"/"+self.parameters["sra_prefix"]+batch+".txt"#"raymond_b"+batch+".txt"

     m1_prefix = "_1.fastq"
     m2_prefix = "_2.fastq"

     runs_list = []
     with open(sra_list_file, 'r') as sra_f:
      for line in sra_f.readlines():
        runs_list.append(line.replace("\n", ""))

     files_list = os.listdir(samples_dir)

     # map each SRA run to corresponding sample
     sra_dict = {}
     print(metadata_file)
     with open(metadata_file, "r") as f:
       f.readline()
       for row in f.readlines():
        row_list = row.split(",")
        run = row_list[0]
        sample = row_list[1]
        sra_dict[run] = sample

     for run in runs_list:
      # Combine mates:
      combine_mate(m1_prefix, samples_dir, run, out_dir, sra_dict)
      combine_mate(m2_prefix, samples_dir, run, out_dir, sra_dict)

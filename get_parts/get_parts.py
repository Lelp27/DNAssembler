import sys
sys.path.append('/mnt/kun/git/ot2/protocol/assembly/get_parts')
from get_parts_param import *
from xlsx_fun import *

from get_parts_fun import *
import pandas as pd
import pickle
import argparse

"""
Mode1 = RUN (export pickle)
Mode2 = Export Excel
Mode3 = Excel Edit (without pickle) 3
Mode4 = make OT2 (get script directly)
"""

def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-o', type=str, help='pickle output path', default="./data.pickle" , required=False)
    parser.add_argument('--xlsx', type=str, help='xlsx output path', required=False)
    
    args=parser.parse_args()
    return args

def main():
    part_dna = []
    for i1 in part_order:
        part_dna.append(internal_part_to_dna_form(i1, db))

    # Export data
    ## plate data
    plates = []
    for i in sum(part_dna, []):
        plates.append(i.plate)
    plates = list(set(plates))

    ## External DNA data
    if 'EXT' in plates:
        ext_dna = []
        n = 0

        for i in sum(part_order, []):
            if type(i) == dna:
                ext_dna.append(i)

        for i in ext_dna:
            i.well = EXT_dna_wells[n]
            n += 1

    well_gen = set_part_to_assembly(part_dna, n2=part_number, target_MW=target_MW, final_volume=final_volume, n1=0)

    well_list = [] 
    for i in well_gen:
        well_list.append(i)
    well_list.append(plates)
    # Data Export
    ## Pickle (protocol=3 for python2 of ot2 machine)

    pickle_path = args.o
    with open(pickle_path, 'wb') as f:
        pickle.dump(well_list, f, protocol=3)

    ## Excel (Optional)
    ### Excel에서 Edtiing 후 다시 가져오도록..
    if args.xlsx:
        writer = pd.ExcelWriter(args.xlsx, engine='xlsxwriter')

        wells_df = export_wells_to_xlsx(well_list[:-1])
        parts_df = export_parts_to_xlsx(sum(part_dna, []))

        wells_df.to_excel(writer, sheet_name='well')
        parts_df.to_excel(writer, sheet_name='part')
        
        writer.save()

if __name__ == "__main__":
    args = get_args()
    main()
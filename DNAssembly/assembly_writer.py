from signal import SIG_DFL
import sys
sys.path.append('/mnt/c/workspace/git/DNAssembler/DNAssembly')
import pandas as pd
from assembly_fun import *

import argparse
import datetime
import re


"""
assembly writer
with parameter, write assembly script to use.
"""
def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument('-i', type=str, help='DNA input matrix want to assemble', required=True)
    parser.add_argument('-t', type=str, help='The template .py file, default is assembly_template.py', required=True)
    parser.add_argument('-o', type=str, help='Output path of assembly-script', default="./assembly.py", required=True)
    args = parser.parse_args()
    return (args)

def get_args2():
    parser=argparse.ArgumentParser()
    parser.add_argument('-m', type=str, help='meta_data path', required=True)
    parser.add_argument('-p', type=str, default = 'assembly', choices=['assembly', 'pooling'], help='protocol', required=True)
    parser.add_argument('-t', type=str, help = 'template.py file path', required=True)
    parser.add_argument('-o', type=str, help='script output', default="./assembly.py" , required=True)

    args=parser.parse_args()
    return args

def assembly():
    pass

def calc_meta():
    pass

# calculate meta_data
## Parameters
input_path = '/mnt/c/workspace/git/DNAssembler/DNAssembly/assembly_input.xlsx'
db_path = '/mnt/c/workspace/git/DNAssembler/DNAssembly/Part_DB_ot2.xlsx'
db = pd.read_excel(db_path)

## input parameter
wells = pd.read_excel(input_path).iloc()[:,:3].fillna(0)
well_parts = [i.split('_') for i in wells['DNA']]
uni_parts = list(set(sum(well_parts, [])))
part_check(uni_parts, db)
parameter_check(wells)

print (f"Final Well number: {len(wells['DNA'])}")
print (f"Used Parts: {uni_parts}")

## convert to dna class
part_dna = [internal_part_to_dna_form(i, db) for i in uni_parts]
ext_dna = [i for i in part_dna if i.plate == 'ext']

n=0
for i in ext_dna:
    i.well = EXT_wells[n]
    n+=1

plates = list(set([i.plate for i in part_dna]))


#==
def assembly(DNA, target_MW, final_volume):
    n = 0
    No_list, name_list, vol_list, well_dict = [], [], [], {}
    for i2, mw in zip(DNA, target_MW):
        vol, dil = check_dilution(i2, mw)
        well_dict[f'part{n}'] = {'well': i2.well, 'vol':vol, 'dil':dil, 'plate':i2.plate}
        No_list.append(i2.No)
        name_list.append(i2.name)
        vol_list.append(vol)
        n+=1
    meta_data = {
        'No':'_'.join(No_list),
        'name':'_'.join(name_list),
        'DW': round((final_volume*4/5) - sum(vol_list), 2)
        }
    well_dict['meta'] = meta_data

    return (well_dict)

def set_part_to_assembly(part_dna, n2, target_MW, final_volume, n1=0):
    
    if n1 == n2:
        parts = []
        for i in range(n2):
            parts.append(eval(f"part{i}"))
        yield assembly(DNA=parts, target_MW = target_MW, final_volume=final_volume)
    else:
        for globals()[f'part{n1}'] in part_dna[0+n1]:
            yield from set_part_to_assembly(part_dna, n2=n2, target_MW=target_MW, final_volume=final_volume, n1 = n1+1)
#==

for i in wells.values:
    n = 0
    No_list, name_list, vol_list, well_dict = [], [], [], {}
    for i2, mw in zip(i[0])






## Parameters 
date = datetime.datetime.now().strftime("%x")
enzyme_mix_vol = 4
input_matrix = ''
load_plate

##



def assembly(*args):
    """
    Arguments = [time, meta_data, enzyme_mix_vol, load_plate]
    """
    args=get_args()

    ## Load metadata
    meta_data = calc_meta()
    ## Load template
    with open(args.t, 'r') as f:
        template = ''.join(f.readlines())

    ### load_plate
    plates = meta_data[-1]
    plates.remove('EXT')
    if len(plates) > 4:
        sys.exit("Too many plates !\nMaximum is 4.")

    load_plate = []
    n = 1
    for i in plates:
        load_plate.append(f"globals()['{i}'] = protocol.load_labware('biorad_96_wellplate_200ul_pcr', {n})")
        n+=1

    ### Template.replace
    hash_tag = re.compile("#!#.+#!#")
    template = re.sub(hash_tag, "", template)
    new_script = template.format(date = time, meta_data = str(meta_data), enzyme_mix_vol=enz_vol, load_plate='\n    '.join(load_plate))

    ### Write
    with open(args.o, 'w') as f:
        f.write(new_script)
        f.close()
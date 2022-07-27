import pickle
import sys
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
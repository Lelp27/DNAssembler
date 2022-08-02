import sys
sys.path.append('/mnt/c/workspace/git/DNAssembler/DNAssembly')
import argparse
from assembly_fun import *
from datetime import datetime
import re

def get_args():
    parser = argparse.ArgumentParser(prog = "OT2 writer", usage = '%(prog)s [options]')
    parser.add_argument('-i', type=str, help='input.xlsx path', required=True)
    parser.add_argument('-db', type=str, help='database path', required=True)
    parser.add_argument('-t', type=str, help='templatey.py path', default='./assembly_template.py')
    parser.add_argument('-o', type=str, help='output.py path', default='{date}_protocol.py'.format(date = datetime.now().strftime("%y%m%d")))
    parser.add_argument('--thermo', dest='thermo', action='store_true')
    parser.set_defaults(thermo=False)

    args = parser.parse_args()
    return (args)


def main():
    args=get_args()
    final_volume = 16


    # Protocol Writing
    ## Parameters for protocol generation
    date = datetime.now().strftime("%x")
    data = calculate_metadata(input_path=args.i, db_path=args.db, final_volume=final_volume)

    ### Load plate Labware
    try:
        data['plate'].remove('ext')
    except:
        pass
    
    plate = data['plate']

    if len(plate) > 4:
        sys.exit("Too many plates ! Maximum is 4. \nProtocol End")

    n, load_plate = 1, []
    for i in plate:
        load_plate.append(f"globals()['{i}'] = protocol.load_labware('biorad_96_wellplate_200ul_pcr', {n})")
        n+=1

    ### Load template
    with open(args.t, 'r') as f:
        template = ''.join(f.readlines())
        f.close()

    ### Write protocol
    comment_tag = re.compile("#!#.+#!#") # for comment in protocol
    template = re.sub(comment_tag, "", template)
    new_script = template.format(date = date, meta_data = str(data), load_plate='\n    '.join(load_plate), thermocycler=args.thermo)

    # Output protocol
    with open(args.o, 'w') as f:
        f.write(new_script)
        f.close()


if __name__ == "__main__":
    main()

"""
def export_xlsx():
    # Excel export (optional)
    writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
    well_df = export_wells_to_xlsx()
    part_df = export_parts_to_xlsx()

    well_df.to_excel(writer, sheet_name='well')
    part_df.to_excel(writer, sheet_name='part')

    writer.save()
"""
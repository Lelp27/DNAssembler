import sys
import pandas as pd

class dna:
    # Basic information
    ## MW can calculate with python or Excel.
    ## MW & name is necessary
    def __init__(self, name, MW=None, No=None, well=None, plate="EXT"):
        #self.length = length
        #self.conc = conc
        self.MW = MW
        self.name = name
        self.No = No
        self.well = well
        self.plate = plate
    
    # get optimal volume based on [part, cds, vector]_MW parameter.
    def get_volume(self, goal_MW):
        if self.MW == None:
            return (self.vol)
        final = round(goal_MW/self.MW, 2)
        return (final)

# 220726
def part_check(uni_parts, db):
    for i1 in uni_parts:
        if i1 in db['No'].values:
            continue
        else:
            print (f"Break! {i1} isn't in DB")
            #sys.exit('Parts No Error')
    print ("Parts confirmed")

def parameter_check(wells):
    for well in wells.iloc():
        part_num = len(well['DNA'].split('_'))
        vol_num = len(well['Volume'].split('_'))
        if part_num != vol_num:
            sys.exit(f"Warning!, {well['DNA']}'s Volume must be same length with part number \nExit Protocol.")
    print ("Parameters Confrimed")

def part_to_dna_form(uni_parts, db):
    tmp = db[db["No"] == uni_parts]
    tmp_dna = dna(
        name = tmp.Name.values[0],
        MW = tmp.MW.values[0],
        well = tmp.Well.values[0],
        No = tmp.No.values[0],
        plate = tmp.plate.values[0])
    
    return (tmp_dna)

def assembly(well, part_list, part_list_dna, final_volume):
    n = 0
    No_list, name_list, vol_list, well_dict = [], [], [], {}
    for no, vol in zip(well['DNA'].split('_'), well['Volume'].split('_')):
        DNA = part_list_dna[part_list.index(no)]
        well_dict[f'part{n+1}'] = {'plate':DNA.plate, 'well': DNA.well, 'vol':vol}
        No_list.append(DNA.No)
        name_list.append(DNA.name)
        vol_list.append(float(vol))
        n+=1
    meta_data = {
        'No': '_'.join(No_list),
        'name': '_'.join(name_list),
        'DW': round(final_volume - sum(vol_list), 2)
        }
    well_dict['meta'] = meta_data

    return (well_dict)


def calculate_metadata(**kwargs):
    """
    input_path, db_path, final_volume
    """
    pass
    ## input parameter
    db = pd.read_excel(db_path)
    wells = pd.read_excel(input_path).iloc()[:,:2].fillna(0)
    well_parts = [i.split('_') for i in wells['DNA']]
    part_list = list(set(sum(well_parts, [])))
    part_check(part_list, db)
    parameter_check(wells)

    print (f"Final Well number: {len(wells['DNA'])}")
    print (f"Used Parts: {part_list}")

    ## convert to dna class
    part_list_dna = [part_to_dna_form(i, db) for i in part_list]

    ### EXT parts
    n, ext_dna = 0, {}
    for i in part_list_dna:
        if i.plate == 'ext':
            ext_dna[i.No] = EXT_wells[n]
            i.well = EXT_wells[n]
            n+=1

    plates = list(set([i.plate for i in part_list_dna]))

    meta_data = {}
    n, well_data = 1, {}
    for well in wells.iloc():
        well_data[f'well{n}'] = assembly(well, part_list, part_list_dna, final_volume)
        n+=1

    meta_data['well_data'] = well_data
    meta_data['part'] = part_list
    meta_data['plate'] = plates
    meta_data['EXT'] = ext_dna

    return (meta_data)


## tmp_dna's well The well's architechture is from opentrons 24 wells plate.
EXT_wells = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
import sys

# Functions
class dna:
    # Basic information
    ## MW can calculate with python or Excel.
    ## MW & name is necessary
    def __init__(self, name, MW=None, vol=None, No=None, well=None, plate="EXT", external=True):
        #self.length = length
        #self.conc = conc
        self.MW = MW
        self.vol = vol
        self.name = name
        self.No = No
        self.well = well
        self.plate = plate

        if external:
            self.necessary_parameter()
        else:
            pass

    def necessary_parameter(self):
        if (self.vol == None) & (self.MW == None):
            print ("Warnning, \nWrong Part! \nOne of MW or vol is necessary! \n")
            sys.exit("Exit Protocol")

        if self.vol:
            print ("Volume parameter is only for Vector.\n")

        print ("DNA part accepted")
    
    # get optimal volume based on [part, cds, vector]_MW parameter.
    def get_volume(self, goal_MW):
        if self.MW == None:
            return (self.vol)
        final = round(goal_MW/self.MW, 2)
        return (final)

def parameter_check(part_order, part_number):
    # for logging
    if len(part_order) != part_number:
        print ("Part number is not equal to length of order, Plz check it")
    print ("Parameter Checked")

def internal_part_check(part_order, db):
    
    for i1 in part_order:
        for i2 in i1:
            if type(i2) == dna:
                # External DNA
                continue
            if i2 in db['No'].values:
                continue
            else:
                print (f"Break! {i2} in {i1} isn't in DB")
                sys.exit("Exit Protocol")
    print ("Internal Part Checked")

def internal_part_to_dna_form(part_list, part_db):
    return_list = []
    for i in part_list:
        if type(i) == dna:
            return_list.append(i)
        else:
            tmp = part_db[part_db["No"] == i]
            locals()[f'{i}_dna'] = dna(
                name = tmp.Name.values[0],
                MW = tmp.MW.values[0],
                well = tmp.Well.values[0],
                No = tmp.No.values[0],
                plate = tmp.plate.values[0],
                vol = tmp.vol.values[0],
                external=False)
            return_list.append(locals()[f'{i}_dna'])
        
    return (return_list)


# make assembly well
def check_dilution(dna, target_MW):
    if dna.get_volume(target_MW) < 0.5:
        return (round(dna.get_volume(target_MW)*5, 2), 5)
    else:
        return (round(dna.get_volume(target_MW), 2), 0)

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

EXT_dna_wells = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
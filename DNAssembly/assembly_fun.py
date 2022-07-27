import sys

class dna:
    # Basic information
    ## MW can calculate with python or Excel.
    ## MW & name is necessary
    def __init__(self, name, MW=None, vol=None, No=None, well=None, plate="EXT"):
        #self.length = length
        #self.conc = conc
        self.MW = MW
        self.vol = vol
        self.name = name
        self.No = No
        self.well = well
        self.plate = plate

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

# 220726
def input_parts_check(uni_parts, db):
    for i1 in uni_parts:
        if i1 in db['No'].values:
            continue
        else:
            print (f"Break! {i1} isn't in DB")
            #sys.exit('Parts No Error')
    print ("Input Part checked")

def internal_part_to_dna_form(uni_parts, db):
    tmp = db[db["No"] == uni_parts]
    tmp_dna = dna(
        name = tmp.Name.values[0],
        MW = tmp.MW.values[0],
        well = tmp.Well.values[0],
        No = tmp.No.values[0],
        plate = tmp.plate.values[0],
        vol = tmp.vol.values[0],
        external=False)
    
    return (tmp_dna)

## tmp_dna's well The well's architechture is from opentrons 24 wells plate.
EXT_dna_wells = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
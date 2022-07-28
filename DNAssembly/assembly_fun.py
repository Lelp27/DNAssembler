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
    for well in wells.values:
        part_num = len(well[0].split('_'))
        if (well[1] == 0) & (well[2] == 0):
            print ("Warning, MW ratio or Volume must be filled ! \nExit Protocol.")
            #sys.exit("Warning, MW ratio or Volume must be filled !\nExit Protocol.")

        elif (well[1]==0):
            try:
                tmp_num = len(well[2].split('_'))
            except:
                tmp_num = 0
        elif (well[2]==0):
            try:
                tmp_num = len(well[1].split('_'))
            except:
                tmp_num=0
        if part_num != tmp_num:
            print (f"Warning {well[0]}'s MW or Volumn must be same length with part number \nExit Protocol.")
            #sys.exit(f"Warning {well[0]}'s MW or Volumn must be same length with part number \nExit Protocol.")
    print ("Parameteres confirmed")

def internal_part_to_dna_form(uni_parts, db):
    tmp = db[db["No"] == uni_parts]
    tmp_dna = dna(
        name = tmp.Name.values[0],
        MW = tmp.MW.values[0],
        well = tmp.Well.values[0],
        No = tmp.No.values[0],
        plate = tmp.plate.values[0],
        vol = tmp.vol.values[0])
    
    return (tmp_dna)

## tmp_dna's well The well's architechture is from opentrons 24 wells plate.
EXT_wells = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'B1', 'B2', 'B3', 'B4', 'B5', 'B6']
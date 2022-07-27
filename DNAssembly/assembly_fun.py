import sys
import pandas as pd

sys.path.append('/mnt/c/workspace/git/automated-protocol-ot2/protocols/DNAssembly')

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

path = '/mnt/c/workspace/git/automated-protocol-ot2/protocols/DNAssembly/assembly_input.xlsx'
df = pd.read_excel(path)['DNA'].values
df = [i.split('_') for i in df]

print (f"Final Well number: {len(df)}")
dna_parts = list(set(sum(df, [])))


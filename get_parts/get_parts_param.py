import sys
sys.path.append('/mnt/kun/git/ot2/protocol/assembly/get_parts')
import pandas as pd
from get_parts_fun import dna, parameter_check, internal_part_check

# Parameters
db_path = "/mnt/kun/git/ot2/protocol/assembly/sample/Part_DB_ot2.xlsx"
part_number = 5
final_volume = 20

## External Parts
### Sample
"""
pACBB_vec = dna(name = "pACBB", No = 'pBB', vol = 5, well='A1', plate='enz')
"""

pACBB_vec = dna(name = "pACBB", No = 'pBB', vol = 5)
dmpR = dna(name="DmpR", MW=34, No="Dm")

## Internal Parts
pro = ['p1','p6','p12','p18','p21']
rbs = ['r1','r18','r22','r23']
ter = ['t25']
vec = [pACBB_vec]
cds = [dmpR]

## Order & Target MW
### order can affect to Assembled DNA's name order & Device Input order
part_order = [vec, cds, pro, rbs, ter]
target_MW = [56, 112, 112, 112, 112]

# Part_check
db = pd.read_excel(db_path)

parameter_check(part_order, part_number)
internal_part_check(part_order, db)
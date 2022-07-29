import sys
sys.path.append('/mnt/c/workspace/git/DNAssembler/DNAssembly')
from assembly_fun import *
from datetime import datetime
import re

# calculate meta_data
## Parameters for data calculation
input_path = '/mnt/c/workspace/git/DNAssembler/DNAssembly/assembly_input.xlsx'
db_path = '/mnt/c/workspace/git/DNAssembler/DNAssembly/Part_DB_ot2.xlsx'
template_path = '/mnt/c/workspace/git/DNAssembler/DNAssembly/assembly_template.py'
output_path = '/mnt/c/workspace/git/DNAssembler/test.py'
final_volume = 16

data = calculate_metadata(input_path=input_path, db_path=db_path, final_volume=final_volume)

# Excel export (optional)
writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
well_df = export_wells_to_xlsx()
part_df = export_parts_to_xlsx()

well_df.to_excel(writer, sheet_name='well')
part_df.to_excel(writer, sheet_name='part')

writer.save()

# Protocol Writing
## Parameters for protocol generation
date = datetime.now().strftime("%x")

### Load plate Labware
try:
    plate = data['plate'].remove('ext')
except:
    plate = data['plate']

if len(plate) > 4:
    sys.exit("Too many plates ! Maximum is 4. \nProtocol End")

n, load_plate = 1, []
for i in plate:
    load_plate.append(f"globals()['{i}'] = protocol.load_labware('biorad_96_wellplate_200ul_pcr', {n})")
    n+=1

### Load template
with open(template_path, 'r') as f:
    template = ''.join(f.readlines())
    f.close()

### Write protocol
comment_tag = re.compile("#!#.+#!#") # for comment in protocol
template = re.sub(comment_tag, "", template)
new_script = template.format(date = date, meta_data = str(data), load_plate='\n    '.join(load_plate))

# Output protocol
with open(output_path, 'w') as f:
    f.write(new_script)
    f.close()
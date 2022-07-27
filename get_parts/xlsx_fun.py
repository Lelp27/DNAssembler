import pandas as pd

def part_to_xlsx(dna_part):
    part_df = {}
    
    part_df['No'] = dna_part.No
    part_df['plate'] = dna_part.plate
    part_df['well'] = dna_part.well
    part_df['name'] = dna_part.name

    return (part_df)

def well_to_xlsx(well):
    
    well_df = {}
    well_df['No'] = well['meta']['No']

    n = 0
    for _ in range(1, len(well)):
        vol = well[f'part{n}']['vol']
        dil = well[f'part{n}']['dil']
        if dil:
            well_df[f'part{n}'] = ' / '.join([str(vol), str(dil)])
        else:
            well_df[f'part{n}'] = str(vol)
        n+=1
        
    well_df['DW'] = well['meta']['DW']

    return (well_df)

def export_wells_to_xlsx(well_list):
    tmp_list = []
    for i in well_list:
        tmp_list.append(well_to_xlsx(i))
    
    return (pd.DataFrame(tmp_list))

def export_parts_to_xlsx(well_list):
    tmp_list = []
    for i in well_list:
        tmp_list.append(part_to_xlsx(i))
    
    return (pd.DataFrame(tmp_list))
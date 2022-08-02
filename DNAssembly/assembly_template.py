from opentrons import types, protocol_api
from math import floor

#|# Verified at 2022-08-02 by kun without Thermocycler. #|#

#|# DNA assembly template script. #|#
#|# Don't Run This script directly with OT2! #|#

"""
parameters = [date, meta_data, enzyme_mix_vol, load_plate]
"""

metadata = {{
    'protocolName': 'Golden gate assembly used by SBL (96 well plate based)',
    'author': 'Seong-Kun Bak <tjdrns27@kribb.re.kr>',
    'apiLevel': '2.11',
    'description': 'Simultaneous part assembly with different part combination',
    'date' : '{date}'
}}

# Parameters from protocol writer.

META_DATA = {meta_data}
RUN_THERMO = {thermocycler}


def run(protocol: protocol_api.ProtocolContext):

    ## get global parameters
    well_data = META_DATA['well_data']

    # Deck Setting
    ## Modules  
    module_thermocycler = protocol.load_module("thermocycler Module")

    ## Racks
    {load_plate}

    assemble_plate = module_thermocycler.load_labware("biorad_96_wellplate_200ul_pcr")
    ext = protocol.load_labware('opentrons_24_tuberack_eppendorf_1.5ml_safelock_snapcap', 9)
    trash = protocol.loaded_labwares[12]["A1"]

    tiprack_20_1 = protocol.load_labware("opentrons_96_tiprack_20ul", 6)
    tiprack_20_2 = protocol.load_labware("opentrons_96_tiprack_20ul", 5)
    p20_sin = protocol.load_instrument("p20_single_gen2", "right", tip_racks=[tiprack_20_1, tiprack_20_2])

    ## Start Tiprack positions
    p20_sin.starting_tip = tiprack_20_1.well("A1")

    ## Reagents
    ### Every reagent should be in 1.5ml Bioneer screw tube.
    #enz_mix = EXT['D1']
    DW = ext['D1']

    # Protocol
    ## Functions
    def enzyme_transfer(pipette, volume, src, dest, delay_second=[0, 0],
                    top_delay=False, asp_rate=None, dis_rate=None,
                    mix_after=False, drop_tip = True):
        # top_delay = list, delay_second= list, mix_after = list

        if asp_rate:
            pipette.flow_rate.aspirate=asp_rate
        if dis_rate:
            pipette.flow_rate.dispense=dis_rate
        if pipette._has_tip == False:
            pipette.pick_up_tip()

        pipette.aspirate(volume, src)
        protocol.delay(seconds=delay_second[0])
        if top_delay:
            pipette.move_to(src.top(z=-3))
            protocol.delay(seconds=top_delay[0])
        pipette.dispense(volume, dest)
        protocol.delay(seconds=delay_second[1])
        pipette.dispense(1, dest.top(z=-3))
        if type(mix_after) == list:
            try:
                pipette.flow_rate.aspirate=mix_after[2]
                pipette.flow_rate.dispense=mix_after[2]
            except:
                pass
            pipette.mix(mix_after[0], mix_after[1])
        if top_delay:
            pipette.move_to(src.top(z=-3))
            protocol.delay(seconds=top_delay[1])
        if drop_tip:
            pipette.drop_tip()

    ## Transfer
    if module_thermocycler.lid_position == 'close':
        module_thermocycler.open_lid()


    ### DW Transfer
    tip_count = 0
    for i1 in range(len(well_data)):
        if tip_count == 3:
            p20_sin.drop_tip()
            tip_count = 0
        data = well_data[f'well{{i1+1}}']['meta']
        dest = assemble_plate.wells()[i1]
        src = DW
        vol = float(data['DW'])

        enzyme_transfer(p20_sin, vol, src, dest,
                        asp_rate=5, dis_rate=5, drop_tip=False)
        tip_count += 1

    p20_sin.drop_tip()

    ### Part Transfer
    for i1 in range(len(well_data)):
        data = well_data.get(f'well{{i1+1}}')
        dest = assemble_plate.wells()[i1]

        for i2 in range(len(data)-1):
            tmp = data.get(f'part{{i2+1}}')
            vol = float(tmp['vol'])

            src = eval(tmp['plate']).wells_by_name()[tmp['well']]
            enzyme_transfer(p20_sin, vol, src, dest,
                            asp_rate = 5, dis_rate =5, drop_tip=True)
        
        """
        #DW transfer
        tmp = data['meta']
        src = DW
        vol = float(tmp['DW'])
        
        enzyme_transfer(p20_sin, vol, src, dest,
                        asp_rate=5, dis_rate=5, drop_tip=True)
        """
    ## Thermocycling

    if RUN_THERMO:
        module_thermocycler.set_lid_temperature(90)
        
        profile = [{{'temperature': 37, 'hold_time_minutes':1}},
                {{'temperature': 16, 'hold_time_minutes': 1}}]

        module_thermocycler.execute_profile(steps=profile, repetitions=30, block_max_volume=20)
        module_thermocycler.deactivate_lid()
        module_thermocycler.set_block_temperature(4, hold_time_minutes=5)

        protocol.pause("Protocol END \nIf you close this message, thermocycler open and deactivate.")
        module_thermocycler.deactivate()
        module_thermocycler.open_lid()
    
    else:
        protocol.comment('Protocol END.')
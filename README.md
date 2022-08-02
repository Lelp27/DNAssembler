# DNA assembly builder (dasbuilder) with OT2

DNA part assembly with OT2 liquid handler.  
It makes a protocol for assemble DNA parts on 96-well plate.  
Also, can run the thermocycler involved in OT2.  


## Deck Position

The Deck positon can change with assemble_template.py file
![Deck_position](/OT2_assembler-deck.png){height="12px" width="12px"}

## Usage

### DB & Input format

In database, set the "Plate-name", "Well-position", "Labels", "Name".  
Input "_" separated Label strings ex) "P1_R23_T12"  
Now it support only xlsx.  

    1. Set the Part labels into assembly_input.xlsx.  
    2. Run the assembly_writer.py with below command.  
    3. Run the output protocol.py with OT2.

``` python
python assembly_writer -i {input} -r {db} -t {template.py} -o {output_path}
```

## DB architecture

> Colume : Part number, target volume 
> * All data should be separated with underbar ('_').

|DNA|Volume|
|---|---|
|v1_p12_r23_t2|3_1.2_2.1_1.5|
|p1_r5_t7|2_3_1|
|r12_t21|5_3|

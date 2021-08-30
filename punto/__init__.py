"""
Compartmentalize:

 [ ascii art input ]
   ---------------
| maybe some        | 
| sort of auxillary |
| drawing program   |
       |
       |
      \ /
       v     
 [ lex/parser ] --> [ translater ]  
   ---------          ----------
  | grammar |      | notes literals|
                   | to numerical  |
                   | patterns with |
                   | timestamps    |
                   | and midi meta |
                   | data          |
                            |
   ,------------------------'
  |
   `--> [ sequencer ]   
         -----------
       | do the     | 
       | sequencing |
       | duh        |

            |
            | 
           \ /
            v
       [ midi sender ]
         ----------
      | communicate to |
      | midi external  |                      

"""

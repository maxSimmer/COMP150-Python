      LOD #4    ; n = 4  # high level for comparison        
      STO n                     
      LOD #0    ; sum = 0         
      STO sum                     
LOOP: LOD n     ; while n != 0:   
      JMZ DONE                   
      ADD sum   ;     sum += n      
      STO sum                       
      LOD n     ;     n -= 1     
      SUB #1                   
      STO n                      
      JMP LOOP                    
                   
DONE: LOD sum   ; # for easy display - result in accumulator                   
      HLT                        

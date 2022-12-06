; while example 2 with alternate condition n >= 0

      LOD #4    ; n = 4  # high level for comparison        
      STO n                     
      LOD #0    ; sum = 0         
      STO sum                     
LOOP: CPL n     ; while n >= 0: ; only inequality is CPL n, tests n < 0
      NOT       ;                but that is backwards: so use NOT command
      JMZ DONE                  ; rest is the same
      LOD n
      ADD sum   ;     sum += n      
      STO sum                       
      LOD n     ;     n -= 1     
      SUB #1                   
      STO n                      
      JMP LOOP                    
                   
DONE: LOD sum   ; # for easy display - result in accumulator                   
      HLT                        

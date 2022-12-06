      ; a simple if-else construction for

      ; if x != 0
      ;    y=2  
      ; else:
      ;    y=3  
      ; x=5  


      LOD x       ; if x != 0
      JMZ ELSE
      LOD #2      ;    y=2  if-true clause
      STO y
      JMP PAST    ; else:
ELSE: LOD #3      ;    y=3  if-false clause
      STO y
PAST: LOD #5      ; x=5  past if-else statement
      STO x     

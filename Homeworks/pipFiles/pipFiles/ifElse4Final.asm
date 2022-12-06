; ifElse 4: final version

      LOD x       ; if x == 0 same as if NOT (x != 0):
      NOT         ; 
      JMZ ELSE
      LOD #3      ;     y=3  if-true clause
      STO y
      JMP PAST    ; else:
ELSE: LOD #5      ;     y=5  if-false clause
      STO y
PAST: LOD z      ; z=z+y  past if-else statement
      ADD y
      STO z
      HLT

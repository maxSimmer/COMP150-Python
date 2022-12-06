      ; if x < 0:
      ;    x = -x  ( = -1*x)

      CPL x
      JMZ PAST
      LOD #-1  ; x = -1*x
      MUL x
      STO x
PAST: HLT
      
      


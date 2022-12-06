; if z < 0:   ; only inequality is with CPL:  must use it
;     z = z + 10
; else:
;     y = 5
; z = z + y
      
      ; initialize y, z by hand in the simulator!
      CPL z       ; if z < 0  set ACC to true (1)
      JMZ ELSE    ; if acc == 0 (false) jump to ELSE
      LOD #10     ; acc = 10 (part if true)
      ADD z       ; acc = acc + z (= z + 10)
      STO z       ; z = acc  (so z = z + 10)
      JMP PAST    ; (avoid else part)
ELSE: LOD #5      ; acc = 5 (part if false) 
      STO y       ; y = acc  (so y = 5)
PAST: LOD z       ; acc = z
      ADD y       ; acc = acc + y (= z+y)
      STO z       ; z = acc (=z+y)
      HLT

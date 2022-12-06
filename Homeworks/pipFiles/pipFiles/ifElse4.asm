; skeleton for:

; if  condition:
;   block1
; else:
;   block2
; linesPastIf

; if x == 0:   ; From example 3, LOD x provides test x != 0 ; want x == 0
;      y = 3
; else:
;      y = 5
; z = z+y

      LOD x   ; Want test  x == 0: reverse of x != 0  How reverse?  NOT
      NOT     ; ... may take several instructions!
      JMZ ELSE  ; if the condition is false, skip block1 to the ELSE label
      LOD #3  ; block1 y = 3 translated
      STO y ; ... how ever many instructions
      JMP PAST  ; skipping the else part
ELSE: LOD #5   ; start block2 y = 5 translation on THIS labeled line
      STO y    ; ... how ever many instructions
PAST: LOD y   ;  start linesPastIf z = z+y translation on THIS labeled line
      ADD z   ;  ... how ever many instructions
      STO z
      HLT


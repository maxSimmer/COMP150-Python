; The new part here is the inequality test not with 0:  rewrite
; if y > x: ; only can compare to 0!  so rewrite:  0 > x - y
;    x = x*2     ; rest is like others
; else:
;    y = y*2
; z = x + y
      
      ; initialize x, y by hand in the simulator!
      LOD x       ; if y > x   ; same as 0 > x - y
      SUB y       ; acc = x-y
      STO temp    ; temp = x-y  ; CPL requires a memory variable
      CPL temp    ; if temp < 0: acc = 1 else: acc = 0
                  ; if x-y < 0: ...
      JMZ ELSE    ; if acc == 0 jump to ELSE
                  ; if not x-y < 0 jump to ELSE
      LOD x       ; acc = x (part if true)
      MUL #2      ; acc = acc*2 (=x*2)
      STO x       ; x = acc  (so x = x*2)
      JMP PAST    ; (avoid else part)
ELSE: LOD y       ; acc = y (part if false) 
      MUL #2      ; acc = acc*2 (=y*2)
      STO y       ; y = acc  (so y = y*2)
PAST: LOD x       ; acc = x
      ADD y       ; acc = acc + y (= x+y)
      STO z       ; z = acc (=x+y)
      HLT

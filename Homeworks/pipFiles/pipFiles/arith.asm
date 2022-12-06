           ; arith.asm
  LOD #7   ; acc = 7   initialize variables
  STO W    ; W = acc  
  LOD #3   ; acc = 3
  STO X    ; X = acc  
  LOD #6   ; acc = 8
  STO Y    ; Y = acc
 
           ; Z = (W + X) * Y / 2
  LOD W    ; acc = W        # set X, Y in simulator first
  ADD X    ; acc = acc + X (= W+X)         
  MUL Y    ; acc = acc * Y (= (W+X)*Y)    
  DIV #2   ; acc = acc/2  (= (W+X)*Y/2)              
  STO Z    ; Z = acc  (= (W+X)*Y/2)
  HLT                        

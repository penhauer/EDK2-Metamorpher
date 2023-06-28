
  jmp start
start:
  instr1 
  jmp l1
l3:
  instr4
  jmp l4
l1:
  jmp l2
l2:
  instr2 
  instr3
  jmp l3
l4:
  instr5
  jmp end
end:


  jmp start
l3:
  instr5
  jmp end
l2:
  instr3
  jmp l3
l1:
  instr2 
  jmp l2
start:
  instr1 
  jmp l1
  instr4
end:

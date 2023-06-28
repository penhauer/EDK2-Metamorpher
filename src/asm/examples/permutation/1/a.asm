
  jmp start
l1:
  instr3
  jmp l2
l3:
  instr5
  jmp end
start:
  instr1 
  instr2 
  jmp l1
l2:
  instr4
  jmp l3
end:


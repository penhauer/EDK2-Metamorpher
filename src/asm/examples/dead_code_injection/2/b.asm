# Transformed Code
PrintPciExtendedCapabilityDetails:
	endbr64
	movzwl	(%rsi), %r9d
	leal	-1(%r9), %eax

# Start of Junk Code
  pushq   %rax
  pushq   %rdx
  movl	{register}, %eax
  addl	$1, %eax
  imull	{register}, %eax
  cltd
  shrl	$31, %edx
  addl	%edx, %eax
  andl	$1, %eax
  subl	%edx, %eax
  cmpl	$1, %eax
  jne	loc
  jmp PrintPciExtendedCapabilityDetails
loc:
  popq    %rdx
  popq    %rax
# End of Junk Code

	cmpw	$24, %ax
	ja	.L319
	leaq	.L321(%rip), %rcx
	movzwl	%ax, %eax
	pushq %rdi
	popq %r8
	pushq %rsi
	popq %rdi
	movslq	(%rcx,%rax,4), %rax
	addq	%rcx, %rax
	notrack jmp	*%rax

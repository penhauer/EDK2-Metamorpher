# Original Code
PrintPciExtendedCapabilityDetails:
	endbr64
	movzwl	(%rsi), %r9d
	leal	-1(%r9), %eax
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


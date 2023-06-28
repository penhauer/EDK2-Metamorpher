# Transformed Code
	movb	34(%rbx), %r9b
	orl	$-1, %edx
	orl	$-1, %ecx
	leaq	.LC120(%rip), %r8
	xorl $-1, %r9d
	orl $4294967295, %r9d

  # Start of Junk Code
  push %eax
  pop %eax
	xorl	$-1, %edx
	xorl	$-1, %edx
  # End of Junk Code

	xorl $-1, %r9d
	call	ShellPrintEx
	movb	34(%rbx), %r9b
	orl	$-1, %edx
	orl	$-1, %ecx
	leaq	.LC121(%rip), %r8
	shrb	%r9b


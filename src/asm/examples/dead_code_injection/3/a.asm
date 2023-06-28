# Original Code
	movb	34(%rbx), %r9b
	orl	$-1, %edx
	orl	$-1, %ecx
	leaq	.LC120(%rip), %r8
	xorl $-1, %r9d
	orl $4294967295, %r9d
	xorl $-1, %r9d
	call	ShellPrintEx
	movb	34(%rbx), %r9b
	orl	$-1, %edx
	orl	$-1, %ecx
	leaq	.LC121(%rip), %r8
	shrb	%r9b


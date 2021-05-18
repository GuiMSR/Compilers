	.text
	.file	"test2.ll"
	.globl	Object__print                   # -- Begin function Object__print
	.p2align	4, 0x90
	.type	Object__print,@function
Object__print:                          # @Object__print
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	movl	$.str, %edi
	xorl	%eax, %eax
	callq	printf
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end0:
	.size	Object__print, .Lfunc_end0-Object__print
	.cfi_endproc
                                        # -- End function
	.globl	Object__printBool               # -- Begin function Object__printBool
	.p2align	4, 0x90
	.type	Object__printBool,@function
Object__printBool:                      # @Object__printBool
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	movl	$.str.1, %ecx
	movl	$.str.2, %eax
	testl	%esi, %esi
	cmovneq	%rcx, %rax
	movl	$.str, %edi
	movq	%rax, %rsi
	xorl	%eax, %eax
	callq	printf
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end1:
	.size	Object__printBool, .Lfunc_end1-Object__printBool
	.cfi_endproc
                                        # -- End function
	.globl	Object__printInt32              # -- Begin function Object__printInt32
	.p2align	4, 0x90
	.type	Object__printInt32,@function
Object__printInt32:                     # @Object__printInt32
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	movl	$.str.3, %edi
	xorl	%eax, %eax
	callq	printf
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end2:
	.size	Object__printInt32, .Lfunc_end2-Object__printInt32
	.cfi_endproc
                                        # -- End function
	.globl	Object__inputLine               # -- Begin function Object__inputLine
	.p2align	4, 0x90
	.type	Object__inputLine,@function
Object__inputLine:                      # @Object__inputLine
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$is_eol, %edi
	callq	read_until
	testq	%rax, %rax
	je	.LBB3_1
# %bb.2:
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.LBB3_1:
	.cfi_def_cfa_offset 16
	movl	$.str.4, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end3:
	.size	Object__inputLine, .Lfunc_end3-Object__inputLine
	.cfi_endproc
                                        # -- End function
	.globl	Object__inputBool               # -- Begin function Object__inputBool
	.p2align	4, 0x90
	.type	Object__inputBool,@function
Object__inputBool:                      # @Object__inputBool
	.cfi_startproc
# %bb.0:
	pushq	%r14
	.cfi_def_cfa_offset 16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	pushq	%rax
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -24
	.cfi_offset %r14, -16
	movl	$isspace, %edi
	callq	skip_while
	movl	$isspace, %edi
	callq	read_until
	testq	%rax, %rax
	je	.LBB4_8
# %bb.1:
	movq	%rax, %r14
	movq	%rax, %rdi
	callq	strlen
	movq	%rax, %rbx
	cmpq	$4, %rax
	jne	.LBB4_4
# %bb.2:
	movl	$.str.1, %esi
	movl	$4, %edx
	movq	%r14, %rdi
	callq	strncmp
	testl	%eax, %eax
	je	.LBB4_3
.LBB4_4:
	cmpq	$5, %rbx
	jne	.LBB4_9
# %bb.5:
	movl	$.str.2, %esi
	movl	$5, %edx
	movq	%r14, %rdi
	callq	strncmp
	testl	%eax, %eax
	jne	.LBB4_9
# %bb.6:
	movq	%r14, %rdi
	callq	free
	xorl	%eax, %eax
.LBB4_7:
                                        # kill: def $al killed $al killed $eax
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%r14
	.cfi_def_cfa_offset 8
	retq
.LBB4_3:
	.cfi_def_cfa_offset 32
	movq	%r14, %rdi
	callq	free
	movb	$1, %al
	jmp	.LBB4_7
.LBB4_9:
	movq	stderr(%rip), %rdi
	movl	$.str.6, %esi
	movq	%r14, %rdx
	xorl	%eax, %eax
	callq	fprintf
	movq	%r14, %rdi
	callq	free
	movl	$1, %edi
	callq	exit
.LBB4_8:
	movq	stderr(%rip), %rdi
	movl	$.str.5, %esi
	xorl	%eax, %eax
	callq	fprintf
	movl	$1, %edi
	callq	exit
.Lfunc_end4:
	.size	Object__inputBool, .Lfunc_end4-Object__inputBool
	.cfi_endproc
                                        # -- End function
	.globl	Object__inputInt32              # -- Begin function Object__inputInt32
	.p2align	4, 0x90
	.type	Object__inputInt32,@function
Object__inputInt32:                     # @Object__inputInt32
	.cfi_startproc
# %bb.0:
	pushq	%rbx
	.cfi_def_cfa_offset 16
	subq	$16, %rsp
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -16
	movl	$isspace, %edi
	callq	skip_while
	movl	$isspace, %edi
	callq	read_until
	testq	%rax, %rax
	je	.LBB5_20
# %bb.1:
	movq	%rax, %rbx
	movq	%rax, %rdi
	callq	strlen
	cmpq	$3, %rax
	jb	.LBB5_4
# %bb.2:
	cmpb	$48, (%rbx)
	jne	.LBB5_4
# %bb.3:
	movb	$1, %cl
	cmpb	$120, 1(%rbx)
	je	.LBB5_12
.LBB5_4:
	cmpq	$4, %rax
	jb	.LBB5_11
# %bb.5:
	cmpb	$43, (%rbx)
	je	.LBB5_7
# %bb.6:
	cmpb	$45, (%rbx)
	jne	.LBB5_11
.LBB5_7:
	cmpb	$48, 1(%rbx)
	jne	.LBB5_11
# %bb.8:
	cmpb	$120, 2(%rbx)
	sete	%cl
	jmp	.LBB5_12
.LBB5_11:
	xorl	%ecx, %ecx
.LBB5_12:
	leaq	8(%rsp), %rsi
	movq	%rbx, %rdi
	testb	%cl, %cl
	je	.LBB5_14
# %bb.13:
	movl	$16, %edx
	jmp	.LBB5_15
.LBB5_14:
	movl	$10, %edx
.LBB5_15:
	callq	strtoll
	movq	8(%rsp), %rcx
	cmpb	$0, (%rcx)
	jne	.LBB5_21
# %bb.16:
	cmpq	$-2147483648, %rax              # imm = 0x80000000
	jl	.LBB5_19
# %bb.17:
	movl	$2147483648, %ecx               # imm = 0x80000000
	cmpq	%rcx, %rax
	jge	.LBB5_19
# %bb.18:
                                        # kill: def $eax killed $eax killed $rax
	addq	$16, %rsp
	.cfi_def_cfa_offset 16
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.LBB5_19:
	.cfi_def_cfa_offset 32
	movq	stderr(%rip), %rdi
	movl	$.str.9, %esi
	jmp	.LBB5_22
.LBB5_20:
	movq	stderr(%rip), %rdi
	movl	$.str.7, %esi
	xorl	%eax, %eax
	callq	fprintf
	movl	$1, %edi
	callq	exit
.LBB5_21:
	movq	stderr(%rip), %rdi
	movl	$.str.8, %esi
.LBB5_22:
	movq	%rbx, %rdx
	xorl	%eax, %eax
	callq	fprintf
	movl	$1, %edi
	callq	exit
.Lfunc_end5:
	.size	Object__inputInt32, .Lfunc_end5-Object__inputInt32
	.cfi_endproc
                                        # -- End function
	.globl	Object___new                    # -- Begin function Object___new
	.p2align	4, 0x90
	.type	Object___new,@function
Object___new:                           # @Object___new
	.cfi_startproc
# %bb.0:
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$8, %edi
	callq	malloc
	movq	%rax, %rdi
	callq	Object___init
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end6:
	.size	Object___new, .Lfunc_end6-Object___new
	.cfi_endproc
                                        # -- End function
	.globl	Object___init                   # -- Begin function Object___init
	.p2align	4, 0x90
	.type	Object___init,@function
Object___init:                          # @Object___init
	.cfi_startproc
# %bb.0:
	movq	%rdi, %rax
	testq	%rdi, %rdi
	je	.LBB7_2
# %bb.1:
	movq	$Object___vtable, (%rax)
.LBB7_2:
	retq
.Lfunc_end7:
	.size	Object___init, .Lfunc_end7-Object___init
	.cfi_endproc
                                        # -- End function
	.p2align	4, 0x90                         # -- Begin function read_until
	.type	read_until,@function
read_until:                             # @read_until
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%r15
	.cfi_def_cfa_offset 24
	pushq	%r14
	.cfi_def_cfa_offset 32
	pushq	%r12
	.cfi_def_cfa_offset 40
	pushq	%rbx
	.cfi_def_cfa_offset 48
	.cfi_offset %rbx, -48
	.cfi_offset %r12, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	.cfi_offset %rbp, -16
	movq	%rdi, %r14
	movl	$1024, %r15d                    # imm = 0x400
	movl	$1024, %edi                     # imm = 0x400
	callq	malloc
	movq	%rax, %r12
	xorl	%ebx, %ebx
	jmp	.LBB8_1
	.p2align	4, 0x90
.LBB8_11:                               #   in Loop: Header=BB8_1 Depth=1
	incq	%rbx
.LBB8_1:                                # =>This Inner Loop Header: Depth=1
	testq	%r12, %r12
	je	.LBB8_2
# %bb.3:                                #   in Loop: Header=BB8_1 Depth=1
	movq	stdin(%rip), %rdi
	callq	getc
	movl	%eax, %ebp
	cmpl	$-1, %eax
	je	.LBB8_5
# %bb.4:                                #   in Loop: Header=BB8_1 Depth=1
	movsbl	%bpl, %edi
	callq	*%r14
	testl	%eax, %eax
	jne	.LBB8_5
# %bb.9:                                #   in Loop: Header=BB8_1 Depth=1
	movb	%bpl, (%r12,%rbx)
	leaq	-1(%r15), %rax
	cmpq	%rax, %rbx
	jne	.LBB8_11
# %bb.10:                               #   in Loop: Header=BB8_1 Depth=1
	addq	%r15, %r15
	movq	%r12, %rdi
	movq	%r15, %rsi
	callq	realloc
	movq	%rax, %r12
	jmp	.LBB8_11
.LBB8_5:
	cmpl	$-1, %ebp
	je	.LBB8_7
# %bb.6:
	movq	stdin(%rip), %rsi
	movl	%ebp, %edi
	callq	ungetc
.LBB8_7:
	movb	$0, (%r12,%rbx)
	jmp	.LBB8_8
.LBB8_2:
	xorl	%r12d, %r12d
.LBB8_8:
	movq	%r12, %rax
	popq	%rbx
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r14
	.cfi_def_cfa_offset 24
	popq	%r15
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end8:
	.size	read_until, .Lfunc_end8-read_until
	.cfi_endproc
                                        # -- End function
	.p2align	4, 0x90                         # -- Begin function is_eol
	.type	is_eol,@function
is_eol:                                 # @is_eol
	.cfi_startproc
# %bb.0:
	xorl	%eax, %eax
	cmpl	$10, %edi
	sete	%al
	retq
.Lfunc_end9:
	.size	is_eol, .Lfunc_end9-is_eol
	.cfi_endproc
                                        # -- End function
	.p2align	4, 0x90                         # -- Begin function skip_while
	.type	skip_while,@function
skip_while:                             # @skip_while
	.cfi_startproc
# %bb.0:
	pushq	%rbp
	.cfi_def_cfa_offset 16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	pushq	%rax
	.cfi_def_cfa_offset 32
	.cfi_offset %rbx, -24
	.cfi_offset %rbp, -16
	movq	%rdi, %rbx
	jmp	.LBB10_1
	.p2align	4, 0x90
.LBB10_3:                               #   in Loop: Header=BB10_1 Depth=1
	movl	%ebp, %edi
	callq	*%rbx
	testl	%eax, %eax
	setne	%al
	testb	%al, %al
	je	.LBB10_5
.LBB10_1:                               # =>This Inner Loop Header: Depth=1
	movq	stdin(%rip), %rdi
	callq	getc
	movl	%eax, %ebp
	cmpl	$-1, %eax
	jne	.LBB10_3
# %bb.2:                                #   in Loop: Header=BB10_1 Depth=1
	xorl	%eax, %eax
	testb	%al, %al
	jne	.LBB10_1
.LBB10_5:
	cmpl	$-1, %ebp
	je	.LBB10_7
# %bb.6:
	movq	stdin(%rip), %rsi
	movl	%ebp, %edi
	callq	ungetc
.LBB10_7:
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end10:
	.size	skip_while, .Lfunc_end10-skip_while
	.cfi_endproc
                                        # -- End function
	.globl	Main__guessN                    # -- Begin function Main__guessN
	.p2align	4, 0x90
	.type	Main__guessN,@function
Main__guessN:                           # @Main__guessN
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%r13
	pushq	%r12
	pushq	%rbx
	subq	$40, %rsp
	.cfi_offset %rbx, -56
	.cfi_offset %r12, -48
	.cfi_offset %r13, -40
	.cfi_offset %r14, -32
	.cfi_offset %r15, -24
	movq	%rdi, -48(%rbp)
	movq	(%rdi), %rax
	movl	$string, %esi
	callq	*(%rax)
	movq	(%rax), %rcx
	movq	-48(%rbp), %rdx
	movl	8(%rdx), %esi
	movq	%rax, %rdi
	callq	*16(%rcx)
	movq	(%rax), %rcx
	movl	$string.1, %esi
	movq	%rax, %rdi
	callq	*(%rcx)
	movb	$1, %al
	testb	%al, %al
	jne	.LBB11_3
# %bb.1:                                # %.3.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.2, %esi
	callq	*(%rax)
	jmp	.LBB11_2
.LBB11_3:                               # %.3.else
	movq	%rsp, %rbx
	addq	$-16, %rbx
	movq	%rbx, %rsp
	movq	-48(%rbp), %rax
	cmpl	$100, 8(%rax)
	jbe	.LBB11_4
# %bb.12:                               # %.3.else.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.3, %esi
	callq	*(%rax)
	jmp	.LBB11_13
.LBB11_4:                               # %.3.else.else
	movq	%rsp, %r14
	addq	$-16, %r14
	movq	%r14, %rsp
	movq	-48(%rbp), %rax
	cmpl	$50, 8(%rax)
	jae	.LBB11_14
# %bb.5:                                # %.3.else.else.if
	movq	%rsp, %r15
	addq	$-16, %r15
	movq	%r15, %rsp
	movq	-48(%rbp), %rax
	cmpl	$25, 8(%rax)
	jae	.LBB11_16
# %bb.6:                                # %.3.else.else.if.if
	movq	%rsp, %r12
	addq	$-16, %r12
	movq	%r12, %rsp
	movq	-48(%rbp), %rax
	cmpl	$12, 8(%rax)
	jae	.LBB11_18
# %bb.7:                                # %.3.else.else.if.if.if
	movq	%rsp, %r13
	addq	$-16, %r13
	movq	%r13, %rsp
	movq	-48(%rbp), %rax
	cmpl	$6, 8(%rax)
	jae	.LBB11_30
# %bb.8:                                # %.3.else.else.if.if.if.if
	movq	%rsp, %rcx
	addq	$-16, %rcx
	movq	%rcx, %rsp
	movq	-48(%rbp), %rax
	cmpl	$3, 8(%rax)
	movq	%rcx, -72(%rbp)                 # 8-byte Spill
	movq	%rsp, %rdx
	jae	.LBB11_25
# %bb.9:                                # %.3.else.else.if.if.if.if.if
	addq	$-16, %rdx
	movq	%rdx, %rsp
	movq	-48(%rbp), %rax
	cmpl	$2, 8(%rax)
	movq	%rdx, -64(%rbp)                 # 8-byte Spill
	jae	.LBB11_20
# %bb.10:                               # %.3.else.else.if.if.if.if.if.if
	movq	%rsp, %rax
	addq	$-16, %rax
	movq	%rax, -56(%rbp)                 # 8-byte Spill
	movq	%rax, %rsp
	movq	-48(%rbp), %rax
	cmpl	$0, 8(%rax)
	jne	.LBB11_23
# %bb.11:                               # %.3.else.else.if.if.if.if.if.if.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.4, %esi
	jmp	.LBB11_24
.LBB11_14:                              # %.3.else.else.else
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.18, %esi
	callq	*(%rax)
	jmp	.LBB11_15
.LBB11_16:                              # %.3.else.else.if.else
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.17, %esi
	callq	*(%rax)
	jmp	.LBB11_17
.LBB11_18:                              # %.3.else.else.if.if.else
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.16, %esi
	callq	*(%rax)
	jmp	.LBB11_19
.LBB11_30:                              # %.3.else.else.if.if.if.else
	movq	%rsp, %rcx
	addq	$-16, %rcx
	movq	%rcx, %rsp
	movq	-48(%rbp), %rax
	cmpl	$9, 8(%rax)
	movq	%rcx, -72(%rbp)                 # 8-byte Spill
	movq	%rsp, %rdx
	jae	.LBB11_31
# %bb.33:                               # %.3.else.else.if.if.if.else.if
	addq	$-16, %rdx
	movq	%rdx, %rsp
	movq	-48(%rbp), %rax
	cmpl	$7, 8(%rax)
	movq	%rdx, -64(%rbp)                 # 8-byte Spill
	jae	.LBB11_34
# %bb.36:                               # %.3.else.else.if.if.if.else.if.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.10, %esi
	jmp	.LBB11_21
.LBB11_25:                              # %.3.else.else.if.if.if.if.else
	addq	$-16, %rdx
	movq	%rdx, %rsp
	movq	-48(%rbp), %rax
	cmpl	$4, 8(%rax)
	movq	%rdx, -64(%rbp)                 # 8-byte Spill
	jae	.LBB11_26
# %bb.28:                               # %.3.else.else.if.if.if.if.else.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.7, %esi
	jmp	.LBB11_21
.LBB11_31:                              # %.3.else.else.if.if.if.else.else
	addq	$-16, %rdx
	movq	%rdx, %rsp
	movq	-48(%rbp), %rax
	cmpl	$10, 8(%rax)
	movq	%rdx, -64(%rbp)                 # 8-byte Spill
	jae	.LBB11_39
# %bb.32:                               # %.3.else.else.if.if.if.else.else.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.13, %esi
	jmp	.LBB11_21
.LBB11_20:                              # %.3.else.else.if.if.if.if.if.else
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.6, %esi
.LBB11_21:                              # %.3.else.else.if.if.if.if.if.endif
	callq	*(%rax)
	movq	-64(%rbp), %rdx                 # 8-byte Reload
	movq	-72(%rbp), %rcx                 # 8-byte Reload
	movq	%rax, (%rdx)
	jmp	.LBB11_22
.LBB11_34:                              # %.3.else.else.if.if.if.else.if.else
	movq	%rsp, %rax
	addq	$-16, %rax
	movq	%rax, -56(%rbp)                 # 8-byte Spill
	movq	%rax, %rsp
	movq	-48(%rbp), %rax
	cmpl	$8, 8(%rax)
	jae	.LBB11_37
# %bb.35:                               # %.3.else.else.if.if.if.else.if.else.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.11, %esi
	jmp	.LBB11_24
.LBB11_26:                              # %.3.else.else.if.if.if.if.else.else
	movq	%rsp, %rax
	addq	$-16, %rax
	movq	%rax, -56(%rbp)                 # 8-byte Spill
	movq	%rax, %rsp
	movq	-48(%rbp), %rax
	cmpl	$5, 8(%rax)
	jae	.LBB11_29
# %bb.27:                               # %.3.else.else.if.if.if.if.else.else.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.8, %esi
	jmp	.LBB11_24
.LBB11_39:                              # %.3.else.else.if.if.if.else.else.else
	movq	%rsp, %rax
	addq	$-16, %rax
	movq	%rax, -56(%rbp)                 # 8-byte Spill
	movq	%rax, %rsp
	movq	-48(%rbp), %rax
	cmpl	$11, 8(%rax)
	jae	.LBB11_40
# %bb.38:                               # %.3.else.else.if.if.if.else.else.else.if
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.14, %esi
	jmp	.LBB11_24
.LBB11_23:                              # %.3.else.else.if.if.if.if.if.if.else
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.5, %esi
	jmp	.LBB11_24
.LBB11_37:                              # %.3.else.else.if.if.if.else.if.else.else
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.12, %esi
	jmp	.LBB11_24
.LBB11_29:                              # %.3.else.else.if.if.if.if.else.else.else
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.9, %esi
	jmp	.LBB11_24
.LBB11_40:                              # %.3.else.else.if.if.if.else.else.else.else
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.15, %esi
.LBB11_24:                              # %.3.else.else.if.if.if.if.if.if.endif
	callq	*(%rax)
	movq	-56(%rbp), %rcx                 # 8-byte Reload
	movq	%rax, (%rcx)
	movq	%rcx, %rax
	movq	(%rcx), %rax
	movq	-64(%rbp), %rdx                 # 8-byte Reload
	movq	%rax, (%rdx)
	movq	-72(%rbp), %rcx                 # 8-byte Reload
.LBB11_22:                              # %.3.else.else.if.if.if.if.if.endif
	movq	(%rdx), %rax
	movq	%rax, (%rcx)
	movq	(%rcx), %rax
	movq	%rax, (%r13)
	movq	(%r13), %rax
.LBB11_19:                              # %.3.else.else.if.if.endif
	movq	%rax, (%r12)
	movq	(%r12), %rax
.LBB11_17:                              # %.3.else.else.if.endif
	movq	%rax, (%r15)
	movq	(%r15), %rax
.LBB11_15:                              # %.3.else.else.endif
	movq	%rax, (%r14)
	movq	(%r14), %rax
.LBB11_13:                              # %.3.else.endif
	movq	%rax, (%rbx)
	movq	(%rbx), %rax
.LBB11_2:                               # %.3.endif
	movq	%rax, -80(%rbp)
	movq	-48(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.19, %esi
	callq	*(%rax)
	xorl	%eax, %eax
	leaq	-40(%rbp), %rsp
	popq	%rbx
	popq	%r12
	popq	%r13
	popq	%r14
	popq	%r15
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end11:
	.size	Main__guessN, .Lfunc_end11-Main__guessN
	.cfi_endproc
                                        # -- End function
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rax
	.cfi_def_cfa_offset 16
	callq	Main___new
	movq	%rax, (%rsp)
	movq	(%rax), %rcx
	movq	%rax, %rdi
	callq	*48(%rcx)
	movq	(%rsp), %rax
	movl	$1, 8(%rax)
	movq	(%rsp), %rdi
	movq	(%rdi), %rax
	callq	*48(%rax)
	movq	(%rsp), %rax
	movl	$2, 8(%rax)
	movq	(%rsp), %rdi
	movq	(%rdi), %rax
	callq	*48(%rax)
	movq	(%rsp), %rax
	movl	$4, 8(%rax)
	movq	(%rsp), %rdi
	movq	(%rdi), %rax
	callq	*48(%rax)
	movq	(%rsp), %rax
	movl	$8, 8(%rax)
	movq	(%rsp), %rdi
	movq	(%rdi), %rax
	callq	*48(%rax)
	movq	(%rsp), %rax
	movl	$16, 8(%rax)
	movq	(%rsp), %rdi
	movq	(%rdi), %rax
	callq	*48(%rax)
	movq	(%rsp), %rax
	movl	$32, 8(%rax)
	movq	(%rsp), %rdi
	movq	(%rdi), %rax
	callq	*48(%rax)
	movq	(%rsp), %rax
	movl	$64, 8(%rax)
	movq	(%rsp), %rdi
	movq	(%rdi), %rax
	callq	*48(%rax)
	movq	(%rsp), %rax
	movl	$128, 8(%rax)
	movq	(%rsp), %rdi
	movq	(%rdi), %rax
	callq	*48(%rax)
	xorl	%eax, %eax
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end12:
	.size	main, .Lfunc_end12-main
	.cfi_endproc
                                        # -- End function
	.globl	Main___new                      # -- Begin function Main___new
	.p2align	4, 0x90
	.type	Main___new,@function
Main___new:                             # @Main___new
	.cfi_startproc
# %bb.0:                                # %.2
	pushq	%rax
	.cfi_def_cfa_offset 16
	movl	$16, %edi
	callq	malloc
	movq	%rax, %rdi
	callq	Main___init
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end13:
	.size	Main___new, .Lfunc_end13-Main___new
	.cfi_endproc
                                        # -- End function
	.globl	Main___init                     # -- Begin function Main___init
	.p2align	4, 0x90
	.type	Main___init,@function
Main___init:                            # @Main___init
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset %rbx, -16
	movq	%rdi, %rbx
	testq	%rdi, %rdi
	je	.LBB14_2
# %bb.1:                                # %.3.if
	movq	%rbx, %rdi
	callq	Object___init
	movq	$MainVT, (%rbx)
	movl	$0, 8(%rbx)
.LBB14_2:                               # %.3.endif
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end14:
	.size	Main___init, .Lfunc_end14-Main___init
	.cfi_endproc
                                        # -- End function
	.type	.str,@object                    # @.str
	.section	.rodata,"a",@progbits
	.globl	.str
.str:
	.asciz	"%s"
	.size	.str, 3

	.type	.str.1,@object                  # @.str.1
	.globl	.str.1
.str.1:
	.asciz	"true"
	.size	.str.1, 5

	.type	.str.2,@object                  # @.str.2
	.globl	.str.2
.str.2:
	.asciz	"false"
	.size	.str.2, 6

	.type	.str.3,@object                  # @.str.3
	.globl	.str.3
.str.3:
	.asciz	"%d"
	.size	.str.3, 3

	.type	.str.4,@object                  # @.str.4
	.globl	.str.4
.str.4:
	.zero	1
	.size	.str.4, 1

	.type	.str.5,@object                  # @.str.5
	.globl	.str.5
	.p2align	4
.str.5:
	.asciz	"Object::inputBool: cannot read word!\n"
	.size	.str.5, 38

	.type	.str.6,@object                  # @.str.6
	.globl	.str.6
	.p2align	4
.str.6:
	.asciz	"Object::inputBool: `%s` is not a valid boolean!\n"
	.size	.str.6, 49

	.type	.str.7,@object                  # @.str.7
	.globl	.str.7
	.p2align	4
.str.7:
	.asciz	"Object::inputInt32: cannot read word!\n"
	.size	.str.7, 39

	.type	.str.8,@object                  # @.str.8
	.globl	.str.8
	.p2align	4
.str.8:
	.asciz	"Object::inputInt32: `%s` is not a valid integer literal!\n"
	.size	.str.8, 58

	.type	.str.9,@object                  # @.str.9
	.globl	.str.9
	.p2align	4
.str.9:
	.asciz	"Object::inputInt32: `%s` does not fit a 32-bit integer!\n"
	.size	.str.9, 57

	.type	Object___vtable,@object         # @Object___vtable
	.globl	Object___vtable
	.p2align	4
Object___vtable:
	.quad	Object__print
	.quad	Object__printBool
	.quad	Object__printInt32
	.quad	Object__inputLine
	.quad	Object__inputBool
	.quad	Object__inputInt32
	.size	Object___vtable, 48

	.type	MainVT,@object                  # @MainVT
	.globl	MainVT
	.p2align	4
MainVT:
	.quad	Object__print
	.quad	Object__printBool
	.quad	Object__printInt32
	.quad	Object__inputLine
	.quad	Object__inputBool
	.quad	Object__inputInt32
	.quad	Main__guessN
	.quad	main
	.size	MainVT, 64

	.type	string,@object                  # @string
	.globl	string
string:
	.asciz	"n = "
	.size	string, 5

	.type	string.1,@object                # @string.1
	.globl	string.1
string.1:
	.asciz	", guess is "
	.size	string.1, 12

	.type	string.2,@object                # @string.2
	.globl	string.2
string.2:
	.asciz	"n < 0"
	.size	string.2, 6

	.type	string.3,@object                # @string.3
	.globl	string.3
string.3:
	.asciz	"n > 100"
	.size	string.3, 8

	.type	string.4,@object                # @string.4
	.globl	string.4
string.4:
	.asciz	"n = 0"
	.size	string.4, 6

	.type	string.5,@object                # @string.5
	.globl	string.5
string.5:
	.asciz	"n = 1"
	.size	string.5, 6

	.type	string.6,@object                # @string.6
	.globl	string.6
string.6:
	.asciz	"n = 2"
	.size	string.6, 6

	.type	string.7,@object                # @string.7
	.globl	string.7
string.7:
	.asciz	"n = 3"
	.size	string.7, 6

	.type	string.8,@object                # @string.8
	.globl	string.8
string.8:
	.asciz	"n = 4"
	.size	string.8, 6

	.type	string.9,@object                # @string.9
	.globl	string.9
string.9:
	.asciz	"n = 5"
	.size	string.9, 6

	.type	string.10,@object               # @string.10
	.globl	string.10
string.10:
	.asciz	"n = 6"
	.size	string.10, 6

	.type	string.11,@object               # @string.11
	.globl	string.11
string.11:
	.asciz	"n = 7"
	.size	string.11, 6

	.type	string.12,@object               # @string.12
	.globl	string.12
string.12:
	.asciz	"n = 8"
	.size	string.12, 6

	.type	string.13,@object               # @string.13
	.globl	string.13
string.13:
	.asciz	"n = 9"
	.size	string.13, 6

	.type	string.14,@object               # @string.14
	.globl	string.14
string.14:
	.asciz	"n = 10"
	.size	string.14, 7

	.type	string.15,@object               # @string.15
	.globl	string.15
string.15:
	.asciz	"n = 11"
	.size	string.15, 7

	.type	string.16,@object               # @string.16
	.globl	string.16
string.16:
	.asciz	"12 <= n < 25"
	.size	string.16, 13

	.type	string.17,@object               # @string.17
	.globl	string.17
string.17:
	.asciz	"25 <= n < 50"
	.size	string.17, 13

	.type	string.18,@object               # @string.18
	.globl	string.18
string.18:
	.asciz	"50 <= n <= 100"
	.size	string.18, 15

	.type	string.19,@object               # @string.19
	.globl	string.19
string.19:
	.asciz	"\n"
	.size	string.19, 2

	.section	".note.GNU-stack","",@progbits

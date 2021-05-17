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
	.globl	main                            # -- Begin function main
	.p2align	4, 0x90
	.type	main,@function
main:                                   # @main
	.cfi_startproc
# %bb.0:                                # %.3
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$16, %rsp
	.cfi_offset %rbx, -32
	.cfi_offset %r14, -24
	callq	Main___new
	movq	%rax, -24(%rbp)
	xorl	%eax, %eax
	testb	%al, %al
	je	.LBB11_1
# %bb.2:                                # %.3.else
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.1, %esi
	jmp	.LBB11_3
.LBB11_1:                               # %.3.if
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string, %esi
.LBB11_3:                               # %.3.endif
	callq	*(%rax)
	movq	%rax, -32(%rbp)
	movq	%rsp, %rbx
	addq	$-16, %rbx
	movq	%rbx, %rsp
	movq	-24(%rbp), %r14
	callq	Main___new
	cmpq	%rax, %r14
	je	.LBB11_4
# %bb.5:                                # %.3.endif.else
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.3, %esi
	jmp	.LBB11_6
.LBB11_4:                               # %.3.endif.if
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.2, %esi
.LBB11_6:                               # %.3.endif.endif
	callq	*(%rax)
	movq	%rax, (%rbx)
	movq	%rsp, %rax
	leaq	-16(%rax), %r14
	movq	%r14, %rsp
	movq	$0, -16(%rax)
	movq	%rsp, %rbx
	addq	$-16, %rbx
	movq	%rbx, %rsp
	movq	-16(%rax), %rax
	cmpq	-24(%rbp), %rax
	je	.LBB11_7
# %bb.8:                                # %.3.endif.endif.else
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.5, %esi
	jmp	.LBB11_9
.LBB11_7:                               # %.3.endif.endif.if
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.4, %esi
.LBB11_9:                               # %.3.endif.endif.endif
	callq	*(%rax)
	movq	%rax, (%rbx)
	movq	%rsp, %rbx
	addq	$-16, %rbx
	movq	%rbx, %rsp
	movq	-24(%rbp), %rax
	cmpq	(%r14), %rax
	je	.LBB11_10
# %bb.11:                               # %.3.endif.endif.endif.else
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.7, %esi
	jmp	.LBB11_12
.LBB11_10:                              # %.3.endif.endif.endif.if
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.6, %esi
.LBB11_12:                              # %.3.endif.endif.endif.endif
	callq	*(%rax)
	movq	%rax, (%rbx)
	movq	-24(%rbp), %rax
	movq	%rax, (%r14)
	movq	%rsp, %rbx
	addq	$-16, %rbx
	movq	%rbx, %rsp
	movq	(%r14), %rax
	cmpq	-24(%rbp), %rax
	je	.LBB11_13
# %bb.14:                               # %.3.endif.endif.endif.endif.else
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.9, %esi
	jmp	.LBB11_15
.LBB11_13:                              # %.3.endif.endif.endif.endif.if
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.8, %esi
.LBB11_15:                              # %.3.endif.endif.endif.endif.endif
	callq	*(%rax)
	movq	%rax, (%rbx)
	movq	%rsp, %rbx
	addq	$-16, %rbx
	movq	%rbx, %rsp
	movq	-24(%rbp), %rax
	cmpq	(%r14), %rax
	je	.LBB11_16
# %bb.17:                               # %.3.endif.endif.endif.endif.endif.else
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.11, %esi
	jmp	.LBB11_18
.LBB11_16:                              # %.3.endif.endif.endif.endif.endif.if
	movq	-24(%rbp), %rdi
	movq	(%rdi), %rax
	movl	$string.10, %esi
.LBB11_18:                              # %.3.endif.endif.endif.endif.endif.endif
	callq	*(%rax)
	movq	%rax, (%rbx)
	xorl	%eax, %eax
	leaq	-16(%rbp), %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	.cfi_def_cfa %rsp, 8
	retq
.Lfunc_end11:
	.size	main, .Lfunc_end11-main
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
	movl	$8, %edi
	callq	malloc
	movq	%rax, %rdi
	callq	Main___init
	popq	%rcx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end12:
	.size	Main___new, .Lfunc_end12-Main___new
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
	je	.LBB13_2
# %bb.1:                                # %.3.if
	movq	%rbx, %rdi
	callq	Object___init
	movq	$Main_vtable, (%rbx)
.LBB13_2:                               # %.3.endif
	movq	%rbx, %rax
	popq	%rbx
	.cfi_def_cfa_offset 8
	retq
.Lfunc_end13:
	.size	Main___init, .Lfunc_end13-Main___init
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

	.type	Main_vtable,@object             # @Main_vtable
	.globl	Main_vtable
	.p2align	4
Main_vtable:
	.quad	Object__print
	.quad	Object__printBool
	.quad	Object__printInt32
	.quad	Object__inputLine
	.quad	Object__inputBool
	.quad	Object__inputInt32
	.quad	main
	.size	Main_vtable, 56

	.type	string,@object                  # @string
	.globl	string
string:
	.asciz	"OK\n"
	.size	string, 4

	.type	string.1,@object                # @string.1
	.globl	string.1
string.1:
	.asciz	"KO\n"
	.size	string.1, 4

	.type	string.2,@object                # @string.2
	.globl	string.2
string.2:
	.asciz	"KO\n"
	.size	string.2, 4

	.type	string.3,@object                # @string.3
	.globl	string.3
string.3:
	.asciz	"OK\n"
	.size	string.3, 4

	.type	string.4,@object                # @string.4
	.globl	string.4
string.4:
	.asciz	"KO\n"
	.size	string.4, 4

	.type	string.5,@object                # @string.5
	.globl	string.5
string.5:
	.asciz	"OK\n"
	.size	string.5, 4

	.type	string.6,@object                # @string.6
	.globl	string.6
string.6:
	.asciz	"KO\n"
	.size	string.6, 4

	.type	string.7,@object                # @string.7
	.globl	string.7
string.7:
	.asciz	"OK\n"
	.size	string.7, 4

	.type	string.8,@object                # @string.8
	.globl	string.8
string.8:
	.asciz	"OK\n"
	.size	string.8, 4

	.type	string.9,@object                # @string.9
	.globl	string.9
string.9:
	.asciz	"KO\n"
	.size	string.9, 4

	.type	string.10,@object               # @string.10
	.globl	string.10
string.10:
	.asciz	"OK\n"
	.size	string.10, 4

	.type	string.11,@object               # @string.11
	.globl	string.11
string.11:
	.asciz	"KO\n"
	.size	string.11, 4

	.section	".note.GNU-stack","",@progbits

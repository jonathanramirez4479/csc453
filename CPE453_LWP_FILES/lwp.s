	.file	"lwp.c"
	.globl	WORD_SIZE
	.section	.rodata
	.align 4
	.type	WORD_SIZE, @object
	.size	WORD_SIZE, 4
WORD_SIZE:
	.long	4
	.comm	lwp_ptable,960,32
	.globl	lwp_procs
	.bss
	.align 4
	.type	lwp_procs, @object
	.size	lwp_procs, 4
lwp_procs:
	.zero	4
	.comm	current_scheduler,8,8
	.globl	pid_start
	.data
	.align 4
	.type	pid_start, @object
	.size	pid_start, 4
pid_start:
	.long	1000
	.globl	lwp_running
	.align 4
	.type	lwp_running, @object
	.size	lwp_running, 4
lwp_running:
	.long	-1
	.globl	original_sp
	.bss
	.align 8
	.type	original_sp, @object
	.size	original_sp, 8
original_sp:
	.zero	8
	.text
	.globl	new_lwp
	.type	new_lwp, @function
new_lwp:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$64, %rsp
	movq	%rdi, -40(%rbp)
	movq	%rsi, -48(%rbp)
	movq	%rdx, -56(%rbp)
	movl	lwp_procs(%rip), %eax
	cmpl	$30, %eax
	jne	.L2
	movl	$-1, %eax
	jmp	.L3
.L2:
	movl	lwp_procs(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable, %rax
	movq	%rax, -8(%rbp)
	movl	pid_start(%rip), %eax
	movslq	%eax, %rdx
	movq	-8(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rax
	movq	-56(%rbp), %rdx
	movq	%rdx, 16(%rax)
	movq	-56(%rbp), %rax
	salq	$3, %rax
	movq	%rax, %rdi
	call	malloc
	movq	%rax, %rdx
	movq	-8(%rbp), %rax
	movq	%rdx, 8(%rax)
	movl	pid_start(%rip), %eax
	addl	$1, %eax
	movl	%eax, pid_start(%rip)
	movq	-8(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, -16(%rbp)
	movq	-56(%rbp), %rax
	salq	$3, %rax
	addq	%rax, -16(%rbp)
	subq	$8, -16(%rbp)
	movq	-48(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -16(%rbp)
	movl	$exit, %edx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -16(%rbp)
	movq	-40(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	subq	$8, -16(%rbp)
	movq	-16(%rbp), %rax
	movl	$4276993775, %ecx
	movq	%rcx, (%rax)
	movq	-16(%rbp), %rax
	movq	%rax, -24(%rbp)
	subq	$56, -16(%rbp)
	movq	-24(%rbp), %rdx
	movq	-16(%rbp), %rax
	movq	%rdx, (%rax)
	movq	-8(%rbp), %rax
	movq	-16(%rbp), %rdx
	movq	%rdx, 24(%rax)
	movl	lwp_procs(%rip), %eax
	addl	$1, %eax
	movl	%eax, lwp_procs(%rip)
	movq	-8(%rbp), %rax
	movq	(%rax), %rax
.L3:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	new_lwp, .-new_lwp
	.globl	lwp_yield
	.type	lwp_yield, @function
lwp_yield:
.LFB3:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
#APP
# 72 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 72 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 72 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 72 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 72 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 72 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 72 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 72 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 72 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 72 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 72 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 72 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 72 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 72 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 72 "lwp.c" 1
	pushq %rbp
# 0 "" 2
#NO_APP
	movl	lwp_running(%rip), %edx
#APP
# 73 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movslq	%edx, %rdx
	salq	$5, %rdx
	addq	$lwp_ptable+16, %rdx
	movq	%rax, 8(%rdx)
	movq	current_scheduler(%rip), %rax
	call	*%rax
	movl	%eax, -4(%rbp)
	movl	-4(%rbp), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable+16, %rax
	movq	8(%rax), %rax
	movq	%rax, -16(%rbp)
	movq	-16(%rbp), %rax
#APP
# 78 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 79 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 79 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 79 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 79 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 79 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 79 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 79 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 79 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 79 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 79 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 79 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 79 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 79 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 79 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 79 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 79 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	lwp_yield, .-lwp_yield
	.globl	round_robin
	.type	round_robin, @function
round_robin:
.LFB4:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	lwp_running(%rip), %eax
	addl	$1, %eax
	movl	%eax, lwp_running(%rip)
	movl	lwp_running(%rip), %edx
	movl	lwp_procs(%rip), %eax
	cmpl	%eax, %edx
	jl	.L7
	movl	$0, lwp_running(%rip)
.L7:
	movl	lwp_running(%rip), %eax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	round_robin, .-round_robin
	.globl	lwp_set_scheduler
	.type	lwp_set_scheduler, @function
lwp_set_scheduler:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movq	%rdi, -8(%rbp)
	cmpq	$0, -8(%rbp)
	je	.L10
	movq	-8(%rbp), %rax
	movq	%rax, current_scheduler(%rip)
	jmp	.L9
.L10:
	movq	$round_robin, current_scheduler(%rip)
.L9:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	lwp_set_scheduler, .-lwp_set_scheduler
	.globl	lwp_start
	.type	lwp_start, @function
lwp_start:
.LFB6:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 110 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 110 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 110 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 110 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 110 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 110 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 110 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 110 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 110 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 110 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 110 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 110 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 110 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 110 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 110 "lwp.c" 1
	pushq %rbp
# 0 "" 2
# 111 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movq	%rax, original_sp(%rip)
	movq	current_scheduler(%rip), %rax
	testq	%rax, %rax
	jne	.L13
	movq	$round_robin, current_scheduler(%rip)
.L13:
	movl	lwp_procs(%rip), %eax
	testl	%eax, %eax
	jne	.L14
#APP
# 118 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 118 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 118 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 118 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	jmp	.L12
.L14:
	movq	current_scheduler(%rip), %rax
	call	*%rax
	movl	%eax, lwp_running(%rip)
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable+16, %rax
	movq	8(%rax), %rax
#APP
# 124 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 125 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 125 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 125 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 125 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 125 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 125 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 125 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 125 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 125 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 125 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 125 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 125 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 125 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 125 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 125 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 125 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	nop
.L12:
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE6:
	.size	lwp_start, .-lwp_start
	.globl	lwp_getpid
	.type	lwp_getpid, @function
lwp_getpid:
.LFB7:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable, %rax
	movq	(%rax), %rax
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE7:
	.size	lwp_getpid, .-lwp_getpid
	.globl	lwp_exit
	.type	lwp_exit, @function
lwp_exit:
.LFB8:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movl	lwp_running(%rip), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable, %rax
	movq	%rax, -16(%rbp)
	movl	lwp_running(%rip), %eax
	movl	%eax, -4(%rbp)
	movl	lwp_procs(%rip), %eax
	leal	-1(%rax), %edx
	movl	lwp_running(%rip), %eax
	cmpl	%eax, %edx
	jne	.L19
	movq	-16(%rbp), %rax
	movq	$0, (%rax)
	movq	-16(%rbp), %rax
	movq	$0, 24(%rax)
	movq	-16(%rbp), %rax
	movq	$0, 16(%rax)
	movq	-16(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, %rdi
	call	free
	movq	-16(%rbp), %rax
	movq	$0, 8(%rax)
	movq	current_scheduler(%rip), %rax
	call	*%rax
	movl	%eax, -4(%rbp)
	jmp	.L20
.L19:
	movq	-16(%rbp), %rax
	movq	$0, (%rax)
	movq	-16(%rbp), %rax
	movq	$0, 24(%rax)
	movq	-16(%rbp), %rax
	movq	$0, 16(%rax)
	movq	-16(%rbp), %rax
	movq	8(%rax), %rax
	movq	%rax, %rdi
	call	free
	movq	-16(%rbp), %rax
	movq	$0, 8(%rax)
	movl	lwp_running(%rip), %eax
	movl	%eax, -8(%rbp)
	jmp	.L21
.L22:
	movl	-8(%rbp), %eax
	leal	1(%rax), %edx
	movl	-8(%rbp), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable, %rax
	movslq	%edx, %rdx
	salq	$5, %rdx
	addq	$lwp_ptable, %rdx
	movq	(%rdx), %rcx
	movq	%rcx, (%rax)
	movq	8(%rdx), %rcx
	movq	%rcx, 8(%rax)
	movq	16(%rdx), %rcx
	movq	%rcx, 16(%rax)
	movq	24(%rdx), %rdx
	movq	%rdx, 24(%rax)
	addl	$1, -8(%rbp)
.L21:
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	cmpl	-8(%rbp), %eax
	jg	.L22
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable, %rax
	movq	$0, (%rax)
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable+16, %rax
	movq	$0, 8(%rax)
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable, %rax
	movq	$0, 8(%rax)
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable+16, %rax
	movq	$0, (%rax)
	movq	current_scheduler(%rip), %rax
	cmpq	$round_robin, %rax
	je	.L20
	movq	current_scheduler(%rip), %rax
	call	*%rax
	movl	%eax, lwp_running(%rip)
.L20:
	movl	lwp_procs(%rip), %eax
	subl	$1, %eax
	movl	%eax, lwp_procs(%rip)
	movl	lwp_procs(%rip), %eax
	testl	%eax, %eax
	jne	.L23
	movq	original_sp(%rip), %rax
#APP
# 181 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 182 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 182 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 182 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 182 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 182 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 182 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 182 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 182 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 182 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 182 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 182 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 182 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 182 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 182 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 182 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 182 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	jmp	.L18
.L23:
	movl	-4(%rbp), %eax
	cltq
	salq	$5, %rax
	addq	$lwp_ptable+16, %rax
	movq	8(%rax), %rax
	movq	%rax, -24(%rbp)
	movq	-24(%rbp), %rax
#APP
# 189 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 190 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 190 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 190 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 190 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 190 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 190 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 190 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 190 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 190 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 190 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 190 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 190 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 190 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 190 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 190 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 190 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	nop
.L18:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE8:
	.size	lwp_exit, .-lwp_exit
	.globl	lwp_stop
	.type	lwp_stop, @function
lwp_stop:
.LFB9:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
#APP
# 197 "lwp.c" 1
	pushq %rax
# 0 "" 2
# 197 "lwp.c" 1
	pushq %rbx
# 0 "" 2
# 197 "lwp.c" 1
	pushq %rcx
# 0 "" 2
# 197 "lwp.c" 1
	pushq %rdx
# 0 "" 2
# 197 "lwp.c" 1
	pushq %rsi
# 0 "" 2
# 197 "lwp.c" 1
	pushq %rdi
# 0 "" 2
# 197 "lwp.c" 1
	pushq %r8
# 0 "" 2
# 197 "lwp.c" 1
	pushq %r9
# 0 "" 2
# 197 "lwp.c" 1
	pushq %r10
# 0 "" 2
# 197 "lwp.c" 1
	pushq %r11
# 0 "" 2
# 197 "lwp.c" 1
	pushq %r12
# 0 "" 2
# 197 "lwp.c" 1
	pushq %r13
# 0 "" 2
# 197 "lwp.c" 1
	pushq %r14
# 0 "" 2
# 197 "lwp.c" 1
	pushq %r15
# 0 "" 2
# 197 "lwp.c" 1
	pushq %rbp
# 0 "" 2
#NO_APP
	movl	lwp_running(%rip), %edx
#APP
# 198 "lwp.c" 1
	movq  %rsp,%rax
# 0 "" 2
#NO_APP
	movslq	%edx, %rdx
	salq	$5, %rdx
	addq	$lwp_ptable+16, %rdx
	movq	%rax, 8(%rdx)
	movq	original_sp(%rip), %rax
#APP
# 199 "lwp.c" 1
	movq  %rax,%rsp
# 0 "" 2
# 200 "lwp.c" 1
	popq  %rbp
# 0 "" 2
# 200 "lwp.c" 1
	popq  %r15
# 0 "" 2
# 200 "lwp.c" 1
	popq  %r14
# 0 "" 2
# 200 "lwp.c" 1
	popq  %r13
# 0 "" 2
# 200 "lwp.c" 1
	popq  %r12
# 0 "" 2
# 200 "lwp.c" 1
	popq  %r11
# 0 "" 2
# 200 "lwp.c" 1
	popq  %r10
# 0 "" 2
# 200 "lwp.c" 1
	popq  %r9
# 0 "" 2
# 200 "lwp.c" 1
	popq  %r8
# 0 "" 2
# 200 "lwp.c" 1
	popq  %rdi
# 0 "" 2
# 200 "lwp.c" 1
	popq  %rsi
# 0 "" 2
# 200 "lwp.c" 1
	popq  %rdx
# 0 "" 2
# 200 "lwp.c" 1
	popq  %rcx
# 0 "" 2
# 200 "lwp.c" 1
	popq  %rbx
# 0 "" 2
# 200 "lwp.c" 1
	popq  %rax
# 0 "" 2
# 200 "lwp.c" 1
	movq  %rbp,%rsp
# 0 "" 2
#NO_APP
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE9:
	.size	lwp_stop, .-lwp_stop
	.ident	"GCC: (GNU) 4.8.5 20150623 (Red Hat 4.8.5-44)"
	.section	.note.GNU-stack,"",@progbits

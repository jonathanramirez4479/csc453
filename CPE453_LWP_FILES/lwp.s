	.file	"lwp.c"
	.text
.Ltext0:
	.globl	WORD_SIZE
	.section	.rodata
	.align 4
	.type	WORD_SIZE, @object
	.size	WORD_SIZE, 4
WORD_SIZE:
	.long	4
	.comm	lwp_ptable,480,32
	.globl	lwp_procs
	.bss
	.align 4
	.type	lwp_procs, @object
	.size	lwp_procs, 4
lwp_procs:
	.zero	4
	.text
	.globl	new_lwp
	.type	new_lwp, @function
new_lwp:
.LFB2:
	.file 1 "lwp.c"
	.loc 1 10 0
	.cfi_startproc
	pushl	%ebp
	.cfi_def_cfa_offset 8
	.cfi_offset 5, -8
	movl	%esp, %ebp
	.cfi_def_cfa_register 5
	subl	$40, %esp
	.loc 1 20 0
	movl	lwp_procs, %eax
	cmpl	$30, %eax
	jne	.L2
	.loc 1 22 0
	movl	$-1, %eax
	jmp	.L3
.L2:
	.loc 1 29 0
	movl	$0, -16(%ebp)
	jmp	.L4
.L7:
	.loc 1 30 0
	movl	-16(%ebp), %eax
	sall	$4, %eax
	addl	$lwp_ptable+4, %eax
	movl	(%eax), %eax
	testl	%eax, %eax
	jne	.L5
	.loc 1 32 0
	movl	-16(%ebp), %eax
	movl	%eax, -12(%ebp)
	.loc 1 33 0
	jmp	.L6
.L5:
	.loc 1 29 0
	addl	$1, -16(%ebp)
.L4:
	.loc 1 29 0 is_stmt 0 discriminator 1
	cmpl	$30, -16(%ebp)
	jle	.L7
.L6:
	.loc 1 36 0 is_stmt 1
	movl	-12(%ebp), %eax
	addl	$1, %eax
	movl	-12(%ebp), %edx
	sall	$4, %edx
	addl	$lwp_ptable, %edx
	movl	%eax, (%edx)
	.loc 1 37 0
	movl	-12(%ebp), %eax
	sall	$4, %eax
	leal	lwp_ptable+8(%eax), %edx
	movl	16(%ebp), %eax
	movl	%eax, (%edx)
	.loc 1 39 0
	movl	$4, %eax
	imull	16(%ebp), %eax
	movl	%eax, (%esp)
	call	malloc
	movl	-12(%ebp), %edx
	sall	$4, %edx
	addl	$lwp_ptable+4, %edx
	movl	%eax, (%edx)
	.loc 1 41 0
	movl	-12(%ebp), %eax
	sall	$4, %eax
	addl	$lwp_ptable+4, %eax
	movl	(%eax), %eax
	movl	%eax, -20(%ebp)
	.loc 1 42 0
	movl	-12(%ebp), %eax
	sall	$4, %eax
	leal	lwp_ptable+12(%eax), %edx
	movl	-20(%ebp), %eax
	movl	%eax, (%edx)
	.loc 1 43 0
	movl	$4, %eax
	imull	16(%ebp), %eax
	sall	$2, %eax
	addl	%eax, -20(%ebp)
	.loc 1 45 0
	movl	12(%ebp), %edx
	movl	-20(%ebp), %eax
	movl	%edx, (%eax)
	.loc 1 46 0
	subl	$4, -20(%ebp)
	.loc 1 48 0
	movl	$exit, %edx
	movl	-20(%ebp), %eax
	movl	%edx, (%eax)
	.loc 1 49 0
	subl	$4, -20(%ebp)
	.loc 1 51 0
	movl	8(%ebp), %edx
	movl	-20(%ebp), %eax
	movl	%edx, (%eax)
	.loc 1 52 0
	subl	$4, -20(%ebp)
	.loc 1 54 0
	movl	-20(%ebp), %eax
	movl	$-17973521, (%eax)
	.loc 1 56 0
	movl	-20(%ebp), %eax
	movl	%eax, -24(%ebp)
	.loc 1 57 0
	subl	$28, -20(%ebp)
	.loc 1 59 0
	movl	-24(%ebp), %edx
	movl	-20(%ebp), %eax
	movl	%edx, (%eax)
	.loc 1 61 0
	movl	lwp_procs, %eax
	addl	$1, %eax
	movl	%eax, lwp_procs
	.loc 1 63 0
	movl	-12(%ebp), %eax
	sall	$4, %eax
	addl	$lwp_ptable, %eax
	movl	(%eax), %eax
.L3:
	.loc 1 65 0
	leave
	.cfi_restore 5
	.cfi_def_cfa 4, 4
	ret
	.cfi_endproc
.LFE2:
	.size	new_lwp, .-new_lwp
.Letext0:
	.file 2 "/usr/lib/gcc/x86_64-redhat-linux/4.8.5/include/stddef.h"
	.file 3 "lwp.h"
	.section	.debug_info,"",@progbits
.Ldebug_info0:
	.long	0x1b7
	.value	0x4
	.long	.Ldebug_abbrev0
	.byte	0x4
	.uleb128 0x1
	.long	.LASF23
	.byte	0x1
	.long	.LASF24
	.long	.LASF25
	.long	.Ltext0
	.long	.Letext0-.Ltext0
	.long	.Ldebug_line0
	.uleb128 0x2
	.long	.LASF11
	.byte	0x2
	.byte	0xd4
	.long	0x30
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.long	.LASF0
	.uleb128 0x3
	.byte	0x1
	.byte	0x8
	.long	.LASF1
	.uleb128 0x3
	.byte	0x2
	.byte	0x7
	.long	.LASF2
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.long	.LASF3
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.long	.LASF4
	.uleb128 0x3
	.byte	0x2
	.byte	0x5
	.long	.LASF5
	.uleb128 0x4
	.byte	0x4
	.byte	0x5
	.string	"int"
	.uleb128 0x3
	.byte	0x8
	.byte	0x5
	.long	.LASF6
	.uleb128 0x3
	.byte	0x8
	.byte	0x7
	.long	.LASF7
	.uleb128 0x3
	.byte	0x4
	.byte	0x5
	.long	.LASF8
	.uleb128 0x3
	.byte	0x4
	.byte	0x7
	.long	.LASF9
	.uleb128 0x5
	.byte	0x4
	.uleb128 0x3
	.byte	0x1
	.byte	0x6
	.long	.LASF10
	.uleb128 0x2
	.long	.LASF12
	.byte	0x3
	.byte	0x6
	.long	0x45
	.uleb128 0x6
	.long	.LASF26
	.byte	0x10
	.byte	0x3
	.byte	0x11
	.long	0xcd
	.uleb128 0x7
	.string	"pid"
	.byte	0x3
	.byte	0x13
	.long	0x45
	.byte	0
	.uleb128 0x8
	.long	.LASF13
	.byte	0x3
	.byte	0x14
	.long	0xcd
	.byte	0x4
	.uleb128 0x8
	.long	.LASF14
	.byte	0x3
	.byte	0x15
	.long	0x45
	.byte	0x8
	.uleb128 0x7
	.string	"sp"
	.byte	0x3
	.byte	0x16
	.long	0xcd
	.byte	0xc
	.byte	0
	.uleb128 0x9
	.byte	0x4
	.long	0x86
	.uleb128 0x2
	.long	.LASF15
	.byte	0x3
	.byte	0x18
	.long	0x91
	.uleb128 0x2
	.long	.LASF16
	.byte	0x3
	.byte	0x29
	.long	0xe9
	.uleb128 0x9
	.byte	0x4
	.long	0xef
	.uleb128 0xa
	.long	0xfa
	.uleb128 0xb
	.long	0x7d
	.byte	0
	.uleb128 0xc
	.long	.LASF27
	.byte	0x1
	.byte	0x9
	.long	0x5a
	.long	.LFB2
	.long	.LFE2-.LFB2
	.uleb128 0x1
	.byte	0x9c
	.long	0x172
	.uleb128 0xd
	.long	.LASF17
	.byte	0x1
	.byte	0x9
	.long	0xde
	.uleb128 0x2
	.byte	0x91
	.sleb128 0
	.uleb128 0xe
	.string	"arg"
	.byte	0x1
	.byte	0x9
	.long	0x7d
	.uleb128 0x2
	.byte	0x91
	.sleb128 4
	.uleb128 0xd
	.long	.LASF18
	.byte	0x1
	.byte	0x9
	.long	0x25
	.uleb128 0x2
	.byte	0x91
	.sleb128 8
	.uleb128 0xf
	.long	.LASF19
	.byte	0x1
	.byte	0x19
	.long	0x5a
	.uleb128 0x2
	.byte	0x91
	.sleb128 -20
	.uleb128 0x10
	.string	"i"
	.byte	0x1
	.byte	0x1a
	.long	0x5a
	.uleb128 0x2
	.byte	0x91
	.sleb128 -24
	.uleb128 0x10
	.string	"sp"
	.byte	0x1
	.byte	0x29
	.long	0xcd
	.uleb128 0x2
	.byte	0x91
	.sleb128 -28
	.uleb128 0x10
	.string	"bp"
	.byte	0x1
	.byte	0x38
	.long	0xcd
	.uleb128 0x2
	.byte	0x91
	.sleb128 -32
	.byte	0
	.uleb128 0x11
	.long	0xd3
	.long	0x182
	.uleb128 0x12
	.long	0x76
	.byte	0x1d
	.byte	0
	.uleb128 0x13
	.long	.LASF20
	.byte	0x1
	.byte	0x6
	.long	0x172
	.uleb128 0x5
	.byte	0x3
	.long	lwp_ptable
	.uleb128 0x13
	.long	.LASF21
	.byte	0x1
	.byte	0x7
	.long	0x5a
	.uleb128 0x5
	.byte	0x3
	.long	lwp_procs
	.uleb128 0x13
	.long	.LASF22
	.byte	0x1
	.byte	0x5
	.long	0x1b5
	.uleb128 0x5
	.byte	0x3
	.long	WORD_SIZE
	.uleb128 0x14
	.long	0x30
	.byte	0
	.section	.debug_abbrev,"",@progbits
.Ldebug_abbrev0:
	.uleb128 0x1
	.uleb128 0x11
	.byte	0x1
	.uleb128 0x25
	.uleb128 0xe
	.uleb128 0x13
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x1b
	.uleb128 0xe
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x6
	.uleb128 0x10
	.uleb128 0x17
	.byte	0
	.byte	0
	.uleb128 0x2
	.uleb128 0x16
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x3
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0xe
	.byte	0
	.byte	0
	.uleb128 0x4
	.uleb128 0x24
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3e
	.uleb128 0xb
	.uleb128 0x3
	.uleb128 0x8
	.byte	0
	.byte	0
	.uleb128 0x5
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x6
	.uleb128 0x13
	.byte	0x1
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x7
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x8
	.uleb128 0xd
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x38
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x9
	.uleb128 0xf
	.byte	0
	.uleb128 0xb
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xa
	.uleb128 0x15
	.byte	0x1
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xb
	.uleb128 0x5
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xc
	.uleb128 0x2e
	.byte	0x1
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x27
	.uleb128 0x19
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x11
	.uleb128 0x1
	.uleb128 0x12
	.uleb128 0x6
	.uleb128 0x40
	.uleb128 0x18
	.uleb128 0x2116
	.uleb128 0x19
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0xd
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0xe
	.uleb128 0x5
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0xf
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x10
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0x8
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x11
	.uleb128 0x1
	.byte	0x1
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x1
	.uleb128 0x13
	.byte	0
	.byte	0
	.uleb128 0x12
	.uleb128 0x21
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x2f
	.uleb128 0xb
	.byte	0
	.byte	0
	.uleb128 0x13
	.uleb128 0x34
	.byte	0
	.uleb128 0x3
	.uleb128 0xe
	.uleb128 0x3a
	.uleb128 0xb
	.uleb128 0x3b
	.uleb128 0xb
	.uleb128 0x49
	.uleb128 0x13
	.uleb128 0x3f
	.uleb128 0x19
	.uleb128 0x2
	.uleb128 0x18
	.byte	0
	.byte	0
	.uleb128 0x14
	.uleb128 0x26
	.byte	0
	.uleb128 0x49
	.uleb128 0x13
	.byte	0
	.byte	0
	.byte	0
	.section	.debug_aranges,"",@progbits
	.long	0x1c
	.value	0x2
	.long	.Ldebug_info0
	.byte	0x4
	.byte	0
	.value	0
	.value	0
	.long	.Ltext0
	.long	.Letext0-.Ltext0
	.long	0
	.long	0
	.section	.debug_line,"",@progbits
.Ldebug_line0:
	.section	.debug_str,"MS",@progbits,1
.LASF16:
	.string	"lwpfun"
.LASF27:
	.string	"new_lwp"
.LASF11:
	.string	"size_t"
.LASF13:
	.string	"stack"
.LASF21:
	.string	"lwp_procs"
.LASF1:
	.string	"unsigned char"
.LASF3:
	.string	"long unsigned int"
.LASF15:
	.string	"lwp_context"
.LASF2:
	.string	"short unsigned int"
.LASF24:
	.string	"lwp.c"
.LASF26:
	.string	"context_st"
.LASF17:
	.string	"func"
.LASF25:
	.string	"//home/jrami245/csc453/git_csc453/CPE453_LWP_FILES"
.LASF19:
	.string	"free_thread_index"
.LASF22:
	.string	"WORD_SIZE"
.LASF12:
	.string	"ptr_int_t"
.LASF0:
	.string	"unsigned int"
.LASF7:
	.string	"long long unsigned int"
.LASF9:
	.string	"sizetype"
.LASF6:
	.string	"long long int"
.LASF18:
	.string	"stack_size"
.LASF10:
	.string	"char"
.LASF5:
	.string	"short int"
.LASF14:
	.string	"stacksize"
.LASF20:
	.string	"lwp_ptable"
.LASF23:
	.string	"GNU C 4.8.5 20150623 (Red Hat 4.8.5-44) -m32 -mtune=generic -march=x86-64 -g"
.LASF8:
	.string	"long int"
.LASF4:
	.string	"signed char"
	.ident	"GCC: (GNU) 4.8.5 20150623 (Red Hat 4.8.5-44)"
	.section	.note.GNU-stack,"",@progbits

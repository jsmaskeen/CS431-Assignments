extern unsigned long long g_600ff8;

void _init(void)
{
    if (!g_600ff8)
        return;
    __gmon_start__(); /* do not return */
}

extern unsigned long long g_601008;
extern unsigned long long g_601010;

void sub_400670(void)
{
    unsigned long v0;  // [bp-0x8]

    v0 = g_601008;
    goto g_601010;
}

void _start(unsigned long a0, unsigned long a1, unsigned long long a2)
{
    unsigned long v3;  // rax
    unsigned long v0;  // [bp+0x0]
    unsigned long long v1;  // [bp+0x0]
    unsigned long v2;  // [bp+0x8]

    v0 = v3;
    __libc_start_main(main, v1, &v2, __libc_csu_init, __libc_csu_fini, a2, &v1, v3); /* do not return */
}

void sub_400749(void)
{
    [D] Unsupported jumpkind Ijk_SigTRAP at address 4196169()
}

void deregister_tm_clones(void)
{
    return;
}

void register_tm_clones(void)
{
    return;
}

extern char completed.7594;

void __do_global_dtors_aux(void)
{
    if (!completed.7594)
    {
        deregister_tm_clones();
        completed.7594 = 1;
    }
    return;
}

extern unsigned long long __JCR_END__;

void frame_dummy(void)
{
    unsigned long long *v1;  // rdi

    v1 = &__JCR_END__;
    if (__JCR_END__)
    {
        register_tm_clones();
        return;
    }
    register_tm_clones();
    return;
}

int display_number(unsigned int a0, unsigned int a1)
{
    // a0 is 15, a1 is 20
    unsigned int v0;  // [bp-0xc]

    v0 = a0 + rand() % (a1 - a0 + 1);
    printf("%d\n", v0);
    return v0;
}

unsigned long long f(unsigned int a0)
{
    unsigned int i;  // [bp-0x14]
    unsigned long long v1;  // [bp-0x10]

    v1 = 1;
    for (i = 2; i <= a0; i += 1)
    {
        v1 *= i;
    }
    return v1;
}

long long C(unsigned int a0, unsigned int a1)
{
    unsigned long long v1;  // rax
    unsigned long long v2;  // rax

    v1 = f(a0);
    v2 = f(a1);
    return v1 / (f(a0 - a1) * v2);
}

void process(unsigned int a0)
{
    unsigned int v0;  // [bp-0x1c]
    unsigned int flag;  // [bp-0x18]
    unsigned int i;  // [bp-0x14]

    flag = 1;
    for (i = 0; i <= a0; i += 1)
    {
        __isoc99_scanf("%d", (unsigned int)&v0);
        if ((int)C(a0, i) != v0)
            flag = 0;
    }
    if (flag == 1)
        system("cat flag.txt");
    return;
}

typedef struct FILE {
} FILE;

extern FILE *stderr;
extern FILE *stdin;
extern FILE *stdout;

unsigned int main(void)
{
    unsigned int v0;  // [bp-0x14]
    unsigned int v1;  // [bp-0x10]
    unsigned int v2;  // [bp-0xc]

    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    v0 = 15;
    v1 = 20;
    srand(time(NULL));
    v2 = display_number(v0, v1);
    process(v2);
    return 0;
}

typedef struct struct_1 {
    unsigned long long field_0;
} struct_1;

typedef struct struct_0 {
    struct struct_1 *field_0;
    unsigned long long field_8;
    unsigned long long field_10;
    unsigned long long field_18;
} struct_0;

extern struct_0 __init_array_start;

void __libc_csu_init(unsigned int a0, unsigned long a1, unsigned long a2)
{
    unsigned long long flag;  // rbx

    _init();
    flag = 0;
    do
    {
        (&__init_array_start.field_0)[flag](a0, a1, a2);
        flag += 1;
    } while (flag != 1);
    return;
}

void __libc_csu_fini(void)
{
    return;
}

void _fini(void)
{
    return;
}


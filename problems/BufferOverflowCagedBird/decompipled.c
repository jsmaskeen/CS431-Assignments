extern unsigned long long g_600ff8;

void _init(void)
{
    if (g_600ff8)
        __gmon_start__();
    return;
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

void sub_400839(void)
{
    [D] Unsupported jumpkind Ijk_SigTRAP at address 4196409()
}

void deregister_tm_clones(void)
{
    return;
}

void register_tm_clones(void)
{
    return;
}

extern char completed.6982;

void __do_global_dtors_aux(void)
{
    if (!completed.6982)
    {
        deregister_tm_clones();
        completed.6982 = 1;
    }
    return;
}

extern unsigned long long __JCR_END__;

void frame_dummy(void)
{
    if (!__JCR_END__)
    {
        register_tm_clones();
        return;
    }
    register_tm_clones();
    return;
}

typedef struct FILE {
} FILE;

extern FILE *__TMC_END__;

unsigned int win(void)
{
    char v0[136];  // [bp-0x98]
    FILE *fp;  // [bp-0x10]

    fp = fopen("flag.txt", "r");
    fgets(&v0, 128, fp);
    puts(&v0);
    return fflush(__TMC_END__);
}

typedef struct FILE {
} FILE;

extern void global_canary;

void read_canary(void)
{
    FILE *fp;  // [bp-0x10]

    fp = fopen("flag.txt", "r");
    fread(&global_canary, 1, 4, fp);
    fclose(fp);
    return;
}

typedef struct FILE {
} FILE;

extern FILE *__TMC_END__;
extern void global_canary;

void vuln(void)
{
    unsigned int v0;  // [bp-0x11c]
    char v1[128];  // [bp-0x118]
    char v2;  // [bp-0x98]
    unsigned int v3;  // [bp-0x18]
    unsigned int i;  // [bp-0xc]

    i = 0;
    v3 = *((int *)&global_canary);
    puts("Go ahead, try to overflow me! I'll let you pick how many bytes to read");
                        // read one byte into v1[i]          input = \n
    for (; i <= 127 && (read(0, (long long)(int)i + &v1, 1), v1[i] != 10); i += 1);
    __isoc99_sscanf(&v1, "%d", (unsigned int)&v0);
    puts("Now enter the string\n");
    fflush(__TMC_END__);
    read(0, &v2, v0);
    if (!memcmp(&v3, &global_canary, 4))
    {
        puts("You said something");
        putchar(10);
        fflush(__TMC_END__);
        return;
    }
    puts("hacker detected!");
    exit(-1); /* do not return */
}

unsigned int main(unsigned int a0, unsigned long long a1)
{
    unsigned long long v0;  // [bp-0x28]
    unsigned int v1;  // [bp-0x1c]
    unsigned int v2;  // [bp-0xc]

    v1 = a0;
    v0 = a1;
    v2 = getegid();
    setresgid(v2, v2, v2, v2);
    read_canary();
    vuln();
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

    flag = 0;
    _init();
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


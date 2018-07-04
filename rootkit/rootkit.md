# pwnable rootkit

### 非预期

这道题据google到的解法是这样的，将open函数拆成2个系统调用`name_to_handle_at` 和 `open_by_handle_at`，静态链接编译后用base加解密传到远程主机，就可以查看flag，看到的是不可见字符，file一下发现是gzip，于是解压一下得到flag。

然而这道题如果这么解就失去了rootkit的意义。所为我觉得这是非预期解法。

### 预期解法尝试

Elf文件的程序的patch可以用sed命令。例如:
`sed -i 's/\x14\x00\x00\x00\x00\xc7/\x14\x70\x8d\x15\xc1\xc7/g' rootkit `
（有时候16进制直接加\x不行，远程的就不行，和sed的版本有关）

这里有个问题就是原来的rootkit.ko是写在init脚本里的，而且阅读rootkit.ko里的代码发现，驱动实现了模块的隐藏，`_this_module->head_list`的前驱和后继都指向了自己，所以`cat /proc/modules`和`lsmod`都找不到这个模块，`rmmod`也就无法删掉这个模块。

因为原驱动将`sys_call_table`改掉了，所以预期解法应该是把它改回来。

```c
.init.text:08000334                 mov     eax, ds:sct
.init.text:08000339                 mov     dword ptr [eax+14h], (offset sys_open_hooked-46EA74E0h)
.init.text:08000340                 mov     dword ptr [eax+49Ch], offset sys_openat_hooked
.init.text:0800034A                 mov     dword ptr [eax+14Ch], offset sys_symlink_hooked
.init.text:08000354                 mov     dword ptr [eax+4C0h], offset sys_symlinkat_hooked
.init.text:0800035E                 mov     dword ptr [eax+24h], offset sys_link_hooked
.init.text:08000365                 mov     dword ptr [eax+4BCh], offset sys_linkat_hooked
.init.text:0800036F                 mov     dword ptr [eax+98h], offset sys_rename_hooked
.init.text:08000379                 mov     dword ptr [eax+4B8h], offset sys_renameat_hooked
```

在`/porc/kallsyms`可以知道原来系统调用的地址。

patch的地方应该是在上面那段，但不了解驱动模块的加载机制。从ko文件的hex编码来看，上述所有的offset都是`\x00\x00\x00\x00`，如果patch掉这个地方的话，就会如上面所示，变成对offset 函数地址进行加减操作。但是`offset sys_open_hook` 的地址在驱动模块加载到内核之后是变化的，因此就会将系统调用表里open这个系统调用偏移处指向的函数就是一个随机的地址。这里我无论怎么patch都会panic。

所以patch rootkit.ko感觉是困难的做法。
目前能想到的做法是编译一个和远程相同版本的linux内核，写驱动将系统调用表改回来，但还没有去实践。


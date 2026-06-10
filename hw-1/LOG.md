# P0 Compiler Extension: While Loop & Function Call Architecture

This repository documents the enhancement of the P0 compiler to support `while` loop control flow and contains a detailed architectural breakdown of the execution runtime environment.

---

## 📋 Session Summary

- **Date**: 2026-04-22
- **Objective**: Implement `while` loop syntax handling into the P0 compiler and document the underlying Dynamic Stack Frame Mechanism.
- **Status**: 🟢 **Completed & Verified**

---

## 📥 Features & Requirements

1. **Syntax Extension**: Integrated `while` loop parsing into both the Lexer, Parser, and Virtual Machine (VM).
2. **Control Flow Architecture**: Implemented a **Two-Label Control Flow** model with **Backpatching (回填技術)** to handle forward references.
3. **Execution Runtime Isolation**: Explicitly documented the stack-frame allocation lifecycle enabling seamless nested and recursive function calls.

---

Implemented the while loop layout inside the statement() routine using late-bound address backpatching.
} else if (cur_token.type == TK_WHILE) {
    next_token(); // consume 'while'
    next_token(); // consume '('

    int loop_start = quad_count; // 1. Record the condition evaluation entry address
    char cond[32];
    expression(cond);            // 2. Parse condition expression
    
    next_token(); // consume ')'
    next_token(); // consume '{'
    
    int jmp_f_idx = quad_count;
    emit("JMP_F", cond, "-", "?"); // 3. Placeholder jump on condition false
    
    while (cur_token.type != TK_RBRACE)
        statement();               // 4. Recursively parse loop body statements
    next_token(); // consume '}'
    
    int jmp_idx = quad_count;
    emit("JMP", "-", "-", "?");    // 5. Generate loop-back instruction
    
    // 6. Backpatching: Resolve lazy-bound addresses
    sprintf(quads[jmp_f_idx].result, "%d", quad_count); // False branch jumps to loop exit
    sprintf(quads[jmp_idx].result, "%d", loop_start);   // Loop bottom jumps back to condition
}

000: IMM        1          -          t1
001: STORE      t1         -          i
002: IMM        0          -          t2
003: STORE      t2         -          sum
004: IMM        11         -          t3
005: CMP_LT     i          t3         t4
006: JMP_F      t4         -          013    <-- Backpatched: Jump to Exit (013)
007: ADD        sum        i          t5
008: STORE      t5         -          sum
009: IMM        1          -          t6
010: ADD        i          t6         t7
011: STORE      t7         -          i
012: JMP        -          -          004    <-- Backpatched: Loop back to Cond (004)

=== VM Execution ===
>> i = 11
>> sum = 55
🧠 Architectural Design Principles

Single-Pass Compilation via Backpatching: Because the loop exit destination address is completely unknown until the entire loop body has been traversed, the compiler emits a placeholder target ("?"). After the full body is processed, it leverages the cached quadruple indexes (jmp_f_idx, jmp_idx) to fix the target addresses in-place.

Instruction State Balance: The evaluation of the condition expression safely leaves its binary flag in a distinct temporary register (cond). The conditional operation (JMP_F) reads this token directly, ensuring that no dirty operand data leaks into the nested execution block.

The P0 architecture uses an explicit, hardware-independent Stack Frame (Activation Record) model managed by a dedicated frame tracking index (sp). The runtime lifecycle behaves through 4 segregated stages:
Caller Frame (sp)          Callee Frame (sp + 1)
┌──────────────────┐       ┌───────────────────────┐
│  PARAM arg1  ────┼──────>│ 1. incoming_args[0]   │
│  PARAM arg2  ────┼──────>│    incoming_args[1]   │
│                  │       ├───────────────────────┤
│  CALL func ──────┼──────>│ 2. Save ret_pc & var  │
│                  │       ├───────────────────────┤
│                  │       │ 3. FORMAL binds names │
│  Resume PC <─────┼───────┼─── RET_VAL returns    │
└──────────────────┘       └───────────────────────┘
PARAM (Argument Marshalling): The caller side iteratively evaluates expression bounds and stages individual arguments onto a global scratchpad buffer param_stack.

CALL (Frame Context Creation):

Increments the active frame reference stack depth pointer (sp++), generating a pristine local variable scope boundary.

Saves the return tracking pointer address (ret_pc = pc + 1) along with the target writeback tracking variable label (ret_var).

Flushes staged values from the global param_stack directly into the callee frame's dedicated incoming_args buffer array.

FORMAL (Parameter Scope Binding): As initialization routines run inside the callee prologue, the parser maps structural formal names to the data blocks extracted linearly from the local frame's incoming_args bank.

RET_VAL (Context Teardown & Return):

Evaluates the terminal expression return structure block.

Decrements the active environment depth index (sp--), immediately destroying and popping the active frame scope context.

References the recalled ret_var, re-injects the calculated return expression product into the restored active caller context space, and safely hands back control (pc = ret_pc).

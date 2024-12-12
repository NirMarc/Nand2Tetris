
public enum InstructionType {
    A_INSTRUCTION,
    C_INSTRUCTION,
    L_INSTRUCTION;

    public static InstructionType getInstructionType(String instruction) {
        if (instruction.charAt(0) == '@')
            return InstructionType.A_INSTRUCTION;
        else if (instruction.charAt(0) == '(')
            return InstructionType.L_INSTRUCTION;
        else
            return InstructionType.C_INSTRUCTION;
    }
}
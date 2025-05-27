package com.example.quadterm2_home;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class InstarctionSet {
    public List<Instruction> instructions = new ArrayList<>();

    InstarctionSet(String instarctionsLine) {
        String regex = "[;]";
        List<String> instructions = Arrays.stream(instarctionsLine.split(regex)).toList();
//        System.out.println("Set:");
//        System.out.println(instructions);
        for (String instruction : instructions) {
            Instruction instr = new Instruction(instruction);
            this.instructions.add(instr);
        }
    }

    public Instruction getInstruction(int index) {
        return this.instructions.get(index);
    }

    public int size() {
        return this.instructions.size();
    }

    public List<Instruction> getInstructions() {
        return instructions;
    }
}


package com.example.quadterm2_home;

import java.util.Arrays;
import java.util.List;

public class Instruction {
    public String instruction;
    public int argument;
    public Sign sign;

    Instruction(String instructionStr) {
        String regex = " ";
        List<String> instructionParts = Arrays.stream(instructionStr.split(regex)).toList();
        this.instruction = instructionParts.getFirst();
        String arg = instructionParts.getLast();
        if (arg.charAt(0) == '+') {
            sign = Sign.PLUS;
            argument = Integer.parseInt(arg.substring(1));
        } else if (arg.charAt(0) == '-') {
            sign = Sign.MINUS;
            argument = Integer.parseInt(arg.substring(1));
        }else {
            sign = Sign.NONE;
            argument = Integer.parseInt(arg);
        }
        System.out.println(this.instruction + " " + argument + " " + sign);
    }
}

package com.example.quadterm2_home;

import javafx.geometry.Point2D;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.paint.Color;

public class Korytnachka {
    public Point2D position = new Point2D(0, 0);
    public int angle;
    public int stepSize;
    public int color = 0;
    public long sleepTime = 0;
    public long startTime;

    private InstarctionSet instarctionSet;
    private Instruction currentInstruction;
    private int currInstrIndex = 0;

    public boolean shouldRun = true;

    Image turtleImage = new Image("file:turtle.png");
    ImageView turtleImageView = new ImageView(turtleImage);
    int turtleWidth = 30;
    int turtleHeight = 30;


    int xShift;
    int yShift;
    Korytnachky app;

    Korytnachka(InstarctionSet instarctionSet, Korytnachky app, int xShift, int yShift) {
        this.instarctionSet = instarctionSet;
        this.app = app;
        this.xShift = xShift;
        this.yShift = yShift;
    }

    public void draw() {
        turtleImageView.setX(position.getX() + xShift);
        turtleImageView.setY(position.getY() + yShift);

        turtleImageView.setFitWidth(turtleWidth);
        turtleImageView.setFitHeight(turtleHeight);

        app.pane.getChildren().add(turtleImageView);
    }

    public void updateInstruction(){
        if (!shouldRun) return;
        if (currentInstruction == null){
            currentInstruction = instarctionSet.getInstruction(currInstrIndex);
        }

        if (sleepTime > 0){
            if (startTime == 0) startTime = System.nanoTime();
            long time = (System.nanoTime() - startTime);
            if (time < sleepTime * 1_000_000L) {
                return;
            }
            startTime = 0;
        }

        switch (currentInstruction.instruction) {
            case "TURN" -> angleInstruction(currentInstruction.argument, currentInstruction.sign);
            case "STEP" -> stepSizeInstruction(currentInstruction.argument, currentInstruction.sign);
            case "COLOR" -> colorInstruction(currentInstruction.argument, currentInstruction.sign);
            case "SLEEP" -> sleepTimeInstruction(currentInstruction.argument, currentInstruction.sign);
            case "FORWARD" -> forwardInstruction(currentInstruction.argument, currentInstruction.sign);
        }
        currInstrIndex = (currInstrIndex + 1) % instarctionSet.size();
        currentInstruction = instarctionSet.getInstruction(currInstrIndex);
    }

    private void forwardInstruction(int argument, Sign sign) {
        argument = sign == Sign.MINUS ? -argument : argument;
        Point2D deltaPosition = new Point2D(stepSize * argument * Math.cos(Math.toRadians(angle)),
                                            stepSize * argument * Math.sin(Math.toRadians(angle)));
        app.drawLine(position, position.add(deltaPosition), intToColor(color));
        position = position.add(deltaPosition);
    }

    public void angleInstruction(int newAngle, Sign operation) {
        if (operation == Sign.PLUS) angle += newAngle;
        else if (operation == Sign.MINUS) angle -= newAngle;
        else if (operation == Sign.NONE) angle = newAngle;
    }

    public void stepSizeInstruction(int newStepSize, Sign operation) {
        if (operation == Sign.PLUS) stepSize += newStepSize;
        else if (operation == Sign.MINUS) stepSize -= newStepSize;
        else if (operation == Sign.NONE) stepSize = newStepSize;
    }

    public void colorInstruction(int newColor, Sign operation) {
        if (operation == Sign.PLUS) color += newColor;
        else if (operation == Sign.MINUS) color -= newColor;
        else if (operation == Sign.NONE) color = newColor;
    }

    public void sleepTimeInstruction(int newSleepTime, Sign operation) {
        if (operation == Sign.PLUS) sleepTime += newSleepTime;
        else if (operation == Sign.MINUS) sleepTime -= newSleepTime;
        else if (operation == Sign.NONE) sleepTime = newSleepTime;
    }

    private Color intToColor(int colorInt) {
        int a = (colorInt>>16) & 0xff;
        int b = (colorInt>>8) & 0xff;
        int c = colorInt & 0xff;
        return Color.rgb(colorInt>>16&0xff, colorInt>>8&0xff, colorInt&0xff);
    }
}

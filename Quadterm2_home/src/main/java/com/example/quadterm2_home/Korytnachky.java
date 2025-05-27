package com.example.quadterm2_home;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Application;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.geometry.Point2D;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.stage.Stage;
import javafx.util.Duration;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class Korytnachky extends Application {
    private static final int SIZE = 800;
    private static final String INSTRUCTIONS = "turtles2.txt";
    private static List<String> instructionBlocks = new ArrayList<>();
    private static List<InstarctionSet> instructionSets = new ArrayList<>();
    public List<Korytnachka> korytnachky = new ArrayList<>();
    public Pane pane;
    GraphicsContext gc;

    @Override
    public void start(Stage stage) {
        Canvas canvas = new Canvas(SIZE, SIZE);

        parseInstructions(INSTRUCTIONS);
        initKorytnachky();

        gc = canvas.getGraphicsContext2D();

        pane = new Pane(canvas);
        Scene scene = new Scene(pane);
        scene.setFill(Color.ORANGE);

        scene.widthProperty().addListener(observable -> canvas.setWidth(scene.getWidth()));
        scene.heightProperty().addListener(observable -> canvas.setHeight(scene.getHeight()));

        EventHandler<ActionEvent> eventHandler = e -> {
            update();
        };


        Timeline animation = new Timeline(new KeyFrame(Duration.millis(16), eventHandler));
        animation.setCycleCount(Timeline.INDEFINITE);
        animation.play();

        stage.setTitle("Korytnachky");
        stage.setScene(scene);
        stage.show();
    }

    private void parseInstructions(String fileName) {
        try {
            List<String> lines = Files.readAllLines(Paths.get(fileName));

            for (String line : lines) {
                instructionBlocks.add(line);
                instructionSets.add(new InstarctionSet(line));
            }

        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void initKorytnachky(){
        for (InstarctionSet instructionSet : instructionSets){
            Korytnachka korytnachka = new Korytnachka(instructionSet, this, SIZE / 2, SIZE / 2);
            korytnachky.add(korytnachka);
        }
    }

    public void update() {
        for (Korytnachka korytnachka : korytnachky){
            korytnachka.updateInstruction();
            pane.getChildren().remove(korytnachka.turtleImageView);
            korytnachka.draw();

        }
    }

    public void drawLine(Point2D startPoint, Point2D endPoint, Color color) {
        gc.setStroke(color);
        gc.setLineWidth(2);
        gc.strokeLine(startPoint.getX() + (double) SIZE / 2, startPoint.getY() + (double) SIZE / 2,
                endPoint.getX() + (double) SIZE / 2, endPoint.getY() + (double) SIZE / 2);
    }

}

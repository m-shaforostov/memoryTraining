package com.example.balls;

import javafx.animation.AnimationTimer;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.layout.Pane;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import javafx.scene.text.Font;
import javafx.scene.text.Text;
import javafx.stage.Stage;

import java.util.*;

public class Balls extends Application {
    @Override
    public void start(Stage stage) {
        BallsGame game = new BallsGame(800, 600);
        Scene scene = new Scene(game);
        stage.setScene(scene);
        stage.setTitle("2048 Balls");
        stage.show();

        game.startAnimation();

        // pohyb myši -> posun preview gule
        scene.setOnMouseMoved(e -> game.updatePreviewPosition(e.getX()));

        // klik -> pustenie gule a generovanie novej preview
        scene.setOnMouseClicked(e -> game.spawnBall());

//        scene.setOnKeyPressed(keyEvent -> {
//            stop();
//        });

        // (nespracované: pauza cez KeyPressed)
    }

    public static void main(String[] args) { launch(args); }
}

// Trieda hry: spravuje logiku náhľadu aj zoznam padajúcich guľí
class BallsGame extends Pane {
    private final double width, height;
    private final Map<Integer, Color> valueColor = new HashMap<>();
    private final Random rnd = new Random();

    private final double baseValue = 2;      // pre škálovanie
    private final double baseRadius = 20;    // polomer pri hodnote 2

    private int previewValue;
    private Circle previewCircle;
    private Text previewText;

    private final List<Ball> balls = new ArrayList<>();
    private AnimationTimer timer;

    public BallsGame(double w, double h) {
        this.width = w;
        this.height = h;
        setPrefSize(w, h);

        initColors();
        createPreview();
    }

    // 2ⁿ -> náhodná farba (rovnaká pre danú hodnotu)
    private void initColors() {
        for (int exp = 1; exp <= 10; exp++) {
            int val = (int)Math.pow(2, exp);
            Color c = Color.hsb(rnd.nextDouble()*360, 0.5 + rnd.nextDouble()*0.5, 0.7 + rnd.nextDouble()*0.3);
            valueColor.put(val, c);
        }
    }

    private Color getColor(int value) {
        return valueColor.get(value);
    }

    // vytvorí preview guľu s náhodnou hodnotou 2,4 alebo 8
    private void createPreview() {
        previewValue = randomValue();
        double r = computeRadius(previewValue);

        previewCircle = new Circle(r, getColor(previewValue));
        previewCircle.setStroke(Color.BLACK);

        previewText = new Text(String.valueOf(previewValue));
        previewText.setFont(Font.font(r * 0.6));
        previewText.setMouseTransparent(true);

        getChildren().addAll(previewCircle, previewText);
        updatePreviewPosition(width / 2);
    }

    // prepočítavame radiál podľa plochy ~ value
    private double computeRadius(int value) {
        return baseRadius * Math.sqrt(value / baseValue);
    }

    private int randomValue() {
        int[] opts = {2, 4, 8};
        return opts[rnd.nextInt(opts.length)];
    }

    // posunie preview guľu a text podľa X-ky myši
    public void updatePreviewPosition(double mouseX) {
        double r = previewCircle.getRadius();
        double x = Math.max(r, Math.min(width - r, mouseX));
        double y = r + 5;

        previewCircle.setCenterX(x);
        previewCircle.setCenterY(y);

        // centrovanie textu
        double textW = previewText.getLayoutBounds().getWidth();
        double textH = previewText.getLayoutBounds().getHeight();
        previewText.setX(x - textW / 2);
        previewText.setY(y + textH / 4);
    }

    // pri kliknutí: pridaj novú guľu a prepni preview
    public void spawnBall() {
        Ball b = new Ball(width,
                height,
                previewValue,
                new Vector2D(previewCircle.getCenterX(), previewCircle.getCenterY()),
                computeRadius(previewValue),
                getColor(previewValue));
        balls.add(b);
        getChildren().addAll(b.view, b.label);

        // nová preview
        getChildren().removeAll(previewCircle, previewText);
        createPreview();
    }

    // spustenie hlavnej slučky (nateraz len na prípravu budúcej fyziky)
    public void startAnimation() {
        timer = new AnimationTimer() {
            @Override
            public void handle(long now) {
                double dt = 1/60.0;  // fixný timestep na 60 FPS
//                getChildren().clear();
                for (int i = 0; i < balls.size(); i++) {
                    Ball b1 = balls.get(i);
                    for (int j = i + 1; j < balls.size(); j++) {
                        Ball b2 = balls.get(j);
                        b1.processColission(b2);
                    }
                    b1.update(dt);
                }
            }
        };
        timer.start();
    }


}

// Pomocná trieda pre každú gulu
class Ball {
    int value;
    Circle view;
    Text label;
    private final double G = 980;
    public Vector2D position = new Vector2D(0, 0);
    public Vector2D acceleration = new Vector2D(0, 980);
    public Vector2D velocity = new Vector2D(0, 0);
    public final double radius;

    private final double width, height;

    public Ball(double width, double height, int value, Vector2D position, double radius, Color color) {
        this.value = value;
        this.width = width;
        this.height = height;
        this.position = position;
        this.radius = radius;
        view = new Circle(radius, color);
        view.setStroke(Color.BLACK);
        view.setCenterX(position.x);
        view.setCenterY(position.y);

        label = new Text(String.valueOf(value));
        label.setFont(Font.font(radius * 0.6));
        label.setMouseTransparent(true);
        updateLabelPosition();
    }

    // prechodné volanie na ďalšie časti úlohy
    void update(double dt) {
        // tu neskôr pridáme gravitáciu, kolízie a odrazy
        // pre teraz iba prekreslíme text

        checkBounds();
        changePosition(dt);
        updateLabelPosition();
    }

    public void processColission(Ball otherBall) {
        if (otherBall.position.distance(position) <= otherBall.radius + radius) {
            velocity = new Vector2D(otherBall.velocity.getAdded(velocity));
            otherBall.velocity = new Vector2D(otherBall.velocity.getAdded(velocity));
        }
    }

    private void changePosition(double dt) {
        velocity.add(acceleration.getMultiplied(dt));
        position.add(velocity.getMultiplied(dt));

        view.setCenterX(position.x);
        view.setCenterY(position.y);
    }

    public void checkBounds(){

        if (position.y + view.getRadius() >= height) {
            velocity.y = -0.8 * Math.abs(velocity.y);
            position.y = Math.min(position.y , height - view.getRadius());
        }
    }

    private void updateLabelPosition() {
        double cx = view.getCenterX(), cy = view.getCenterY();
        double textW = label.getLayoutBounds().getWidth();
        double textH = label.getLayoutBounds().getHeight();
        label.setX(cx - textW/2);
        label.setY(cy + textH/4);
    }
}

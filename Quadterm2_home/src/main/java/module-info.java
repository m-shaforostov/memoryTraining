module com.example.quadterm2_home {
    requires javafx.controls;
    requires javafx.fxml;
    requires java.desktop;


    opens com.example.quadterm2_home to javafx.fxml;
    exports com.example.quadterm2_home;
}
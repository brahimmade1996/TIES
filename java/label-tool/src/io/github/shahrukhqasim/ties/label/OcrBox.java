package io.github.shahrukhqasim.ties.label;

import javafx.geometry.Rectangle2D;
import javafx.scene.paint.Color;
import javafx.scene.paint.Paint;

/**
 * Created by srq on 12.10.17.
 */
public class OcrBox extends Box {

    public OcrBox(Rectangle2D box) {
        super(box);
    }

    @Override
    public Paint getStroke() {
        if (selected)
            return Color.color(1, 0, 0);
        else
            return Color.color(0, 1, 0);
    }
}

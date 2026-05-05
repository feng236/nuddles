package noodleshop;

public class SoupNoodle extends Noodle {
    public SoupNoodle() {
        description = "汤面";
    }

    @Override
    public double cost() {
        return 7.0;
    }
}

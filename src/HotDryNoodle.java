package noodleshop;

public class HotDryNoodle extends Noodle {
    public HotDryNoodle() {
        description = "热干面";
    }

    @Override
    public double cost() {
        return 8.0;
    }
}

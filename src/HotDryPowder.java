package noodleshop;

public class HotDryPowder extends Noodle {
    public HotDryPowder() {
        description = "热干粉";
    }

    @Override
    public double cost() {
        return 8.0;
    }
}

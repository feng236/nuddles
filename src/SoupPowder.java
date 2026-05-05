package noodleshop;

public class SoupPowder extends Noodle {
    public SoupPowder() {
        description = "汤粉";
    }

    @Override
    public double cost() {
        return 7.0;
    }
}

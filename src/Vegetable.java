package noodleshop;

public class Vegetable extends ToppingDecorator {
    public Vegetable(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 时蔬";
    }

    @Override
    public double cost() {
        return noodle.cost() + 2.0;
    }
}

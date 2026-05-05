package noodleshop;

public class Chicken extends ToppingDecorator {
    public Chicken(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 鸡肉";
    }

    @Override
    public double cost() {
        return noodle.cost() + 6.0;
    }
}

package noodleshop;

public class Beef extends ToppingDecorator {
    public Beef(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 牛肉";
    }

    @Override
    public double cost() {
        return noodle.cost() + 10.0;
    }
}

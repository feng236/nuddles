package noodleshop;

public class BeefTripe extends ToppingDecorator {
    public BeefTripe(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 牛肚";
    }

    @Override
    public double cost() {
        return noodle.cost() + 9.0;
    }
}

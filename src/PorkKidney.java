package noodleshop;

public class PorkKidney extends ToppingDecorator {
    public PorkKidney(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 腰花";
    }

    @Override
    public double cost() {
        return noodle.cost() + 10.0;
    }
}

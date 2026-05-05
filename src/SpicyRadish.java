package noodleshop;

public class SpicyRadish extends ToppingDecorator {
    public SpicyRadish(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 辣萝卜丁";
    }

    @Override
    public double cost() {
        return noodle.cost() + 1.0;
    }
}

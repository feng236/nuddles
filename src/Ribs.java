package noodleshop;

public class Ribs extends ToppingDecorator {
    public Ribs(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 排骨";
    }

    @Override
    public double cost() {
        return noodle.cost() + 12.0;
    }
}

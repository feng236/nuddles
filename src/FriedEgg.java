package noodleshop;

public class FriedEgg extends ToppingDecorator {
    public FriedEgg(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 煎蛋";
    }

    @Override
    public double cost() {
        return noodle.cost() + 2.5;
    }
}

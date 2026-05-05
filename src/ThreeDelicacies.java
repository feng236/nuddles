package noodleshop;

public class ThreeDelicacies extends ToppingDecorator {
    public ThreeDelicacies(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 三鲜";
    }

    @Override
    public double cost() {
        return noodle.cost() + 8.0;
    }
}

package noodleshop;

public class SourBeans extends ToppingDecorator {
    public SourBeans(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 酸豆角";
    }

    @Override
    public double cost() {
        return noodle.cost() + 1.0;
    }
}

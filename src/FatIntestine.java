package noodleshop;

public class FatIntestine extends ToppingDecorator {
    public FatIntestine(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 肥肠";
    }

    @Override
    public double cost() {
        return noodle.cost() + 11.0;
    }
}

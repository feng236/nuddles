package noodleshop;

public class Eel extends ToppingDecorator {
    public Eel(Noodle noodle) {
        super(noodle);
    }

    @Override
    public String getDescription() {
        return noodle.getDescription() + " + 鳝鱼";
    }

    @Override
    public double cost() {
        return noodle.cost() + 13.0;
    }
}

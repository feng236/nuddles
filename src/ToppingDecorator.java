package noodleshop;

public abstract class ToppingDecorator extends Noodle {
    protected Noodle noodle;

    public ToppingDecorator(Noodle noodle) {
        this.noodle = noodle;
    }

    @Override
    public abstract String getDescription();

    @Override
    public abstract double cost();
}

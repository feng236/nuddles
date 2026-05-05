package noodleshop;

public abstract class Noodle {
    protected String description = "未知面食";

    public String getDescription() {
        return description;
    }

    public abstract double cost();
}

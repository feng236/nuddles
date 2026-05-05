package noodleshop;

public class Main {
    public static void main(String[] args) {
        Noodle order = new Beef(new Vegetable(new HotDryNoodle()));

        System.out.println("订单: " + order.getDescription());
        System.out.printf("合计: %.2f 元%n", order.cost());
    }
}

# 遥记天天见面 - 面馆点餐系统

这是一个使用装饰器模式实现的面馆点餐示例项目。项目同时包含 Python 图形界面版本和 Java 类结构版本，用来展示如何通过基础面食和配料装饰器动态组合订单，并自动计算总价。

## 功能介绍

- 支持选择面底：热干面、热干粉、汤面、汤粉
- 支持添加多种配料：时蔬、鸡肉、煎蛋、三鲜、牛肉、牛肚、排骨、肥肠、鳝鱼、腰花等
- 支持配菜和加量项：酸豆角、辣萝卜丁、葱花、香菜、芹菜、加面、加粉
- 自动生成订单描述和小票
- 自动计算订单总价
- 根据面底限制加量项：面类可加面，粉类可加粉
- 后端订单组合逻辑会校验未知面底、未知配料、数量上限和不兼容搭配

## 项目结构

```text
nuddles/
├── noodle_shop.py                         # Python 核心业务逻辑
├── noodle_shop_gui.py                     # Tkinter 图形界面
├── src/                                   # Java 装饰器模式实现
│   ├── Noodle.java                        # 抽象面食类
│   ├── ToppingDecorator.java              # 抽象配料装饰器
│   ├── HotDryNoodle.java                  # 热干面
│   ├── HotDryPowder.java                  # 热干粉
│   ├── SoupNoodle.java                    # 汤面
│   ├── SoupPowder.java                    # 汤粉
│   ├── Beef.java 等                       # 具体配料装饰器
│   └── Main.java                          # Java 示例入口
├── noodle-shop-architecture-simple.drawio # 架构图
├── noodle-shop-class-diagram.drawio       # 类图
└── README.md
```

## 运行 Python 图形界面

本项目的 Python 版本只使用标准库，不需要额外安装依赖。

```bash
python noodle_shop_gui.py
```

运行后会打开点餐窗口，可以选择面底、增加或减少配料，并在右侧查看订单描述、小票和总价。

## 运行 Python 业务逻辑示例

```bash
python -c "from noodle_shop import compose_order; order = compose_order('hot_dry_noodle', ['vegetable', 'beef', 'extra_noodle']); print(order.get_description()); print(order.cost())"
```

示例输出表示一份热干面加时蔬、牛肉和加面，总价会自动累加。

## 运行 Java 示例

Java 文件声明了 `noodleshop` 包，建议从项目根目录编译到单独输出目录：

```bash
javac -encoding UTF-8 -d out src/*.java
java -cp out noodleshop.Main
```

示例入口会创建一份热干面，并添加时蔬和牛肉，然后输出订单描述与总价。

## 设计模式说明

项目核心使用装饰器模式：

- `Noodle` 是抽象构件，定义面食描述和价格接口
- `HotDryNoodle`、`HotDryPowder`、`SoupNoodle`、`SoupPowder` 是具体构件
- `ToppingDecorator` 是抽象装饰器，持有一个 `Noodle` 对象
- 各种配料类是具体装饰器，会在原有面食基础上追加描述并增加价格

这种设计可以在不修改基础面食类的情况下，灵活扩展新的配料和加价规则。

## 校验与规则

Python 核心逻辑提供了订单校验：

- 面底 key 不存在时抛出错误
- 配料 key 不存在时抛出错误
- 配料数量超过上限时抛出错误
- 加面不能搭配粉类面底
- 加粉不能搭配面类面底

GUI 会复用同一套规则，让界面展示和后端业务逻辑保持一致。

## 相关图表

仓库中包含两个 Draw.io 文件：

- `noodle-shop-architecture-simple.drawio`：系统架构图
- `noodle-shop-class-diagram.drawio`：类图

可以使用 Draw.io 或 diagrams.net 打开查看。

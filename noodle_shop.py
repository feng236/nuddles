# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from collections import Counter
from typing import Iterable


# ============ 抽象构件 ============
class Noodle(ABC):
    description = "未知面食"

    def get_description(self) -> str:
        return self.description

    @abstractmethod
    def cost(self) -> float: ...


class HotDryNoodle(Noodle):
    description = "热干面"
    def cost(self): return 8.0

class HotDryPowder(Noodle):
    description = "热干粉"
    def cost(self): return 8.0

class SoupNoodle(Noodle):
    description = "汤面"
    def cost(self): return 7.0

class SoupPowder(Noodle):
    description = "汤粉"
    def cost(self): return 7.0

class ToppingDecorator(Noodle):
    topping_name = ""
    topping_price = 0.0

    def __init__(self, noodle: Noodle):
        self.noodle = noodle

    def get_description(self) -> str:
        return f"{self.noodle.get_description()} + {self.topping_name}"

    def cost(self) -> float:
        return self.noodle.cost() + self.topping_price


class Vegetable(ToppingDecorator):        topping_name, topping_price = "时蔬",   2.0
class Chicken(ToppingDecorator):          topping_name, topping_price = "鸡肉",   6.0
class FriedEgg(ToppingDecorator):         topping_name, topping_price = "煎蛋",   2.5
class ThreeDelicacies(ToppingDecorator):  topping_name, topping_price = "三鲜",   8.0
class Beef(ToppingDecorator):             topping_name, topping_price = "牛肉",  10.0
class BeefTripe(ToppingDecorator):        topping_name, topping_price = "牛肚",   9.0
class Ribs(ToppingDecorator):             topping_name, topping_price = "排骨",  12.0
class FatIntestine(ToppingDecorator):     topping_name, topping_price = "肥肠",  11.0
class Eel(ToppingDecorator):              topping_name, topping_price = "鳝鱼",  13.0
class PorkKidney(ToppingDecorator):       topping_name, topping_price = "腰花",  10.0

class SourBeans(ToppingDecorator):        topping_name, topping_price = "酸豆角",   1.0
class SpicyRadish(ToppingDecorator):      topping_name, topping_price = "辣萝卜丁", 1.0
class GreenOnion(ToppingDecorator):       topping_name, topping_price = "葱花",    0.0
class Cilantro(ToppingDecorator):         topping_name, topping_price = "香菜",    0.0
class Celery(ToppingDecorator):           topping_name, topping_price = "芹菜",    0.0

class ExtraNoodle(ToppingDecorator):      topping_name, topping_price = "加面", 3.0
class ExtraPowder(ToppingDecorator):      topping_name, topping_price = "加粉", 3.0


def _base_option(key: str, cls: type[Noodle], group: str) -> dict:
    return {
        "key": key,
        "label": cls.description,
        "cls": cls,
        "price": cls().cost(),
        "group": group,
    }


def _topping_option(
    key: str,
    cls: type[ToppingDecorator],
    group: str,
    max_count: int | None,
) -> dict:
    return {
        "key": key,
        "label": cls.topping_name,
        "cls": cls,
        "price": cls.topping_price,
        "group": group,
        "max": max_count,
    }


BASE_OPTIONS = [
    _base_option("hot_dry_noodle", HotDryNoodle, "干拌"),
    _base_option("hot_dry_powder", HotDryPowder, "干拌"),
    _base_option("soup_noodle", SoupNoodle, "汤类"),
    _base_option("soup_powder", SoupPowder, "汤类"),
]

TOPPING_OPTIONS = [
    _topping_option("vegetable", Vegetable, "主浇头", None),
    _topping_option("chicken", Chicken, "主浇头", None),
    _topping_option("fried_egg", FriedEgg, "主浇头", None),
    _topping_option("three_delicacies", ThreeDelicacies, "主浇头", None),
    _topping_option("beef", Beef, "主浇头", None),
    _topping_option("beef_tripe", BeefTripe, "主浇头", None),
    _topping_option("ribs", Ribs, "主浇头", None),
    _topping_option("fat_intestine", FatIntestine, "主浇头", None),
    _topping_option("eel", Eel, "主浇头", None),
    _topping_option("pork_kidney", PorkKidney, "主浇头", None),
    _topping_option("sour_beans", SourBeans, "配菜", None),
    _topping_option("spicy_radish", SpicyRadish, "配菜", None),
    _topping_option("green_onion", GreenOnion, "配菜", None),
    _topping_option("cilantro", Cilantro, "配菜", None),
    _topping_option("celery", Celery, "配菜", None),
    _topping_option("extra_noodle", ExtraNoodle, "加量", None),
    _topping_option("extra_powder", ExtraPowder, "加量", None),
]

BASE_OPTION_MAP = {option["key"]: option for option in BASE_OPTIONS}
TOPPING_OPTION_MAP = {option["key"]: option for option in TOPPING_OPTIONS}
NOODLE_BASE_KEYS = {"hot_dry_noodle", "soup_noodle"}
POWDER_BASE_KEYS = {"hot_dry_powder", "soup_powder"}
TOPPING_COMPATIBLE_BASES = {
    "extra_noodle": NOODLE_BASE_KEYS,
    "extra_powder": POWDER_BASE_KEYS,
}


def create_base(base_key: str) -> Noodle:
    option = BASE_OPTION_MAP.get(base_key)
    if option is not None:
        return option["cls"]()
    raise ValueError(f"未知面底: {base_key}")


def is_topping_allowed_for_base(base_key: str, topping_key: str) -> bool:
    compatible_bases = TOPPING_COMPATIBLE_BASES.get(topping_key)
    return compatible_bases is None or base_key in compatible_bases


def validate_order(base_key: str, toppings: Iterable[str]) -> list[str]:
    if base_key not in BASE_OPTION_MAP:
        raise ValueError(f"未知面底: {base_key}")

    topping_list = list(toppings)
    topping_counts = Counter(topping_list)
    for topping_key in topping_list:
        option = TOPPING_OPTION_MAP.get(topping_key)
        if option is None:
            raise ValueError(f"未知配料: {topping_key}")
        max_count = option["max"]
        if max_count is not None and topping_counts[topping_key] > max_count:
            raise ValueError(f"{option['label']}最多可选 {max_count} 份")
        if not is_topping_allowed_for_base(base_key, topping_key):
            raise ValueError(f"{BASE_OPTION_MAP[base_key]['label']}不能搭配{option['label']}")
    return topping_list


def compose_order(base_key: str, toppings: Iterable[str]) -> Noodle:
    topping_list = validate_order(base_key, toppings)
    noodle = create_base(base_key)
    for topping_key in topping_list:
        option = TOPPING_OPTION_MAP[topping_key]
        noodle = option["cls"](noodle)
    return noodle


def unwrap_order(noodle: Noodle) -> list[dict[str, float | str]]:
    layers: list[dict[str, float | str]] = []
    current = noodle
    while isinstance(current, ToppingDecorator):
        layers.append({
            "type": "topping",
            "label": current.topping_name,
            "price": current.topping_price,
        })
        current = current.noodle
    layers.append({
        "type": "base",
        "label": current.get_description(),
        "price": current.cost(),
    })
    layers.reverse()
    return layers

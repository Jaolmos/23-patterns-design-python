"""
PATRON ITERATOR - Menu de Restaurante

Analogia: Como el mesero que te va mostrando el menu por secciones: primero
entradas, luego platos principales, luego postres. No necesitas ver toda la
carta de golpe, vas navegando secuencialmente por las categorias. El mesero
(iterator) sabe como recorrer el menu sin que tu conozcas la estructura interna.

PROBLEMA: Quieres recorrer elementos de una coleccion sin exponer su estructura
interna (lista, arbol, diccionario). Si expones la estructura, el cliente se
acopla a ella y cambiarla se vuelve dificil.

SOLUCION: Crear un objeto Iterator que encapsula el recorrido de la coleccion.
El iterator proporciona metodos standar (next, has_next) sin revelar la
representacion interna de la coleccion.

VENTAJA: Desacopla el algoritmo de recorrido de la estructura de datos.
Puedes tener multiples iteradores sobre la misma coleccion. Simplifica
la interfaz de las colecciones.

Conceptos OOP usados:
- Abstraccion: Interfaz Iterator con next() y has_next()
- Encapsulacion: El iterator oculta la estructura interna
- Polimorfismo: Diferentes colecciones con mismo iterador
"""

from abc import ABC, abstractmethod
from typing import List, Any


# =============================================================================
# MODELO: Items del menu
# =============================================================================

class MenuItem:
    """
    Representa un item del menu del restaurante.
    """

    def __init__(self, name: str, description: str, vegetarian: bool, price: float):
        self._name = name
        self._description = description
        self._vegetarian = vegetarian
        self._price = price

    def get_name(self) -> str:
        return self._name

    def get_description(self) -> str:
        return self._description

    def is_vegetarian(self) -> bool:
        return self._vegetarian

    def get_price(self) -> float:
        return self._price

    def __str__(self) -> str:
        veg_mark = "[V]" if self._vegetarian else ""
        return f"{self._name} {veg_mark} - ${self._price:.2f}\n  {self._description}"


# =============================================================================
# ITERATOR: Interfaz abstracta para iterar
# =============================================================================

class Iterator(ABC):
    """
    Interfaz Iterator: Define los metodos para recorrer una coleccion.
    """

    @abstractmethod
    def has_next(self) -> bool:
        """Verifica si hay mas elementos por recorrer."""
        pass

    @abstractmethod
    def next(self) -> Any:
        """Retorna el siguiente elemento."""
        pass


# =============================================================================
# ITERADORES CONCRETOS
# =============================================================================

class MenuIterator(Iterator):
    """
    Iterator concreto: Itera sobre una lista de items del menu.
    Encapsula el recorrido sin exponer la estructura interna.
    """

    def __init__(self, items: List[MenuItem]):
        self._items = items
        self._position = 0

    def has_next(self) -> bool:
        """Verifica si quedan items por iterar."""
        return self._position < len(self._items)

    def next(self) -> MenuItem:
        """Retorna el siguiente item y avanza la posicion."""
        if not self.has_next():
            raise StopIteration("No hay mas items en el menu")

        item = self._items[self._position]
        self._position += 1
        return item


# =============================================================================
# COLECCION ITERABLE: Menu que puede ser iterado
# =============================================================================

class Menu(ABC):
    """
    Interfaz Menu: Define que un menu debe proporcionar un iterator.
    """

    @abstractmethod
    def create_iterator(self) -> Iterator:
        """Crea un iterator para recorrer el menu."""
        pass

    @abstractmethod
    def add_item(self, name: str, description: str, vegetarian: bool, price: float) -> None:
        """Agrega un item al menu."""
        pass


# =============================================================================
# MENUS CONCRETOS
# =============================================================================

class BreakfastMenu(Menu):
    """
    Menu de desayunos: Almacena items de desayuno.
    Usa una lista internamente pero el cliente no lo sabe.
    """

    def __init__(self):
        self._items: List[MenuItem] = []

    def add_item(self, name: str, description: str, vegetarian: bool, price: float) -> None:
        """Agrega un item de desayuno."""
        item = MenuItem(name, description, vegetarian, price)
        self._items.append(item)

    def create_iterator(self) -> Iterator:
        """Crea un iterator para el menu de desayunos."""
        return MenuIterator(self._items)


class LunchMenu(Menu):
    """
    Menu de almuerzos: Almacena items de almuerzo.
    Podria usar diferente estructura interna sin afectar al cliente.
    """

    def __init__(self):
        self._items: List[MenuItem] = []

    def add_item(self, name: str, description: str, vegetarian: bool, price: float) -> None:
        """Agrega un item de almuerzo."""
        item = MenuItem(name, description, vegetarian, price)
        self._items.append(item)

    def create_iterator(self) -> Iterator:
        """Crea un iterator para el menu de almuerzos."""
        return MenuIterator(self._items)


class DinnerMenu(Menu):
    """
    Menu de cenas: Almacena items de cena.
    """

    def __init__(self):
        self._items: List[MenuItem] = []

    def add_item(self, name: str, description: str, vegetarian: bool, price: float) -> None:
        """Agrega un item de cena."""
        item = MenuItem(name, description, vegetarian, price)
        self._items.append(item)

    def create_iterator(self) -> Iterator:
        """Crea un iterator para el menu de cenas."""
        return MenuIterator(self._items)


# =============================================================================
# CLIENTE: Mesero que usa los iterators
# =============================================================================

class Waiter:
    """
    Cliente: El mesero usa los iterators para mostrar los menus
    sin conocer su estructura interna.
    """

    def __init__(self, breakfast_menu: Menu, lunch_menu: Menu, dinner_menu: Menu):
        self._breakfast_menu = breakfast_menu
        self._lunch_menu = lunch_menu
        self._dinner_menu = dinner_menu

    def print_menu(self) -> None:
        """Imprime todos los menus usando iterators."""
        print("\n" + "=" * 60)
        print("MENU DEL RESTAURANTE")
        print("=" * 60)

        print("\n--- DESAYUNO ---")
        self._print_menu_items(self._breakfast_menu.create_iterator())

        print("\n--- ALMUERZO ---")
        self._print_menu_items(self._lunch_menu.create_iterator())

        print("\n--- CENA ---")
        self._print_menu_items(self._dinner_menu.create_iterator())

    def _print_menu_items(self, iterator: Iterator) -> None:
        """Imprime items usando el iterator."""
        while iterator.has_next():
            item = iterator.next()
            print(f"\n{item}")

    def print_vegetarian_menu(self) -> None:
        """Imprime solo items vegetarianos de todos los menus."""
        print("\n" + "=" * 60)
        print("OPCIONES VEGETARIANAS")
        print("=" * 60)

        print("\n--- DESAYUNO ---")
        self._print_vegetarian_items(self._breakfast_menu.create_iterator())

        print("\n--- ALMUERZO ---")
        self._print_vegetarian_items(self._lunch_menu.create_iterator())

        print("\n--- CENA ---")
        self._print_vegetarian_items(self._dinner_menu.create_iterator())

    def _print_vegetarian_items(self, iterator: Iterator) -> None:
        """Imprime solo items vegetarianos."""
        while iterator.has_next():
            item = iterator.next()
            if item.is_vegetarian():
                print(f"\n{item}")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON ITERATOR - Menu de Restaurante")
    print("=" * 70)

    # --- Crear menus y agregar items ---
    print("\n[PASO 1] Creando menus y agregando items")
    print("-" * 70)

    breakfast_menu = BreakfastMenu()
    breakfast_menu.add_item(
        "Huevos Rancheros",
        "Huevos estrellados con salsa ranchera y frijoles",
        False,
        8.99
    )
    breakfast_menu.add_item(
        "Hotcakes",
        "Stack de hotcakes con miel de maple y mantequilla",
        True,
        6.99
    )
    breakfast_menu.add_item(
        "Omelette de Vegetales",
        "Omelette con espinacas, champiñones y queso",
        True,
        7.99
    )

    lunch_menu = LunchMenu()
    lunch_menu.add_item(
        "Hamburguesa Clasica",
        "Hamburguesa de res con papas fritas",
        False,
        12.99
    )
    lunch_menu.add_item(
        "Ensalada Caesar",
        "Lechuga romana con aderezo caesar y crutones",
        True,
        9.99
    )
    lunch_menu.add_item(
        "Sandwich de Pavo",
        "Pavo, lechuga, tomate y mayonesa",
        False,
        10.99
    )

    dinner_menu = DinnerMenu()
    dinner_menu.add_item(
        "Filete de Salmon",
        "Salmon a la parrilla con vegetales asados",
        False,
        18.99
    )
    dinner_menu.add_item(
        "Pasta Alfredo",
        "Fettuccine con salsa alfredo cremosa",
        True,
        14.99
    )
    dinner_menu.add_item(
        "Costillas BBQ",
        "Costillas de cerdo con salsa BBQ",
        False,
        16.99
    )

    print("  Menus creados con varios items cada uno")

    # --- Crear mesero y mostrar menu completo ---
    print("\n[PASO 2] Mesero muestra menu completo usando iterators")
    print("-" * 70)

    waiter = Waiter(breakfast_menu, lunch_menu, dinner_menu)
    waiter.print_menu()

    # --- Mostrar solo opciones vegetarianas ---
    print("\n[PASO 3] Mostrar solo opciones vegetarianas")
    print("-" * 70)

    waiter.print_vegetarian_menu()

    # --- Demostrar que el iterator encapsula el recorrido ---
    print("\n" + "=" * 70)
    print("[PASO 4] Iterar manualmente para demostrar encapsulacion")
    print("=" * 70)

    print("\n  Recorriendo menu de desayuno manualmente:")
    iterator = breakfast_menu.create_iterator()
    count = 0
    while iterator.has_next():
        item = iterator.next()
        count += 1
        print(f"    {count}. {item.get_name()} - ${item.get_price():.2f}")

    """
    =========================================================================
    VENTAJAS DEL PATRON ITERATOR
    =========================================================================
    1. DESACOPLAMIENTO: El cliente no conoce la estructura interna

    2. ENCAPSULACION: El recorrido esta encapsulado en el iterator

    3. MULTIPLES ITERADORES: Puedes tener varios iteradores simultaneos

    4. INTERFAZ UNIFORME: Mismo metodo para recorrer diferentes colecciones

    5. RESPONSABILIDAD UNICA: El menu se enfoca en almacenar, el iterator
       en recorrer
    """

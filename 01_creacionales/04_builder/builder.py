"""
PATRON BUILDER
==============
Separa la construccion de un objeto complejo de su representacion,
permitiendo crear diferentes configuraciones con el mismo proceso.

Analogia: Crear un personaje en un videojuego. Eliges nombre, clase,
atributos, armas, etc. paso a paso hasta tener tu personaje listo.

PROBLEMA: Objetos con muchos parametros en el constructor. Es confuso
y dificil de leer: Character("Goku", "warrior", 80, 50, 30, "sword"...)

SOLUCION: Construir el objeto paso a paso con metodos claros:
CharacterBuilder().set_name("Goku").set_class("warrior").build()

VENTAJA: Codigo legible, flexible, y puedes crear configuraciones
predefinidas (guerrero, mago, arquero) reutilizando el mismo builder.
"""


class Character:
    """
    PRODUCTO: El objeto complejo que queremos construir.
    Tiene muchos atributos que seria confuso pasar todos al constructor.
    """

    def __init__(self) -> None:
        # Atributos basicos
        self.name: str | None = None
        self.character_class: str | None = None

        # Atributos de combate (0-100)
        self.strength: int = 0
        self.agility: int = 0
        self.intelligence: int = 0
        self.health: int = 100

        # Equipamiento
        self.weapon: str | None = None
        self.armor: str | None = None
        self.accessory: str | None = None

    def show_stats(self) -> None:
        """Muestra las estadisticas del personaje."""
        print(f"\n{'='*40}")
        print(f"  PERSONAJE: {self.name}")
        print(f"  Clase: {self.character_class}")
        print(f"{'='*40}")
        print(f"  [ATRIBUTOS]")
        print(f"    Fuerza:       {self.strength}")
        print(f"    Agilidad:     {self.agility}")
        print(f"    Inteligencia: {self.intelligence}")
        print(f"    Salud:        {self.health}")
        print(f"  [EQUIPAMIENTO]")
        print(f"    Arma:      {self.weapon or 'Ninguna'}")
        print(f"    Armadura:  {self.armor or 'Ninguna'}")
        print(f"    Accesorio: {self.accessory or 'Ninguno'}")
        print(f"{'='*40}")


class CharacterBuilder:
    """
    BUILDER: Clase que construye el personaje paso a paso.
    Cada metodo configura una parte y devuelve 'self' para encadenar.
    """

    def __init__(self) -> None:
        # Crear un personaje vacio para ir construyendo
        self._character = Character()

    def set_name(self, name: str) -> "CharacterBuilder":
        """Define el nombre del personaje."""
        self._character.name = name
        return self  # Devuelve self para encadenar metodos

    def set_class(self, character_class: str) -> "CharacterBuilder":
        """Define la clase del personaje (warrior, mage, archer, etc)."""
        self._character.character_class = character_class
        return self

    def set_strength(self, value: int) -> "CharacterBuilder":
        """Define la fuerza (0-100)."""
        self._character.strength = min(100, max(0, value))
        return self

    def set_agility(self, value: int) -> "CharacterBuilder":
        """Define la agilidad (0-100)."""
        self._character.agility = min(100, max(0, value))
        return self

    def set_intelligence(self, value: int) -> "CharacterBuilder":
        """Define la inteligencia (0-100)."""
        self._character.intelligence = min(100, max(0, value))
        return self

    def set_health(self, value: int) -> "CharacterBuilder":
        """Define la salud inicial."""
        self._character.health = max(1, value)
        return self

    def set_weapon(self, weapon: str) -> "CharacterBuilder":
        """Define el arma del personaje."""
        self._character.weapon = weapon
        return self

    def set_armor(self, armor: str) -> "CharacterBuilder":
        """Define la armadura del personaje."""
        self._character.armor = armor
        return self

    def set_accessory(self, accessory: str) -> "CharacterBuilder":
        """Define el accesorio del personaje."""
        self._character.accessory = accessory
        return self

    def build(self) -> Character:
        """
        Finaliza la construccion y devuelve el personaje.
        Tambien reinicia el builder para poder crear otro.
        """
        character = self._character
        self._character = Character()  # Reinicia para el siguiente
        return character


class CharacterDirector:
    """
    DIRECTOR (opcional): Conoce recetas predefinidas de personajes.
    Usa el builder para crear configuraciones comunes.
    """

    def __init__(self, builder: CharacterBuilder) -> None:
        self._builder = builder

    def create_warrior(self, name: str) -> Character:
        """Crea un guerrero: alta fuerza, armadura pesada."""
        return self._builder \
            .set_name(name) \
            .set_class("Guerrero") \
            .set_strength(80) \
            .set_agility(40) \
            .set_intelligence(20) \
            .set_health(150) \
            .set_weapon("Espada de Acero") \
            .set_armor("Armadura Pesada") \
            .set_accessory("Escudo") \
            .build()

    def create_mage(self, name: str) -> Character:
        """Crea un mago: alta inteligencia, tunicas."""
        return self._builder \
            .set_name(name) \
            .set_class("Mago") \
            .set_strength(20) \
            .set_agility(30) \
            .set_intelligence(90) \
            .set_health(80) \
            .set_weapon("Baston Magico") \
            .set_armor("Tunica Arcana") \
            .set_accessory("Amuleto de Mana") \
            .build()

    def create_archer(self, name: str) -> Character:
        """Crea un arquero: alta agilidad, arco."""
        return self._builder \
            .set_name(name) \
            .set_class("Arquero") \
            .set_strength(40) \
            .set_agility(85) \
            .set_intelligence(40) \
            .set_health(100) \
            .set_weapon("Arco Largo") \
            .set_armor("Armadura de Cuero") \
            .set_accessory("Carcaj de Flechas") \
            .build()


# =============================================================================
# DEMOSTRACION DEL PATRON
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION DEL PATRON BUILDER")
    print("=" * 60)
    
    # Crear el builder
    builder = CharacterBuilder()
    
    # FORMA 1: Construccion manual paso a paso
    print("\n[1] CONSTRUCCION MANUAL (paso a paso):")
    
    mi_personaje = builder \
        .set_name("Arthas") \
        .set_class("Paladin") \
        .set_strength(70) \
        .set_agility(50) \
        .set_intelligence(60) \
        .set_health(120) \
        .set_weapon("Martillo de Luz") \
        .set_armor("Armadura Sagrada") \
        .set_accessory("Anillo de Proteccion") \
        .build()
    
    mi_personaje.show_stats()
    
    # FORMA 2: Usando el Director con recetas predefinidas
    print("\n[2] USANDO DIRECTOR (recetas predefinidas):")
    
    director = CharacterDirector(builder)
    
    guerrero = director.create_warrior("Conan")
    guerrero.show_stats()
    
    mago = director.create_mage("Gandalf")
    mago.show_stats()
    
    arquero = director.create_archer("Legolas")
    arquero.show_stats()
    
    # FORMA 3: Personaje minimo (solo lo necesario)
    print("\n[3] PERSONAJE MINIMO:")
    
    simple = builder \
        .set_name("Novato") \
        .set_class("Aprendiz") \
        .build()
    
    simple.show_stats()
    
    """
    =========================================================================
    VENTAJAS DEL PATRON BUILDER
    =========================================================================
    1. LEGIBILIDAD: Cada metodo dice que hace
       .set_name("X") es mas claro que el 1er parametro
    
    2. FLEXIBILIDAD: Puedes omitir atributos opcionales
       Solo .set_name() y .set_class() si quieres
    
    3. REUTILIZABLE: El Director guarda recetas comunes
       create_warrior(), create_mage(), create_archer()
    
    4. INMUTABILIDAD: build() devuelve el objeto final
       El builder puede crear otro diferente despues
    """


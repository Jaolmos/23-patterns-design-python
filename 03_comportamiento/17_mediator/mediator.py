"""
PATRON MEDIATOR - Chat Grupal

Analogia: Como un grupo de WhatsApp. Cuando envias un mensaje, no lo mandas
directamente a cada persona. Lo envias al grupo (mediador) y el grupo se
encarga de distribuirlo a todos los miembros. Los usuarios no necesitan
conocerse entre si, solo conocen al grupo.

PROBLEMA: Cuando muchos objetos se comunican directamente entre si, se crea
una red compleja de dependencias (todos conocen a todos). Esto hace el sistema
dificil de mantener y modificar.

SOLUCION: Crear un mediador que centralice toda la comunicacion. Los objetos
no se comunican directamente, sino a traves del mediador. El mediador conoce
a todos y coordina su interaccion.

VENTAJA: Reduce acoplamiento entre objetos. Centraliza logica de control.
Facil agregar nuevos participantes sin modificar los existentes. Reutilizas
la logica de interaccion.

Conceptos OOP usados:
- Mediador: Objeto central que coordina la comunicacion
- Composicion: El mediador contiene referencias a los colegas
- Desacoplamiento: Los colegas no se conocen directamente
"""

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


# =============================================================================
# MEDIATOR: Interfaz del mediador
# =============================================================================

class ChatMediator(ABC):
    """
    Interfaz Mediator: Define como los usuarios interactuan a traves del mediador.
    """

    @abstractmethod
    def send_message(self, message: str, sender: 'User') -> None:
        """Envia un mensaje desde un usuario a todos los demas."""
        pass

    @abstractmethod
    def add_user(self, user: 'User') -> None:
        """Agrega un usuario al chat."""
        pass


# =============================================================================
# MEDIADOR CONCRETO
# =============================================================================

class ChatRoom(ChatMediator):
    """
    Mediador concreto: La sala de chat que coordina los mensajes entre usuarios.
    """

    def __init__(self, name: str):
        self._name = name
        self._users: List['User'] = []

    def add_user(self, user: 'User') -> None:
        """Agrega un usuario a la sala de chat."""
        self._users.append(user)
        user.set_chat_room(self)
        print(f"[{self._name}] {user.get_name()} se ha unido al chat")

    def send_message(self, message: str, sender: 'User') -> None:
        """
        Recibe un mensaje de un usuario y lo distribuye a todos los demas.
        El mediador coordina quien recibe el mensaje.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Enviar a todos excepto al emisor
        for user in self._users:
            if user != sender:
                user.receive_message(message, sender, timestamp)


# =============================================================================
# COLLEAGUE: Usuario que se comunica a traves del mediador
# =============================================================================

class User:
    """
    Colleague: Un usuario del chat.
    No conoce a otros usuarios directamente, solo al mediador (chat room).
    """

    def __init__(self, name: str):
        self._name = name
        self._chat_room: ChatMediator = None

    def get_name(self) -> str:
        return self._name

    def set_chat_room(self, chat_room: ChatMediator) -> None:
        """Establece el mediador (sala de chat) para este usuario."""
        self._chat_room = chat_room

    def send(self, message: str) -> None:
        """
        Envia un mensaje a traves del mediador.
        El usuario no sabe a quien le llega, el mediador lo decide.
        """
        print(f"\n[{self._name}] Enviando: '{message}'")
        if self._chat_room:
            self._chat_room.send_message(message, self)
        else:
            print(f"  [ERROR] {self._name} no esta en ningun chat")

    def receive_message(self, message: str, sender: 'User', timestamp: str) -> None:
        """
        Recibe un mensaje enviado por otro usuario a traves del mediador.
        """
        print(f"  [{timestamp}] {self._name} recibio de {sender.get_name()}: '{message}'")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON MEDIATOR - Chat Grupal")
    print("=" * 70)

    # --- Crear sala de chat (mediador) ---
    print("\n[PASO 1] Creando sala de chat")
    print("-" * 70)
    chat_room = ChatRoom("Equipo Python")
    print(f"  Sala '{chat_room._name}' creada")

    # --- Crear usuarios ---
    print("\n[PASO 2] Creando usuarios")
    print("-" * 70)
    alice = User("Alice")
    bob = User("Bob")
    charlie = User("Charlie")
    diana = User("Diana")
    print("  Usuarios creados: Alice, Bob, Charlie, Diana")

    # --- Agregar usuarios al chat ---
    print("\n[PASO 3] Usuarios se unen al chat")
    print("-" * 70)
    chat_room.add_user(alice)
    chat_room.add_user(bob)
    chat_room.add_user(charlie)
    chat_room.add_user(diana)

    # --- Usuarios envian mensajes ---
    print("\n[PASO 4] Usuarios intercambian mensajes")
    print("-" * 70)

    alice.send("Hola a todos!")

    bob.send("Hola Alice, como estas?")

    charlie.send("Alguien termino el proyecto?")

    diana.send("Yo ya termine mi parte")

    # --- Demostrar que sin mediador no funciona ---
    print("\n[PASO 5] Usuario sin sala de chat intenta enviar mensaje")
    print("-" * 70)

    eve = User("Eve")
    print(f"  Nuevo usuario: {eve.get_name()} (no esta en el chat)")
    eve.send("Hola, hay alguien ahi?")

    # --- Agregar el nuevo usuario y probar ---
    print("\n[PASO 6] Nuevo usuario se une y envia mensaje")
    print("-" * 70)
    chat_room.add_user(eve)
    eve.send("Ahora si puedo hablar!")

    """
    =========================================================================
    VENTAJAS DEL PATRON MEDIATOR
    =========================================================================
    1. DESACOPLAMIENTO: Los objetos no se conocen directamente

    2. CENTRALIZACION: La logica de comunicacion esta en un solo lugar

    3. FACIL EXTENSION: Agregar nuevos participantes sin modificar existentes

    4. REUTILIZACION: La logica de coordinacion es reutilizable

    5. SIMPLIFICACION: Elimina dependencias muchos-a-muchos
    """

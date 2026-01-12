"""
PATRON OBSERVER - Sistema de Notificaciones

Analogia: Como suscribirse a un canal de YouTube. Cuando el canal sube un nuevo
video (evento), todos los suscriptores reciben una notificacion automaticamente.
No necesitas estar revisando constantemente. Los suscriptores pueden unirse o
salirse cuando quieran.

PROBLEMA: Necesitas notificar automaticamente a multiples objetos cuando el
estado de otro objeto cambia. Si los objetos estan acoplados directamente,
es dificil agregar o quitar observadores.

SOLUCION: Definir una dependencia uno-a-muchos entre objetos. Cuando el objeto
observable (Subject) cambia de estado, notifica automaticamente a todos sus
observadores registrados. Los observadores pueden suscribirse o desuscribirse
dinamicamente.

VENTAJA: Desacopla el subject de los observers. Puedes agregar observers sin
modificar el subject. Soporte para broadcast de comunicacion.

Conceptos OOP usados:
- Abstraccion: Interfaces Subject y Observer
- Composicion: Subject contiene lista de observers
- Polimorfismo: Diferentes observers con misma interfaz
"""

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


# =============================================================================
# OBSERVER: Interfaz para los observadores
# =============================================================================

class Observer(ABC):
    """
    Interfaz Observer: Define como los observers reciben notificaciones.
    """

    @abstractmethod
    def update(self, event_type: str, message: str, timestamp: str) -> None:
        """Recibe notificaciones del subject."""
        pass


# =============================================================================
# SUBJECT: Interfaz para el objeto observable
# =============================================================================

class Subject(ABC):
    """
    Interfaz Subject: Define como manejar observers (suscribir/desuscribir/notificar).
    """

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Suscribe un observer."""
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Desuscribe un observer."""
        pass

    @abstractmethod
    def notify(self, event_type: str, message: str) -> None:
        """Notifica a todos los observers."""
        pass


# =============================================================================
# SUBJECT CONCRETO: El objeto observable
# =============================================================================

class EventNotifier(Subject):
    """
    Subject concreto: Sistema de eventos que notifica a observers suscritos.
    Cuando ocurre un evento, todos los observers son notificados.
    """

    def __init__(self, name: str):
        self._name = name
        # Composicion: el subject contiene lista de observers
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Suscribe un observer al notificador."""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"[{self._name}] Observer '{observer.__class__.__name__}' suscrito")

    def detach(self, observer: Observer) -> None:
        """Desuscribe un observer del notificador."""
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"[{self._name}] Observer '{observer.__class__.__name__}' desuscrito")

    def notify(self, event_type: str, message: str) -> None:
        """
        Notifica a todos los observers cuando ocurre un evento.
        Cada observer recibe la notificacion y reacciona segun su implementacion.
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"\n[{self._name}] Evento: {event_type}")
        print(f"  Notificando a {len(self._observers)} observers...")

        # Polimorfismo: itera sobre observers sin saber su tipo concreto
        for observer in self._observers:
            observer.update(event_type, message, timestamp)


# =============================================================================
# OBSERVERS CONCRETOS: Diferentes tipos de observadores
# =============================================================================

class EmailObserver(Observer):
    """
    Observer concreto: Envia notificaciones por email.
    """

    def __init__(self, email: str):
        self._email = email

    def update(self, event_type: str, message: str, timestamp: str) -> None:
        """Recibe la notificacion y envia un email."""
        print(f"  [Email -> {self._email}] [{timestamp}]")
        print(f"    Asunto: {event_type}")
        print(f"    Mensaje: {message}")


class SMSObserver(Observer):
    """
    Observer concreto: Envia notificaciones por SMS.
    """

    def __init__(self, phone: str):
        self._phone = phone

    def update(self, event_type: str, message: str, timestamp: str) -> None:
        """Recibe la notificacion y envia un SMS."""
        print(f"  [SMS -> {self._phone}] [{timestamp}]")
        print(f"    {event_type}: {message}")


class PushObserver(Observer):
    """
    Observer concreto: Envia notificaciones push a dispositivos moviles.
    """

    def __init__(self, device_id: str):
        self._device_id = device_id

    def update(self, event_type: str, message: str, timestamp: str) -> None:
        """Recibe la notificacion y envia una push notification."""
        print(f"  [Push -> Device {self._device_id}] [{timestamp}]")
        print(f"    {event_type}")
        print(f"    {message}")


class LogObserver(Observer):
    """
    Observer concreto: Registra eventos en un log.
    """

    def __init__(self, log_file: str):
        self._log_file = log_file

    def update(self, event_type: str, message: str, timestamp: str) -> None:
        """Recibe la notificacion y la registra en el log."""
        print(f"  [Log -> {self._log_file}] [{timestamp}]")
        print(f"    [{event_type}] {message}")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON OBSERVER - Sistema de Notificaciones")
    print("=" * 70)

    # --- Crear el notificador (subject) ---
    print("\n[PASO 1] Crear sistema de notificaciones")
    print("-" * 70)
    notifier = EventNotifier("Sistema de Eventos")

    # --- Crear observers ---
    print("\n[PASO 2] Crear diferentes observers")
    print("-" * 70)
    email_obs = EmailObserver("usuario@example.com")
    sms_obs = SMSObserver("+52-555-1234")
    push_obs = PushObserver("device-ABC-123")
    log_obs = LogObserver("/var/log/events.log")
    print("  Observers creados: Email, SMS, Push, Log")

    # --- Suscribir observers ---
    print("\n[PASO 3] Suscribir observers al notificador")
    print("-" * 70)
    notifier.attach(email_obs)
    notifier.attach(sms_obs)
    notifier.attach(push_obs)
    notifier.attach(log_obs)

    # --- Generar eventos ---
    print("\n[PASO 4] Generar eventos (todos los observers son notificados)")
    print("-" * 70)

    notifier.notify("Nuevo pedido", "Pedido #12345 ha sido creado")

    notifier.notify("Pago recibido", "Se recibio el pago de $1,500.00")

    # --- Desuscribir un observer ---
    print("\n[PASO 5] Desuscribir observer de SMS")
    print("-" * 70)
    notifier.detach(sms_obs)

    # --- Generar mas eventos ---
    print("\n[PASO 6] Nuevo evento (SMS ya no recibe notificaciones)")
    print("-" * 70)

    notifier.notify("Pedido enviado", "Pedido #12345 esta en camino")

    # --- Agregar nuevo observer dinamicamente ---
    print("\n[PASO 7] Agregar nuevo observer dinamicamente")
    print("-" * 70)
    email_obs2 = EmailObserver("admin@example.com")
    notifier.attach(email_obs2)

    print("\n[PASO 8] Evento con nuevo observer incluido")
    print("-" * 70)
    notifier.notify("Pedido entregado", "Pedido #12345 fue entregado exitosamente")

    """
    =========================================================================
    VENTAJAS DEL PATRON OBSERVER
    =========================================================================
    1. DESACOPLAMIENTO: Subject y observers estan desacoplados

    2. DINAMICO: Puedes agregar/quitar observers en tiempo de ejecucion

    3. BROADCAST: Un evento notifica automaticamente a multiples observers

    4. OPEN/CLOSED: Agregas nuevos observers sin modificar el subject

    5. CONSISTENCIA: Todos los observers reciben la misma notificacion
    """

"""
PATRON DECORATOR - Sistema de Notificaciones

Analogia: Vestir a una persona. Empiezas con la ropa base (camiseta) y vas
añadiendo capas: jersey, chaqueta, bufanda. Cada capa "envuelve" la anterior
y añade funcionalidad (mas abrigo) sin modificar las capas interiores.

PROBLEMA: Quieres añadir funcionalidades a objetos de forma dinamica.
Usar herencia crearia una explosion de subclases: NotifierEmail,
NotifierSMS, NotifierEmailSMS, NotifierEmailSMSSlack...

SOLUCION: Crear decoradores que "envuelven" al objeto original. Cada
decorador añade su funcionalidad y delega al objeto envuelto.

VENTAJA: Combinas funcionalidades en tiempo de ejecucion. Puedes apilar
decoradores como quieras sin crear nuevas clases para cada combinacion.

Conceptos OOP usados:
- Agregacion: El decorador RECIBE el componente (no lo crea)
- Herencia: Los decoradores heredan de la misma interfaz que decoran
- Polimorfismo: El cliente no distingue entre componente y decorador
"""

from abc import ABC, abstractmethod


# =============================================================================
# COMPONENT: Interfaz base para notificadores
# =============================================================================

class Notifier(ABC):
    """
    Componente base.
    Define la interfaz que todos los notificadores deben implementar.
    """
    
    @abstractmethod
    def send(self, message: str):
        """Envia una notificacion."""
        pass


# =============================================================================
# COMPONENTE CONCRETO: Notificador basico
# =============================================================================

class BasicNotifier(Notifier):
    """
    Componente concreto: notificador basico.
    Solo muestra el mensaje en consola (como un log).
    """
    
    def send(self, message: str):
        print(f"[LOG] Notificacion: {message}")


# =============================================================================
# DECORADOR BASE: Clase base para todos los decoradores
# =============================================================================

class NotifierDecorator(Notifier):
    """
    Decorador base.
    Mantiene una referencia al componente envuelto y delega las llamadas.
    Todos los decoradores concretos heredan de esta clase.
    """
    
    def __init__(self, notifier: Notifier):
        # Agregacion: el decorador RECIBE el notificador que envuelve
        self._wrapped = notifier
    
    def send(self, message: str):
        # Por defecto, delega al componente envuelto
        self._wrapped.send(message)


# =============================================================================
# DECORADORES CONCRETOS: Añaden funcionalidad
# =============================================================================

class EmailDecorator(NotifierDecorator):
    """
    Decorador: añade notificacion por email.
    Primero envia por email, luego delega al componente envuelto.
    """
    
    def __init__(self, notifier: Notifier, email: str = "usuario@email.com"):
        super().__init__(notifier)
        self.email = email
    
    def send(self, message: str):
        # Añade su funcionalidad
        print(f"[EMAIL] Enviando a {self.email}: {message}")
        # Delega al componente envuelto
        self._wrapped.send(message)


class SMSDecorator(NotifierDecorator):
    """
    Decorador: añade notificacion por SMS.
    Primero envia por SMS, luego delega al componente envuelto.
    """
    
    def __init__(self, notifier: Notifier, phone: str = "+34 600 000 000"):
        super().__init__(notifier)
        self.phone = phone
    
    def send(self, message: str):
        # Añade su funcionalidad
        print(f"[SMS] Enviando a {self.phone}: {message}")
        # Delega al componente envuelto
        self._wrapped.send(message)


class SlackDecorator(NotifierDecorator):
    """
    Decorador: añade notificacion por Slack.
    Primero envia a Slack, luego delega al componente envuelto.
    """
    
    def __init__(self, notifier: Notifier, channel: str = "#alertas"):
        super().__init__(notifier)
        self.channel = channel
    
    def send(self, message: str):
        # Añade su funcionalidad
        print(f"[SLACK] Enviando a {self.channel}: {message}")
        # Delega al componente envuelto
        self._wrapped.send(message)


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PATRON DECORATOR - Sistema de Notificaciones")
    print("=" * 60)
    
    # --- Notificador basico ---
    print("\n[1] Notificador basico (solo log):")
    print("-" * 40)
    basic = BasicNotifier()
    basic.send("Mensaje de prueba")
    
    # --- Un solo decorador ---
    print("\n[2] Notificador con Email:")
    print("-" * 40)
    with_email = EmailDecorator(BasicNotifier())
    with_email.send("Servidor reiniciado")
    
    # --- Dos decoradores apilados ---
    print("\n[3] Notificador con Email + SMS:")
    print("-" * 40)
    with_email_sms = SMSDecorator(
        EmailDecorator(BasicNotifier())
    )
    with_email_sms.send("Base de datos al 90%")
    
    # --- Tres decoradores apilados ---
    print("\n[4] Notificador con Email + SMS + Slack:")
    print("-" * 40)
    full_notifier = SlackDecorator(
        SMSDecorator(
            EmailDecorator(BasicNotifier())
        )
    )
    full_notifier.send("ALERTA: Servidor caido!")
    
    # --- La magia: el cliente no sabe cuantos decoradores hay ---
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Polimorfismo")
    print("=" * 60)
    
    def enviar_alerta(notifier: Notifier, mensaje: str):
        """
        Esta funcion no sabe si recibe un BasicNotifier o uno
        con 10 decoradores apilados. Solo llama a send().
        """
        print(f"\n    Enviando: '{mensaje}'")
        notifier.send(mensaje)
    
    print("\n[5] Misma funcion, diferentes configuraciones:")
    
    # Configuracion simple
    simple = BasicNotifier()
    enviar_alerta(simple, "Test simple")
    
    # Configuracion completa
    completo = SlackDecorator(
        SMSDecorator(
            EmailDecorator(
                BasicNotifier(),
                email="admin@empresa.com"
            ),
            phone="+34 666 777 888"
        ),
        channel="#emergencias"
    )
    enviar_alerta(completo, "Test completo")
    
    # --- Orden de los decoradores importa ---
    print("\n" + "=" * 60)
    print("NOTA: El orden de los decoradores importa")
    print("=" * 60)
    print("""
    SlackDecorator(SMSDecorator(EmailDecorator(BasicNotifier())))
    
    Ejecuta en este orden:
    1. Slack envia
    2. SMS envia
    3. Email envia
    4. Log (BasicNotifier)
    
    El decorador MAS EXTERNO ejecuta PRIMERO.
    """)
    
    """
    =========================================================================
    VENTAJAS DEL PATRON DECORATOR
    =========================================================================
    1. FLEXIBILIDAD: Combinas funcionalidades sin crear subclases
    
    2. PRINCIPIO ABIERTO/CERRADO: Nuevos decoradores sin tocar codigo existente
    
    3. RESPONSABILIDAD UNICA: Cada decorador tiene una sola responsabilidad
    
    4. DINAMICO: Puedes añadir/quitar decoradores en tiempo de ejecucion
    """


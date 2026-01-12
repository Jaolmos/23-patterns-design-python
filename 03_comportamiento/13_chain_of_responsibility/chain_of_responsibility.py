"""
PATRON CHAIN OF RESPONSIBILITY - Sistema de Soporte Tecnico

Analogia: Un sistema de escalamiento en soporte tecnico. Cuando llamas al
soporte, primero te atiende un agente basico. Si no puede resolver tu problema,
te pasa a un especialista. Si tampoco puede, va al supervisor. Y si el problema
es critico, llega al gerente. Cada nivel intenta resolver o pasa al siguiente.

PROBLEMA: Tienes multiples objetos que pueden procesar una solicitud, pero
no sabes cual debe manejarla. No quieres acoplar el emisor con el receptor
especifico. Quieres que varios objetos tengan la oportunidad de procesar
la solicitud en orden.

SOLUCION: Crear una cadena de manejadores donde cada uno decide si procesa
la solicitud o la pasa al siguiente. Cada manejador tiene referencia al
siguiente en la cadena. El cliente solo envia la solicitud al primer manejador.

VENTAJA: Desacopla el emisor del receptor. Añades o reordenas manejadores
facilmente. Cada manejador se enfoca en su responsabilidad especifica.
Flexibilidad para decidir quien procesa que.

Conceptos OOP usados:
- Herencia: Todos los manejadores heredan de Handler base
- Composicion: Cada manejador CONTIENE referencia al siguiente
- Polimorfismo: El cliente no sabe que manejador concreto procesa
- Encapsulacion: Cada manejador encapsula su logica de decision
"""

from abc import ABC, abstractmethod
from enum import Enum


# =============================================================================
# ENUMS: Niveles de complejidad de tickets
# =============================================================================

class Priority(Enum):
    """Niveles de complejidad de un ticket de soporte."""
    LOW = "Baja"        # Consultas simples
    MEDIUM = "Media"    # Problemas tecnicos
    HIGH = "Alta"       # Problemas criticos
    CRITICAL = "Critica"  # Emergencias que afectan todo el sistema


# =============================================================================
# MODELO: Ticket de soporte
# =============================================================================

class SupportTicket:
    """
    Representa un ticket de soporte tecnico.
    Contiene descripcion, prioridad y categoria del problema.
    """
    
    def __init__(self, ticket_id: str, description: str, priority: Priority):
        self.ticket_id = ticket_id
        self.description = description
        self.priority = priority
    
    def __str__(self) -> str:
        return f"Ticket #{self.ticket_id} [{self.priority.value}]: {self.description}"


# =============================================================================
# HANDLER BASE: Define la interfaz y la cadena
# =============================================================================

class SupportHandler(ABC):
    """
    Handler base abstracto.
    Define la cadena (next) y el metodo abstracto para procesar tickets.
    """
    
    def __init__(self):
        # Composicion: cada handler CONTIENE referencia al siguiente
        self._next_handler = None
    
    def set_next(self, handler: 'SupportHandler') -> 'SupportHandler':
        """
        Establece el siguiente handler en la cadena.
        Retorna el handler para permitir encadenamiento fluido.
        """
        self._next_handler = handler
        return handler  # Permite hacer: h1.set_next(h2).set_next(h3)
    
    def handle(self, ticket: SupportTicket) -> None:
        """
        Metodo template que primero intenta procesar,
        si no puede, pasa al siguiente en la cadena.
        """
        # Intenta procesar este nivel
        if self._can_handle(ticket):
            self._process(ticket)
        # Si no puede y hay siguiente, delega
        elif self._next_handler:
            print(f"  [{self.__class__.__name__}] Escalando al siguiente nivel...")
            self._next_handler.handle(ticket)
        # Si no puede y no hay siguiente, no se procesa
        else:
            print(f"  [{self.__class__.__name__}] ⚠️  Ticket no pudo ser procesado (fin de cadena)")
    
    @abstractmethod
    def _can_handle(self, ticket: SupportTicket) -> bool:
        """Decide si este handler puede procesar el ticket."""
        pass
    
    @abstractmethod
    def _process(self, ticket: SupportTicket) -> None:
        """Procesa el ticket (logica especifica de cada handler)."""
        pass


# =============================================================================
# HANDLERS CONCRETOS: Cada nivel de soporte
# =============================================================================

class Level1Support(SupportHandler):
    """
    Nivel 1: Soporte basico.
    Maneja consultas simples y de baja prioridad.
    """
    
    def _can_handle(self, ticket: SupportTicket) -> bool:
        # Solo maneja tickets de baja prioridad
        return ticket.priority == Priority.LOW
    
    def _process(self, ticket: SupportTicket) -> None:
        print(f"  [Nivel 1 - Agente Basico] ✅ Resolviendo: {ticket.description}")
        print(f"    → Respuesta: 'Consulte nuestra seccion de FAQ o reinicie el sistema'")


class Level2Support(SupportHandler):
    """
    Nivel 2: Soporte especializado.
    Maneja problemas tecnicos de complejidad media.
    """
    
    def _can_handle(self, ticket: SupportTicket) -> bool:
        # Maneja tickets de prioridad media
        return ticket.priority == Priority.MEDIUM
    
    def _process(self, ticket: SupportTicket) -> None:
        print(f"  [Nivel 2 - Especialista] ✅ Resolviendo: {ticket.description}")
        print(f"    → Analizando logs, verificando configuracion...")
        print(f"    → Problema identificado y solucionado")


class SupervisorSupport(SupportHandler):
    """
    Nivel 3: Supervisor.
    Maneja problemas criticos que requieren experiencia senior.
    """
    
    def _can_handle(self, ticket: SupportTicket) -> bool:
        # Maneja tickets de alta prioridad
        return ticket.priority == Priority.HIGH
    
    def _process(self, ticket: SupportTicket) -> None:
        print(f"  [Nivel 3 - Supervisor] ✅ Resolviendo: {ticket.description}")
        print(f"    → Coordinando con equipo de ingenieria...")
        print(f"    → Aplicando hotfix y monitoreando")


class ManagerSupport(SupportHandler):
    """
    Nivel 4: Gerente.
    Maneja emergencias criticas que afectan todo el sistema.
    """
    
    def _can_handle(self, ticket: SupportTicket) -> bool:
        # Maneja tickets de prioridad critica
        return ticket.priority == Priority.CRITICAL
    
    def _process(self, ticket: SupportTicket) -> None:
        print(f"  [Nivel 4 - GERENTE] 🚨 EMERGENCIA: {ticket.description}")
        print(f"    → Activando protocolo de crisis")
        print(f"    → Movilizando todo el equipo tecnico")
        print(f"    → Comunicando a clientes y stakeholders")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON CHAIN OF RESPONSIBILITY - Sistema de Soporte Tecnico")
    print("=" * 70)
    
    # --- Construir la cadena ---
    print("\n[PASO 1] Construyendo cadena de responsabilidad:")
    print("-" * 70)
    
    # Crear los handlers
    level1 = Level1Support()
    level2 = Level2Support()
    supervisor = SupervisorSupport()
    manager = ManagerSupport()
    
    # Enlazar la cadena: Level1 → Level2 → Supervisor → Manager
    # El metodo set_next() retorna el handler para encadenar
    level1.set_next(level2).set_next(supervisor).set_next(manager)
    
    print("  Cadena creada: Nivel 1 → Nivel 2 → Supervisor → Gerente")
    
    # --- Crear diferentes tickets ---
    tickets = [
        SupportTicket("001", "¿Como cambio mi contraseña?", Priority.LOW),
        SupportTicket("002", "La aplicacion no carga mis datos", Priority.MEDIUM),
        SupportTicket("003", "El servidor de produccion esta caido", Priority.HIGH),
        SupportTicket("004", "Brecha de seguridad detectada - datos comprometidos", Priority.CRITICAL),
    ]
    
    # --- Procesar tickets ---
    print("\n[PASO 2] Procesando tickets a traves de la cadena:")
    print("=" * 70)
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\n[Ticket {i}] {ticket}")
        print("-" * 70)
        # Todos los tickets entran por el nivel 1
        # La cadena decide quien lo procesa
        level1.handle(ticket)
    
    # --- Demostrar flexibilidad de la cadena ---
    print("\n" + "=" * 70)
    print("[PASO 3] Demostrar flexibilidad: Cambiar el orden de la cadena")
    print("=" * 70)
    
    print("\n¿Que pasa si quitamos el Nivel 2?")
    print("  Nueva cadena: Nivel 1 → Supervisor → Gerente")
    print("-" * 70)
    
    # Reconstruir sin nivel 2
    level1_alt = Level1Support()
    supervisor_alt = SupervisorSupport()
    manager_alt = ManagerSupport()
    level1_alt.set_next(supervisor_alt).set_next(manager_alt)
    
    # Intentar procesar un ticket de prioridad MEDIUM
    ticket_medium = SupportTicket("005", "Problema de conexion intermitente", Priority.MEDIUM)
    print(f"\n{ticket_medium}")
    print("-" * 70)
    level1_alt.handle(ticket_medium)
    print("  ⚠️  Al no haber Nivel 2, nadie pudo manejarlo")
    
    # --- Demostrar patron desde diferente punto ---
    print("\n" + "=" * 70)
    print("[PASO 4] Iniciar cadena desde otro punto (saltar Nivel 1)")
    print("=" * 70)
    
    print("\nSi sabemos que es un problema complejo, podemos iniciar en Nivel 2:")
    print("-" * 70)
    ticket_tech = SupportTicket("006", "Error de base de datos", Priority.MEDIUM)
    print(f"\n{ticket_tech}")
    print("-" * 70)
    # Iniciar directamente desde nivel 2
    level2.handle(ticket_tech)
    
    """
    =========================================================================
    VENTAJAS DEL PATRON CHAIN OF RESPONSIBILITY
    =========================================================================
    1. DESACOPLAMIENTO: El emisor no necesita conocer quien procesa
    
    2. FLEXIBILIDAD: Puedes añadir/quitar/reordenar handlers facilmente
    
    3. RESPONSABILIDAD UNICA: Cada handler se enfoca en su criterio
    
    4. OPEN/CLOSED: Añades nuevos handlers sin modificar los existentes
    
    5. CONTROL DE FLUJO: El cliente solo interactua con el primer handler
    
    CUANDO USARLO:
    - Multiples objetos pueden manejar una solicitud
    - El handler no se conoce de antemano
    - Quieres enviar solicitud a uno de varios objetos sin especificar cual
    - El conjunto de handlers debe asignarse dinamicamente
    
    EJEMPLOS REALES:
    - Sistemas de soporte (como este)
    - Middleware en frameworks web (Express, Django)
    - Event bubbling en interfaces graficas
    - Filtros de peticiones HTTP
    - Validadores de formularios
    - Procesamiento de logs por niveles
    """


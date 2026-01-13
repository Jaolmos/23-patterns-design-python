"""
PATRON MEMENTO - Configuracion de Aplicacion

Analogia: Como los puntos de restauracion de Windows. Guardas el estado completo
del sistema en un momento dado (un memento). Si algo sale mal, puedes restaurar
ese punto guardado y volver al estado anterior sin conocer los detalles internos.

PROBLEMA: Necesitas guardar y restaurar el estado de un objeto sin violar su
encapsulacion. No puedes exponer los detalles internos del objeto, pero necesitas
capturar su estado completo.

SOLUCION: El objeto (Originator) crea un Memento que contiene una instantanea
de su estado interno. Un Caretaker guarda los mementos pero no puede ver ni
modificar su contenido. Para restaurar, el Originator recibe el Memento y
recupera su estado.

VENTAJA: Preserva encapsulacion. Simplifica el Originator (no tiene que gestionar
versiones). Puedes implementar deshacer/rehacer facilmente.

Conceptos OOP usados:
- Encapsulacion: El Memento oculta los detalles del estado
- Composicion: Caretaker contiene lista de Mementos
- Inmutabilidad: Los Mementos no deben modificarse despues de crearse
"""

from typing import List
from datetime import datetime


# =============================================================================
# MEMENTO: Almacena el estado del Originator
# =============================================================================

class ConfigurationMemento:
    """
    Memento: Guarda una instantanea del estado de la configuracion.
    Es inmutable - una vez creado no puede modificarse.
    """

    def __init__(self, theme: str, language: str, notifications: bool, volume: int, timestamp: str):
        # Encapsulacion: el memento guarda el estado internamente
        # Estado guardado (privado, no debe modificarse - inmutable)
        self._theme = theme
        self._language = language
        self._notifications = notifications
        self._volume = volume
        self._timestamp = timestamp

    def get_state(self) -> dict[str, str | bool | int]:
        """Retorna el estado guardado. Solo el Originator deberia usarlo."""
        return {
            "theme": self._theme,
            "language": self._language,
            "notifications": self._notifications,
            "volume": self._volume
        }

    def get_timestamp(self) -> str:
        """Retorna cuando fue creado este memento."""
        return self._timestamp


# =============================================================================
# ORIGINATOR: El objeto cuyo estado queremos guardar/restaurar
# =============================================================================

class ApplicationConfig:
    """
    Originator: La configuracion de la aplicacion.
    Puede crear mementos de su estado y restaurarse desde un memento.
    """

    def __init__(self) -> None:
        # Estado actual de la configuracion
        self._theme = "light"
        self._language = "es"
        self._notifications = True
        self._volume = 50

    def set_theme(self, theme: str) -> None:
        """Cambia el tema de la aplicacion."""
        print(f"  [Config] Tema cambiado a: {theme}")
        self._theme = theme

    def set_language(self, language: str) -> None:
        """Cambia el idioma de la aplicacion."""
        print(f"  [Config] Idioma cambiado a: {language}")
        self._language = language

    def set_notifications(self, enabled: bool) -> None:
        """Activa/desactiva notificaciones."""
        status = "activadas" if enabled else "desactivadas"
        print(f"  [Config] Notificaciones {status}")
        self._notifications = enabled

    def set_volume(self, volume: int) -> None:
        """Ajusta el volumen."""
        print(f"  [Config] Volumen ajustado a: {volume}")
        self._volume = volume

    def save(self) -> ConfigurationMemento:
        """
        Crea un Memento con el estado actual.
        Guarda una instantanea que puede restaurarse despues.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"  [Config] Guardando configuracion... [{timestamp}]")
        return ConfigurationMemento(
            self._theme,
            self._language,
            self._notifications,
            self._volume,
            timestamp
        )

    def restore(self, memento: ConfigurationMemento) -> None:
        """
        Restaura el estado desde un Memento.
        Recupera la configuracion guardada.
        """
        state = memento.get_state()
        self._theme = state["theme"]
        self._language = state["language"]
        self._notifications = state["notifications"]
        self._volume = state["volume"]
        print(f"  [Config] Configuracion restaurada desde: {memento.get_timestamp()}")

    def show_config(self) -> None:
        """Muestra la configuracion actual."""
        notif_status = "SI" if self._notifications else "NO"
        print(f"\n  [Configuracion Actual]")
        print(f"    Tema: {self._theme}")
        print(f"    Idioma: {self._language}")
        print(f"    Notificaciones: {notif_status}")
        print(f"    Volumen: {self._volume}")


# =============================================================================
# CARETAKER: Gestiona los mementos (historial)
# =============================================================================

class ConfigurationHistory:
    """
    Caretaker: Guarda el historial de configuraciones (mementos).
    No conoce ni modifica el contenido de los mementos.
    """

    def __init__(self) -> None:
        # Composicion: el caretaker contiene lista de mementos
        self._history: list[ConfigurationMemento] = []

    def save(self, memento: ConfigurationMemento) -> None:
        """Guarda un memento en el historial."""
        self._history.append(memento)
        print(f"  [History] Configuracion guardada en historial (total: {len(self._history)})")

    def get(self, index: int) -> ConfigurationMemento | None:
        """Obtiene un memento especifico del historial."""
        if 0 <= index < len(self._history):
            return self._history[index]
        return None

    def get_latest(self) -> ConfigurationMemento | None:
        """Obtiene el memento mas reciente."""
        if self._history:
            return self._history[-1]
        return None

    def list_history(self) -> None:
        """Lista todo el historial de configuraciones."""
        print(f"\n  [Historial de Configuraciones] ({len(self._history)} versiones guardadas)")
        for i, memento in enumerate(self._history):
            print(f"    {i}. {memento.get_timestamp()}")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON MEMENTO - Configuracion de Aplicacion")
    print("=" * 70)

    # --- Crear configuracion e historial ---
    print("\n[PASO 1] Crear configuracion inicial")
    print("-" * 70)
    config = ApplicationConfig()
    history = ConfigurationHistory()
    config.show_config()

    # --- Guardar estado inicial ---
    print("\n[PASO 2] Guardar configuracion inicial")
    print("-" * 70)
    history.save(config.save())

    # --- Hacer cambios y guardar ---
    print("\n[PASO 3] Personalizar configuracion y guardar")
    print("-" * 70)
    config.set_theme("dark")
    config.set_language("en")
    config.set_volume(75)
    config.show_config()
    history.save(config.save())

    # --- Mas cambios ---
    print("\n[PASO 4] Hacer mas cambios y guardar")
    print("-" * 70)
    config.set_notifications(False)
    config.set_volume(100)
    config.set_theme("blue")
    config.show_config()
    history.save(config.save())

    # --- Ver historial ---
    print("\n[PASO 5] Ver historial de configuraciones")
    print("-" * 70)
    history.list_history()

    # --- Restaurar version anterior ---
    print("\n[PASO 6] Restaurar configuracion anterior (version 1)")
    print("-" * 70)
    print("  Restaurando...")
    config.restore(history.get(1))
    config.show_config()

    # --- Restaurar version inicial ---
    print("\n[PASO 7] Restaurar configuracion inicial (version 0)")
    print("-" * 70)
    print("  Restaurando...")
    config.restore(history.get(0))
    config.show_config()

    # --- Hacer nuevos cambios despues de restaurar ---
    print("\n[PASO 8] Nuevos cambios y guardar nueva version")
    print("-" * 70)
    config.set_theme("dark")
    config.set_language("fr")
    config.show_config()
    history.save(config.save())

    # --- Ver historial final ---
    print("\n[PASO 9] Historial final")
    print("-" * 70)
    history.list_history()

    """
    =========================================================================
    VENTAJAS DEL PATRON MEMENTO
    =========================================================================
    1. PRESERVA ENCAPSULACION: No expone detalles internos del Originator

    2. SIMPLIFICA ORIGINATOR: No tiene que gestionar historial de versiones

    3. DESHACER/REHACER: Implementacion facil de undo/redo

    4. PUNTOS DE RESTAURACION: Puedes guardar estados en momentos clave

    5. INMUTABILIDAD: Los mementos no se modifican, son seguros
    """

"""
PATRON STATE - Reproductor de Musica

Analogia: Como un reproductor de musica. Segun su estado (reproduciendo, pausado,
detenido), los botones hacen cosas diferentes. Si estas reproduciendo, el boton
play no hace nada, pero pause si. Si estas pausado, play reanuda, pero stop
detiene. El comportamiento cambia segun el estado actual.

PROBLEMA: Un objeto necesita cambiar su comportamiento cuando su estado interno
cambia. Usar muchos if/else para cada estado hace el codigo dificil de mantener
y extender.

SOLUCION: Encapsular cada estado en una clase separada. El objeto (Context)
delega el comportamiento al estado actual. Cuando el estado cambia, solo se
cambia el objeto estado.

VENTAJA: Elimina condicionales complejos. Cada estado encapsula su logica.
Facil agregar nuevos estados. Transiciones de estado explicitas.

Conceptos OOP usados:
- Abstraccion: Interfaz State con operaciones comunes
- Herencia: Estados concretos heredan de State
- Composicion: Context contiene referencia al estado actual
- Polimorfismo: Diferentes estados con misma interfaz
"""

from abc import ABC, abstractmethod


# =============================================================================
# STATE: Interfaz para los estados
# =============================================================================

class PlayerState(ABC):
    """
    Interfaz State: Define las operaciones que cada estado debe implementar.
    """

    @abstractmethod
    def play(self, player: 'MusicPlayer') -> None:
        """Accion al presionar play."""
        pass

    @abstractmethod
    def pause(self, player: 'MusicPlayer') -> None:
        """Accion al presionar pause."""
        pass

    @abstractmethod
    def stop(self, player: 'MusicPlayer') -> None:
        """Accion al presionar stop."""
        pass

    @abstractmethod
    def get_status(self) -> str:
        """Obtiene el nombre del estado."""
        pass


# =============================================================================
# ESTADOS CONCRETOS
# =============================================================================

class PlayingState(PlayerState):
    """
    Estado concreto: Reproduciendo musica.
    """

    def play(self, player: 'MusicPlayer') -> None:
        """Ya esta reproduciendo, no hace nada."""
        print("  [Playing] Ya esta reproduciendo")

    def pause(self, player: 'MusicPlayer') -> None:
        """Pausa la reproduccion."""
        print("  [Playing -> Paused] Pausando musica")
        player.set_state(PausedState())

    def stop(self, player: 'MusicPlayer') -> None:
        """Detiene la reproduccion."""
        print("  [Playing -> Stopped] Deteniendo musica")
        player.set_state(StoppedState())

    def get_status(self) -> str:
        return "REPRODUCIENDO"


class PausedState(PlayerState):
    """
    Estado concreto: Musica pausada.
    """

    def play(self, player: 'MusicPlayer') -> None:
        """Reanuda la reproduccion."""
        print("  [Paused -> Playing] Reanudando musica")
        player.set_state(PlayingState())

    def pause(self, player: 'MusicPlayer') -> None:
        """Ya esta pausado, no hace nada."""
        print("  [Paused] Ya esta pausado")

    def stop(self, player: 'MusicPlayer') -> None:
        """Detiene la reproduccion."""
        print("  [Paused -> Stopped] Deteniendo musica")
        player.set_state(StoppedState())

    def get_status(self) -> str:
        return "PAUSADO"


class StoppedState(PlayerState):
    """
    Estado concreto: Reproductor detenido.
    """

    def play(self, player: 'MusicPlayer') -> None:
        """Inicia la reproduccion desde el principio."""
        print("  [Stopped -> Playing] Iniciando reproduccion")
        player.set_state(PlayingState())

    def pause(self, player: 'MusicPlayer') -> None:
        """No se puede pausar si esta detenido."""
        print("  [Stopped] No se puede pausar, esta detenido")

    def stop(self, player: 'MusicPlayer') -> None:
        """Ya esta detenido, no hace nada."""
        print("  [Stopped] Ya esta detenido")

    def get_status(self) -> str:
        return "DETENIDO"


# =============================================================================
# CONTEXT: El reproductor de musica
# =============================================================================

class MusicPlayer:
    """
    Context: El reproductor que mantiene el estado actual.
    Delega las acciones al estado actual.
    """

    def __init__(self, song: str):
        self._song = song
        self._state: PlayerState = StoppedState()  # Estado inicial
        print(f"[Reproductor] Cancion cargada: '{self._song}'")

    def set_state(self, state: PlayerState) -> None:
        """Cambia el estado del reproductor."""
        self._state = state

    def play(self) -> None:
        """Delega la accion al estado actual."""
        print(f"\n[Reproductor] Presionando PLAY...")
        self._state.play(self)

    def pause(self) -> None:
        """Delega la accion al estado actual."""
        print(f"\n[Reproductor] Presionando PAUSE...")
        self._state.pause(self)

    def stop(self) -> None:
        """Delega la accion al estado actual."""
        print(f"\n[Reproductor] Presionando STOP...")
        self._state.stop(self)

    def show_status(self) -> None:
        """Muestra el estado actual."""
        print(f"  Estado actual: {self._state.get_status()}")
        print(f"  Cancion: {self._song}")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("PATRON STATE - Reproductor de Musica")
    print("=" * 70)

    # --- Crear reproductor ---
    print("\n[PASO 1] Crear reproductor de musica")
    print("-" * 70)
    player = MusicPlayer("Bohemian Rhapsody - Queen")
    player.show_status()

    # --- Intentar pausar cuando esta detenido ---
    print("\n[PASO 2] Intentar pausar (esta detenido)")
    print("-" * 70)
    player.pause()
    player.show_status()

    # --- Reproducir ---
    print("\n[PASO 3] Reproducir musica")
    print("-" * 70)
    player.play()
    player.show_status()

    # --- Intentar reproducir de nuevo ---
    print("\n[PASO 4] Intentar reproducir de nuevo (ya esta reproduciendo)")
    print("-" * 70)
    player.play()
    player.show_status()

    # --- Pausar ---
    print("\n[PASO 5] Pausar musica")
    print("-" * 70)
    player.pause()
    player.show_status()

    # --- Reanudar ---
    print("\n[PASO 6] Reanudar reproduccion")
    print("-" * 70)
    player.play()
    player.show_status()

    # --- Detener ---
    print("\n[PASO 7] Detener musica")
    print("-" * 70)
    player.stop()
    player.show_status()

    # --- Intentar detener de nuevo ---
    print("\n[PASO 8] Intentar detener de nuevo (ya esta detenido)")
    print("-" * 70)
    player.stop()
    player.show_status()

    # --- Reproducir desde detenido ---
    print("\n[PASO 9] Reproducir desde estado detenido")
    print("-" * 70)
    player.play()
    player.show_status()

    """
    =========================================================================
    VENTAJAS DEL PATRON STATE
    =========================================================================
    1. ELIMINA CONDICIONALES: No necesitas if/else para cada estado

    2. ENCAPSULACION: Cada estado encapsula su propia logica

    3. FACIL EXTENSION: Agregar nuevos estados sin modificar existentes

    4. TRANSICIONES EXPLICITAS: Los cambios de estado son claros

    5. RESPONSABILIDAD UNICA: Cada clase estado se enfoca en un comportamiento
    """

"""
PATRON ADAPTER
==============
Convierte la interfaz de una clase en otra interfaz que el cliente espera.
Permite que clases con interfaces incompatibles trabajen juntas.

Analogia: Un adaptador de enchufe. Tienes un dispositivo con clavija
europea pero el enchufe es americano. El adaptador hace compatible ambos.

PROBLEMA: Tienes clases con metodos diferentes (play_mp3, play_wav) pero
tu codigo espera una interfaz comun (play). No puedes cambiar las clases
originales porque vienen de librerias externas.

SOLUCION: Crear un adaptador que envuelve la clase incompatible y expone
la interfaz que el cliente espera.

VENTAJA: Puedes usar codigo antiguo o de terceros sin modificarlo. Solo
creas un adaptador que traduce las llamadas.
"""

from abc import ABC, abstractmethod


# =============================================================================
# INTERFAZ TARGET: La interfaz que el cliente espera
# =============================================================================

class MediaPlayer(ABC):
    """
    Interfaz que el cliente espera.
    Todos los reproductores deberian tener un metodo play().
    """
    
    @abstractmethod
    def play(self, filename):
        """Reproduce un archivo."""
        pass


# =============================================================================
# CLASES INCOMPATIBLES: Reproductores con interfaces diferentes
# =============================================================================

class MP3Player:
    """
    Reproductor MP3 de una libreria externa.
    Usa el metodo play_mp3() en lugar de play().
    """
    
    def play_mp3(self, filename):
        """Metodo especifico de MP3Player."""
        print(f"[MP3Player] Reproduciendo MP3: {filename}")


class WAVPlayer:
    """
    Reproductor WAV de otra libreria.
    Usa el metodo play_wav() en lugar de play().
    """
    
    def play_wav(self, filename):
        """Metodo especifico de WAVPlayer."""
        print(f"[WAVPlayer] Reproduciendo WAV: {filename}")


class FLACPlayer:
    """
    Reproductor FLAC de otra libreria.
    Usa el metodo play_flac() en lugar de play().
    """
    
    def play_flac(self, filename):
        """Metodo especifico de FLACPlayer."""
        print(f"[FLACPlayer] Reproduciendo FLAC: {filename}")


# =============================================================================
# ADAPTERS: Envuelven las clases incompatibles
# =============================================================================

class MP3Adapter(MediaPlayer):
    """
    Adaptador para MP3Player.
    Implementa MediaPlayer pero internamente usa MP3Player.
    """
    
    def __init__(self):
        # Composicion: el adapter CONTIENE el reproductor original
        self.mp3_player = MP3Player()
    
    def play(self, filename):
        """
        Implementa play() como espera el cliente.
        Internamente llama a play_mp3() del reproductor original.
        """
        self.mp3_player.play_mp3(filename)


class WAVAdapter(MediaPlayer):
    """
    Adaptador para WAVPlayer.
    Implementa MediaPlayer pero internamente usa WAVPlayer.
    """
    
    def __init__(self):
        # Composicion: el adapter CONTIENE el reproductor original
        self.wav_player = WAVPlayer()
    
    def play(self, filename):
        """
        Implementa play() como espera el cliente.
        Internamente llama a play_wav() del reproductor original.
        """
        self.wav_player.play_wav(filename)


class FLACAdapter(MediaPlayer):
    """
    Adaptador para FLACPlayer.
    Implementa MediaPlayer pero internamente usa FLACPlayer.
    """
    
    def __init__(self):
        # Composicion: el adapter CONTIENE el reproductor original
        self.flac_player = FLACPlayer()
    
    def play(self, filename):
        """
        Implementa play() como espera el cliente.
        Internamente llama a play_flac() del reproductor original.
        """
        self.flac_player.play_flac(filename)


# =============================================================================
# CLIENTE: Codigo que usa la interfaz MediaPlayer
# =============================================================================

class AudioApp:
    """
    Aplicacion de audio que usa reproductores.
    Solo conoce la interfaz MediaPlayer, no los reproductores especificos.
    """
    
    def __init__(self):
        self.players = []
    
    def add_player(self, player: MediaPlayer):
        """Agrega un reproductor (cualquiera que implemente MediaPlayer)."""
        self.players.append(player)
    
    def play_all(self, filename):
        """Reproduce un archivo con todos los reproductores."""
        print(f"\nReproduciendo '{filename}' con todos los reproductores:")
        for player in self.players:
            player.play(filename)  # Llama a play() sin importar el tipo real


# =============================================================================
# DEMOSTRACION DEL PATRON
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DEMOSTRACION DEL PATRON ADAPTER")
    print("=" * 60)
    
    # Crear la aplicacion
    app = AudioApp()
    
    # Agregar reproductores adaptados
    print("\n[1] Agregando reproductores a la app:")
    app.add_player(MP3Adapter())
    app.add_player(WAVAdapter())
    app.add_player(FLACAdapter())
    print("    - MP3Adapter agregado")
    print("    - WAVAdapter agregado")
    print("    - FLACAdapter agregado")
    
    # Usar la aplicacion (no sabe que tipo de reproductor es cada uno)
    print("\n[2] Usando la aplicacion:")
    app.play_all("cancion.mp3")
    
    # Demostracion individual
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Uso individual")
    print("=" * 60)
    
    print("\n[3] Usando cada reproductor individualmente:")
    
    # El codigo cliente solo conoce MediaPlayer
    players = [
        MP3Adapter(),
        WAVAdapter(),
        FLACAdapter()
    ]
    
    for player in players:
        player.play("audio_file")  # Misma interfaz para todos
    
    """
    =========================================================================
    SIN ADAPTER: El problema original
    =========================================================================
    Sin adapter, tendrias que hacer esto:
    
    mp3 = MP3Player()
    mp3.play_mp3("file.mp3")      # Metodo diferente
    
    wav = WAVPlayer()
    wav.play_wav("file.wav")      # Otro metodo diferente
    
    flac = FLACPlayer()
    flac.play_flac("file.flac")   # Otro metodo diferente
    
    No puedes tratarlos de forma uniforme!
    
    =========================================================================
    VENTAJAS DEL PATRON ADAPTER
    =========================================================================
    1. INTERFAZ UNIFORME: Todos usan play(), facil de usar
    
    2. NO MODIFICA CODIGO ORIGINAL: MP3Player, WAVPlayer, FLACPlayer
       no se tocan (pueden ser de librerias externas)
    
    3. PRINCIPIO ABIERTO/CERRADO: Abierto a extension (nuevos adapters)
       cerrado a modificacion (no cambias codigo existente)
    
    4. REUTILIZACION: Puedes usar codigo antiguo con APIs nuevas
    """


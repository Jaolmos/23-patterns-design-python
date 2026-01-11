"""
PATRON BRIDGE - Dispositivos y Controles Remotos

PROBLEMA: Tienes abstracciones (controles) e implementaciones (dispositivos)
que crecen de forma independiente. Sin Bridge, necesitarias una clase por
cada combinacion: ControlBasicoTV, ControlBasicoRadio, ControlAvanzadoTV...

SOLUCION: Separar la abstraccion (Control) de la implementacion (Dispositivo)
usando composicion. El control TIENE un dispositivo, no ES un dispositivo.

VENTAJA: Puedes agregar nuevos controles O nuevos dispositivos sin modificar
el codigo existente. Ambas jerarquias evolucionan independientemente.

Conceptos OOP usados:
- Composicion: El control CONTIENE una referencia al dispositivo
- Herencia: Para crear variantes de controles y dispositivos
- Interfaces (ABC): Para definir contratos de dispositivos
"""

from abc import ABC, abstractmethod


# =============================================================================
# IMPLEMENTACION (Implementation) - Los dispositivos
# =============================================================================

class Device(ABC):
    """
    Interfaz de implementacion.
    Define las operaciones que todos los dispositivos deben tener.
    """
    
    @abstractmethod
    def is_enabled(self) -> bool:
        """Retorna si el dispositivo esta encendido."""
        pass
    
    @abstractmethod
    def enable(self):
        """Enciende el dispositivo."""
        pass
    
    @abstractmethod
    def disable(self):
        """Apaga el dispositivo."""
        pass
    
    @abstractmethod
    def get_volume(self) -> int:
        """Retorna el volumen actual (0-100)."""
        pass
    
    @abstractmethod
    def set_volume(self, volume: int):
        """Establece el volumen (0-100)."""
        pass
    
    @abstractmethod
    def get_channel(self) -> int:
        """Retorna el canal actual."""
        pass
    
    @abstractmethod
    def set_channel(self, channel: int):
        """Cambia al canal especificado."""
        pass


# =============================================================================
# IMPLEMENTACIONES CONCRETAS - Tipos de dispositivos
# =============================================================================

class TV(Device):
    """
    Implementacion concreta: Television.
    """
    
    def __init__(self):
        self._enabled = False
        self._volume = 30
        self._channel = 1
    
    def is_enabled(self) -> bool:
        return self._enabled
    
    def enable(self):
        self._enabled = True
        print("[TV] Encendida")
    
    def disable(self):
        self._enabled = False
        print("[TV] Apagada")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, volume: int):
        # Limitar volumen entre 0 y 100
        self._volume = max(0, min(100, volume))
        print(f"[TV] Volumen: {self._volume}")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int):
        self._channel = channel
        print(f"[TV] Canal: {self._channel}")


class Radio(Device):
    """
    Implementacion concreta: Radio.
    """
    
    def __init__(self):
        self._enabled = False
        self._volume = 20
        self._channel = 88  # Frecuencia FM
    
    def is_enabled(self) -> bool:
        return self._enabled
    
    def enable(self):
        self._enabled = True
        print("[Radio] Encendida")
    
    def disable(self):
        self._enabled = False
        print("[Radio] Apagada")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, volume: int):
        self._volume = max(0, min(100, volume))
        print(f"[Radio] Volumen: {self._volume}")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int):
        # Frecuencias FM tipicas: 88-108
        self._channel = channel
        print(f"[Radio] Frecuencia: {self._channel} FM")


class SmartTV(Device):
    """
    Implementacion concreta: Smart TV con funciones adicionales.
    """
    
    def __init__(self):
        self._enabled = False
        self._volume = 25
        self._channel = 1
        self._apps = ["Netflix", "YouTube", "Prime Video"]
    
    def is_enabled(self) -> bool:
        return self._enabled
    
    def enable(self):
        self._enabled = True
        print("[SmartTV] Encendida - Cargando sistema...")
    
    def disable(self):
        self._enabled = False
        print("[SmartTV] Apagada")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, volume: int):
        self._volume = max(0, min(100, volume))
        print(f"[SmartTV] Volumen: {self._volume}")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int):
        self._channel = channel
        print(f"[SmartTV] Canal: {self._channel}")
    
    # Metodo adicional especifico de SmartTV
    def open_app(self, app_name: str):
        if app_name in self._apps:
            print(f"[SmartTV] Abriendo {app_name}...")
        else:
            print(f"[SmartTV] App '{app_name}' no disponible")


# =============================================================================
# ABSTRACCION (Abstraction) - El control remoto base
# =============================================================================

class RemoteControl:
    """
    Abstraccion base: Control remoto.
    
    COMPOSICION: El control CONTIENE un dispositivo (no hereda de el).
    Esto permite que cualquier control funcione con cualquier dispositivo.
    """
    
    def __init__(self, device: Device):
        # Composicion: guardamos referencia al dispositivo
        self._device = device
    
    def toggle_power(self):
        """Enciende o apaga el dispositivo."""
        if self._device.is_enabled():
            self._device.disable()
        else:
            self._device.enable()
    
    def volume_up(self):
        """Sube el volumen en 10 unidades."""
        current = self._device.get_volume()
        self._device.set_volume(current + 10)
    
    def volume_down(self):
        """Baja el volumen en 10 unidades."""
        current = self._device.get_volume()
        self._device.set_volume(current - 10)
    
    def channel_up(self):
        """Sube un canal."""
        current = self._device.get_channel()
        self._device.set_channel(current + 1)
    
    def channel_down(self):
        """Baja un canal."""
        current = self._device.get_channel()
        self._device.set_channel(current - 1)


# =============================================================================
# ABSTRACCIONES REFINADAS - Variantes del control
# =============================================================================

class AdvancedRemote(RemoteControl):
    """
    Abstraccion refinada: Control avanzado con funciones extra.
    Hereda de RemoteControl y agrega funcionalidades.
    """
    
    def mute(self):
        """Silencia el dispositivo."""
        self._device.set_volume(0)
        print("[Control Avanzado] Silenciado")
    
    def set_channel_direct(self, channel: int):
        """Cambia directamente a un canal especifico."""
        self._device.set_channel(channel)
    
    def show_info(self):
        """Muestra informacion del dispositivo."""
        status = "Encendido" if self._device.is_enabled() else "Apagado"
        print(f"[Control Avanzado] Estado: {status}")
        print(f"[Control Avanzado] Volumen: {self._device.get_volume()}")
        print(f"[Control Avanzado] Canal: {self._device.get_channel()}")


class SmartRemote(RemoteControl):
    """
    Abstraccion refinada: Control inteligente para Smart TV.
    Puede acceder a funciones especificas si el dispositivo las tiene.
    """
    
    def open_app(self, app_name: str):
        """Abre una aplicacion si el dispositivo lo soporta."""
        # Verificamos si el dispositivo tiene el metodo open_app
        if hasattr(self._device, 'open_app'):
            self._device.open_app(app_name)
        else:
            print("[Control Smart] Este dispositivo no soporta aplicaciones")
    
    def voice_command(self, command: str):
        """Simula un comando de voz."""
        print(f"[Control Smart] Comando de voz: '{command}'")
        # Aqui iria la logica de procesamiento de voz
        if "encender" in command.lower():
            self._device.enable()
        elif "apagar" in command.lower():
            self._device.disable()


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PATRON BRIDGE - Dispositivos y Controles Remotos")
    print("=" * 60)
    
    # --- Ejemplo 1: Control basico con TV ---
    print("\n--- Ejemplo 1: Control Basico + TV ---")
    tv = TV()
    control_basico = RemoteControl(tv)
    
    control_basico.toggle_power()  # Enciende
    control_basico.volume_up()     # Sube volumen
    control_basico.channel_up()    # Sube canal
    control_basico.toggle_power()  # Apaga
    
    # --- Ejemplo 2: Control avanzado con Radio ---
    print("\n--- Ejemplo 2: Control Avanzado + Radio ---")
    radio = Radio()
    control_avanzado = AdvancedRemote(radio)
    
    control_avanzado.toggle_power()       # Enciende
    control_avanzado.set_channel_direct(95)  # Frecuencia directa
    control_avanzado.volume_up()
    control_avanzado.show_info()          # Muestra estado
    control_avanzado.mute()               # Silencia
    
    # --- Ejemplo 3: Control smart con SmartTV ---
    print("\n--- Ejemplo 3: Control Smart + SmartTV ---")
    smart_tv = SmartTV()
    control_smart = SmartRemote(smart_tv)
    
    control_smart.toggle_power()
    control_smart.open_app("Netflix")     # Abre app
    control_smart.voice_command("subir volumen")
    control_smart.volume_up()
    
    # --- Ejemplo 4: Flexibilidad del Bridge ---
    print("\n--- Ejemplo 4: El mismo control con diferentes dispositivos ---")
    print("\nControl avanzado controlando TV:")
    control_avanzado_tv = AdvancedRemote(TV())
    control_avanzado_tv.toggle_power()
    control_avanzado_tv.show_info()
    
    print("\nControl avanzado controlando Radio:")
    control_avanzado_radio = AdvancedRemote(Radio())
    control_avanzado_radio.toggle_power()
    control_avanzado_radio.show_info()
    
    # --- Ejemplo 5: Control smart con dispositivo no compatible ---
    print("\n--- Ejemplo 5: Control Smart con dispositivo no compatible ---")
    control_smart_radio = SmartRemote(Radio())
    control_smart_radio.toggle_power()
    control_smart_radio.open_app("Netflix")  # No soportado en Radio
    
    # --- Resumen de ventajas ---
    print("\n" + "=" * 60)
    print("VENTAJAS DEL PATRON BRIDGE")
    print("=" * 60)
    print("""
    1. INDEPENDENCIA: Abstraccion e implementacion evolucionan por separado
       (puedes agregar nuevos controles sin tocar dispositivos y viceversa)
    
    2. PRINCIPIO ABIERTO/CERRADO: Abierto a extension, cerrado a modificacion
       (nuevos controles o dispositivos sin cambiar codigo existente)
    
    3. PRINCIPIO DE RESPONSABILIDAD UNICA: El control se enfoca en la logica
       de alto nivel, el dispositivo en los detalles de implementacion
    
    4. FLEXIBILIDAD EN TIEMPO DE EJECUCION: Puedes cambiar el dispositivo
       de un control sin recrear el control
    """)
    
    print("=" * 60)
    print("FIN DE LA DEMOSTRACION")
    print("=" * 60)


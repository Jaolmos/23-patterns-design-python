"""
PATRON FLYWEIGHT - Productos en Tienda Online

Analogia: Una biblioteca. Los libros fisicos (datos pesados) estan en las
estanterias y se comparten. Cada usuario tiene una ficha de prestamo (contexto)
que dice que libro tiene, pero el libro en si es uno solo compartido.

PROBLEMA: Tienes miles de objetos similares en memoria. Cada carrito de compra
tiene productos con imagen, descripcion, precio... multiplicado por miles de
usuarios consume mucha memoria.

SOLUCION: Separar datos compartidos (flyweight/intrinseco) de datos unicos
(contexto/extrinseco). Los datos pesados se almacenan una sola vez y se
referencian desde multiples lugares.

VENTAJA: Reduces drasticamente el uso de memoria cuando tienes muchos objetos
similares. Ideal para catalogos, inventarios, sistemas con datos repetidos.

Conceptos OOP usados:
- Composicion: CartItem CONTIENE referencia a Product
- Factory: ProductCatalog gestiona y reutiliza los flyweights
"""


# =============================================================================
# FLYWEIGHT: Datos compartidos (pesados, intrinsecos)
# =============================================================================

class Product:
    """
    Flyweight: Representa los datos compartidos de un producto.
    Estos datos son "pesados" (imagen, descripcion) y se comparten
    entre todos los usuarios que tengan este producto.
    """
    
    def __init__(self, product_id: str, name: str, description: str, 
                 image_url: str, base_price: float):
        # Datos intrinsecos (compartidos, no cambian por usuario)
        self.product_id = product_id
        self.name = name
        self.description = description  # Texto largo, pesado
        self.image_url = image_url      # Referencia a imagen, pesado
        self.base_price = base_price
    
    def display_info(self):
        """Muestra informacion del producto."""
        print(f"    ID: {self.product_id}")
        print(f"    Nombre: {self.name}")
        print(f"    Precio: ${self.base_price:.2f}")
        print(f"    Imagen: {self.image_url}")


# =============================================================================
# CONTEXTO: Datos unicos (ligeros, extrinsecos)
# =============================================================================

class CartItem:
    """
    Contexto: Representa un item en el carrito de un usuario.
    Contiene datos unicos (cantidad, usuario) y una referencia
    al producto compartido (flyweight).
    """
    
    def __init__(self, product: Product, quantity: int, user_id: str):
        # Referencia al flyweight (compartido)
        self.product = product
        # Datos extrinsecos (unicos por cada item)
        self.quantity = quantity
        self.user_id = user_id
    
    def get_total(self) -> float:
        """Calcula el total de este item."""
        return self.product.base_price * self.quantity
    
    def display(self):
        """Muestra el item del carrito."""
        print(f"  [{self.user_id}] {self.quantity}x {self.product.name} = ${self.get_total():.2f}")


# =============================================================================
# FLYWEIGHT FACTORY: Gestiona y reutiliza los flyweights
# =============================================================================

class ProductCatalog:
    """
    Flyweight Factory: Gestiona los productos (flyweights).
    Asegura que cada producto se cree una sola vez y se reutilice.
    """
    
    def __init__(self):
        # Cache de productos creados
        self._products: dict[str, Product] = {}
    
    def get_product(self, product_id: str, name: str = "", 
                    description: str = "", image_url: str = "", 
                    base_price: float = 0) -> Product:
        """
        Obtiene un producto del catalogo.
        Si no existe, lo crea. Si ya existe, lo reutiliza.
        """
        if product_id not in self._products:
            # Crear nuevo producto (solo la primera vez)
            print(f"[Catalogo] Creando nuevo producto: {product_id}")
            self._products[product_id] = Product(
                product_id, name, description, image_url, base_price
            )
        else:
            # Reutilizar producto existente
            print(f"[Catalogo] Reutilizando producto: {product_id}")
        
        return self._products[product_id]
    
    def get_product_count(self) -> int:
        """Retorna cuantos productos unicos hay en memoria."""
        return len(self._products)
    
    def list_products(self):
        """Lista todos los productos en el catalogo."""
        print(f"\n[Catalogo] Productos en memoria: {len(self._products)}")
        for product_id, product in self._products.items():
            print(f"    - {product_id}: {product.name}")


# =============================================================================
# DEMOSTRACION
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("PATRON FLYWEIGHT - Productos en Tienda Online")
    print("=" * 60)
    
    # Crear el catalogo (factory)
    print("\n[1] Creando catalogo de productos:")
    catalog = ProductCatalog()
    
    # Agregar productos al catalogo
    print("\n[2] Registrando productos en el catalogo:")
    catalog.get_product(
        "SHIRT-001", 
        "Camiseta Azul", 
        "Camiseta de algodon 100%, talla M, color azul marino",
        "images/shirts/blue_shirt.jpg",
        29.99
    )
    catalog.get_product(
        "PANTS-001",
        "Pantalon Negro",
        "Pantalon casual de vestir, talla 32, color negro",
        "images/pants/black_pants.jpg",
        49.99
    )
    catalog.get_product(
        "SHOES-001",
        "Zapatillas Deportivas",
        "Zapatillas running con amortiguacion, talla 42",
        "images/shoes/running_shoes.jpg",
        89.99
    )
    
    # Simular carritos de varios usuarios
    print("\n[3] Creando carritos de usuarios (reutilizando productos):")
    print("-" * 50)
    
    # Usuario Ana quiere camiseta y pantalon
    cart_ana = [
        CartItem(catalog.get_product("SHIRT-001"), quantity=2, user_id="ana"),
        CartItem(catalog.get_product("PANTS-001"), quantity=1, user_id="ana"),
    ]
    
    # Usuario Luis quiere camiseta y zapatillas
    cart_luis = [
        CartItem(catalog.get_product("SHIRT-001"), quantity=1, user_id="luis"),
        CartItem(catalog.get_product("SHOES-001"), quantity=1, user_id="luis"),
    ]
    
    # Usuario Maria quiere solo camisetas
    cart_maria = [
        CartItem(catalog.get_product("SHIRT-001"), quantity=5, user_id="maria"),
    ]
    
    # Mostrar carritos
    print("\n[4] Contenido de los carritos:")
    print("-" * 50)
    
    print("\nCarrito de Ana:")
    for item in cart_ana:
        item.display()
    
    print("\nCarrito de Luis:")
    for item in cart_luis:
        item.display()
    
    print("\nCarrito de Maria:")
    for item in cart_maria:
        item.display()
    
    # Demostrar que comparten el mismo objeto
    print("\n" + "=" * 60)
    print("DEMOSTRACION: Los productos son el MISMO objeto")
    print("=" * 60)
    
    print("\n[5] Verificando que los productos se comparten:")
    shirt_ana = cart_ana[0].product
    shirt_luis = cart_luis[0].product
    shirt_maria = cart_maria[0].product
    
    print(f"    Camiseta de Ana   ID: {id(shirt_ana)}")
    print(f"    Camiseta de Luis  ID: {id(shirt_luis)}")
    print(f"    Camiseta de Maria ID: {id(shirt_maria)}")
    print(f"\n    Son el mismo objeto? {shirt_ana is shirt_luis is shirt_maria}")
    
    # Mostrar ahorro de memoria
    print("\n[6] Ahorro de memoria:")
    catalog.list_products()
    
    total_cart_items = len(cart_ana) + len(cart_luis) + len(cart_maria)
    print(f"\n    Items totales en carritos: {total_cart_items}")
    print(f"    Productos en memoria: {catalog.get_product_count()}")
    print(f"    Sin Flyweight: {total_cart_items} objetos Product")
    print(f"    Con Flyweight: {catalog.get_product_count()} objetos Product")
    
    """
    =========================================================================
    VENTAJAS DEL PATRON FLYWEIGHT
    =========================================================================
    1. AHORRO DE MEMORIA: Datos pesados se almacenan una sola vez
    
    2. RENDIMIENTO: Menos objetos = menos trabajo para el garbage collector
    
    3. CONSISTENCIA: Todos ven los mismos datos del producto
    
    4. ESCALABILIDAD: Puedes tener miles de referencias sin multiplicar memoria
    """


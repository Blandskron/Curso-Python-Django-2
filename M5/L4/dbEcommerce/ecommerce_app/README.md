## Uso del sistema (ejemplos reales)

Esta aplicación se opera mediante **CLI** (`python main.py <comando>`).
La lógica crítica de negocio (stock, historial, validaciones) se ejecuta **en la base de datos** mediante funciones y triggers; Python actúa como orquestador.

---

### A) Inicialización de la base de datos (solo la primera vez)

Crea todas las tablas, funciones, triggers y vistas necesarias.
El proceso es **idempotente**: si ya está inicializado, no recrea ni elimina datos.

```bash
python main.py init-db
```

**Resultado esperado:**

* Esquema creado
* Automatizaciones activas
* Migraciones registradas internamente

---

### B) Creación de datos básicos (catálogo y clientes)

Crear una categoría:

```bash
python main.py create-category --name "Electrónica"
```

Crear un cliente:

```bash
python main.py create-customer \
  --first-name "Ana" \
  --last-name "Pérez" \
  --email "ana@correo.com"
```

Crear un producto asociado a una categoría:

```bash
python main.py create-product \
  --category-id 1 \
  --name "Mouse" \
  --price 9990 \
  --description "Mouse USB"
```

---

### C) Carga de stock inicial

Registra una entrada de inventario (movimiento `IN`).

```bash
python main.py stock-in \
  --product-id 1 \
  --quantity 10 \
  --reference "INIT"
```

> El stock disponible se calcula dinámicamente en la base de datos mediante `fn_stock_available`.

---

### D) Flujo de venta: crear orden → agregar ítems → pagar

Crear una orden:

```bash
python main.py create-order --customer-id 1
python main.py add-item --order-id 10 --product-id 1 --quantity 2
python main.py add-item --order-id 10 --product-id 3 --quantity 1
python main.py pay-order --order-id 10

```

Agregar un producto a la orden:

```bash
python main.py add-item \
  --order-id 1 \
  --product-id 1 \
  --quantity 2
```

Pagar la orden:

```bash
python main.py pay-order --order-id 1
```

**Qué ocurre al pagar:**

* Se valida stock disponible en la base de datos
* Se descuenta inventario automáticamente
* Se registra el historial de estados
* Todo ocurre dentro de una transacción segura

❌ **Si el stock es insuficiente**, la base de datos lanza una excepción y Python mostrará:

```
ERROR al pagar: Stock insuficiente para producto X
```

---

### E) Cancelación de una orden

Cancela una orden.
Si la orden estaba pagada, el stock se **restaura automáticamente** (operación idempotente).

```bash
python main.py cancel-order --order-id 1
```

---

### F) Consultas y reportes

Ver productos visibles (activos y con stock disponible):

```bash
python main.py visible-products
```

Ver resumen de ventas (solo órdenes pagadas):

```bash
python main.py sales-summary
```

Ver detalle completo de una orden (estado, ítems e historial):

```bash
python main.py order-info --order-id 1
```

---

### Notas importantes

* Python **no recalcula stock** ni replica reglas de negocio
  → la **base de datos es la fuente de verdad**
* Todas las operaciones críticas usan transacciones
* El sistema es seguro ante reinicios, reintentos y errores parciales

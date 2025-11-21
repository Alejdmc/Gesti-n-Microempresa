"""
Descripción:
 - Integración con Supabase (Postgres)
 - QuickSort optimizado (pivote aleatorio) + MergeSort + BubbleSort
 - Métricas empíricas por algoritmo (comparaciones, intercambios, recursión)
 - Busqueda Binaria(búsqueda en lista ordenada por nombre)
 - Reposición greedy
 - Promedio móvil
 - Exportación CSV y logging
"""

from supabase import create_client, Client
import time
import copy
import random
import csv
import logging
from typing import List, Dict, Any, Optional

# -----------------------
# Configuración logger
# -----------------------
logging.basicConfig(
    filename="sistema_inventario.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -----------------------
# Conexión Supabase
# -----------------------
url: str = "https://nsihoxbvamqppebocmki.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5zaWhveGJ2YW1xcHBlYm9jbWtpIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTkxMTIxOTIsImV4cCI6MjA3NDY4ODE5Mn0.sYaXyZNUZFgjItp496Ml-QHFkgR-ks6DA8FUYxuXb_0"

supabase: Client = create_client(url, key)


# -----------------------
# Clase principal
# -----------------------
class InventorySystem:
    def __init__(self, client: Client):
        self.client = client
        # métricas del último algoritmo ejecutado
        self.metrics = {
            "comparaciones": 0,
            "intercambios": 0,
            "llamadas_recursivas": 0
        }

    # -----------------------
    # Utilidades
    # -----------------------
    def _log_info(self, msg: str):
        logging.info(msg)
        print(msg)

    def _log_error(self, msg: str):
        logging.error(msg)
        print(msg)

    def probar_conexion(self, retry: int = 2) -> bool:
        attempt = 0
        while attempt <= retry:
            try:
                data = self.client.table("accesorios").select("*").limit(1).execute()
                if data.data is not None:
                    self._log_info("Conexión exitosa con Supabase")
                    return True
                else:
                    self._log_error("Conexión pero sin datos")
                    return True
            except Exception as e:
                self._log_error(f"Error al conectar con Supabase (intento {attempt}): {e}")
                attempt += 1
        return False

    def obtener_productos_raw(self) -> List[Dict[str, Any]]:
        #Obtiene los registros crudos desde Supabase y aplica limpieza básica."""
        try:
            res = self.client.table("accesorios").select("*").execute()
            productos = res.data or []
            # Validación: eliminar registros sin 'cantidad' o con cantidad negativa
            limpios = []
            for p in productos:
                cantidad = p.get("cantidad")
                nombre = p.get("nombre")
                if cantidad is None:
                    logging.warning(f"Registro ignorado por cantidad nula: {p}")
                    continue
                try:
                    cantidad_num = int(cantidad)
                except Exception:
                    logging.warning(f"Registro ignorado por tipo inválido de cantidad: {p}")
                    continue
                if cantidad_num < 0:
                    logging.warning(f"Registro ignorado por cantidad negativa: {p}")
                    continue
                # normalizar campo
                p["cantidad"] = cantidad_num
                p["nombre"] = nombre if nombre is not None else "SIN_NOMBRE"
                limpios.append(p)
            return limpios
        except Exception as e:
            self._log_error(f"Error al obtener productos: {e}")
            return []

    # -----------------------
    # MÉTRICAS
    # -----------------------
    def reset_metrics(self):
        self.metrics = {
            "comparaciones": 0,
            "intercambios": 0,
            "llamadas_recursivas": 0
        }

    # -----------------------
    # QuickSort (optimizado: pivot aleatorio)
    # -----------------------
    def quicksort(self, lista: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.reset_metrics()
        result = self._quicksort_recursive(lista)
        self._log_info(f"QuickSort métricas: {self.metrics}")
        return result

    def _quicksort_recursive(self, lista: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        n = len(lista)
        if n <= 1:
            return lista
        self.metrics["llamadas_recursivas"] += 1
        # Pivot aleatorio para evitar peor caso
        pivot_index = random.randrange(0, n)
        pivote = lista[pivot_index]['cantidad']
        menores, iguales, mayores = [], [], []
        for x in lista:
            self.metrics["comparaciones"] += 1
            if x['cantidad'] < pivote:
                menores.append(x)
            elif x['cantidad'] == pivote:
                iguales.append(x)
            else:
                mayores.append(x)
        return self._quicksort_recursive(menores) + iguales + self._quicksort_recursive(mayores)

    # -----------------------
    # MergeSort
    # -----------------------
    def mergesort(self, lista: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.reset_metrics()
        result = self._mergesort_recursive(lista)
        self._log_info(f"MergeSort métricas: {self.metrics}")
        return result

    def _mergesort_recursive(self, lista: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if len(lista) <= 1:
            return lista
        self.metrics["llamadas_recursivas"] += 1
        mitad = len(lista) // 2
        left = self._mergesort_recursive(lista[:mitad])
        right = self._mergesort_recursive(lista[mitad:])
        return self._merge(left, right)

    def _merge(self, left: List[Dict[str, Any]], right: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        i = j = 0
        resultado = []
        while i < len(left) and j < len(right):
            self.metrics["comparaciones"] += 1
            if left[i]['cantidad'] <= right[j]['cantidad']:
                resultado.append(left[i])
                i += 1
            else:
                resultado.append(right[j])
                j += 1
                self.metrics["intercambios"] += 1
        resultado.extend(left[i:])
        resultado.extend(right[j:])
        return resultado

    # -----------------------
    # BubbleSort
    # -----------------------
    def bubblesort(self, lista: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.reset_metrics()
        arr = lista.copy()
        n = len(arr)
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                self.metrics["comparaciones"] += 1
                if arr[j]['cantidad'] > arr[j + 1]['cantidad']:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.metrics["intercambios"] += 1
                    swapped = True
            if not swapped:
                break
        self._log_info(f"BubbleSort métricas: {self.metrics}")
        return arr

    # -----------------------
    # Busqueda binaria (por nombre)
    # -----------------------
    def binary_search_by_name(self, lista_sorted_by_name: List[Dict[str, Any]], target_name: str) -> Optional[Dict[str, Any]]:
        low, high = 0, len(lista_sorted_by_name) - 1
        while low <= high:
            mid = (low + high) // 2
            name_mid = lista_sorted_by_name[mid].get("nombre", "").lower()
            if name_mid == target_name.lower():
                return lista_sorted_by_name[mid]
            elif name_mid < target_name.lower():
                low = mid + 1
            else:
                high = mid - 1
        return None

    # -----------------------
    # Reposición Greedy
    # -----------------------
    def reposicion_greedy(self, productos: List[Dict[str, Any]], umbral: int = 10) -> List[Dict[str, Any]]:
        resultado = []
        for p in productos:
            if p["cantidad"] < umbral:
                resultado.append({
                    "nombre": p["nombre"],
                    "cantidad_actual": p["cantidad"],
                    "a_reponer": umbral - p["cantidad"]
                })
        return resultado

    # -----------------------
    # Forecast: Promedio Móvil simple (por producto)
    # Utiliza tabla detalle_ventas: agrupa por producto (accesorio_id) y fechas
    # -----------------------
    def moving_average_forecast(self, accessory_id: int, window: int = 3) -> Optional[float]:

        try:
            # Obtener historico de ventas por accessory_id
            res = self.client.table("detalle_ventas").select("venta_id, accesorio_id, cantidad_vendida").eq("accesorio_id", accessory_id).execute()
            ventas = res.data or []
            # Si no hay ventas, no hay forecast
            if not ventas:
                return None
            # Consideramos la serie de cantidades vendidas (orden original)
            cantidades = [int(v["cantidad_vendida"]) for v in ventas]
            if len(cantidades) < 1:
                return None
            # Tomar último `window` valores
            ultima_ventana = cantidades[-window:]
            forecast = sum(ultima_ventana) / len(ultima_ventana)
            return forecast
        except Exception as e:
            self._log_error(f"Error en forecast: {e}")
            return None

    # -----------------------
    # Exportar CSV
    # -----------------------
    def export_to_csv(self, lista: List[Dict[str, Any]], filename: str = "export.csv"):
        if not lista:
            self._log_info("No hay datos para exportar.")
            return
        keys = lista[0].keys()
        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                dict_writer = csv.DictWriter(f, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(lista)
            self._log_info(f"Exportado correctamente a {filename}")
        except Exception as e:
            self._log_error(f"Error exportando CSV: {e}")

    # -----------------------
    # Comparación de algoritmos (tiempo real + métricas)
    # -----------------------
    def comparar_algoritmos(self):
        productos = self.obtener_productos_raw()
        if not productos:
            self._log_info("No hay productos para comparar.")
            return

        self._log_info("Iniciando comparación temporal y de métricas...")

        # QuickSort
        inicio = time.time()
        qs_sorted = self.quicksort(copy.deepcopy(productos))
        tiempo_qs = time.time() - inicio
        metrics_qs = copy.deepcopy(self.metrics)

        # MergeSort
        inicio = time.time()
        ms_sorted = self.mergesort(copy.deepcopy(productos))
        tiempo_ms = time.time() - inicio
        metrics_ms = copy.deepcopy(self.metrics)

        # BubbleSort
        inicio = time.time()
        bs_sorted = self.bubblesort(copy.deepcopy(productos))
        tiempo_bs = time.time() - inicio
        metrics_bs = copy.deepcopy(self.metrics)

        # Resumen
        resumen = [
            {"algoritmo": "QuickSort", "tiempo_s": tiempo_qs, **metrics_qs},
            {"algoritmo": "MergeSort", "tiempo_s": tiempo_ms, **metrics_ms},
            {"algoritmo": "BubbleSort", "tiempo_s": tiempo_bs, **metrics_bs},
        ]

        # Mostrar y exportar
        print("\n--- Resultados de comparación ---")
        for r in resumen:
            print(f"{r['algoritmo']}: {r['tiempo_s']:.6f} s | métricas: comps={r.get('comparaciones')} swaps={r.get('intercambios')} rec_calls={r.get('llamadas_recursivas')}")
        self.export_to_csv(resumen, filename="comparacion_algoritmos.csv")
        self._log_info("Comparación terminada y exportada.")

    # -----------------------
    # Operaciones del menú
    # -----------------------
    def mostrar_inventario(self):
        productos = self.obtener_productos_raw()
        print("\n--- Inventario de accesorios ---")
        for p in productos:
            print(f"{p['nombre']} - {p['cantidad']} unidades")

    def ordenar_por_cantidad_quick(self):
        productos = self.obtener_productos_raw()
        ordenados = self.quicksort(productos)
        print("\n--- Productos ordenados por cantidad (asc) ---")
        for p in ordenados:
            print(f"{p['nombre']} - {p['cantidad']}")

    def ordenar_por_cantidad_merge(self):
        productos = self.obtener_productos_raw()
        ordenados = self.mergesort(productos)
        print("\n--- Productos ordenados por cantidad (asc) MergeSort ---")
        for p in ordenados:
            print(f"{p['nombre']} - {p['cantidad']}")

    def ordenar_por_cantidad_bubble(self):
        productos = self.obtener_productos_raw()
        ordenados = self.bubblesort(productos)
        print("\n--- Productos ordenados por cantidad (asc) BubbleSort ---")
        for p in ordenados:
            print(f"{p['nombre']} - {p['cantidad']}")

    def detectar_bajo_stock(self, umbral: int = 10):
        productos = self.obtener_productos_raw()
        alerta = self.reposicion_greedy(productos, umbral=umbral)
        print("\n--- Productos a reponer ---")
        if not alerta:
            print("Todos los productos están en buen nivel de stock.")
        for p in alerta:
            print(f"{p['nombre']} → Faltan {p['a_reponer']} unidades (actual: {p['cantidad_actual']})")
        # exportar
        self.export_to_csv(alerta, filename="reposicion_alerta.csv")

    def buscar_producto_por_nombre(self, nombre: str):
        productos = self.obtener_productos_raw()
        # ordenar por nombre
        productos_sorted = sorted(productos, key=lambda x: x.get("nombre", "").lower())
        encontrado = self.binary_search_by_name(productos_sorted, nombre)
        if encontrado:
            print(f"Producto encontrado: {encontrado['nombre']} - {encontrado['cantidad']} unidades")
        else:
            print("Producto no encontrado.")

    def forecast_producto(self, accessory_id: int, window: int = 3):
        forecast = self.moving_average_forecast(accessory_id, window=window)
        if forecast is None:
            print("No es posible generar forecast para el producto (sin historial).")
        else:
            print(f"Forecast (promedio móvil, window={window}): {forecast:.2f} unidades")

    # -----------------------
    # Menú
    # -----------------------
    def menu(self):
        while True:
            print("\n=== SISTEMA DE GESTIÓN DE INVENTARIO ===")
            print("1. Mostrar inventario")
            print("2. Ordenar productos (QuickSort)")
            print("3. Ordenar productos (MergeSort)")
            print("4. Ordenar productos (BubbleSort)")
            print("5. Detectar productos con bajo stock (Greedy)")
            print("6. Comparar algoritmos (tiempo y métricas)")
            print("7. Buscar producto por nombre (Binary Search)")
            print("8. Forecast (promedio móvil) por accessory_id")
            print("9. Probar conexión a Supabase")
            print("10. Exportar inventario a CSV")
            print("11. Salir")

            opcion = input("Seleccione una opción: ").strip()

            if opcion == "1":
                self.mostrar_inventario()
            elif opcion == "2":
                self.ordenar_por_cantidad_quick()
            elif opcion == "3":
                self.ordenar_por_cantidad_merge()
            elif opcion == "4":
                self.ordenar_por_cantidad_bubble()
            elif opcion == "5":
                umbral = input("Ingrese umbral de reposición [10]: ").strip()
                try:
                    umbral = int(umbral) if umbral else 10
                except:
                    umbral = 10
                self.detectar_bajo_stock(umbral=umbral)
            elif opcion == "6":
                self.comparar_algoritmos()
            elif opcion == "7":
                nombre = input("Nombre exacto del producto: ").strip()
                self.buscar_producto_por_nombre(nombre)
            elif opcion == "8":
                aid = input("Accessory ID (accesorio_id) para forecast: ").strip()
                try:
                    aid = int(aid)
                    window = int(input("Window (número periodos) [3]: ").strip() or 3)
                    self.forecast_producto(aid, window=window)
                except:
                    print("ID inválido.")
            elif opcion == "9":
                self.probar_conexion()
            elif opcion == "10":
                productos = self.obtener_productos_raw()
                self.export_to_csv(productos, filename="inventario_export.csv")
            elif opcion == "11":
                print("Saliendo...")
                break
            else:
                print("Opción inválida, intente de nuevo.")


if __name__ == "__main__":
    sistema = InventorySystem(supabase)
    if sistema.probar_conexion():
        sistema.menu()
    else:
        print("No se pudo establecer conexión con Supabase. Verifique credenciales y red.")

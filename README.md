
# Sistema Gestión Microempresa

Este proyecto implementa un sistema básico de gestión de inventario para una microempresa dedicada a la venta de accesorios para celulares. Combina conceptos de bases de datos relacionales con análisis y diseño de algoritmos, integrando ambas asignaturas en una solución funcional que permite:
Consultar inventario en tiempo real desde Supabase.
Ordenar productos utilizando tres algoritmos clásicos (QuickSort, MergeSort y BubbleSort).
Detectar productos con bajo stock mediante un enfoque Greedy.
Comparar el rendimiento temporal de los algoritmos sobre datos reales del inventario.
El sistema está diseñado en Python y se conecta a una base de datos en Supabase que almacena la información del inventario de la microempresa.

Objetivos del Proyecto:

Implementar un sistema funcional que gestione el inventario de accesorios de celulares.
Aplicar algoritmos de ordenamiento y análisis de complejidad.
Integrar análisis algorítmico con un sistema real basado en base de datos.
Automatizar procesos clave como la reposición de productos.
Evaluar eficiencia en escenarios con datos reales.


Tecnologías Utilizadas
- Python 3.10+
- Supabase (PostgreSQL en la nube)
- API oficial de Supabase para Python
Librerías:
- supabase
- copy
- time

Funcionalidades:

✔ Mostrar inventario
Consulta todos los productos almacenados en la tabla accesorios.
✔ Ordenar productos (QuickSort)
Clasifica los productos según su cantidad en inventario (ascendente).
✔ Comparación de algoritmos
Evalúa y compara los tiempos de ejecución de:
QuickSort
MergeSort
BubbleSort
✔ Detección de bajo stock (Greedy)
Identifica productos por debajo de un umbral (10 unidades por defecto).
✔ Probar la conexión
Verifica conexión y lectura desde Supabase.

Algoritmos Implementados
- QuickSort — O(n log n)
Elegido como algoritmo principal por su eficiencia promedio y estabilidad en cargas moderadas.
- MergeSort — O(n log n)
Usado para comparación; eficiente pero requiere más memoria.
- BubbleSort — O(n²)
Incluido únicamente para efectos educativos y comparativos.
- Greedy de reposición — O(n)
Detecta rápidamente qué productos deben reponerse.

Estructura de la Base de Datos (Supabase)
Tabla: accesorios
Campo	Tipo	Descripción
id	integer	Identificador único
nombre	text	Nombre del accesorio
cantidad	integer	Stock disponible
precio	numeric	Precio de venta
categoria	text	Tipo de accesorio (fundas, cables…)

Ejecución del Proyecto
Clonar el repositorio:
git clone <URL_DEL_REPO>

Instalar dependencias:
pip install supabase

Actualizar las variables url y key del proyecto.
Ejecutar:
python main.py


Proyecto desarrollado por estudiantes de Ingeniería de Sistemas – 5° semestre, Bogotá, Colombia.

Licencia:
Este proyecto es de uso académico y no está diseñado para producción.
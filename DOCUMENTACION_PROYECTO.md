# Documentación del Proyecto

## 1. Descripción general

Este repositorio agrupa el material académico y práctico del bootcamp **Desarrollo de Aplicaciones Full Stack Python Trainee V2.0**. Incluye recursos de front-end, fundamentos de programación en Python, programación orientada a objetos, bases de datos y múltiples ejercicios aplicados distribuidos por módulos, lecciones y días.

## 2. Estructura real del repositorio

La organización principal observada en el proyecto es:

- `M2/`: contenidos de fundamentos de desarrollo front-end (HTML, CSS, JavaScript), ejercicios, retos y portafolio.
- `M3/`: fundamentos de programación en Python, ejercicios diarios, material PDF, proyecto final de módulo y ejemplos adicionales.
- `M4/`: programación avanzada en Python (POO, UML, excepciones, testing) y proyectos aplicados.
- `M5/`: contenidos de bases de datos relacionales, ejercicios por lección, reto y proyecto final de módulo.
- `README.md`: presentación general del bootcamp.
- `LICENSE`: licencia del repositorio.

## 3. Convención de carpetas y archivos

En gran parte del repositorio se utiliza una estructura tipo:

- `Lx/`: lección.
- `Dx/`: día o bloque temático dentro de la lección.
- `NN_python.py`: script numerado de ejercicios o ejemplos.
- `ejercicio_practico/`: actividad aplicada de la lección.
- Archivos `.pdf`: guía teórica o informe complementario.

## 4. Tipos de contenido incluidos

1. **Material teórico**
   - PDF de fundamentos, informes técnicos y apuntes por módulo.
2. **Prácticas guiadas**
   - Scripts cortos numerados para reforzar sintaxis, control de flujo, funciones, POO y manejo de errores.
3. **Ejercicios prácticos**
   - Carpetas específicas con mini proyectos y resoluciones.
4. **Proyectos finales por módulo**
   - Ejemplos integradores (por ejemplo, e-commerce en Python o ejercicios de arquitectura orientada a objetos).

## 5. Recomendaciones para navegar el repositorio

- Revisar primero los `README.md` locales dentro de carpetas de ejercicios para entender objetivos concretos.
- Avanzar en orden por módulo (`M2` a `M5`) y dentro de cada uno por lección (`L1`, `L2`, ...).
- Ejecutar scripts Python desde la raíz del repositorio o desde la carpeta del ejercicio para evitar rutas relativas incorrectas.
- Mantener un entorno virtual activo al probar contenidos que dependan de librerías externas.

## 6. Ejecución básica de scripts Python

Ejemplo general:

```bash
python3 M3/L1/D1/01_python.py
```

Para proyectos más grandes (por ejemplo, subcarpetas con `main.py`), ejecutar el archivo principal desde su carpeta:

```bash
cd M3/ejercicio_final
python3 main.py
```

## 7. Mantenimiento documental

Si se agregan nuevos módulos, lecciones o proyectos:

1. Actualizar este archivo con la nueva estructura real.
2. Mantener el `README.md` principal como portada breve.
3. Añadir `README.md` locales cuando un ejercicio o proyecto requiera instrucciones específicas.

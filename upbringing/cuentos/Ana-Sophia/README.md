# Doce armaduras para Ana-Sophia

Proyecto de cuento infantil personalizado en el que Ana-Sophia viaja a distintos
momentos de la historia y encarna a doce guerreras que existieron realmente.

La estética visual obligatoria y las reglas de continuidad del personaje se
encuentran en [`DIRECCION_ARTISTICA.md`](DIRECCION_ARTISTICA.md).

El estado consolidado está en [`HANDOFF.md`](HANDOFF.md) y la distribución del
trabajo en grupos de tres se encuentra en
[`PLAN_PERSONAJES.md`](PLAN_PERSONAJES.md).

## Flujo de trabajo

1. Escribir y revisar por separado el texto de cada guerrera.
2. Fijar los tres momentos visuales del capítulo.
3. Crear una ficha visual estable de Ana-Sophia.
4. Generar y aprobar las tres ilustraciones.
5. Maquetar texto e imágenes en dos páginas cuadradas.
6. Exportar cada página terminada como PNG/JPG en sRGB.
7. Exportar también el libro completo como PDF maestro.

## Estructura

- `01_textos/`: originales editables; una guerrera por archivo.
- `02_referencias/`: referencias históricas y visuales no privadas.
- `03_ilustraciones/`: ilustraciones originales sin texto incrustado.
- `04_paginas/`: páginas terminadas con imagen y texto.
- `05_impresion/`: PDF maestro, portada y archivos definitivos.

Las fotografías personales de Ana-Sophia se mantienen fuera del repositorio.

## Extensión objetivo por guerrera

- Presentación: 75-95 palabras.
- Momento histórico 1: 45-60 palabras.
- Momento histórico 2: 45-60 palabras.
- Frase de la armadura: 5-10 palabras.
- Total orientativo: 175-215 palabras.

Cada texto debe explicar tres cosas: cuál era el problema, qué hizo la guerrera
y por qué aquello fue importante. Se evitarán fechas y nombres que no ayuden a
comprender la historia.

## Prueba de concepto: Juana de Arco

La primera página aprobada se puede regenerar desde la raíz del repositorio con:

```powershell
python upbringing/cuentos/Ana-Sophia/tools/build_juana_page1.py
```

El PDF resultante se guarda en
`output/pdf/doce_armaduras_juana_pagina1_aprobada.pdf`.

La antigua maqueta de dos páginas se conserva únicamente como prueba anterior;
no representa la dirección visual aprobada.


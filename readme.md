# ORS4GHOST
![ORS4GHOST Banner](https://github.com/n0rs4rt/Ors4Ghost/blob/9ecdb6e94acf8a3853cbcb1136dee6e5133c5410/assets/ors4gosht.png)
Herramienta desarrollada en Python orientada a la ocultación estructurada de archivos y carpetas en sistemas Windows.

## Descripción

ORS4GHOST permite ocultar archivos y carpetas moviéndolos a una ubicación interna protegida dentro del sistema, evitando que sean visibles incluso cuando está activada la opción de mostrar archivos ocultos en Windows.

A diferencia de una ocultación básica, los elementos no permanecen en su ubicación original, sino que son reorganizados y gestionados internamente junto a metadatos que permiten su recuperación posterior.

## Importante

Esta herramienta no es un sistema de cifrado avanzado ni una solución de seguridad de alto nivel.

Está pensada para:

- Ocultar información de forma práctica
- Evitar acceso casual o visual
- Proteger contenido frente a usuarios sin conocimientos técnicos intermédios o avanzados

Un usuario con conocimientos intermedios o avanzados en sistemas operativos podría acceder a la información si sabe qué buscar.

[ Descargar última versión](https://github.com/n0rs4rt/)

## Características principales

- Ocultación de archivos y carpetas en una ubicación interna no visible
- No visibles mediante la opción estándar de "mostrar archivos ocultos" en Windows
- Compatible con almacenamiento local y dispositivos externos (USB, discos externos, etc.)
- Sistema de recuperación manual en caso de cambios en rutas o unidades
- Gestión automática de conflictos de nombres (evita sobrescritura)
- Registro de actividad (historial de elementos protegidos)
- Interfaz con autenticación de usuario

![ORS4GHOST funcion ](https://github.com/n0rs4rt/Ors4Ghost/blob/9ecdb6e94acf8a3853cbcb1136dee6e5133c5410/assets/Screenshot%202026-04-15%20070055.png)

## Sistema de usuario

- Solo se permite un usuario
- Contraseña protegida mediante hashing (no almacenada en texto plano)
- Clave de recuperación generada en el registro inicial
- Registro del último acceso al sistema
- Verificación básica de integridad de la base de datos

![ORS4GHOST Loggin](https://github.com/n0rs4rt/Ors4Ghost/blob/main/assets/Screenshot%202026-04-15%20070219.png)

## Funcionamiento general

Cuando un archivo o carpeta es protegido:

1. Se mueve a una carpeta interna oculta
2. Se almacena información asociada (metadatos)
3. Se registra en una base de datos para su gestión desde la interfaz

Para restaurar:

- Puede hacerse desde el registro (modo normal)
- O mediante recuperación manual seleccionando la ruta original

## Escenarios a tener en cuenta

Algunos escenarios comunes:

- Ruta original no disponible  
  Puede ocurrir si la carpeta fue movida, eliminada o si cambió la letra de unidad (por ejemplo en dispositivos externos).

- Elemento dentro de carpeta protegida  
  Si un archivo fue protegido y posteriormente su carpeta contenedora también fue protegida, será necesario desproteger primero la carpeta principal y luego restaurar el elemento interno.

- Archivo en uso  
  No se pueden proteger archivos que estén siendo utilizados por el sistema.

- Carpetas del sistema  
  No se permite proteger rutas críticas del sistema como Windows, Program Files etc.

## Registro de actividad

La aplicación muestra:

- Elementos protegidos
- Fecha de protección
- Ubicación original
- Actividad reciente

## Estado del proyecto

Proyecto funcional en fase de mejora continua.

Se prioriza:

- Estabilidad
- Manejo de errores
- Simplicidad de uso

## Código fuente

El código está disponible con fines educativos y de mejora.

Puedes:

- Analizarlo
- Adaptarlo
- Mejorarlo

En caso de redistribución o uso derivado, se solicita mantener el crédito al autor original.

## Licencia

Este proyecto está bajo la licencia MIT.

Autor: ORS4TECH (Nelson Arteaga)  
GitHub: https://github.com/n0rs4rt

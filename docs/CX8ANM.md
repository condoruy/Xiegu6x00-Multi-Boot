# Línea de prueba CX8ANM (`cx8anm-prueba`)

Fork de [TomekR1/Xiegu6x00-Multi-Boot](https://github.com/TomekR1/Xiegu6x00-Multi-Boot) (SQ6RT, GPL-3.0)
mantenido por CX8ANM. Lo probado en `cx8anm-prueba` está publicado en `main`: cada subida a `main` con un número
nuevo en `x6100mb/assets/versions.json` (`…-cx8anm.N`) saca una versión en Releases. Las ramas `cx8anm-*` se
compilan y prueban sin publicar.

## Qué es este proyecto (y qué no es)

No es un firmware para la radio. Es una **aplicación de PC** (Windows, macOS, Linux; Python + Tk) que
arma una tarjeta SD con **hasta 5 sistemas** y un **menú de arranque en U-Boot**: al encender, la radio
muestra los logos y se elige con F1–F5. También puede arrancar el sistema original de Xiegu desde la
eMMC y trae Doom como extra.

| | X6100-CX8ANM (1.0.x) | OpenX6X00-CX8ANM (1.1.x) | Multi-Boot (este fork) |
|---|---|---|---|
| Qué es | firmware (base IU1WXY ≤0.127) | firmware (base OpenX6X00 de Guru-RF) | app de PC que compone tarjetas |
| Corre en | la radio | la radio | la computadora (+ un U-Boot propio en la tarjeta) |
| Radios | X6100 | X6100 y X6200 | **solo X6100** por ahora |
| Idioma | español | español | polaco/inglés → **+ español en esta rama** |
| Relación | ya está en el catálogo de la app | ya está en el catálogo de la app (asset `-x6100-`) | — |

## Qué mejora para CX8ANM

- **Probar sin miedo**: CX8ANM 1.1.x, OpenX6X00 original y Xiegu de fábrica en la misma tarjeta;
  si una versión de prueba falla, F2 y arranca otra. Ideal para la rama `remoto` / versiones privadas
  (se agregan con **+ Imagen de tarjeta…**, sin publicarlas).
- **DATA por sistema**: cada sistema conserva sus ajustes, log QSO, WiFi, SSH y Bluetooth; la app
  hace copias `.zip` y las pasa a la tarjeta nueva.
- **Usuarios de la comunidad**: CX8ANM aparece en el catálogo con su logo; quien lo pruebe no pierde su
  sistema anterior.
- **U-Boot con pantalla**: el U-Boot del menú inicializa el panel ST7701S, algo que los U-Boot de las
  imágenes no hacen. Es reutilizable para un futuro menú propio.

## Qué empeora o hay que vigilar

- **Solo X6100**: el U-Boot, la matriz de teclas y la detección de imágenes son del X6100. Las imágenes
  `-x6200-` se ignoran a propósito.
- **Actualizaciones de imagen**: las actualizaciones OTA de CX8ANM (Ajustes → Info → Actualizar) son
  seguras porque solo cambian archivos del sistema propio. Pero cuando una versión pide **imagen nueva**
  (`image-required`), hay que rearmar la tarjeta con la app, no grabar la imagen suelta (eso borra el menú
  y los otros sistemas).
- **Espacio**: cada sistema ocupa su partición entera; con 5 sistemas conviene una tarjeta de 16 GB o más.
- **Arranque**: el menú suma de 0 a 15 s (configurable, `bm_secs` en `bootmenu.env`).
- **Logo en la radio**: OpenX6X00-CX8ANM todavía trae en `boot/logo.png` el logo de OpenX6X00; el
  catálogo de la app toma el logo cóndor de X6100-CX8ANM (dice "XIEGU X6100").

## Compatibilidad revisada en el código de CX8ANM 1.1.x

| Punto | Resultado |
|---|---|
| `S00adata` (crea/repara DATA) | Seguro: si hay una partición FAT32, solo revisa DATA; nunca crea particiones en una tarjeta multiarranque |
| `fstab` (`/dev/mmcblk0p3` en `/mnt`) | Funciona: con DATA por sistema, U-Boot reescribe el MBR para que la DATA de cada sistema sea siempre p3 |
| `x6100-update` (OTA) | Seguro: escribe archivos en el root propio (`ALLOWED`), nunca toca particiones |
| Raíz del sistema | La app arranca cada sistema con `root=/dev/mmcblk0pN`; CX8ANM no asume p2 en ningún script |
| Nombres de assets | `OpenX6X00-CX8ANM-x6100-vX.Y.Z-sdcard.img.zip` coincide con el patrón del catálogo |
| Bluetooth en Doom | La app ya declara CX8ANM compatible |

## X6200: qué haría falta

Revisado contra `AetherX6200Buildroot` (Guru-RF): el X6200 usa **el mismo SoC (Allwinner R16)**,
**el mismo panel** (JLT4013A / ST7701S, mismo SPI por software en PL7–PL10) y **la misma matriz de
teclas** (filas PG6–PG10, columnas PE11–PE17). Diferencias encontradas en el device tree:

- alimentación del panel/LCD en **PL4** (X6100: PD12);
- encoders: orden de pines de VFO y MFK distinto, y el MFK del X6200 tiene perilla interna extra;
- I²C0 por hardware en vez de i2c-gpio;
- eMMC con `mmc2-pwrseq` propio (afecta la entrada "Xiegu desde eMMC");
- `boot.cmd` de las imágenes X6200: `root=/dev/mmcblk0p2`, igual que el X6100.

Plan de port (requiere probar en un X6200 real, por eso no está en esta rama):

1. `uboot/`: defconfig y `.dts` del X6200 (PL4 para el LCD); compilar `u-boot-x6200-menu.bin` en CI.
2. Confirmar con la radio qué celdas de la matriz son F1–F5 en el panel del X6200 (`KEYS` en `compose.py`).
3. `catalog.py`: un modelo elegido en la app (X6100/X6200) que filtre los assets `-x6100-` / `-x6200-`.
4. `image.py`: detectar el modelo por el `.dtb` de cada imagen y no mezclar radios en una tarjeta.
5. Doom: compilar con los encoders del X6200.

## Qué trae esta rama

- **Español** en toda la app (`x6100mb/i18n_es.py`, 251 textos + la ayuda de Doom, con voseo como el firmware), elegible en el
  selector de idioma y automático en sistemas en español. Si falta algún texto, cae a inglés y luego a
  polaco. Los textos que muestra la radio en U-Boot van sin tildes (la fuente de la consola no las tiene).
- Prueba automática `tests/test_i18n_es.py`: todos los textos traducidos, mismas `{variables}`, textos de
  la radio en ASCII.
- Marca `x6100mb=<tecla>` en los bootargs de cada sistema: CX8ANM (rama `cx8anm-multiboot`) la lee y avisa que una imagen nueva va por la app.
- CI: las ramas `cx8anm-*` se compilan y prueban (apps de Windows/macOS/Linux en *Artifacts* de Actions),
  sin publicar.

## Cómo probar

1. GitHub → Actions → *Build* → la corrida de `cx8anm-prueba` → descargá el artifact de tu sistema
   (macOS en tu caso).
2. Abrí la app → arriba a la derecha **Idioma: Español**.
3. **+ Desde internet…** → CX8ANM (última) + OpenX6X00 + **+ Xiegu desde la eMMC**.
4. Partición DATA: **una por sistema**. **Grabar en la tarjeta** (o **Guardar como archivo .img…** y
   balenaEtcher).
5. En la radio: el menú, la cuenta regresiva ("Inicio F1 en 5 s"), F1–F3 y POWER.
6. Arrancar CX8ANM, cambiar un ajuste, apagar, arrancar OpenX6X00 y volver a CX8ANM: el ajuste debe seguir.
7. En CX8ANM: Ajustes → Info → Actualizar (OTA) y comprobar que el menú sigue después.

## Próximos pasos posibles

- Del lado de CX8ANM: avisar en la radio, cuando una versión pida imagen nueva y el sistema no está en
  p2 (`/proc/cmdline`), que hay que rearmar la tarjeta con Multi-Boot.
- Logo propio de CX8ANM 1.1.x en `OpenX6X00-CX8ANM/boot/logo.png` (vale para la radio y para el catálogo).
- Port al X6200 (arriba).
- Proponer el español a SQ6RT con un pull request, si querés que llegue a la versión oficial.

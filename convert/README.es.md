# convert.py :arrows_counterclockwise:

![Python](https://img.shields.io/badge/Lenguaje-Python-blue.svg)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green.svg)

[![README en inglés](https://img.shields.io/badge/lang-en-red.svg)](./README.md)

Convert es un script de Python que te permite traducir un archivo de
un formato a otro utilizando diferentes estrategias de lectura y escritura.

## :hammer_and_wrench: Instalación

Antes de usar el script, asegurate de tener Python instalado en tu sistema.
Luego, podés seguir estos pasos:

1. Cloná este repositorio:

```bash
git clone https://github.com/cientopolis/observatorioInmobiliario-ER-Evaluation
```

2. Ingresá al directorio del script para crear un entorno virtual:

```bash
cd observatorioInmobiliario-ER-Evaluation/convert
python -m venv .venv
source .venv/bin/activate
```

3. Instalá las dependencias del script:

```bash
pip install -r requirements.txt
```

## :rocket: Uso

Para ver la ayuda y opciones de uso, ejecuta:

```bash
python convert.py -h
```

Podés ejecutar el script de la siguiente manera

```bash
python convert.py -i <archivo_entrada> -o <archivo_salida> -d <datos_entrada> -r <lectura> -w <escritura>
```

- `-i`, `--input`: Especifica el archivo de entrada que deseas convertir.
- `-o`, `--output`: Especifica el archivo de salida donde se escribirá el
    resultado de la conversión. Si este archivo ya existe, se generará un error.
- `-d`, `--data`: Especifica el archivo con los datos de los IDs en el
    archivo de entrada.
- `-r`, `--reader`: Especifica el formato en el que leer el archivo de entrada.
- `-w`, `--writer`: Especifica el formato en el que escribir el archivo de salida.

## :chess_pawn: Estrategias Soportadas

El script admite las siguientes estrategias de lectura y escritura:

- `duke`: Estrategia compatible con el formato usado por [`Duke`](https://github.com/larsga/Duke/).
- `dedupe`: Estrategia compatible con el formato usado por [`Dedupe`](https://github.com/dedupeio/dedupe) en la función `write_training`.
- `jedai`: Estrategia de lectura y escritura compatible con el formato [`Jedai`](https://github.com/AI-team-UoA/pyJedAI/tree/main).

Estas estrategias son utilizadas para leer de un formato y escribir a otro.
Por ejemplo, -r duke y -w jedai lee un archivo de entrada en el formato de Duke
y lo traduce al formato de Jedai.

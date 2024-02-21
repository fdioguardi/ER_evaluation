# convert.py :arrows_counterclockwise:

![Python](https://img.shields.io/badge/Lenguaje-Python-blue.svg)
![Licencia](https://img.shields.io/badge/Licencia-MIT-green.svg)

[![README in spanish](https://img.shields.io/badge/lang-es-red.svg)](./README.es.md)

Convert is a Python script that allows you to translate a file
from one format to another using different reading and writing strategies.

## :hammer_and_wrench: Installation

Before using the script, make sure you have Python installed on your system.
Then, you can follow these steps:

1. Clone this repository:

```bash
git clone https://github.com/cientopolis/observatorioInmobiliario-ER-Evaluation
```

2. Navigate to the script directory and create a virtual environment:

```bash
cd observatorioInmobiliario-ER-Evaluation/convert
python -m venv .venv
source .venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

## :rocket: Usage

To see the help and usage options, run:

```bash
python convert.py -h
```

You can execute the script as follows:

```bash
python convert.py -i <input_file> -o <output_file> -d <data_file> -r <reader> -w <writer>
```

- `-i`, `--input`: Specifies the input file you want to convert.
- `-o`, `--output`: Specifies the output file where the conversion result
    will be written. If this file already exists, an error will be generated.
- `-d`, `--data`: Specifies the file with the IDs data in the input file.
- `-r`, `--reader`: Specifies the format to read the input file.
- `-w`, `--writer`: Specifies the format to write the output file.

## :chess_pawn: Supported Strategies

The script supports the following reading and writing strategies:

- `duke`: Strategy compatible with the format used by [`Duke`](https://github.com/larsga/Duke/).
- `dedupe`: Strategy compatible with the format used by [`Dedupe`](https://github.com/dedupeio/dedupe) in the `write_trainig` function.
- `jedai`: Strategy compatible with the format used by [`Jedai`](https://github.com/AI-team-UoA/pyJedAI/tree/main).

These strategies are used to read from one format and write to another.
For example, -r duke and -w jedai reads an input file in Duke format
and translates it to Jedai format.

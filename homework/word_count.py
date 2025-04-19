"""Taller evaluable"""

# pylint: disable=broad-exception-raised

import fileinput
import glob
import os.path
import time
import string
from itertools import groupby


#
# Escriba la funcion que  genere n copias de los archivos de texto en la
# carpeta files/raw en la carpeta files/input. El nombre de los archivos
# generados debe ser el mismo que el de los archivos originales, pero con
# un sufijo que indique el número de copia. Por ejemplo, si el archivo
# original se llama text0.txt, el archivo generado se llamará text0_1.txt,
# text0_2.txt, etc.
#
def copy_raw_files_to_input_folder(n):
    """Funcion copy_files"""
    if not os.path.exists("files/input"): # Verifica si la carpeta files/input existe
        os.makedirs("files/input") # Si no existe, la crea

    for file in glob.glob("files/raw/*"): # Busca todos los archivos en la carpeta files/raw
        for i in range(1,n+1): # Genera n copias de cada archivo
            # Copia el archivo original en la carpeta files/input con el sufijo _i
            with open (file, "r", encoding="utf-8") as f: 
                with open(
                    f"files/input/{os.path.basename(file).split('.')[0]}_{i}.txt", 
                      "w",
                      encoding="utf-8",
                      ) as f2: # Abre el nuevo archivo en modo escritura
                    # Abre el archivo original en modo lectura
                        f2.write(f.read()) # Escribe el contenido del archivo original en el nuevo archivo

        


#
# Escriba la función load_input que recive como parámetro un folder y retorna
# una lista de tuplas donde el primer elemento de cada tupla es el nombre del
# archivo y el segundo es una línea del archivo. La función convierte a tuplas
# todas las lineas de cada uno de los archivos. La función es genérica y debe
# leer todos los archivos de folder entregado como parámetro.
#
# Por ejemplo:
#   [
#     ('text0'.txt', 'Analytics is the discovery, inter ...'),
#     ('text0'.txt', 'in data. Especially valuable in ar...').
#     ...
#     ('text2.txt'. 'hypotheses.')
#   ]
#
def load_input(input_directory):
    """Funcion load_input"""

    sequence = []
    files = glob.glob(f"{input_directory}/*")
    with fileinput.input(files=files) as f:
        for line in f:
            sequence.append((fileinput.filename(), line))
    return sequence
#
# Escriba la función line_preprocessing que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). Esta función
# realiza el preprocesamiento de las líneas de texto,
#
def line_preprocessing(sequence):
    """Line Preprocessing"""
    
    sequence = [
        (key,value.translate(str.maketrans("", "", string.punctuation)).lower())
        for key, value in sequence
    ] # Elimina los signos de puntuacion y convierte a minusculas
    return sequence

#
# Escriba una función llamada maper que recibe una lista de tuplas de la
# función anterior y retorna una lista de tuplas (clave, valor). En este caso,
# la clave es cada palabra y el valor es 1, puesto que se está realizando un
# conteo.
#
#   [
#     ('Analytics', 1),
#     ('is', 1),
#     ...
#   ]
#
def mapper(sequence):
    """Mapper"""
    return [
        (word, 1) for _, value in sequence for word in value.split()
    ] # Separa las palabras y asigna el valor 1 a cada una de ellas

#
# Escriba la función shuffle_and_sort que recibe la lista de tuplas entregada
# por el mapper, y retorna una lista con el mismo contenido ordenado por la
# clave.
#
#   [
#     ('Analytics', 1),
#     ('Analytics', 1),
#     ...
#   ]
#
def shuffle_and_sort(sequence):
    """Shuffle and Sort"""
    sequence.sort(key=lambda x: x[0]) # Ordena la lista por la clave
    return sequence # Retorna la lista ordenada


#
# Escriba la función reducer, la cual recibe el resultado de shuffle_and_sort y
# reduce los valores asociados a cada clave sumandolos. Como resultado, por
# ejemplo, la reducción indica cuantas veces aparece la palabra analytics en el
# texto.
#
def reducer(sequence):
    """Reducer"""
    sequence = [
        (key, sum(1 for _ in group)) for key, group in groupby(sequence, key=lambda x: x[0])
    ] # Agrupa los elementos por clave y suma los valores asociados a cada clave
    return sequence # Retorna la lista reducida



#
# Escriba la función create_ouptput_directory que recibe un nombre de
# directorio y lo crea. Si el directorio existe, lo borra
#
def create_output_directory(output_directory):
    """Create Output Directory"""
    if os.path.exists(output_directory): # Verifica si el directorio existe
        for file in glob.glob(f"{output_directory}/*"): # Busca todos los archivos en el directorio
            os.remove(file) # Elimina los archivos en el directorio
    else:
        os.makedirs(output_directory) # Si no existe, lo crea
    
    return output_directory # Retorna el directorio creado



#
# Escriba la función save_output, la cual almacena en un archivo de texto
# llamado part-00000 el resultado del reducer. El archivo debe ser guardado en
# el directorio entregado como parámetro, y que se creo en el paso anterior.
# Adicionalmente, el archivo debe contener una tupla por línea, donde el primer
# elemento es la clave y el segundo el valor. Los elementos de la tupla están
# separados por un tabulador.
#
def save_output(output_directory, sequence):
    """Save Output"""
    # Crea el archivo part-00000 en el directorio de salida
    with open(f"{output_directory}/part-00000", "w", encoding="utf-8") as f:
        for key, value in sequence: # Itera sobre la lista de tuplas
            f.write(f"{key}\t{value}\n") # Escribe la clave y el valor separados por un tabulador
    




#
# La siguiente función crea un archivo llamado _SUCCESS en el directorio
# entregado como parámetro.
#
def create_marker(output_directory):
    """Create Marker"""
    with open(f"{output_directory}/_SUCCESS", "w", encoding="utf-8") as f:
        f.write("") # Crea el archivo _SUCCESS vacio
    return output_directory # Retorna el directorio creado


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
from pprint import pprint
def run_job(input_directory, output_directory):
    """Job"""
    sequence = load_input(input_directory) # Carga los archivos de texto
    sequence = line_preprocessing(sequence) # Preprocesa los archivos de texto
    sequence = mapper(sequence) # Mapea los archivos de texto
    sequence = shuffle_and_sort(sequence) # Ordena los archivos de texto
    sequence = reducer(sequence) # Reduce los archivos de texto
    create_output_directory(output_directory) # Crea el directorio de salida
    save_output(output_directory, sequence) # Guarda el resultado en el directorio de salida
    create_marker(output_directory) # Crea el archivo _SUCCESS


    pprint(sequence[:5]) # Muestra los primeros 5 elementos de la lista

if __name__ == "__main__":

    copy_raw_files_to_input_folder(n=1000)

    start_time = time.time()

    run_job(
        "files/input",
        "files/output",
    )

    end_time = time.time()
    print(f"Tiempo de ejecución: {end_time - start_time:.2f} segundos")

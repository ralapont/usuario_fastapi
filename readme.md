# Dos formas de ejecutar uvicorm
    1.- con el comando uvicorn main:app --reload
    2.- añadiendo en el fichero main.py las lineas
        if __name__ == '__main__':
            uvicorn.run("main:app", port=8000)

        y ejecutar python main.py
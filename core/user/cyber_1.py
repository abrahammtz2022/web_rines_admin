import zxcvbn

#Configurar la lista de contraseñas a evaluar
contraseñas = ["r2a0m0m5", "rrmm20aa05m"]

for contraseña in contraseñas:
    resultado = zxcvbn.password_strength(contraseña)
    print("{}: puntuacion {}, entropia {} bits".format(contraseña, resultado["score"], resultado["guesses_log10"]))
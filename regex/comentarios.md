# Comentarios REGEX
## Ejemplos
- `^\d{3}-\d{2}$` permite hacer match con los strings que tengan al principio 3 dígitos, un guión y le sigan dos dígitos.
    * Se hace match con `123-12` o `000-00`
    * No se hace match con `00-000` (antes del guión hay solo dos dígitos) o `a11-11` (hay un caracter que no es un dígito)
- `^[A-Z]\w*$` permite hacer match con los strings que tengan al principio una letra mayúscula (del abecedario inglés) y le siga una cantidad variable (de largo 0 o más) de caracteres alfanuméricos. 
    * Se hace match con `Javiera`, `J` o `Javi3ra`
    * No se hace match con ` ` o `javiera`

- Si nos piden hacer una expresióni regular que represente un nombre de usuario que termine con caracteres númericos y un `_uc`, una expresión regular posible es `^\w+\d+_uc$`

- Si nos piden implementar una expresión regular para filtrar formatos de rut válidos, revisar `ejemplo_2.py`
syntax = {
    "\"Hola \" + \"mundo\"":
    "Operaciones con strings",
    "'Hola ' + 'mundo'":
    "Operaciones con strings de cadena simple",
    "1 + 3":
    "Operaciones con números enteros",
    "0.3 + .5":
    "Operaciones con números flotantes",
    "true != false":
    "Operaciones con booleanos",
    "[\"Hola\", 1, 4.65]":
    "Arrays",
    "{\"hola\": \"mundo\"}":
    "Objects",
    "('Heya', \"bruh\", 5, 1, true)":
    "Tuples",
    "set <var_name>":
    "Así se definirán variables sin contenido",
    "<var_name> = \"Hola\"":
    "Si defines una variable sin contenido, se lo puedes poner después de esta forma",
    "set <var_name> = 'Hola'":
    "Así se definirán variables con contenido",
    "null == null":
    "El valor null",
    """if <element> <operator> <element> then
           ...
       endif""":
    "La declaración if normal",
    """if true then
           ...
       endif""":
    "Podemos crear ifs sin ninguna condicional",
    """if !false then
           ...
       endif""":
    "Usamos '!' para decir que es lo contrario a el valor siguiente, en este caso como es false, pasará a true",
    "!-5":
    "El signo de negación también se puede usar con con números para cambiarlos de negativo a positivo y vice versa",
    """if <element> <operator> <element> then
           ...
       elseif <element> <operator> <element> then
           ...
       else
           ...
       endif""":
    "Declaración if más avanzada con elseif y else",
    """while <element> <operator> <element>
           ...
       endwhile""":
    "el ciclo while :D",
    """do this
           ...
       while <element> <operator> <element>""":
    "DoWhile Hace algo antes de evaluar la condición para seguir con el bucle o terminarlo",
    """while <conditional>
           ...
           break
        endwhile""":
    "Para terminar un bucle usamos break",
    """for set <var_name> = <value> <operator> <element>
           ...
       endfor""":
    "Será como los for de java 'for (i = 0; i < 9; i++)'",
    """for each <element> in <element>
           ...
       endfor""":
    "Será como el for de python",
    """makeFunc <func_name>(<arguments>) then
           ...
       endfunc""":
    "Definiendo funciones",
    """set <func_name> = (<arguments>) then
           ...
       endfunc""":
    "definiendo funciones como en js con sus funciones flecha",
    """makeFunc <func_name>() then
           return <some_value>
       endfunc""":
    "Así se retornan valores",
    "<func_name>(<arguments>)":
    "Llamando funciones con argumentos",
    "set <var_name> = <func_name>()":
    "llamas a una función y guardas lo que retorna en una variable",
    """class <ClassName> then
           ...
       endclass""":
    "Definiendo clases",
    """class <ClassName> inherit from <ClassName> then
           ...
       endclass""":
    "Se podrá heredar clases",
    """class <ClassName> then
           makeFunc init(self, arg1, arg2) then
               set self.arg1 = arg1
               set self.arg1 = arg2
           endfunc

           makeFunc suma(self, num1: Integer, num2: Integer) => Integer then
               return num1 + num2
           endfunc
       endclass

       set <var_name> = <ClassName>(arg1=1, arg2=2)
       print(<var_name>.arg1)
       print(<var_name>.arg2)
       print(<var_name>.suma(<Integer>, <Integer>))""":
    """Podemos acceder a los métodos y argumentos del constructor\
con el '.' después del nombre de la instancia""",
    "set <var_name> = <ClassName>()":
    "Instanciando clases",
    """set <var_name> = <ClassName>()
       <var_name>.<method_class>()""":
    """Supongamos que nuestra clase tiene un método\
y queremos acceder a ella, pues con el punto podemos acceder facilmente a ese\
método, eso podemos hacerlo también con los argumentos del constructor""",
    """interface <InterfaceName> then
           ...
       endinterface""":
    "Definiendo interfaces",
    """class <ClassName> inherit from <InterfaceName> then
           ...
       endclass""":
    "Las clases pueden heredar interfaces",
    "set <var_name>: <TypeName>":
    "No es obligatorio, pero puedes ponerle tipos a las variables",
    """makeFunc <func_name>(<arguments>: <TypeName>) => <TypeName>
           return <value_with_type>
       endfunc""":
    "También puedes añadirle tipos a los argumentos y señalar que es lo que\
va a retornar una función",
    "set <some_var>: <InterfaceName>":
    """Variables, argumentos de funciones, lo que retornara una función.\
Todo a lo que podemos ponerle un tipo puede tener como tipo una interfáz""",
    '// Esto es un comentario':
    'Con la sintaxis de: //, escribimos comentarios',
    "Prefix Operators": ["-", "!", "("],
    "Infix Operators": [
        "+", "-", "*", "/", "<", ">", ">=", "<=", "==", "!=", "(", ".", ":",
        "=>", "and", "or"
    ]
}

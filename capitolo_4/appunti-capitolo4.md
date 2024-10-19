# Appunti del capitolo 4

## Alcune note sull'uso delle classi in Python

- Le classi sono un metodo in Python per creare gli **Oggetti**
- In Python ogni cosa è un oggetto (interi, stringhe, float, liste, widget Tkinter ecc...)
- Quando un oggetto viene costruito in una classe, questo è definito **istanza della classe**
- Le classi permettono di creare delle relazioni esplicite tra funzioni e variabili che operano sugli oggetti
- Le classi aiutano a riutilizzare il codice, grazie al meccanismo dell'ereditarietà

### Sintassi per creare una classe in Python

        class Banana:
            """A tasty tropical fruit """
            pass

**Importante** 

In Python di norma un nome di una classe è definito in Pascal case, cioè con 
la lettera iniziale maiuscola.

### Creare una istanza della classe

        my_banana = Banana()

my_banana è in questo caso specifico un oggetto della classe Banana.
In una classe possiamo inoltre definire **metodi** e **attributi** della classe stessa.

### Definire metodi ed attributi di una classe in Python

        class Banana:
            """A tasty tropical fruit """
            food_group = 'fruit'
            colors = [
                'green', 'green-yellow', 'yellow'
            ]

Gli attributi di una classe sono delle variabili. Possono essere di classe oppure dell'oggetto(istanza).

**Importante**

I membri di una classe(variaibili e metodi) usano lo snake case per convenzione.

#### Varibili di istanza

        my_banana = Banana()

        my_banana.color = 'yellow' 

Per creare queste varibili di istanza dobbiamo accedere all'istanza stessa.

#### Metodi

Sono delle funzioni definite nella classe.

        class Banana:

            def peel(self):
                self.peeled = True

In questo modo definiamo un metodo di istanza per la casse Banana.

La parola **self** può accedere ai campi variabile dell'istanza:

        def set_color(self, color):
            """ Set the banana colors """
            if color in self.color:
                self.color = color
            else:
                raise ValueError(f'A banana cannot be {color}!')

Quando usiamo dei metodi di istanza, la parola self viene passata in forma implicita e non c'è 
il bisogno di esplicitarla.

        my_banana = Banana()
        my_banana.set_color('green')
        my_banana.peel()

#### Metodi di classe

In aggiunta ai metodi delle istanze, le classi possono avere anche:

- metodi di classe
- metodi statici

Questi metodi non hanno accesso alle istanze della classe, e non possono nemmeno 
leggere e scrivere gli attributi delle istanze della classe. I metodi di classe 
vengono creati ponendo loro in testa un **decorator** prima della loro definizione, il 
decoratore si chiama **@classmethod**

        @classmethod
        def check_color(cls, color):
            """ Test a color string to check if it is valid """
            return color in cls.colors

#### Metodi static

Anche questi usano il decoratore, che si chiama **@staticmethod**.

        @staticmethod
        def estimate_calories(num_bananas):
            return num_bananas * 105

Questi metodi spesso vengono definiti per gestire delle funzioni di utilità all'interno di 
una classe.

### Magic Attributes

### Membri di una classe Public, Private e Protected

### Ereditarietà e sottoclassi
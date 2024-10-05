""" 
Calcolo dell'indice di massa corporea preciso
Inserire i dati non con la virgola ma con il punto in quanto per il momento
il programma non è in grado di interpretare e parsificare numeri con la virgola.
"""
import tkinter as tk

root = tk.Tk()

# set the title
root.title("Calcolo indice della massa corporea")
root.geometry('440x180')
root.resizable(False, False)

title = tk.Label(root, text='Calcolo Indice della massa corporea', font=('Arial 18 bold'), fg='yellow', bg='black')
altezza_in_m_label = tk.Label(root, text='Altezza in metri:')
altezza_in_m_inp = tk.Entry(root)
peso_in_kg_label = tk.Label(root, text='Peso in Kg:')
peso_in_kg_inp = tk.Entry(root)
submit_btn = tk.Button(root, text='Calcola BMI')
output_line = tk.Label(root, text='', anchor='w', justify='left')

title.grid(columnspan=2)
altezza_in_m_label.grid(row=1, column=0)
altezza_in_m_inp.grid(row=1, column=1)
peso_in_kg_label.grid(row=2, column=0)
peso_in_kg_inp.grid(row=2, column=1)
submit_btn.grid(row=99)
output_line.grid(row=110, columnspan=2, sticky='NSEW')

def on_submit():
    altezza_in_metri = float(altezza_in_m_inp.get())
    peso_in_kg = int(peso_in_kg_inp.get())
    calcolo_bmi = float(peso_in_kg / (altezza_in_metri * 2))

    print("Risultato BMI: " , calcolo_bmi)

    message = (
        f'Il tuo BMI è pari a, {calcolo_bmi}'
    )
    output_line.configure(text=message)


submit_btn.configure(command=on_submit)
root.mainloop()

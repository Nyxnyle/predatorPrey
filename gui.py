import tkinter as tk


class App:
    def __init__(self):
        self.root = tk.Tk()
        button = tk.Button(self.root, text="Simulate", command=self.click)
        button.grid(row=6, column=1, columnspan=2, pady=10)

        # Labels and entry widgets
        tk.Label(self.root, text="Predators").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self.root, text="Prey").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self.root, text="Pred reproduction rate").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self.root, text="Prey reproduction rate").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self.root, text="Pred death rate").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self.root, text="Prey death rate").grid(row=5, column=0, padx=10, pady=5, sticky="w")

        self.e1 = tk.Entry(self.root)
        self.e1.insert(0, "20")
        self.e1.grid(row=0, column=1, padx=10, pady=5)

        self.e2 = tk.Entry(self.root)
        self.e2.insert(0, "25")
        self.e2.grid(row=1, column=1, padx=10, pady=5)

        self.e3 = tk.Entry(self.root)
        self.e3.insert(0, "0.04")
        self.e3.grid(row=2, column=1, padx=10, pady=5)

        self.e4 = tk.Entry(self.root)
        self.e4.insert(0, "0.038")
        self.e4.grid(row=3, column=1, padx=10, pady=5)

        self.e5 = tk.Entry(self.root)
        self.e5.insert(0, "0.03")
        self.e5.grid(row=4, column=1, padx=10, pady=5)

        self.e6 = tk.Entry(self.root)
        self.e6.insert(0, "0.03")
        self.e6.grid(row=5, column=1, padx=10, pady=5)

    def click(self):
        # Access the values entered in the text boxes
        self.predator_value = self.e1.get()
        self.prey_value = self.e2.get()
        self.predator_repro = self.e3.get()
        self.prey_repro = self.e4.get()
        self.predator_death = self.e5.get()
        self.prey_death = self.e6.get()

        # Perform actions based on the entered values, if needed
        if self.predator_value.isnumeric() and self.prey_value.isnumeric():
            self.predator_value = int(self.predator_value)
            self.prey_value = int(self.prey_value)
            self.predator_repro = float(self.predator_repro)
            self.prey_repro = float(self.prey_repro)
            self.predator_death = float(self.predator_death)
            self.prey_death = float(self.prey_death)
            print("Predators:", self.predator_value)
            print("Prey:", self.prey_value)
            print("predator reproduction:", self.predator_repro)
            print("prey reproduction:", self.prey_repro)
            print("predator death:", self.predator_death)
            print("prey death:", self.prey_death)
            # Close the main window
            self.root.destroy()
        else:
            print("ENTER NUMBERS")


if __name__ == "__main__":
    app = App()
    app.root.mainloop()

import tkinter as tk
from tkinter import messagebox

class ObjectInputPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack()

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.LEFT, padx=5)

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(side=tk.RIGHT, padx=5)

        self.current_id = 0

        self.path_label = tk.Label(self.input_frame, text="Path to Mesh File:")
        self.path_label.grid(row=0, column=0, padx=5, pady=2)
        self.path_text = tk.Entry(self.input_frame, width=25)
        self.path_text.grid(row=0, column=1, padx=5, pady=2)

        self.scale_label = tk.Label(self.input_frame, text="Scale:")
        self.scale_label.grid(row=1, column=0, padx=5, pady=2)
        self.scale_text = tk.Entry(self.input_frame, width=10)
        self.scale_text.grid(row=1, column=1, padx=5, pady=2)

        self.prismatic_label = tk.Label(self.input_frame, text="Prismatic:")
        self.prismatic_label.grid(row=2, column=0, padx=5, pady=2)
        
        self.prismatic_checkboxes_vars = [tk.BooleanVar() for _ in range(3)]
        self.prismatic_checkboxes = [
            (tk.Checkbutton(self.input_frame, text="X", variable=self.prismatic_checkboxes_vars[0]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10)),
            (tk.Checkbutton(self.input_frame, text="Y", variable=self.prismatic_checkboxes_vars[1]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10)),
            (tk.Checkbutton(self.input_frame, text="Z", variable=self.prismatic_checkboxes_vars[2]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10))
        ]
        
        for i, ((checkbox, lower_limit, upper_limit), cb_var) in enumerate(zip(self.prismatic_checkboxes, self.prismatic_checkboxes_vars)):
            checkbox.grid(row=2+i, column=1, padx=2, pady=2)
            lower_limit.grid(row=2+i, column=2, padx=2, pady=2)
            upper_limit.grid(row=2+i, column=3, padx=2, pady=2)

        self.revolute_label = tk.Label(self.input_frame, text="Revolute:")
        self.revolute_label.grid(row=5, column=0, padx=5, pady=2)
        
        self.revolute_checkboxes_vars = [tk.BooleanVar() for _ in range(3)]
        self.revolute_checkboxes = [
            (tk.Checkbutton(self.input_frame, text="R", variable=self.revolute_checkboxes_vars[0]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10)),
            (tk.Checkbutton(self.input_frame, text="P", variable=self.revolute_checkboxes_vars[1]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10)),
            (tk.Checkbutton(self.input_frame, text="Y", variable=self.revolute_checkboxes_vars[2]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10))
        ]
        
        for i, ((checkbox, lower_limit, upper_limit), cb_var) in enumerate(zip(self.revolute_checkboxes, self.revolute_checkboxes_vars)):
            checkbox.grid(row=5+i, column=1, padx=2, pady=2)
            lower_limit.grid(row=5+i, column=2, padx=2, pady=2)
            upper_limit.grid(row=5+i, column=3, padx=2, pady=2)

        self.add_button = tk.Button(self.input_frame, text="Add Object", command=self.add_object)
        self.add_button.grid(row=8, column=1, columnspan=3, padx=5, pady=5)

        self.list_box = tk.Listbox(self.list_frame)
        self.list_box.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.prismatic_lower_limits = [ll for _, ll, _ in self.prismatic_checkboxes]
        self.prismatic_upper_limits = [ul for _, _, ul in self.prismatic_checkboxes]
        self.revolute_lower_limits = [ll for _, ll, _ in self.revolute_checkboxes]
        self.revolute_upper_limits = [ul for _, _, ul in self.revolute_checkboxes]

    def add_object(self):
        path = self.path_text.get()
        scale = self.scale_text.get()

        prismatic_values = [f"{cb.cget('text')}({'checked' if bool(cb_var.get()) else 'unchecked'}, {ll.get()}-{ul.get()})" for (cb, ll, ul), cb_var in zip(self.prismatic_checkboxes, self.prismatic_checkboxes_vars)]
        revolute_values = [f"{cb.cget('text')}({'checked' if bool(cb_var.get()) else 'unchecked'}, {ll.get()}-{ul.get()})" for (cb, ll, ul), cb_var in zip(self.revolute_checkboxes, self.revolute_checkboxes_vars)]
        
        prismatic_str = ", ".join(prismatic_values)
        revolute_str = ", ".join(revolute_values)
        
        self.list_box.insert(tk.END, f"Path: {path}, Scale: {scale}, Prismatic joints: {prismatic_str}, Revolute joints: {revolute_str}")
        
        # Print inputs
        print(f"Path: {path}")
        print(f"Scale: {scale}")

        # Print whether prismatic checkboxes are checked and their values
        print("Prismatic:")
        for checkbox, lower_limit, upper_limit, cb_var, value in zip(self.prismatic_checkboxes, self.prismatic_lower_limits, self.prismatic_upper_limits, self.prismatic_checkboxes_vars, prismatic_values):
            print(f"Checked: {cb_var.get()}, Value: {value}")
            cb_var.set(False)

        # Print whether revolute checkboxes are checked and their values
        print("Revolute:")
        for checkbox, lower_limit, upper_limit, cb_var, value in zip(self.revolute_checkboxes, self.revolute_lower_limits, self.revolute_upper_limits, self.revolute_checkboxes_vars, revolute_values):
            print(f"Checked: {cb_var.get()}, Value: {value}")
            cb_var.set(False)
        print(prismatic_values)
        print(revolute_values)
        
        # Clear the entry fields after adding object
        self.path_text.delete(0, tk.END)
        self.scale_text.delete(0, tk.END)
        for (cb, ll, ul) in self.prismatic_checkboxes:
            ll.delete(0, tk.END)
            ul.delete(0, tk.END)
        for (cb, ll, ul) in self.revolute_checkboxes:
            ll.delete(0, tk.END)
            ul.delete(0, tk.END)

        self.current_id +=1

root = tk.Tk()
root.title("Object Input GUI")
app = ObjectInputPanel(root)
app.mainloop()

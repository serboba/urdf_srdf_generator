import wx

class ObjectInputPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.input_sizer = wx.BoxSizer(wx.VERTICAL)
        self.list_sizer = wx.BoxSizer(wx.VERTICAL)

        # Path to mesh file
        self.path_label = wx.StaticText(self, label="Path to Mesh File:")
        self.path_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(200, -1))

        # Scale
        self.scale_label = wx.StaticText(self, label="Scale:")
        self.scale_text = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))

        # Position checkboxes and limits
        self.pos_label = wx.StaticText(self, label="Position:")
        self.pos_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.pos_x_checkbox = wx.CheckBox(self, label='X')
        self.pos_y_checkbox = wx.CheckBox(self, label='Y')
        self.pos_z_checkbox = wx.CheckBox(self, label='Z')
        
        self.pos_x_lower_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.pos_x_upper_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.pos_y_lower_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.pos_y_upper_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.pos_z_lower_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.pos_z_upper_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))

        self.add_checkbox_with_limits(self.pos_sizer, self.pos_x_checkbox, self.pos_x_lower_limit, self.pos_x_upper_limit)
        self.add_checkbox_with_limits(self.pos_sizer, self.pos_y_checkbox, self.pos_y_lower_limit, self.pos_y_upper_limit)
        self.add_checkbox_with_limits(self.pos_sizer, self.pos_z_checkbox, self.pos_z_lower_limit, self.pos_z_upper_limit)

        # Orientation checkboxes and limits
        self.orient_label = wx.StaticText(self, label="Orientation:")
        self.orient_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.orient_r_checkbox = wx.CheckBox(self, label='R')
        self.orient_p_checkbox = wx.CheckBox(self, label='P')
        self.orient_y_checkbox = wx.CheckBox(self, label='Y')

        self.orient_r_lower_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.orient_r_upper_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.orient_p_lower_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.orient_p_upper_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.orient_y_lower_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))
        self.orient_y_upper_limit = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER, size=(50, -1))

        self.add_checkbox_with_limits(self.orient_sizer, self.orient_r_checkbox, self.orient_r_lower_limit, self.orient_r_upper_limit)
        self.add_checkbox_with_limits(self.orient_sizer, self.orient_p_checkbox, self.orient_p_lower_limit, self.orient_p_upper_limit)
        self.add_checkbox_with_limits(self.orient_sizer, self.orient_y_checkbox, self.orient_y_lower_limit, self.orient_y_upper_limit)

        self.input_sizer.Add(self.path_label, 0, wx.ALL | wx.EXPAND, 5)
        self.input_sizer.Add(self.path_text, 0, wx.ALL | wx.EXPAND, 5)
        self.input_sizer.Add(self.scale_label, 0, wx.ALL | wx.EXPAND, 5)
        self.input_sizer.Add(self.scale_text, 0, wx.ALL | wx.EXPAND, 5)
        self.input_sizer.Add(self.pos_label, 0, wx.ALL | wx.EXPAND, 5)
        self.input_sizer.Add(self.pos_sizer, 0, wx.ALL | wx.EXPAND, 5)
        self.input_sizer.Add(self.orient_label, 0, wx.ALL | wx.EXPAND, 5)
        self.input_sizer.Add(self.orient_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # List box to show added objects
        self.list_box = wx.ListBox(self)

        self.sizer.Add(self.input_sizer, 1, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.list_box, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(self.sizer)

    def add_checkbox_with_limits(self, sizer, checkbox, lower_limit, upper_limit):
        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        vertical_sizer.Add(checkbox, 0, wx.ALL | wx.CENTER, 5)
        limit_sizer = wx.BoxSizer(wx.HORIZONTAL)
        limit_sizer.Add(wx.StaticText(self, label="Limits: "), 0, wx.ALL | wx.CENTER, 5)
        limit_sizer.Add(0, wx.ALL | wx.CENTER, 5)
        limit_sizer.Add(lower_limit, 0, wx.ALL | wx.CENTER, 5)
        limit_sizer.Add(0, wx.ALL | wx.CENTER, 5)
        limit_sizer.Add(upper_limit, 0, wx.ALL | wx.CENTER, 5)
        vertical_sizer.Add(limit_sizer)
        sizer.Add(vertical_sizer)

    def get_values(self):
        return {
            'pos_x': self.pos_x_checkbox.GetValue(),
            'pos_x_lower': self.pos_x_lower_limit.GetValue(),
            'pos_x_upper': self.pos_x_upper_limit.GetValue(),
            'pos_y': self.pos_y_checkbox.GetValue(),
            'pos_y_lower': self.pos_y_lower_limit.GetValue(),
            'pos_y_upper': self.pos_y_upper_limit.GetValue(),
            'pos_z': self.pos_z_checkbox.GetValue(),
            'pos_z_lower': self.pos_z_lower_limit.GetValue(),
            'pos_z_upper': self.pos_z_upper_limit.GetValue(),
            'orient_r': self.orient_r_checkbox.GetValue(),
            'orient_r_lower': self.orient_r_lower_limit.GetValue(),
            'orient_r_upper': self.orient_r_upper_limit.GetValue(),
            'orient_p': self.orient_p_checkbox.GetValue(),
            'orient_p_lower': self.orient_p_lower_limit.GetValue(),
            'orient_p_upper': self.orient_p_upper_limit.GetValue(),
            'orient_y': self.orient_y_checkbox.GetValue(),
            'orient_y_lower': self.orient_y_lower_limit.GetValue(),
            'orient_y_upper': self.orient_y_upper_limit.GetValue()
        }

    def clear_fields(self):
        self.pos_x_checkbox.SetValue(False)
        self.pos_x_lower_limit.SetValue("")
        self.pos_x_upper_limit.SetValue("")
        self.pos_y_checkbox.SetValue(False)
        self.pos_y_lower_limit.SetValue("")
        self.pos_y_upper_limit.SetValue("")
        self.pos_z_checkbox.SetValue(False)
        self.pos_z_lower_limit.SetValue("")
        self.pos_z_upper_limit.SetValue("")
        self.orient_r_checkbox.SetValue(False)
        self.orient_r_lower_limit.SetValue("")
        self.orient_r_upper_limit.SetValue("")
        self.orient_p_checkbox.SetValue(False)
        self.orient_p_lower_limit.SetValue("")
        self.orient_p_upper_limit.SetValue("")
        self.orient_y_checkbox.SetValue(False)
        self.orient_y_lower_limit.SetValue("")
        self.orient_y_upper_limit.SetValue("")

    def add_to_list_box(self, obj):
        pos = f"Position: X({obj['pos_x']}, {obj['pos_x_lower']}-{obj['pos_x_upper']}), " \
              f"Y({obj['pos_y']}, {obj['pos_y_lower']}-{obj['pos_y_upper']}), " \
              f"Z({obj['pos_z']}, {obj['pos_z_lower']}-{obj['pos_z_upper']})"
        orient = f"Orientation: R({obj['orient_r']}, {obj['orient_r_lower']}-{obj['orient_r_upper']}), " \
                 f"P({obj['orient_p']}, {obj['orient_p_lower']}-{obj['orient_p_upper']}), " \
                 f"Y({obj['orient_y']}, {obj['orient_y_lower']}-{obj['orient_y_upper']})"
        self.list_box.Append(f"{pos}, {orient}")

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Object Input GUI')
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.object_panel = ObjectInputPanel(self.panel)

        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.add_button = wx.Button(self.panel, label='Add Object')
        self.create_button = wx.Button(self.panel, label='Create File')

        self.button_sizer.Add(self.add_button, 0, wx.ALL | wx.CENTER, 5)
        self.button_sizer.Add(self.create_button, 0, wx.ALL | wx.CENTER, 5)

        self.sizer.Add(self.object_panel, 1, wx.ALL | wx.EXPAND, 5)
        self.sizer.Add(self.button_sizer, 0, wx.ALL | wx.CENTER, 5)

        self.add_button.Bind(wx.EVT_BUTTON, self.on_add_object)
        self.create_button.Bind(wx.EVT_BUTTON, self.on_create_file)

        self.objects = []

        self.panel.SetSizer(self.sizer)
        self.Show()

    def on_add_object(self, event):
        obj = self.object_panel.get_values()
        self.objects.append(obj)
        self.object_panel.add_to_list_box(obj)
        self.object_panel.clear_fields()

    def on_create_file(self, event):
        with open('output.txt', 'w') as f:
            for obj in self.objects:
                pos = f"Position: X({obj['pos_x']}, {obj['pos_x_lower']}-{obj['pos_x_upper']}), " \
                      f"Y({obj['pos_y']}, {obj['pos_y_lower']}-{obj['pos_y_upper']}), " \
                      f"Z({obj['pos_z']}, {obj['pos_z_lower']}-{obj['pos_z_upper']})"
                orient = f"Orientation: R({obj['orient_r']}, {obj['orient_r_lower']}-{obj['orient_r_upper']}), " \
                         f"P({obj['orient_p']}, {obj['orient_p_lower']}-{obj['orient_p_upper']}), " \
                         f"Y({obj['orient_y']}, {obj['orient_y_lower']}-{obj['orient_y_upper']})"
                f.write(f"{pos}, {orient}\n")
        wx.MessageBox('File created!', 'Info', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()

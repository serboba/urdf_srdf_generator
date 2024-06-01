import tkinter as tk
from tkinter import messagebox
from xml.etree.cElementTree import *
from enum import Enum

class Axis(Enum):
    X = 1
    Y = 2
    Z = 3

class Joint():
    def __init__(self, type_, axis,  lower_limit, upper_limit):
        self.type = type_
        self.axis = axis
        self.lower_limit = lower_limit 
        self.upper_limit = upper_limit
        

class ObjectURDF():
    def __init__(self, id, name, mesh_path, scale, joints):

        self.id = id
        self.name = name
        self.mesh_path = mesh_path
        self.scale = scale
        self.joints = joints


        pass


class ObjectInputPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.pack(fill=tk.BOTH, expand=True)
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side=tk.LEFT, padx=5, fill=tk.Y)

        self.list_frame = tk.Frame(self)
        self.list_frame.pack(side=tk.RIGHT, padx=5, fill=tk.BOTH, expand=True)

        self.current_id = 0

        self.name_label = tk.Label(self.input_frame, text="Link Name:")
        self.name_label.grid(row=0, column=0, padx=5, pady=2)
        self.name_text = tk.Entry(self.input_frame, width=25)
        self.name_text.grid(row=0, column=1, padx=5, pady=2)

        self.path_label = tk.Label(self.input_frame, text="Path to Mesh File:")
        self.path_label.grid(row=1, column=0, padx=5, pady=2)
        self.path_text = tk.Entry(self.input_frame, width=25)
        self.path_text.grid(row=1, column=1, padx=5, pady=2)

        self.scale_label = tk.Label(self.input_frame, text="Scale:")
        self.scale_label.grid(row=2, column=0, padx=5, pady=2)
        self.scale_text = tk.Entry(self.input_frame, width=10)
        self.scale_text.grid(row=2, column=1, padx=5, pady=2)

        self.prismatic_label = tk.Label(self.input_frame, text="Prismatic:")
        self.prismatic_label.grid(row=3, column=0, padx=5, pady=2)

        self.prismatic_checkboxes_vars = [tk.BooleanVar() for _ in range(3)]
        self.prismatic_checkboxes = [
            (tk.Checkbutton(self.input_frame, text="X", variable=self.prismatic_checkboxes_vars[0]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10)),
            (tk.Checkbutton(self.input_frame, text="Y", variable=self.prismatic_checkboxes_vars[1]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10)),
            (tk.Checkbutton(self.input_frame, text="Z", variable=self.prismatic_checkboxes_vars[2]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10))
        ]

        for i, ((checkbox, lower_limit, upper_limit), cb_var) in enumerate(zip(self.prismatic_checkboxes, self.prismatic_checkboxes_vars)):
            checkbox.grid(row=3+i, column=1, padx=2, pady=2)
            lower_limit.grid(row=3+i, column=2, padx=2, pady=2)
            upper_limit.grid(row=3+i, column=3, padx=2, pady=2)

        self.revolute_label = tk.Label(self.input_frame, text="Revolute:")
        self.revolute_label.grid(row=6, column=0, padx=5, pady=2)

        self.revolute_checkboxes_vars = [tk.BooleanVar() for _ in range(3)]
        self.revolute_checkboxes = [
            (tk.Checkbutton(self.input_frame, text="R", variable=self.revolute_checkboxes_vars[0]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10)),
            (tk.Checkbutton(self.input_frame, text="P", variable=self.revolute_checkboxes_vars[1]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10)),
            (tk.Checkbutton(self.input_frame, text="Y", variable=self.revolute_checkboxes_vars[2]), tk.Entry(self.input_frame, width=10), tk.Entry(self.input_frame, width=10))
        ]

        for i, ((checkbox, lower_limit, upper_limit), cb_var) in enumerate(zip(self.revolute_checkboxes, self.revolute_checkboxes_vars)):
            checkbox.grid(row=6+i, column=1, padx=2, pady=2)
            lower_limit.grid(row=6+i, column=2, padx=2, pady=2)
            upper_limit.grid(row=6+i, column=3, padx=2, pady=2)

        self.add_button = tk.Button(self.input_frame, text="Add Object", command=self.add_object)
        self.add_button.grid(row=9, column=1, padx=5, pady=5)

        self.generate_button = tk.Button(self.input_frame, text="Generate Files", command=self.generate_files)
        self.generate_button.grid(row=9, column=2, padx=5, pady=5)

        self.list_box = tk.Listbox(self.list_frame)
        self.list_box.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.prismatic_lower_limits = [ll for _, ll, _ in self.prismatic_checkboxes]
        self.prismatic_upper_limits = [ul for _, _, ul in self.prismatic_checkboxes]
        self.revolute_lower_limits = [ll for _, ll, _ in self.revolute_checkboxes]
        self.revolute_upper_limits = [ul for _, _, ul in self.revolute_checkboxes]

        self.objects_urdf = []

    def generate_files(self):
        print("Generate Files button clicked.")
        # Add further functionality as needed for generating files
        self.build_urdf_tree()

    def get_axis(self, text):
        return Axis.X if text == 'X' else Axis.Y if text == 'Y' else Axis.Z

    def get_joints(self):
        joints = []
        for (cb, ll, ul), cb_var in zip(self.prismatic_checkboxes, self.prismatic_checkboxes_vars):
            if bool(cb_var.get()):
                if ll.get() == '' or ul.get() == '':
                    messagebox.showerror("Error", "Prismatic joint limits must be set")
                    return
                if float(ll.get()) > float(ul.get()) :
                    messagebox.showerror("Error", "Lower limit must be less than upper limit")
                    return

                joints.append(Joint('prismatic', self.get_axis(cb.cget('text')), float(ll.get()), float(ul.get())))
        
        for (cb, ll, ul), cb_var in zip(self.revolute_checkboxes, self.revolute_checkboxes_vars):
            if bool(cb_var.get()):
                if ll.get() == '' or ul.get() == '':
                    messagebox.showerror("Error", "Revolute joint limits must be set")
                    return
                if float(ll.get()) > float(ul.get()) :
                    messagebox.showerror("Error", "Lower limit must be less than upper limit")
                    return

                joints.append(Joint('revolute', self.get_axis(cb.cget('text')), float(ll.get()), float(ul.get())))
        return joints

    def clean_fields(self):
        self.name_text.delete(0, tk.END)
        self.path_text.delete(0, tk.END)
        self.scale_text.delete(0, tk.END)
        for (cb, ll, ul) in self.prismatic_checkboxes:
            cb.deselect()
            ll.delete(0, tk.END)
            ul.delete(0, tk.END)
        for (cb, ll, ul) in self.revolute_checkboxes:
            cb.deselect()
            ll.delete(0, tk.END)
            ul.delete(0, tk.END)

    def add_object(self):

        link_name = self.name_text.get()
        path = self.path_text.get()
        scale = self.scale_text.get()
        joints = self.get_joints()

        # Print inputs
        print(f"Path: {path}")
        print(f"Scale: {scale}")

        print("Obj mesh path: ", path)
        print("Obj scale: ", scale)
        
        if scale == '':
            scale = 1.0
        else:
            try:
                scale = float(scale)
            except ValueError:
                messagebox.showerror("Error", "Scale must be a number")
                return
            
        

        # Clear the entry fields after adding object
        self.clean_fields()

        self.objects_urdf.append(ObjectURDF(self.current_id, link_name, path, scale, joints))

        
        self.list_box.insert(tk.END, f"Link name: {link_name}, #Joints: {len(joints)}, Scale: {scale}, Path: {path}")
        self.current_id +=1


    def create_link_xml_for_obj(self, obj, material_color="0.87450980392 0.87450980392 0.87058823529 0.4"):
        # Assuming the object has a mesh file path

        # We could use obj.name but for simplicity we will use the joint_0 convention
        link_elems = []

        max_joint_id = len(obj.joints)
        for i in range(max_joint_id):
            print("i : "   , i, "- max_joint_id: ", max_joint_id)
            if i == 0:
                link_name = 'link_'+ str(obj.id) + '_joint_0'
                link_elem = Element('link', {'name' : link_name})

                visual = SubElement(link_elem, 'visual')
                geometry_visual = SubElement(visual, 'geometry')
                    
                mesh_visual = SubElement(geometry_visual, 'mesh', {'filename' : obj.mesh_path,
                                                    'scale' : f'{obj.scale}, {obj.scale}, {obj.scale}'})
                
                origin_visual = SubElement(visual, 'origin', {'rpy' : '0 0 0',
                                                            'xyz' : '0 0 0'})
                
                material_visual = SubElement(visual, 'material', {'name' : ""})
                material_visual_color = SubElement(material_visual, 'color', {'rgba' :
                                                                            material_color})
                ##########################

                collision = SubElement(link_elem, 'collision', {'concave': 'yes', 'name': ''})
                geometry_collision = SubElement(collision, 'geometry')
                mesh_collision = SubElement(geometry_collision, 'mesh', {'filename' : obj.mesh_path,
                                                    'scale' : f'{obj.scale}, {obj.scale}, {obj.scale}'})
                
                origin_collision = SubElement(collision, 'origin', {'rpy' : '0 0 0',
                                                            'xyz' : '0 0 0'})
                
                material_collision = SubElement(collision, 'material', {'name' : ""})
                material_collision_color = SubElement(material_collision, 'color', {'rgba' :
                                                                            material_color})
                link_elem_string = tostring(link_elem, encoding='unicode', method='xml')
            else:
                link_name = 'link_'+ str(obj.id) + '_joint_'+ str(i)
                link_elem = Element('link', {'name' : link_name})
            link_elems.append(link_elem)


        return link_elems

    def create_joint_xml_for_obj(self, obj):

        max_joint_id = len(obj.joints)-1
        joints = []
        for i, joint in enumerate(obj.joints):

            joint_name = 'link_'+ str(obj.id) + '_joint_' + str(max_joint_id)
            joint_elem = Element('joint', {'name' : f"{joint_name}",
                                           'type' : joint.type})
            
            if i == 0:
                parent_elem = SubElement(joint_elem, 'parent', {'link' : 'base_link'})
            else:
                parent_elem = SubElement(joint_elem, 'parent', {'link' : f'link_{obj.id}_joint_{max_joint_id+1}'})

            child_elem = SubElement(joint_elem, 'child', {'link' : joint_name})

            
            origin_elem = SubElement(joint_elem, 'origin', {'rpy' : '0 0 0', # long term make this a parameter and pass displacement too
                                                      'xyz' : '0 0 0'})
            
            axis_str = '0 0 0'
            if joint.axis == Axis.X:
                axis_str = '1 0 0'
            elif joint.axis == Axis.Y:
                axis_str = '0 1 0'
            elif joint.axis == Axis.Z:
                axis_str = '0 0 1'

            axis_elem = SubElement(joint_elem, 'axis', {'xyz' : axis_str})
            limit_elem = SubElement(joint_elem, 'limit', {'effort' : '1',
                                                         'velocity' : '1',
                                                         'lower' : f'{joint.lower_limit}',
                                                         'upper' : f'{joint.upper_limit}'})
            joint_elem_string = tostring(joint_elem, encoding='unicode', method='xml')
            print(joint_elem_string)

            joints.append(joint_elem)
        
            max_joint_id -= 1
        return joints
            
    def add_object_to_tree(obj):
        pass
        
        
    

    def build_urdf_tree(self):
        root_urdf = Element('robot', {'name' : 'robot_name'})

        base_link = SubElement(root_urdf, 'base_link',
                               {'name' : 'base_link'})

        for obj in self.objects_urdf:
            links = self.create_link_xml_for_obj(obj)
            for link in links:
                root_urdf.append(link)

        for obj in self.objects_urdf:
            joints = self.create_joint_xml_for_obj(obj)
            for joint in joints:
                root_urdf.append(joint)
        
        tree = ElementTree(root_urdf)
        dump(tree)
        


root = tk.Tk()
root.title("Object Input GUI")
app = ObjectInputPanel(root)
app.mainloop()
import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
import nibabel as nib
import numpy as np
from PIL import Image, ImageTk
import sys
import os
from Exectute_generation_lesions import Create_sphere

cwd="\\".join(os.getcwd().split('\\')[:-1])
sys.path.append(cwd)
print(os.listdir(cwd))
from utils.Packages_file import *
from code_paper.preprocess_TotalSegmentator_scans.Return_label_functions import *
from code_paper.preprocess_TotalSegmentator_scans.generate_synthetic_lesion.Create_synthetic_lesions import Create_sphere_coords
from code_paper.preprocess_TotalSegmentator_scans.generate_synthetic_lesion.Fill_synthetic_lesions import *
from code_paper.preprocessing_yolo_input.Apply_windowing import *




class NiftiViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Medical Imaging Tool")
        self.root.geometry("980x546")
        self.root.configure(bg="#d9d9d9")

        self.ct_data = None
        self.ct_affine = None
        self.No_slices=None
        self.mask_data = None
        self.slice_index = 0
        self.annotation_mode = False
        self.annotations = []  # list of world coordinates
        self.annotations_raw=[]
        self.annotation_ids = []  # link table rows to annotations

        self.create_widgets()

    def create_widgets(self):
        # Top Menu
        top_frame = tk.Frame(self.root, bg="#1e6c83")
        top_frame.pack(fill=tk.X)

        menu_button = tk.Menubutton(top_frame, text="Load data", bg="#1e6c83", fg="white", bd=0)
        menu = Menu(menu_button, tearoff=0)
        menu.add_command(label="Load CT", command=lambda:self.load_ct())
        menu.add_command(label="Load Bone Mask", command=lambda:self.load_mask())
        menu_button.config(menu=menu)
        menu_button.pack(side=tk.LEFT, padx=(10, 2), pady=2)

        settings_button = tk.Button(top_frame, text="Settings", bg="#1e6c83", fg="white", bd=0)
        settings_button.pack(side=tk.LEFT, padx=2, pady=2)

        # Main Layout
        main_frame = tk.Frame(self.root, bg="#d9d9d9")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left Panel
        left_frame = tk.Frame(main_frame, bg="#d9d9d9")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(left_frame, bg="#d9d9d9")
        btn_frame.pack(fill=tk.X)

        self.annotate_button = tk.Button(btn_frame, text="Annotate", bg="#0f5f74", fg="white", width=15, command=self.enable_annotation)
        self.annotate_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.generate_lesion_button=tk.Button(btn_frame, text="Generate Lesions", bg="#0f5f74", fg="white", width=15,
                                    command=self.Generate_synthetic_lesions).pack(side=tk.LEFT, padx=5, pady=5)

        tk.Button(btn_frame, text="Run", bg="#333", fg="white", width=10).pack(side=tk.LEFT, padx=10)

        canvas_frame = tk.Frame(left_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(canvas_frame, bg="#3b3b3b")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<MouseWheel>", self.scroll_slices)
        self.canvas.bind("<Button-1>", self.annotate)

        self.scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.scroll_via_bar)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        #self.scrollbar.set(0,0)
        # Right Panel
        right_frame = tk.Frame(main_frame, bg="#d9d9d9")
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)

        # Right-side Buttons
        btn_right_frame = tk.Frame(right_frame, bg="#d9d9d9")
        btn_right_frame.pack(fill=tk.X, pady=(5, 2))

        tk.Button(btn_right_frame, text="Expand", bg="#333", fg="white", width=10, state="disabled").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_right_frame, text="Visualize", bg="#333", fg="white", width=10, state="disabled").pack(side=tk.LEFT, padx=5)

        # Table
        results_frame = tk.LabelFrame(right_frame, text="Results", bg="#1e6c83", fg="white")
        results_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)

        columns = ("#", "GT", "Prediction")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=6)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<Button-3>", self.right_click_remove)

        # Log
        log_frame = tk.LabelFrame(right_frame, text="Log", bg="#1e6c83", fg="white")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(2, 5))

        self.log_text = tk.Text(log_frame, height=6, bg="black", fg="white", insertbackground="white", state="normal")
        self.log_text.insert(tk.END, ">>>")
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state="disabled")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"\n>>> {message}")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

    def on_tree_click(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        if index < len(self.annotations):
            z, _, _ = self.annotations[index]
            self.slice_index = z
            self.scroll_via_bar(["movetoslice",self.slice_index])


    def load_ct(self):
        filepath = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii *.nii.gz")])
        if filepath:
            try:
                self.log(f"Loading CT: {filepath}")
                img = nib.load(filepath)
                data = img.get_fdata()

                data=Apply_windowing(data,L=400,W=1800,Mute=True)

                self.ct_affine = img.affine
                self.No_slices=img.shape[-1]
                if data.ndim == 4:
                    data = data[:, :, :, 0]

                self.ct_data = np.transpose(data, (2, 0, 1))  # Z, Y, X
                self.scrollbar.set((self.ct_data.shape[0]-1)/self.No_slices,(self.ct_data.shape[0]-1)/self.No_slices)
                self.slice_index = self.ct_data.shape[0] // 2
                self.scroll_via_bar(["movetoslice",self.slice_index])

                self.show_slice()
                self.log("CT loaded.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CT:\n{e}")
                self.log(f"Error: {e}")

    def load_mask(self):
        filepath = filedialog.askopenfilename(filetypes=[("NIfTI files", "*.nii *.nii.gz")])
        if filepath:
            try:
                self.log(f"Loading bone mask: {filepath}")
                img = nib.load(filepath)
                data = img.get_fdata()
                if data.ndim == 4:
                    data = data[:, :, :, 0]
                self.mask_data = np.transpose(data, (2, 0, 1))
                self.log("Bone segmentation mask loaded.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load mask:\n{e}")
                self.log(f"Error: {e}")

    def Generate_synthetic_lesions(self):
        if self.ct_data is not None:
            Synthetic_lesions,Synthetic_CT=Create_sphere(self,self.annotations,self.annotations_raw,self.ct_data)
            self.ct_data=Synthetic_CT
            print('generate lesions')
            self.show_slice()
            self.log("Synthetic Lesions Generated")

        return None

    def show_slice(self):
        if self.ct_data is not None:

            slice_img = self.ct_data[self.slice_index]
            slice_img = np.rot90(slice_img, k=-1)

            slice_img = (slice_img - np.min(slice_img)) / (np.max(slice_img) - np.min(slice_img) + 1e-5)
            slice_img = (slice_img * 255).astype(np.uint8)

            img = Image.fromarray(slice_img)
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if canvas_width > 1 and canvas_height > 1:
                img = img.resize((canvas_width, canvas_height), Image.BILINEAR)

            self.tk_img = ImageTk.PhotoImage(img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

            # Draw annotation markers
            for voxel_coords in self.annotations:
                z, y, x = voxel_coords
                if z != self.slice_index:
                    continue

                # Rotate coordinates to match displayed image
                rotated_coords = np.rot90(np.array([[x, y]]), k=-1)
                x_disp = int(rotated_coords[0] * canvas_width / self.ct_data.shape[2])
                y_disp = int(rotated_coords[1] * canvas_height / self.ct_data.shape[1])

                r = 5
                self.canvas.create_oval(x_disp - r, y_disp - r, x_disp + r, y_disp + r, outline="red", width=2)

    def scroll_slices(self, event):
        if self.ct_data is None:
            return
        direction = -1 if event.delta > 0 else 1
        self.slice_index = np.clip(self.slice_index + direction * 3, 0, self.ct_data.shape[0] - 1)
        self.scroll_via_bar(["movetoslice",self.slice_index])
        self.scrollbar.set((self.slice_index)/self.No_slices,(self.slice_index)/self.No_slices)
        self.show_slice()



    def scroll_via_bar(self, *args):

        if self.ct_data is None:
            return
        if args[0] == 'moveto':
            self.slice_index = int(float(args[1]) * (self.ct_data.shape[0] - 1))
        elif args[0] == 'movetoslice':
            self.slice_index = int(float(args[1]))
        elif args[0] == 'scroll':
            self.slice_index = np.clip(self.slice_index + int(args[1]), 0, self.ct_data.shape[0] - 1)
        self.scrollbar.set((self.slice_index)/self.No_slices,(self.slice_index)/self.No_slices)

        self.show_slice()


    def enable_annotation(self):
        self.annotation_mode = not self.annotation_mode
        mode = "enabled" if self.annotation_mode else "disabled"
        self.annotate_button.config(relief=tk.SUNKEN if self.annotation_mode else tk.RAISED)
        self.log(f"Annotation mode {mode}.")

    def annotate(self, event):
        if not self.annotation_mode or self.ct_data is None:
            return

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width < 1 or canvas_height < 1:
            return

        slice_data = self.ct_data[self.slice_index]
        rotated = np.rot90(slice_data, k=-1)
        h, w = rotated.shape

        # Get clicked position relative to rotated image
        x_rotated = int((event.x / canvas_width) * w)
        y_rotated = int((event.y / canvas_height) * h)

        # Rotate back to get correct voxel coordinates
        y_voxel, x_voxel = np.rot90(np.array([[x_rotated, y_rotated]]), k=1)
        z_voxel = self.slice_index

        print(x_rotated,y_rotated)

        voxel_coords = (z_voxel, y_voxel[0], x_voxel[0])
        self.annotations.append(voxel_coords)
        self.annotations_raw.append((z_voxel,y_rotated,slice_data.shape[0]-x_rotated))
        idx = len(self.annotations)
        self.annotation_ids.append(self.tree.insert("", tk.END, values=(idx, "", "")))

        self.log(f"Annotation #{idx} at voxel: {voxel_coords}")
        self.show_slice()

    def right_click_remove(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            index = self.tree.index(row_id)
            self.tree.delete(row_id)
            del self.annotations[index]
            del self.annotations_raw[index]
            del self.annotation_ids[index]
            self.log(f"Removed annotation #{index + 1}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NiftiViewerApp(root)
    root.mainloop()

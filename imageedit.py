from tkinter import Tk, Button, Label, filedialog, Entry, Frame
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageFilter, ImageDraw, ImageFont
import os
def generate_pholder(text="No Image Loaded"):
    size = (800, 400)
    img = Image.new("RGB", size, "lightgray")
    draw = ImageDraw.Draw(img)
    font_path = "/system/fonts/Roboto-Regular.ttf" if os.name != "nt" else r"C:\Windows\Fonts\arial.ttf"
    font = ImageFont.truetype(font_path, size=100)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    draw.text((text_x, text_y), text, fill="black", font=font)
    return img
    
class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.img = generate_pholder()
        self.tk_img = None
        self.memory = []
        self.drawing = False
        self.mouse_down = False
        self.last_draw = None
        self.draw_tool = None
        self.label = Label(root)
        self.label.place(relx=0.5, rely=0.5, anchor="center")
        self.root.bind("<ButtonPress-1>", lambda e: self.set_mouse(True))
        self.root.bind("<ButtonRelease-1>", lambda e: self.set_mouse(False))
        self.poll_mouse()
        Label(root, text="Resizing Configurations:").grid(row=4, column=0)
        self.width_entry = Entry(root)
        self.width_entry.grid(row=4, column=1)
        self.width_entry.insert(0, "800")
        self.height_entry = Entry(root)
        self.height_entry.grid(row=4, column=2)
        self.height_entry.insert(0, "400")
        Label(root, text="Press 'Resize Image' to resize.").grid(row=4, column=3)
        self.original_image = generate_pholder()
        self.size_label = Label(root, text=f"Size: 800x400")
        self.size_label.place(relx=0.9, rely=0.05)
        infolabel = Label(root, text="Some features may not work very well (Remove Sepia, Convert To RGB, Drawing), you do not have to email me, I have already figured this out.")
        infolabel.place(relx=0.5, rely=0.9, anchor="center")
        line = Frame(root, bg="cyan", height=2, width=1920)
        line.place(relx=0.5, rely=0.85, anchor="center")
        Label(root, text="Essentials: ", font=("Arial", 10)).grid(row=0, column=0)
        Button(root, text="Resize Image", command=self.resize_image).grid(row=0, column=1)
        Button(root, text="Load Image (RGB)", command=self.load_image_rgb).grid(row=0, column=2)
        Button(root, text="Load Image (Grayscale)", command=self.load_image_grayscale).grid(row=0, column=3)
        Button(root, text="Toggle Drawing", command=self.toggle_drawing).grid(row=0, column=4)
        Label(root, text="Brightness/Contrast: ", font=("Arial", 10)).grid(row=1, column=0)
        Button(root, text="Enhance Contrast", command=self.enhance_contrast).grid(row=1, column=1)
        Button(root, text="Enhance Brightness", command=self.enhance_brightness).grid(row=1, column=2)
        Button(root, text="Lower Contrast", command=self.lower_contrast).grid(row=1, column=3)
        Button(root, text="Lower Brightness", command=self.lower_brightness).grid(row=1, column=4)
        Label(root, text="Effects: ", font=("Arial", 10)).grid(row=2, column=0)
        Button(root, text="Sepia", command=self.apply_sepia).grid(row=2, column=1)
        Button(root, text="Remove Sepia", command=self.remove_sepia).grid(row=2, column=2)
        Button(root, text="Blur", command=self.blur_image).grid(row=2, column=3)
        Button(root, text="Sharpen", command=self.sharpen_image).grid(row=2, column=4)
        Label(root, text="Conversion: ", font=("Arial", 10)).grid(row=3, column=0)
        Button(root, text="Convert To RGB (if possible)", command=self.to_rgb).grid(row=3, column=1)
        Button(root, text="Convert To Grayscale", command=self.to_grayscale).grid(row=3, column=2)
        Label(root, text="Saving Essentials: ").place(relx=0.5, rely=0.45, x=690, anchor="center")
        Button(root, text="Reload Image", command=self.reload_image).place(relx=0.6, rely=0.5, x=600, anchor="center")
        Button(root, text="Save Image", command=self.save_image).place(relx=0.5, rely=0.5, x=600, anchor="center")
        Button(root, text="Undo", command=self.undo).place(relx=0.5, rely=0.55, x=690, anchor="center")
        self.show_image()
    def load_image_rgb(self):
        path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.ppm"), ("All Files", "*.*")]
        )
        if path:
            isok = path.endswith((".jpg", ".jpeg", ".png", ".ppm"))
            if isok:
                self.img =  Image.open(path).convert("RGB")
                self.img = self.img.resize((800, 400))
                self.original_image = self.img.copy()                
                self.show_image()
            else:
                warnlabel = Label(self.root, text="Unable to archive image format.")
                warnlabel.place(relx=0.8, rely=0.05)
                self.root.after(4000, warnlabel.destroy)
                
    def load_image_grayscale(self):
        path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.ppm"), ("All Files", "*.*")]
        )
        if path:
            isok = path.endswith((".jpg", ".jpeg", ".png", ".ppm"))
            if isok:
                self.img = Image.open(path).convert("L")
                self.img = self.img.resize((800, 400))
                self.original_image = self.img.copy()
                self.show_image()
            else:
                warnlabel = Label(self.root, text="Unable to archive image format.")
                warnlabel.place(relx=0.8, rely=0.05)
                self.root.after(4000, warnlabel.destroy)
            
    def reload_image(self):
        if self.original_image:
            self.img = self.original_image.copy()
            self.show_image()
            
    def resize_image(self):
        if self.img:
            try:
                w = int(self.width_entry.get())
                h = int(self.height_entry.get())
                self.img = self.img.resize((w, h))
                self.size_label.config(text=f"Size: {self.img.width}x{self.img.height}")
                self.memory.append(self.img.copy())
                self.show_image()
            except:
                return    
                
    def show_image(self):
        self.tk_img = ImageTk.PhotoImage(self.img)   
        self.label.config(image=self.tk_img)
        self.label.image = self.tk_img
        self.size_label.config(text=f"Size: {self.img.width}x{self.img.height}")
        self.draw_tool = ImageDraw.Draw(self.img)
        if len(self.memory) > 30:
            self.memory.pop(0)
        
    def enhance_contrast(self):
        if self.img:
            enhancer = ImageEnhance.Contrast(self.img)
            self.img = enhancer.enhance(1.5)
            self.memory.append(self.img.copy())
            self.show_image()
            
    def enhance_brightness(self):
        if self.img:
            enhancer = ImageEnhance.Brightness(self.img)
            self.img = enhancer.enhance(1.5)
            self.memory.append(self.img.copy())
            self.show_image()
      
    def lower_contrast(self):
        if self.img:
            enhancer = ImageEnhance.Contrast(self.img)
            self.img = enhancer.enhance(0.5)
            self.memory.append(self.img.copy())
            self.show_image()
            
    def lower_brightness(self):
        if self.img:
            enhancer = ImageEnhance.Brightness(self.img)
            self.img = enhancer.enhance(0.5)
            self.memory.append(self.img.copy())
            self.show_image()
            
    def invert_image(self):
        if self.img:
            self.img = ImageOps.invert(self.img.convert("RGB"))
            self.memory.append(self.img.copy())
            self.show_image()
         
    def apply_sepia(self):
        if self.img:
            img = self.img.convert("RGB")
            pixels = img.load()
            for y in range(img.height):
                for x in range(img.width):
                    r, g, b = pixels[x, y]
                    tr = int(0.393*r + 0.769*g + 0.189*b) 
                    tg = int(0.349*r + 0.686*g + 0.168*b)
                    tb = int(0.272*r + 0.534*g + 0.131*b)
                    pixels[x, y] = (min(tr,255), min(tg,255), min(tb,255))
            self.img = img       
            self.memory.append(self.img.copy()) 
            self.show_image()                            
            
    def remove_sepia(self):
        if self.img:
            img = self.img.convert("RGB")
            pixels = img.load()
            for y in range(img.height):
                for x in range(img.width):
                    tr, tg, tb = pixels[x, y]
                    r = int(1.164 * tr - 0.392 * tg - 0.05 * tb)
                    g = int(-0.213 * tr + 1.346 * tg - 0.239 * tb)
                    b = int(-0.101 * tr - 0.714 * tg + 3.022 * tb)
                    pixels[x, y] = (min(r,255), min(g,255), min(b,255))
            self.img = img
            self.memory.append(self.img.copy())
            self.show_image()
            
    def blur_image(self):
        if self.img:
            self.img = self.img.filter(ImageFilter.GaussianBlur(radius=2))
            self.memory.append(self.img.copy())
            self.show_image()
            
    def sharpen_image(self):
        if self.img:
            self.img = self.img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
            self.memory.append(self.img.copy())
            self.show_image()
            
    def undo(self):
        if self.img and self.memory:
            self.img = self.memory.pop()
            self.show_image()
        else:
            warnlabel = Label(self.root, text="Nothing to undo!")
            warnlabel.place(relx=0.9, rely=0.05)
            self.root.after(4000, warnlabel.destroy)            
        
    def to_rgb(self):
        if self.img:
            self.img = self.img.convert("RGB")
            self.memory.append(self.img.copy())
            self.show_image()
            
    def to_grayscale(self):
        if self.img:
            self.img = self.img.convert("L")
            self.memory.append(self.img.copy())
            self.show_image()
            
    def toggle_drawing(self):
        self.drawing = not self.drawing
        status = "ON" if self.drawing else "OFF"
        statlabel = Label(root, text=f"Drawing Mode: {status}")
        statlabel.place(relx=0.9, rely=0.05)
        self.root.after(4000, statlabel.destroy)
        
    def set_mouse(self, state):
        self.mouse_down = state
        if not state:
            self.last_draw = None
            self.draw_tool = None
            if self.img:
                self.memory.append(self.img.copy())
                
    def poll_mouse(self):
        if self.drawing and self.mouse_down and self.img:
            x = self.root.winfo_pointerx() - self.label.winfo_rootx()
            y = self.root.winfo_pointery() - self.label.winfo_rooty()
            if 0 <= x < self.label.winfo_width() and 0 <= y < self.label.winfo_height():
                img_x = int(x / self.label.winfo_width() * self.img.width)
                img_y = int(y / self.label.winfo_height() * self.img.height)
                if not hasattr(self, "draw_tool") or self.draw_tool is None:
                    self.draw_tool = ImageDraw.Draw(self.img)
                if self.last_draw:
                    self.draw_tool.line([self.last_draw, (img_x, img_y)], fill="black", width=3)
                self.last_draw = (img_x, img_y)
                self.tk_img = ImageTk.PhotoImage(self.img)
                self.label.config(image=self.tk_img)
                self.label.image = self.tk_img
        self.root.after(10, self.poll_mouse)             
                                                                                                                                                                                                                                                        
    def save_image(self):
        if self.img:
            path = filedialog.asksaveasfilename(defaultextension=".jpg")
            if path:
                self.img.save(path)
               
root = Tk()
editor = ImageEditor(root)
root.mainloop()                                 


import tkinter

from tkinter import filedialog, simpledialog, messagebox

from PIL import Image, ImageOps

#create a gif from images
def gifMake(paths,out_path,fps,sizeMax):
    if not paths:
        raise ValueError("Image is not selected") # in case of no image
    
    
    processed = [] #holding processed frames

    #build global palette so we have the first frame
    im0 = Image.open(paths[0]).convert("RGBA")
    if sizeMax:
        #if theres a max size then we resize
        im0 = ImageOps.contain(im0,(sizeMax,sizeMax))
    im0=im0.convert("RGB") #then convert to rgb
    p0=im0.quantize(colors=256,method=Image.MEDIANCUT) #256 color reduction
    palette=p0.getpalette() #color paletter exrracted
    processed.append(p0) #first frame added to list


    #frame resuing same palette
    for p in paths[1:]:
        im = Image.open(p).convert("RGBA") #everyimage opened
        if sizeMax:
            im = ImageOps.contain(im,(sizeMax,sizeMax)) #resize
        im=im.convert("RGB")
        q=im.quantize(colors=256,method=Image.MEDIANCUT) #same concept of quantize
        q.putpalette(palette)
        processed.append(q) #adding to said list


        #save it here, frames,add the duration, clear previous frame.etc
    processed[0].save(out_path,save_all=True,append_images=processed[1:],duration=int(1000/max(fps,1.0)),loop=0,disposal=2,optimize=True)


def main():
    #user asked to pick image
    file = filedialog.askopenfilenames(title="Image frames need to be selected",filetypes=[("Images","*.png;*.jpg;*.jpeg;*.webp;*.bmp")])
    if not file: return

    #then fps
    fps = simpledialog.askfloat("FPS","Frames per second:",initialvalue=12.0,minvalue=1.0,maxvalue=60.0)
    if not fps: return
    #max size of gif
    sizeMax = simpledialog.askinteger("Size","Max -- width/height (0 means no resize):",initialvalue=512,minvalue=0)
    #ask output of file
    
    out = filedialog.asksaveasfilename(defaultextension=".gif",filetypes=[("GIF","*.gif")],initialfile="out.gif")

    if not out: return
    try:
        gifMake(file,out,fps,sizeMax)
        #gif generation attempt
        messagebox.showinfo("Finished",f"Saved to {out}")
    except Exception as e:
        messagebox.showerror("Error!",str(e))


#main window
if __name__ =="__main__":
    root = tkinter.Tk()
    root.title("Gif maker")
    root.geometry("300x150")

    btn = tkinter.Button(root,text="CLICK TO MAKE A GIF!",command=main,font=("Arial",14))
    btn.pack(expand=True)

    root.mainloop()
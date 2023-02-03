import json
import tkinter as tk
from tkinter import messagebox

massAdditionCart = []
massAdditionElements = []

class Element:
  def __init__(self,symbol,name,number,category,group,period,mass):
    self.symbol = symbol
    self.name = name
    self.number = number
    self.category = category
    self.group = group
    self.period = period
    self.mass = mass
  
class PlacedElement:
  def __init__(self,row,column,element):
    self.row = row
    self.column = column
    self.element = element

def place_elements(elements):
  OFFSET = 2
  la_offset = 2
  ac_offset = 2

  for element in elements:
      period, group_name = element.period, element.group
      if group_name == 'La':
          group = la_offset + OFFSET
          la_offset += 1
          period += OFFSET
      elif group_name == 'Ac':
          group = ac_offset + OFFSET
          ac_offset += 1
          period += OFFSET
      else:
          group = group_name

      yield PlacedElement(row=period - 1, column=group - 1, element=element)

def load_json(filename: str = 'elements.json'):
  with open(filename, encoding='utf-8') as f:
      for element_dict in json.load(f):
          yield Element(**element_dict)

class MainMenu:
    def __init__(self, master):
        self.mode = None
        self.master = master
        self.frame = tk.Frame(self.master)
        self.button1 = tk.Button(self.frame, text = 'Compound Mass Calculator', width = 50, command = self.massCalc)
        self.button2 = tk.Button(self.frame, text = 'Electron Configuration Calculator', width = 50, command =  self.electronConfigCalc)
        self.button1.pack()
        self.button2.pack()
        self.frame.pack()
    
    def massCalc(self):
        self.newWindow = tk.Toplevel(self.master)
        elements = tuple(place_elements(load_json()))
        for element in elements:
          ElementButton(self.newWindow, element, 'Mass')
          
    def electronConfigCalc(self):
        self.newWindow = tk.Toplevel(self.master)
        self.button1 = tk.Button(self.newWindow, text = 'Button', width = 50)
        elements = tuple(place_elements(load_json()))
        for element in elements:
          ElementButton(self.newWindow, element, 'ElectronConfig')

class ElementButton:
  CATEGORY_COLORS = {'Alkalimetal': '#fbf8cc','AlkalineEarth': '#fde4cf','Transitionmetals': '#ffcfd2','Button': '#f1c0e8','Othermetals': '#cfbaf0','Nonmetal': '#a3c4f3','Halogen': '#90dbf4','Noblegases': '#8eecf5','Lanthanoid': '#98f5e1','Actinoid': '#b9fbc0'}

  def __init__(self, parent, placed_element, mode):
    self.mode = mode
    self.element = placed_element.element
    self.background = self.CATEGORY_COLORS[self.element.category]
    self.frame = frame = tk.Frame(
      parent, relief=tk.RAISED,
      name=f'frame_{self.element.symbol}',
      background=self.background,
      border=3,
    )
    self.frame.grid_columnconfigure(1, weight=2)
    self.frame.grid(row=placed_element.row, column=placed_element.column, sticky=tk.EW)

    self.populate()

    frame.bind('<ButtonPress-1>', self.press)
    frame.bind('<ButtonRelease-1>', self.release)
    for child in frame.winfo_children():
      child.bindtags((frame,))

  def populate(self):
    prefix = f'label_{self.element.symbol}_'
    if self.element.category != 'Button':
      tk.Label(
        self.frame, name=prefix + 'number',
        text=self.element.number, background=self.background,
      ).grid(row=0, column=0, sticky=tk.NW)
    
      tk.Label(
        self.frame, name=prefix + 'mass',
        text=self.element.mass, background=self.background,
      ).grid(row=4, column=0, sticky=tk.NE)
  
      tk.Label(
        self.frame, name=prefix + 'symbol',
        text=self.element.symbol, font='bold', background=self.background
      ).grid(row=1, column=0, sticky=tk.EW, columnspan=3)
      
      tk.Label(
        self.frame, name=prefix + 'name',
        text=self.element.name, background=self.background,
      ).grid(row=2, column=0, sticky=tk.EW, columnspan=3)
    else:
      if self.mode == 'Mass':
        tk.Label(
          self.frame, name = prefix + 'button',
          text= self.element.name, background=self.background,
        ).grid(row=0, column=0, sticky=tk.EW, columnspan=10)

  def electronConfig(self):
    electrons = self.element.number
    orbitals = {'1s':0,'2s':0,'2p':0,'3s':0,'3p':0,'4s':0,'3d':0,'4p':0,'5s':0,'4d':0,'5p':0,'6s':0,'4f':0,'5d':0,'6p':0,'7s':0,'5f':0,'6d':0,'7p':0}
    for i in orbitals:
      if i[1] == 's':
        while orbitals[i] < 2 and electrons:
          orbitals[i] += 1
          electrons -= 1
      elif i[1] == 'p':
        while orbitals[i] < 6 and electrons:
          orbitals[i] += 1
          electrons -= 1
      elif i[1] == 'd':
        while orbitals[i] < 10 and electrons:
          orbitals[i] += 1
          electrons -= 1
      elif i[1] == 'f':
        while orbitals[i] < 14 and electrons:
          orbitals[i] += 1
          electrons -= 1
    return orbitals 

  def formatElectronConfig(self,electronConfig):
    result = ''
    for i in electronConfig:
      if electronConfig[i] != 0:
        result += str(i) + str(electronConfig[i]) + ' '
    return result
   
  def press(self, event):
    self.frame.configure(relief='sunken')
  
  def release(self, event):
    self.frame.configure(relief='raised')
    if self.element.category != 'Button':
      if self.mode == 'Mass':
        massAdditionCart.append(self.element.mass)
        massAdditionElements.append(self.element.name)

        messagebox.showinfo("Element added", "Elements lined up to be calculated: " + str(massAdditionElements))
                                
      if self.mode == "ElectronConfig":
        messagebox.showinfo("Result", "The electron configuration of " + self.element.name + " is: " + str(self.formatElectronConfig(self.electronConfig())))
        
    else:
      if self.element.name == 'Calculate':
        if sum(massAdditionCart) != 0:
          messagebox.showinfo("Result","The total mass of the compound is " + str(round(sum(massAdditionCart),2)))
          massAdditionCart.clear()

        else:
          messagebox.showinfo("Error", "Please select elements to calculate the total mass before calculating.")
          
      if self.element.name == 'Clear All':
        massAdditionCart.clear()
        massAdditionElements.clear()
        messagebox.showinfo("Elements Cleared", "Elements to be calculated has been cleared.")

def main(): 
    root = tk.Tk()
    root.title('Chemistry Helper')
    MainMenu(root)
    root.mainloop()

if __name__ == '__main__':
    main()

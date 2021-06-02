import numpy as np
import pandas as pd
import os
import tkinter as tk
from pandastable import Table
from datetime import date
from tkinter import filedialog
root = tk.Tk()
root.withdraw()
delete_row=[]
delete_rad=[]
row=[]
sug={}
party_a_c={}
veh_cmp={}
base_path=''
mov_path=''
rcm_veh_nos=[]
rcm_drivers_mob_no={}
rcm_drivers=[]
rcm_place_adv=[]
mov_reg=pd.DataFrame()
def get_key(val,my_dict):
    for key, value in my_dict.items():
         if val in value:
             return key
    return ""
mov_reg_cols=np.asarray(['Party','A/C of Party','Size','Movement','Party Ref','Container No','From', 'To-1','To-2','Vehicle No','Company Name','Invoice No','Invoice Date','Invoice Amount','Trip Sheet No','Trip Sheet Amount','Trip Sheet Date','Cash','Advance','Fixed Advance','Diesel Per Litre','Diesel Advance','Fixed Diesel Advance','Status','Driver Name' ])
choices = dict(zip(mov_reg_cols.tolist(), [0]*len(mov_reg_cols)))
spec_suggest_cols={'Party':'A/C of Party','Company Name':'Driver Name'}
dir_sug=['Party','From','To-1','To-2','From','Vehicle No']
indir_sug=['A/C of Party','Vehicle No','Driver Name']
veh_status=['Vehicle No','Driver Name','From','To-1','To-2','Party','Status']
mov_reg=pd.DataFrame()
today=date.today().strftime("%d-%m-%Y")
def browse_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global base_path,mov_reg,mov_path,rcm_veh_nos,rcm_drivers_mob_no,rcm_drivers,rcm_place_adv
    folder_path = tk.StringVar()
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    base_path=filename
    mov_path = base_path+'/Movement Register.xlsx'
    if base_path!='':
        path=base_path+'/Data.xlsx'
        if not os.path.exists(path):
            df1=pd.DataFrame(columns =['Driver Name', 'Mobile Number'])
            df2=pd.DataFrame(columns =['Vehicle Numbers'])
            df3=pd.DataFrame(columns =['From','To-1','To-2','Fixed Advance','Fixed Diesel Advance'])
            writer = pd.ExcelWriter(path, engine='xlsxwriter')
            df1.to_excel(writer, sheet_name='Driver_Mobile',index=False)
            df2.to_excel(writer, sheet_name='Vehicle Numbers',index=False)
            df3.to_excel(writer, sheet_name='Place_Advance',index=False)
            writer.save()
            disp_df(label="Data.xlsx file has been created please fill in the necessary details to proceed")
            win.destroy()
        rcm_veh_nos=pd.read_excel(path,na_filter=False,sheet_name='Vehicle Numbers').values.tolist()
        rcm_veh_nos=[item for sublist in rcm_veh_nos for item in sublist]
        rcm_drivers_mob_no=pd.read_excel(path,na_filter=False,sheet_name='Driver_Mobile').to_dict()
        rcm_drivers=list(rcm_drivers_mob_no['Driver Name'].values())
        rcm_place_adv=pd.read_excel(path,na_filter=False,sheet_name='Place_Advance').values.tolist()
        mov_reg=initialize()
        init_wind()
win=tk.Toplevel(root)
win.title("App")
btn = tk.Button(master=win,text="Choose Base Folder", command=browse_button)
btn.pack()
def initialize(colnames=None):
    global party_a_c,veh_cmp
    mov_reg = excel_df(mov_path)
    if mov_reg is False: #excel file does not exists
        mov_reg=pd.DataFrame(columns=mov_reg_cols) #Creating Empty Data-Frame with Required Columns
    tmp = mov_reg[['Party','A/C of Party']].values.tolist()
    for key, val in tmp:
        party_a_c.setdefault(key, []).append(val) 
    tmp = mov_reg[['Company Name','Vehicle No']].values.tolist()
    for key, val in tmp:
        veh_cmp.setdefault(key, []).append(val) 
    if colnames is not None:
        def clicked():
            veh_stat=mov_reg.loc[(mov_reg['Trip Sheet Date'] == txt.get() ) & (mov_reg['Company Name'] == 'RCM') ][colnames]
            c_keys=[get_key(item,rcm_drivers_mob_no['Driver Name']) for item in veh_stat['Driver Name'].to_string(index=False).split()] #Both Mob no and Dri_name has common key
            try:
                veh_stat['Mobile No']=[rcm_drivers_mob_no['Mobile Number'][c_key] for c_key in c_keys ] #Reading mobile number based on common key
                disp_df(veh_stat)
            except KeyError:
                    disp_df()
        win0=tk.Toplevel(root)
        win0.title("Date")
        lbl = tk.Label(win0,text="Date")
        lbl.pack(side=tk.LEFT)
        txt = tk.Entry(win0,width=30)
        txt.pack(side=tk.LEFT)
        txt.insert(tk.END, today)
        btn = tk.Button(win0,text="Submit",command=clicked)
        btn.pack(side=tk.LEFT)
    return mov_reg
def excel_df(file_name):
  try:
    df = pd.read_excel(file_name,na_filter=False) ##Read as dataframe
    df = df.drop('S.No', axis=1) #Drop S.No to prevent duplication
  except FileNotFoundError:
    df=False
  return df

def add_row_bet(mov_reg,indices,mov_reg_cols=mov_reg_cols):
#  for i in range(0, len(mov_reg_cols) ):
#    row.append(input(mov_reg_cols[i])) #Reading a Row for The Data-Frame in list form
    win1 = tk.Toplevel(root)
    win1.geometry("1000x1000")
    win1.title("Movement Register")
    size=''
    mvt=''
    i=0
    select1 = tk.StringVar()
    select2 = tk.StringVar()
    for key in choices.keys():
        if key=='Fixed Advance' or key=='Fixed Diesel Advance':
            continue
        lbl = tk.Label(win1, text=key)
        lbl.grid(row=i,column=0)
        if key=="Size":
            j=1
            value=['20','40']
            for val in value:
                def chosen_SIZE():
                    nonlocal size
                    size=select1.get()
                rad1 = tk.Radiobutton(win1,text=val, value=val, variable=select1,command=chosen_SIZE)
                rad1.grid(row=i,column=j,sticky="ew")            
                j+=3
        elif key=="Movement":
            j=1
            value=['IMPORT','EXPORT','EMPTY','O/L']
            for val in value:
                def chosen_MVT():
                    nonlocal mvt
                    mvt=select2.get()
                rad2 = tk.Radiobutton(win1,text=val, value=val, variable=select2,command=chosen_MVT)
                rad2.grid(row=i,column=j,sticky="ew")
                j+=2
        else:
            txt = tk.Entry(win1,width=30)
            txt.grid(row=i,column=1)
        def go_to_next_entry(event, entry_list, this_index,label_list):
                next_index = (this_index + 1) % len(entry_list)
                if label_list[this_index]["text"] =="Size":
                    del label_list[this_index]
                elif label_list[this_index]["text"] =="Movement":
                    del label_list[this_index]
                entry_list[next_index].focus_set()
        def go_to_prev_entry(event, entry_list, this_index):
                prev_index = (this_index - 1) % len(entry_list)
                entry_list[prev_index].focus_set()
    
        entries = [child for child in win1.winfo_children() if isinstance(child, tk.Entry)]
        labels = [child for child in win1.winfo_children() if isinstance(child, tk.Label) ]
        for idx, entry in enumerate(entries):
            if idx==0:#Defualt focus on first element
                entry.focus()
            entry.bind('<Return>', lambda e, idx=idx: go_to_next_entry(e, entries, idx,labels))
            entry.bind('<Down>', lambda e, idx=idx: go_to_next_entry(e, entries, idx,labels))
            entry.bind('<Up>', lambda e, idx=idx: go_to_prev_entry(e, entries, idx))
            entry.bind("<Button-1>", lambda e: "break")
        select1.set(delete_rad[0])
        select2.set(delete_rad[1])
        for this_index, entry in enumerate(entries):
             entries[this_index].delete(0,tk.END)
             entries[this_index].insert(0,delete_row[this_index])
        i=i+1
    lbl = tk.Label(win1, text="This Row has been Deleted Please Re-submit if No Edits required")
    lbl.grid(row=i+2,column=0)
    def clear(event,entries):
        nonlocal select1,select2
        select1.set(' ')
        select2.set(' ')
        for idx,entry in enumerate(entries):
             entries[idx].delete(0,tk.END)
    def calc_fixed(From,To_1,To_2):
        for data in rcm_place_adv:
            if data[0]==From and data[1]==To_1 and data[2]==To_2:
                return data[3],data[4]
        return "",""
    def clicked(event,entry_list,this_index,label_list):
        global mov_reg,choices
        nonlocal indices,select1,select2
        mov_reg=initialize()
        choices["Size"]=select1.get()
        choices["Movement"]=select2.get()
        for this_index, entry in enumerate(entries):
            if label_list[this_index]["text"] =="Size":
                    del label_list[this_index]
            if label_list[this_index]["text"] =="Movement":
                    del label_list[this_index]
            choices[label_list[this_index]["text"]]=entry_list[this_index].get()
            choices["Fixed Advance"],choices["Fixed Diesel Advance"]=calc_fixed(choices["From"],choices["To-1"],choices["To-2"])
            msg = tk.Label(win1, text="Submitted Successfully")
            msg.grid(row=i+4, column=0)
            win1.after(5000, msg.destroy)
            print(list(choices.values()))
        row=list(choices.values());
        mov_reg = insert_row(initialize(),indices,row)
        if os.path.exists(mov_path):
            os.remove(mov_path)
        mov_reg.index = mov_reg.index + 1
        mov_reg.to_excel(mov_path,index_label='S.No')
        win1.destroy()
        disp_df(initialize())
    btn_1 = tk.Button(win1, text="Submit")
    btn_1.bind("<Button-1>",lambda e, idx=idx: clicked(e, entries, idx,labels))
    btn_1.grid(row=i+3,column=1)
    btn_2 = tk.Button(win1, text="Clear")
    btn_2.bind("<Button-1>",lambda e: clear(e, entries))
    btn_2.grid(row=i+3,column=2)
    print(choices)
    print(list(choices.values()))

def add_row_end(mov_reg,mov_reg_cols=mov_reg_cols):
#  for i in range(0, len(mov_reg_cols) ):
#    row.append(input(mov_reg_cols[i])) #Reading a Row for The Data-Frame in list form    
    win2=tk.Toplevel(root)
    win2.geometry("1000x1000")
    win2.title("Movement Register")
    mod1 = tk.Frame(win2)
    mod1.grid(row=0, column=0, sticky="nsew")
    size=''
    mvt=''
    i=0
    select1 = tk.StringVar()
    select1.set(' ')
    select2 = tk.StringVar()
    select2.set(' ')
    mod2 = tk.Frame(win2)
    mod2.grid(row=0, column=1, sticky="nsew")
    row_val=0
    def update_listbox(data):
       # Clear the listbox
       list_box.delete(0, tk.END)
       print(data)
       # Add suggestions to listbox
       for item in data:
         list_box.insert(tk.END, item)
     
     # Update txt box with listbox clicked
    def update(e,widget):
       # Delete txt box
       widget.delete(0, tk.END)
     
       # Add clicked list item to txt box
       widget.insert(0, list_box.get(tk.ANCHOR))
       widget.focus_set()
     # Check txt box vs listbox
    def check(e,value):
       # get typed text
       typed_text = e.widget.get()
     
       if typed_text == '':
         data = value
       else:
         data = []
         for item in value:
           if typed_text.lower() in item.lower():
             data.append(item)
     
       # update our listbox
       update_listbox(data) 

    # Create a listbox
    list_box = tk.Listbox(mod2,height=len(choices))
    list_box.grid(row=row_val+1,column=1)
    var=tk.StringVar()
    var.set(' ')
    for key in choices.keys():
        if key=='Fixed Advance' or key=='Fixed Diesel Advance':
            continue
        lbl = tk.Label(mod1, text=key)
        lbl.grid(row=i,column=0)
        if key=="Size":
            j=1
            value=['20','40']
            for val in value:
                def chosen_Size():
                    nonlocal size
                    size=select1.get()
                rad1 = tk.Radiobutton(mod1,text=val, value=val, variable=select1,command=chosen_Size)
                rad1.grid(row=i,column=j,sticky="ew")            
                j+=3
        elif key=="Movement":
            j=1
            value=['IMPORT','EXPORT','EMPTY','O/L']
            for val in value:
                def chosen_MVT():
                    nonlocal mvt
                    mvt=select2.get()
                rad2 = tk.Radiobutton(mod1,text=val, value=val, variable=select2,command=chosen_MVT)
                rad2.grid(row=i,column=j,sticky="ew")
                j+=2
        else:
            txt = tk.Entry(mod1,width=30)
            txt.grid(row=i,column=1)
            def go_to_list_box(event, entry_list, this_index,label):
                global sug
                suggestion=[""]
                if label  in dir_sug:
                    suggestion = suggest(label)
                    entry_list[(this_index+1)%len(entry_list)].delete(0, tk.END)
                    entry_list[(this_index+1)%len(entry_list)].insert(0, str(get_key(entry_list[this_index].get(),veh_cmp)))                    
                elif label == "Company Name":
                    entry_list[(this_index+1)%len(entry_list)].delete(0, tk.END)
                    if entry_list[this_index].get() in str(rcm_veh_nos):
                        entry_list[(this_index+1)%len(entry_list)].insert(0, 'RCM')
                    else:
                        entry_list[(this_index+1)%len(entry_list)].insert(0, str(get_key(entry_list[this_index].get(),veh_cmp)))
                elif label == "Driver Name":
                    val = suggest(label,entry_list[this_index-10].get())
                    if isinstance(val, str):
                        entry_list[(this_index+1)%len(entry_list)].delete(0, tk.END)
                        entry_list[(this_index+1)%len(entry_list)].insert(0, val)
                    else:
                        suggestion=val
                elif label in indir_sug:
                    suggestion =suggest(label,sug[label])
                suggestion = list(set(suggestion))
                list_box.bind("<<ListboxSelect>>", lambda e: update(e, entry_list[(this_index+1)% len(entry_list)]))
                # Create a binding on the txt box
                entry_list[(this_index+1)% len(entry_list)].bind("<KeyRelease>", lambda e: check(e,suggestion))
            def go_to_next_entry(event, entry_list, this_index,label):
                global sug
                prev_label=list(mov_reg_cols)[list(mov_reg_cols).index(label)-1]
                if prev_label in spec_suggest_cols.keys():
                    sug[spec_suggest_cols[prev_label]]=entry_list[this_index].get() 
                go_to_list_box(event, entry_list, this_index,label)
                next_index = (this_index + 1) % len(entry_list)
                entry_list[next_index].focus_set()
        entries = [child for child in mod1.winfo_children() if isinstance(child, tk.Entry)]
        labels = [child for child in mod1.winfo_children() if isinstance(child, tk.Label) ]
        for idx, entry in enumerate(entries):
            if labels[idx]["text"] =="Size":
                    del labels[idx]
            if labels[idx]["text"] =="Movement":
                    del labels[idx]
            #Removing label based on radiobuttons
        lab_ent = dict(zip(entries, labels))
        #Before pressing any keys defualt condition focus on 1st element, suggest 1st element's suggestion, check and update 1st element based suggestions,,,,
        entries[0].focus()
        suggestion = suggest('Party')
        update_listbox(suggestion)
        list_box.bind("<<ListboxSelect>>", lambda e: update(e, entries[0]))
        # Create a binding on the txt box
        entries[0].bind("<KeyRelease>", lambda e: check(e,suggestion))
        for idx, entry in enumerate(entries):
            entry.bind('<Return>', lambda e, idx=idx: go_to_next_entry(e, entries, idx,lab_ent[entries[(entries.index(mod1.focus_get())+1)%len(entries)]]["text"]))
            entry.bind('<Down>', lambda e, idx=idx: go_to_next_entry(e, entries, idx,lab_ent[entries[(entries.index(mod1.focus_get())+1)%len(entries)]]["text"]))
            entry.bind("<Button-1>", lambda e: "break")
        i=i+1
    def clear(event,entries):
        nonlocal select1,select2
        select1.set(' ')
        select2.set(' ')
        for idx,entry in enumerate(entries):
             entries[idx].delete(0,tk.END)
             if idx==0:
                 entry.focus()
    def calc_fixed(From,To_1,To_2):
        for data in rcm_place_adv:
            if data[0]==From and data[1]==To_1 and data[2]==To_2:
                return data[3],data[4]
        return "",""        
    def clicked(event,entry_list,this_index,label_list):
        global mov_reg,choices
        mov_reg=initialize()
        global row
        choices["Size"]=size
        choices["Movement"]=mvt
        for this_index, entry in enumerate(entries):
            if label_list[this_index]["text"] =="Size":
                    del label_list[this_index]
            if label_list[this_index]["text"] =="Movement":
                    del label_list[this_index]
            choices[label_list[this_index]["text"]]=entry_list[this_index].get()
            choices["Fixed Advance"],choices["Fixed Diesel Advance"]=calc_fixed(choices["From"],choices["To-1"],choices["To-2"])
            msg = tk.Label(win2, text="Submitted Successfully")
            msg.grid(row=i+4, column=0)
            win2.after(5000, msg.destroy)
        print(choices)
        mov_reg = mov_reg.append(choices,ignore_index=True) #Add Row to Dataframe
        if os.path.exists(mov_path):
                os.remove(mov_path)
        mov_reg.index = mov_reg.index + 1
        mov_reg.to_excel(mov_path,index_label='S.No')    
    btn_1 = tk.Button(mod1, text="Submit")
    btn_1.bind("<Button-1>",lambda e, idx=idx: clicked(e, entries, idx,labels))
    btn_1.grid(row=i+3,column=1)
    btn_2 = tk.Button(mod1, text="Clear")
    btn_2.bind("<Button-1>",lambda e: clear(e, entries))
    btn_2.grid(row=i+3,column=2)
    print(choices)
    print(list(choices.values()))

def add_row(list_return=False):
    global mov_reg
    add_row_end(mov_reg)

def row_view(df=initialize()):
        row_val=0
        win2 = tk.Toplevel(root)
        win2.geometry("1000x1000")
        win2.title("Modify Entry")
        mod=tk.Frame(win2)
        mod.pack()
        for choice in choices:
            lbl = tk.Label(mod, text=choice)
            lbl.grid(row=row_val,column=0)
            choices[choice]=tk.IntVar()
            chk = tk.Checkbutton(mod,text="",variable=choices[choice])
            chk.deselect()
            chk.grid(row=row_val,column=1,sticky="ew")
            row_val+=1
        def clicked(e):
            global mov_reg
            mov_reg=initialize()
            result=Filter(df,[key for key,val in choices.items() if val.get()==1])
            disp_df(result)
        btn = tk.Button(mod, text="Submit")
        btn.bind("<Button-1>", clicked)
        btn.grid(row=row_val+3,column=1)
        print([key for key,val in choices.items() if val.get()==0])

def col_view():
    win3 = tk.Toplevel(root)
    win3.title("Modify Entry")
    mod = tk.Frame(win3)
    mod.pack()
    row_val=0
    def update_listbox(data):
       # Clear the listbox
       list_box.delete(0, tk.END)
     
       # Add columns to listbox
       for item in data:
         list_box.insert(tk.END, item)
     
     # Update txt box with listbox clicked
    def update(e):
       # Delete txt box
       txt.delete(0, tk.END)
     
       # Add clicked list item to txt box
       txt.insert(0, list_box.get(tk.ANCHOR))
     
     # Check txt box vs listbox
    def check(e):
       # get typed text
       typed_text = txt.get()
     
       if typed_text == '':
         data = cols
       else:
         data = []
         for item in cols:
           if typed_text.lower() in item.lower():
             data.append(item)
     
       # update our listbox
       update_listbox(data) 
      # Create an Entry.. box
    txt = tk.Entry(mod)
    txt.grid(row=row_val,column=0)
     
    # Create a listbox
    list_box = tk.Listbox(mod)
    list_box.grid(row=row_val+1,column=0)
     
    cols=mov_reg_cols.tolist()
     # Add the columns to our list
    update_listbox(cols)
     
     # Create a binding on the listbox
    list_box.bind("<<ListboxSelect>>", update)
     
     # Create a binding on the txt box
    txt.bind("<KeyRelease>", check)
    txt1 = tk.Entry(mod)
    txt1.grid(row=row_val,column=1)
    lbl = tk.Label(mod, text="1.Add ',' for multiple filtering.\n\t2.Edit and Delete can be done only for single rows.")
    lbl.grid(row=row_val+6,column=0)
    var=tk.StringVar()
    var.set(' ')
    var1=tk.IntVar()
    var1.set(0)
    lbl1 = tk.Label(mod, text="Edit")
    lbl1.grid(row=row_val+2,column=0)
    rad1 = tk.Radiobutton(mod,variable=var,value="Edit")
    rad1.grid(row=row_val+2,column=1)
    lbl2 = tk.Label(mod, text="Delete")
    lbl2.grid(row=row_val+2,column=2)
    rad2 = tk.Radiobutton(mod,variable=var,value="Delete")
    rad2.grid(row=row_val+2,column=3)
    lbl3 = tk.Label(mod, text="View")
    lbl3.grid(row=row_val+3,column=0)
    rad3 = tk.Radiobutton(mod,variable=var,value="View")
    rad3.grid(row=row_val+3,column=1)
    lbl4 = tk.Label(mod, text="Select Rows")
    lbl4.grid(row=row_val+3,column=2)
    chk = tk.Checkbutton(mod,variable=var1)
    chk.grid(row=row_val+3,column=3)
    def clicked(e):
        if var.get()=="Edit":
                Filter(initialize(),txt.get(),txt1.get(),True)
        elif var.get()=="Delete":
                Filter(initialize(),txt.get(),txt1.get(),True,True)
        elif var1.get()==1 and var.get()=="View":
                        row_view(Filter(initialize(),txt.get(),txt1.get()))
        elif var1.get()==1 and var.get()!="View":
                        row_view(initialize())
        elif var1.get()==0 and var.get()=="View":
                 disp_df(Filter(initialize(),txt.get(),txt1.get()))
    btn = tk.Button(mod, text="Submit")
    btn.grid(row=row_val+6,column=2)
    btn.bind("<Button-1>",clicked)

def init_wind():
    global mov_reg
    mov_reg=initialize()
    win.destroy()
    win4=tk.Toplevel(root)
    win4.title("Menu")
    btn_1 = tk.Button(win4, text="Data Entry",command=add_row)
    btn_1.pack()
    btn_2 = tk.Button(win4, text="Modify Data",command=col_view)
    btn_2.pack()
    btn_3 = tk.Button(win4,text="Display",command=lambda: disp_df(initialize()))
    btn_3.pack()
    btn_4 = tk.Button(win4,text="Vehicle Status",command=lambda: initialize(veh_status))
    btn_4.pack()
    try:
        if os.path.exists(mov_path):
            os.remove(mov_path)
        mov_reg.index = mov_reg.index + 1
        mov_reg.to_excel(mov_path,index_label='S.No')
    except Exception:
        win.destroy()
        win4.destroy()
        disp_df(label="Close the opened Excel file")

def disp_df(df=None,label="No entries found"):
    error_msg = tk.StringVar()
    error_msg.set(label)
    if  df is None or df.empty:
        frame = tk.Toplevel(root)
        lbl = tk.Label(frame, textvariable=error_msg)
        lbl.grid(row=1,column=0)
    else:
        class TestApp(tk.Frame):
                """Basic test frame for the table"""
                def __init__(self, parent=None):
                    tk.Frame.__init__(self,parent)
                    self.parent = parent
                    self.main = self.master
                    self.main.title('Display')
                    f = tk.Frame(self.main)
                    f.pack(fill=tk.BOTH,expand=1)
                    self.table = pt = Table(f, dataframe=df,
                                            showtoolbar=False, showstatusbar=True)
                    self.label = tk.Label(self.main, text="File Name")
                    self.label.pack(side="left")
                    self.entry = tk.Entry(self.main)
                    self.entry.pack(side="left")
                    self.btn = tk.Button(self.main, text="Export")
                    self.btn.pack(side="left")
                    self.btn.bind("<Button-1>", lambda e: clicked(e,self.entry.get()))
                    pt.show()
                    return
        def clicked(e,file_name):
            path=base_path+'/'+file_name+'.xlsx'
            if os.path.exists(path):
                os.remove(path)
            df.reset_index(drop=True,inplace=True)
            df.index = df.index + 1
            disp_df(label="Saved in your computer")
            df.to_excel(path,index_label='S.No')
        frame = tk.Toplevel(root)
        app=TestApp(frame)
        app.pack()

def Filter(df,df_row=None,df_choice=None,df_write=False,delete=False):
  global row,mov_reg,delete_row,delete_rad
  if df_row is not None and df_choice is None:
    return df[df_row]
  elif df_row is not None and df_choice is not None:
      df_choice = df_choice.split(',')
      result = df.loc[df[df_row].isin(df_choice)]
      if df_write==False:
            return result
      else:
           if len(result.index)!=1:
               disp_df(label="Either there are no rows or multiple rows fulfilling the condition")
           else:
               indices=result.index[0]
               delete_row=df.iloc[indices].tolist()
               delete_row.pop(18)
               delete_row.pop(19)
               for i in range(2):
                   delete_rad.append(delete_row.pop(2)) #Remove Radio Parameters and add them as seperate list
               df.drop(df.index[indices] , inplace =True)
               disp_df(df)
               if os.path.exists(mov_path):
                   os.remove(mov_path)
               df.to_excel(mov_path,index_label='S.No')
               if delete is False:
                   add_row_bet(initialize(),indices)

def insert_row(df,row_number,row_value):
  # Slice the upper half of the dataframe
    df1 = df[0:row_number]
   
    # Store the result of lower half of the dataframe
    df2 = df[row_number:]
   
    # Insert the row in the upper half dataframe
    df1.loc[row_number]=row_value
   
    # Concat the two dataframes
    df_result = pd.concat([df1, df2])
   
    # Reassign the index labels
    df_result.index = [*range(df_result.shape[0])]
    df_result.index+=1
    # Return the updated dataframe
    return df_result

def suggest(col_name,ref=None):
   ##ref is the textbox's value
    if ref is None:
        return list(set(initialize()[col_name].values.tolist()))
    else:
        try:
           if col_name =='A/C of Party':
               return party_a_c[ref]
           elif col_name=='Driver Name':
               if ref =='RCM':
                   return rcm_drivers
               elif ref =='':
                   return ''
               else:
                   return "Other Company"
        except KeyError:
            return [""]        
root.mainloop()
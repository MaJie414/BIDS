import os,sys,re,json,pickle
from tkinter import *
from tkinter import ttk,messagebox
from tkinter.filedialog import askdirectory, askopenfilename
import shutil,textwrap
import numpy as np

def on_closing(root):
    root.destroy()
    sys.exit(0)
def wrap(string, lenght=20):
    return '\n'.join(textwrap.wrap(string, lenght))
def write_lack_json(type,**jsonname):
    if not os.path.exists(os.path.join(os.getcwd(),'jsonfiles','temp')):
        os.makedirs(os.path.join(os.getcwd(),'jsonfiles','temp'))
    if ' ' in type:
        anat_type = type.split(' ')[1]
    def save_json():  # get the text from tk.Text widget
        tar_text,miss = get_data()
        if miss!=1:
            if 'create' in type:
                filename = os.path.join(os.getcwd(), 'jsonfiles','temp',f'{subID}_{anat_type}.json')
            elif type == 'ieeg':
                filename = jsonname['jsonname']
            else:
                filename = os.path.join(targetpath,  'data_description.json')

            with open(filename, 'w') as f:
                json.dump(tar_text, f, indent=4)
            root.destroy()

    if type == 'data_description' or type =='ieeg':
        with open(os.path.join(os.getcwd(), 'jsonfiles', '{}.json'.format(type)), 'r') as f:
            data = json.load(f)
    else:
        with open(os.path.join(os.getcwd(),'jsonfiles', 'anat_{}.json'.format(anat_type)), 'r') as f:
            data = json.load(f)
    text = ''
    root = Tk()
    if type =='ieeg':
        Label(root,text = os.path.split(jsonname['jsonname'])[-1].replace(f'{subID}_',''),fg='red',font=(12)).grid(row=0)
    else:
        Label(root, text=type,fg='red',font=(12)).grid(row=0)
    columns= ('label','description')
    treeview = ttk.Treeview(root, height=18, show="headings", columns=columns)

    treeview.column("label", width=100, anchor='center')  # 表示列,不显示
    treeview.column("description", width=300, anchor='center')

    treeview.heading("label", text="label")  # 显示表头
    treeview.heading("description", text="description")

    for key, value in data.items():
        treeview.insert("",'end',values=[key,value])
    treeview.grid(row=1,column=0,sticky='news')
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.title(f'write the {type} json')

    def del_cell_value(event):  # 双击右键删除
        for item in treeview.selection():
            treeview.delete(item)
        treeview.update()
    def set_cell_value(event):  # 双击左键进入编辑状态
        for item in treeview.selection():
            item_text = treeview.item(item, "values")
        def saveedit():
            treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
            win.destroy()
        column = treeview.identify_column(event.x)  # 列
        col1 = int(column[1::])-1
        win = Tk()
        win.title('编辑框')
        entryedit = Text(win)
        entryedit.insert(INSERT,item_text[col1])
        entryedit.grid(row=0,column=0)
        okb = Button(win, text='OK', width=4, command=saveedit)
        okb.grid(row=1,column=0)
        win.mainloop()
    def newrow():
        treeview.insert('', 'end', values=['None','None'])
        treeview.update()
    def get_data():
        tar_text = {}
        miss=0
        for line in treeview.get_children():
            values = treeview.item(line)['values']
            tar_text[values[0]] = values[1]
            if values[0] in ["Instructions","Marker Meaning","Experiment information"]:
                if len(values[1])<=20:
                    messagebox.showwarning('Warning',f'请尽可能详细的描述{values[0]}')
                    miss = 1
        return tar_text,miss
    treeview.bind('<Double-1>', set_cell_value)
    treeview.bind('<Double-3>', del_cell_value)
    newb = ttk.Button(root, text='add info', width=20, command=newrow)
    newb.grid(row=2,column=0)
    newb = ttk.Button(root, text='Done', width=20, command=save_json)
    newb.grid(row=3,column=0)
    root.mainloop()
'''
step 1: get the informations about paths 
'''

class get_path_info():
    def __init__(self, root):
        self.root = root
        self.paths ={1:StringVar(),
                     2:StringVar(),
                     3:StringVar(),}
        self.subID = StringVar()
        self.all_files ={}
    def files(self,i):
        path_ = askdirectory()
        self.paths[i].set(path_)

    def confirm_input(self):
        message = []
        if self.paths[1].get() == '':
            message.append('anatpath not set')
        if self.paths[2].get() == '':
            message.append('Filepath not set')
        if self.paths[3].get() == '':
            message.append('Targetpath not set')
        if self.subID.get() == '':
            message.append('Subject ID not set')
        matchObj = re.search(r'([gs])_([a-z]*)_(\d{6,})',self.subID.get())
        if not matchObj:
            message.append('The subID has format error!\n\n e.g. g/s_xx(拼音)_123456(6位日期)')
        else:
            if len(matchObj.group(3))>6:
                message.append('The subID has format error!\n\n e.g. g/s_xx(拼音)_123456(6位日期)')
        sub_anat_path = os.path.join(self.paths[1].get(),self.subID.get())
        if not os.path.exists(sub_anat_path):
            message.append(f'The subID-{self.subID.get()} is not in the anat folder')
        else:
            anat_files = os.listdir(sub_anat_path)
            if f'{self.subID.get()}_rT1.nii.gz' not in anat_files:
                message.append('rT1 is not in the anat folder')
            elif f'{self.subID.get()}_rCT_seeg.nii.gz' not in anat_files:
                message.append('CT is not in the anat folder')
            elif f'{self.subID.get()}_Contactor.fcsv' not in anat_files:
                message.append('contactor.fcsv is not in the anat folder')
        if message!= []:
            messagebox.showwarning('warning',message[0])
        else:
            if os.path.exists(os.path.join(self.paths[3].get(),f'{self.subID.get()}')):
                overwrite = messagebox.askyesno('warning', f'The sub: {self.subID.get()} is existed!\n\nDo you want to overwrite it?')
                if overwrite:
                    shutil.rmtree(os.path.join(self.paths[3].get(),f'{self.subID.get()}'))
            #         self.root.destroy()
            # else:
            self.root.destroy()
    def get_files(self,path):
        seeg_file, anat_file,  behaviour_files,info,derivatives= \
            [], [], [], [], []
        for root_path, dirs, files in os.walk(path, topdown=False):
            for name in files:
                filename = os.path.join(root_path, name)
                filetype = os.path.splitext(filename)[1]
                if filetype == '.edf':# or filetype == '.fif'or filetype == '.m00'
                    seeg_file.append(filename)
                elif 'behaviour.mat' in filename:
                    behaviour_files.append(filename)
                elif filetype == '.mat' or filetype=='.pdf':
                    info.append(filename)
        anat_file.extend(['CT json','T1 json'])
        all_files = { 'anat_file':anat_file,
                      'seeg_file': seeg_file,
                      'behaviour_files':behaviour_files,
                      'info':info}#'json_files': json_files,'tsv_files': tsv_files,
        return all_files
    def window(self):
        pwd = os.getcwd()
        def text_path(type):
            try:
                textfile = open(os.path.join(pwd, f'{type}.txt'), 'rb')
                input_path = textfile.read().strip().decode('utf-8')
                if '\ufeff' in input_path:
                    input_path = input_path.replace('\ufeff', '')
                textfile.close()
                if not os.path.exists(input_path):
                    messagebox.showerror('warning', 'targetpath does not exist!')
                    input_path = ''
            except:
                input_path = ''
            return input_path
        targetpath = text_path('targetpath')
        anatpath = text_path('anatpath')
        self.paths[1].set(anatpath)
        self.paths[3].set(targetpath)
        Label(self.root, text='anat path').grid(row=0, column=0)
        entry = Entry(self.root, textvariable=self.paths[1]).grid(row=0, column=1,sticky='ew',columnspan=2)
        Button(self.root, text='path', command=lambda :self.files(1)).grid(row=0, column=3)
        Label(self.root, text='files path').grid(row=1, column=0)
        entry = Entry(self.root, textvariable=self.paths[2]).grid(row=1, column=1,sticky='ew',columnspan=2)
        Button(self.root, text='path', command=lambda :self.files(2)).grid(row=1, column=3)
        Label(self.root, text='target path').grid(row=2, column=0)
        entry = Entry(self.root, textvariable=self.paths[3]).grid(row=2, column=1,sticky='ew',columnspan=2)
        Button(self.root, text='path', command=lambda :self.files(3)).grid(row=2, column=3)
        Label(self.root, text='Subject ID').grid(row=3, column=0)
        entry = Entry(self.root, textvariable=self.subID).grid(row=3, column=1,sticky='ew',columnspan=2)
        Label(self.root, text='ieeg type').grid(row=4, column=0)
        self.ieeg_type = StringVar()
        Radiobutton(self.root, text='CCEP', variable=self.ieeg_type, value= "CCEP").grid(row=4, column=1)
        Radiobutton(self.root, text='SEEG', variable=self.ieeg_type, value="SEEG" ).grid(row=4, column=2)
        self.ieeg_type.set('SEEG')
        Button(self.root, text='OK', command= self.confirm_input,width=10).grid(row=5, column=1)

# path_info contains informations of inputpath,targetpath, subID and filtered files

win = Tk()
win.columnconfigure(1,weight=3)
win.title('BIDS ieeg')
path_info = get_path_info(win)
path_info.window()
win.protocol("WM_DELETE_WINDOW", lambda :on_closing(win))
win.mainloop()

anat_path,files_path, targetpath,subID,ieeg_type = path_info.paths[1].get(),path_info.paths[2].get(),path_info.paths[3].get(),path_info.subID.get(),path_info.ieeg_type.get()
all_files = path_info.get_files(files_path)
with open(os.path.join(os.getcwd(),'infos.pkl'),'wb') as f:
    pickle.dump([anat_path,files_path, targetpath,subID,all_files],f)

# with open(os.path.join(os.getcwd(),'infos.pkl'),'rb') as f:
#     [anat_path,files_path, targetpath,subID,all_files] = pickle.load(f)

# while not os.path.exists(os.path.join(targetpath,'data_description.json')):
# write_lack_json('data_description')



class define_files():
    def __init__(self, root):
        self.root = root
        self.filenames = {}
        self.types = []
        self.session_nums = []
        self.run_nums = []
        self.tasknames = []
        self.deri_widgets = {}
        frame_main = Frame(root)
        frame_main.grid(sticky='news')
        canvas = Canvas(frame_main)
        canvas.grid(row=0, column=0, sticky="news")
        # Link a scrollbar to the canvas
        vsb = Scrollbar(frame_main, orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)
        # Create a frame to contain the buttons
        self.frame_buttons = Frame(canvas)
        self.frame_buttons.grid(sticky='news')
        # create column name
        Label(self.frame_buttons,text = 'filename or path').grid(row=0,column=1)
    def getdirsize(self,dir):
        size = 0
        if os.path.isdir(dir):
            for root, dirs, files in os.walk(dir):
                size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
        else:
            size = os.path.getsize(dir)
        return size
    def create_json(self,type):
        loc = subID[0]
        type = type.split(' ')[0]
        comvalue = StringVar()  # 窗体自带的文本，新建一个值
        comboxlist = Radiobutton(self.frame_buttons, text='shanghai', variable=comvalue,
                                 value=os.path.join(os.getcwd(), 'jsonfiles', f'shanghai_anat_{type}.json'),
                                 command=lambda row=self.rownum: self.select_json(row))
        comboxlist.grid(row=self.rownum, column=4, sticky=W)
        if loc.lower() == 's':
            comboxlist.select()
        comboxlist = Radiobutton(self.frame_buttons, text='guangzhou', variable=comvalue,
                                 value=os.path.join(os.getcwd(), 'jsonfiles', f'guangzhou_anat_{type}.json'),
                                 command=lambda row=self.rownum: self.select_json(row))
        comboxlist.grid(row=self.rownum, column=5, sticky=W,columnspan=2)
        if loc.lower() == 'g':
            comboxlist.select()
        comboxlist = Radiobutton(self.frame_buttons, text='create json', variable=comvalue, value=f'create {type} json',
                                 command=lambda row=self.rownum: self.select_json(row))
        comboxlist.grid(row=self.rownum, column=6, sticky=W)
        anat_type = StringVar()
        Label(self.frame_buttons, textvariable=anat_type).grid(row=self.rownum, column=1,sticky=W)
        anat_type.set(f'{type} json')
        session = StringVar()
        run = StringVar()
        taskname = StringVar()
        return [comvalue, anat_type,session, run, taskname]
    def select_json(self, row):
        # d1 =  self.filenames[row][0].get()
        if 'creat' in self.filenames[row][0].get():
            write_lack_json(self.filenames[row][0].get())
    def get_targetfile_info(self, filename, type, session, run, subID, task):  # parametre only accept str type
        if 'anat-' in type or type in ['CT json', 'T1 json']:
            filepath = os.path.join(targetpath, f'{subID}', 'anat')
        elif type == 'ieeg-ieeg' or type == 'behaviour file':
            filepath = os.path.join(targetpath, f'{subID}', 'ieeg', f'ses-{session}')
        elif type in ['patient info','Electrode','Implantation','Fusion','History','MR','else']:
            filepath = os.path.join(targetpath, f'{subID}', 'info')
        else:
            filepath = os.path.join(targetpath, f'{subID}')

        file_format = '.'.join(filename.split('.')[1::])
        if type == 'ieeg-ieeg' or type == 'behaviour file':
            targetfilename = os.path.join(filepath,
                                              f'{subID}_ses-{session}_run-{run}_task-{task}_{type.split("-")[-1].split(" ")[0]}.{file_format}')
            for del_type in ['run','task']:
                if locals()[del_type] =='':
                    targetfilename = targetfilename.replace(f'_{del_type}-{locals()[del_type]}','')
        elif 'anat' in type:
            targetfilename = os.path.join(filepath,
                                              f'{subID}_{type.split("-")[-1].split(" ")[0]}.{file_format}')
        elif type in ['CT json', 'T1 json']:
            targetfilename = os.path.join(filepath,
                                          '{}_{}.{}'.format(subID,  type.split('-')[-1].split(" ")[0],
                                                                              file_format))
        elif 'source' in type:
            targetfilename = filepath
        else:
            targetfilename = os.path.join(filepath, f'{type.split(" ")[0]}.{file_format}')
        return targetfilename
    def get_files(self):
        targetinfos = []
        del_key = []
        for key in self.filenames.keys():
            value = self.filenames[key]
            if value == ['','','','','']:
                del_key.append(key)
            elif 'Stimuli' in value:
                del_key.append(key)
                targetinfos.append([value[0].get(),os.path.join(targetpath,'Stimuli')])
        for i in del_key:
            del self.filenames[i]
        for i in self.filenames.values():
            filename, type, session,run, taskname = list(map(lambda x:x.get(),i))
            if filename=='None' or type=='None':
                continue
            else:
                targetinfos.append([filename, self.get_targetfile_info(filename, type, session, run, subID, taskname)])
        for i in self.deri_widgets:
            filepath = os.path.join(targetpath,  f'{subID}','derivatives', self.deri_widgets[i][1].get())
            if os.path.isdir(self.deri_widgets[i][0].get()):
                targetfilename = filepath
            else:
                file_format = os.path.splitext(self.deri_widgets[i][0].get())[1]
                targetfilename = os.path.join(filepath,
                                              f'{subID}_{self.deri_widgets[i][1].get()}{file_format}')
            targetinfos.append([self.deri_widgets[i][0].get(),targetfilename])
        cm = confirm_and_move_files(self.root, targetinfos)
        cm.confirm_files(self.filenames,self.deri_widgets)
    def add_filepath(self, event,  row,**para):
        if list(para.values())[0] == 'Stimuli':
            if self.filenames[row][0].get() == 'select folder':
                dd = askdirectory()
                self.filenames[row][0].set(dd)
            elif self.filenames[row][0].get()  == 'select file':
                dd = askopenfilename()
                self.filenames[row][0].set(dd)
        else:
            if self.deri_widgets[row][0].get() == 'select folder':
                dd = askdirectory()
                self.deri_widgets[row][0].set(dd)
            elif self.deri_widgets[row][0].get() == 'select file':
                dd = askopenfilename()
                self.deri_widgets[row][0].set(dd)

    def creat_row_in_root(self,row_info,key,value):
        label = StringVar()
        if key == 'info' or key =='anat_file':
            Label(self.frame_buttons, text = (row_info + '  size = %.2f Mb'%(self.getdirsize(row_info)/1024/1024)).replace(files_path,'...')).grid(row=self.rownum, column=1,sticky=W)
        elif key =='behaviour_files':
            Label(self.frame_buttons,
                  text=(row_info + '  size = %.2f Kb' % (self.getdirsize(row_info) / 1024 )).replace(files_path,
                                                                                                           '...')).grid(
                row=self.rownum, column=1, sticky=W)
        else:
            Label(self.frame_buttons,
                  text=(row_info + '  size = %.2f Gb' % (self.getdirsize(row_info) / 1024 / 1024/ 1024)).replace(files_path,
                                                                                                           '...')).grid(
                row=self.rownum, column=1, sticky=W)

        label.set(row_info)
        max_len = max(list(map(lambda x: len(x),value)))
        comvalue = StringVar()  # 窗体自带的文本，新建一个值
        comboxlist = ttk.Combobox(self.frame_buttons, textvariable=comvalue, values=value, width=max_len+2,height=20)  # 初始化
        comboxlist.grid(row=self.rownum, column=2,padx=15,pady=5,sticky=W)
        comboxlist.current(0)
        if key!='anat_file' and key!='info':
            session = StringVar()
            Entry(self.frame_buttons,textvariable=session,width=8).grid(row=self.rownum,column=4,padx=15)
            run = StringVar()
            Entry(self.frame_buttons,textvariable=run,width=8).grid(row=self.rownum,column=5,padx=15)
            taskname = StringVar()
            Entry(self.frame_buttons, textvariable=taskname, width=8).grid(row=self.rownum, column=6,padx=15)
        else:
            session = StringVar()
            run = StringVar()
            taskname = StringVar()
        return [label, comvalue,session,run,taskname]
    def del_rowwidget(self,row):
        row_widget = self.deri_widgets[row]
        begin_row = self.begin_row
        row_widget[0].grid_forget()
        row_widget[1].grid_forget()
        row_widget[2].grid_forget()
        del self.deri_widgets[row]
        self.rownum -= 1
        for key,values in self.deri_widgets.items():
            values[0].grid(row=begin_row, column=1, padx=15, pady=5, sticky=W)
            values[1].grid(row=begin_row, column=2)
            values[2].grid(row=begin_row, column=3, columnspan=2)
            begin_row += 1
        self.b1.grid(row=self.rownum+1, column=1, columnspan=4)
        self.b2.grid(row=self.rownum + 2, column=1, columnspan=4)
    def derivation_rowinfo(self):
        comvalue = StringVar()
        comboxlist = ttk.Combobox(self.frame_buttons, textvariable=comvalue,
                                  values=['None', 'select file', 'select folder'], width=40)  # 初始化
        comboxlist.grid(row=self.rownum, column=1, padx=15, pady=5, sticky=W)
        comboxlist.bind('<<ComboboxSelected>>', lambda event, row=self.rownum: self.add_filepath(event, row,type='deri'))
        comboxlist.current(0)
        derifile = StringVar()
        e = Entry(self.frame_buttons, text=derifile)
        e.grid(row=self.rownum,column=2)
        b3 = Button(self.frame_buttons, text='—', command=lambda r=self.rownum: self.del_rowwidget(r),width=8)
        b3.grid(row=self.rownum, column=3, columnspan=2)
        self.deri_widgets[self.rownum]=[comboxlist,e,b3,comvalue,derifile]
        self.rownum += 1
        self.b1.grid(row=self.rownum,column=1,columnspan=4)
        self.b2.grid(row=self.rownum+1,column=1,columnspan=4)
    def add_row_indo(self,filename,type,session,run,task):
        self.filenames[self.rownum] = [filename,type,session,run,task]
        self.rownum += 1
    def rows_data(self,all_files):
        self.rownum = 1
        if not os.path.exists(os.path.join(targetpath,'Stimuli')):
            comvalue = StringVar()
            comboxlist = ttk.Combobox(self.frame_buttons, textvariable=comvalue,
                                      values=['None', 'select file', 'select folder'], width=40)  # 初始化
            comboxlist.grid(row=self.rownum, column=1, padx=15, pady=5, sticky=W)
            comboxlist.bind('<<ComboboxSelected>>', lambda event, row=self.rownum: self.add_filepath(event, row,type='Stimuli'))
            comboxlist.current(0)
            Label(self.frame_buttons, text='Stimuli').grid(row=self.rownum, column=0)
            self.filenames[self.rownum] = [comvalue, 'Stimuli', '', '', '']
            self.rownum += 1
        types = { 'anat_file':['anat-CT', 'anat-T1w','None'], 'seeg_file': ['ieeg-ieeg','None'],
                  'behaviour_files':['behaviour file','None'],'info':{'mat':['patient info','Electrode'],'pdf':['Implantation','Fusion','History','MR','else','None']}}

        for key,files in all_files.items():
            if key == 'behaviour_files' and ieeg_type =='CCEP':
                continue
            value = types[key]
            # -------------------------数据分割线以及列名 -----------------------------------
            sh = ttk.Separator(self.frame_buttons, orient=HORIZONTAL)
            sh.grid(row=self.rownum, column=0, columnspan=9, sticky="we")
            self.add_row_indo('','','','','')
            Label(self.frame_buttons, text=f'{key.split("_")[0]}_files').grid(row=self.rownum, column=0)
            if key == 'seeg_file':
                Label(self.frame_buttons, text='file type').grid(row=self.rownum, column=2)
                Label(self.frame_buttons, text='session num').grid(row=self.rownum, column=4)
                Label(self.frame_buttons, text='run num').grid(row=self.rownum, column=5)
                Label(self.frame_buttons, text='taskname').grid(row=self.rownum, column=6)
            self.add_row_indo('','','','','')
            # ----------------------------------------------------------------------------------
            if len(files) != 0:
                for file in files:
                    if file in ['CT json','T1 json']:
                        filename,type,session,run,task = self.create_json(file)
                    elif isinstance(value,dict):
                        filename,type,session,run,task = self.creat_row_in_root(file,key,value[file.split('.')[-1]])
                    else:
                        filename,type,session,run,task = self.creat_row_in_root(file,key,value)
                    self.add_row_indo(filename,type,session,run,task)
        sh = ttk.Separator(self.frame_buttons, orient=HORIZONTAL)
        sh.grid(row=self.rownum, column=0, columnspan=9, sticky="we")
        self.add_row_indo('','','','','')
        Label(self.frame_buttons, text='derivative_files').grid(row=self.rownum, column=0)
        Label(self.frame_buttons, text='label').grid(row=self.rownum, column=2)
        self.begin_row = self.rownum +1
        self.b1= Button(self.frame_buttons,text = '+',command=self.derivation_rowinfo,width=15)
        self.b1.grid(row=self.rownum+1,column=1,columnspan=4)
        self.b2 = Button(self.frame_buttons,text = 'OK',command=self.get_files,width=15)
        self.b2.grid(row=self.rownum+2,column=1,columnspan=4)
        self.rownum = self.rownum+1


class confirm_and_move_files():
    def __init__(self,root, targetinfos):
        self.root = root
        self.targetinfos = targetinfos
    def confirm_files(self, filenames,deri_widgets):
        types ,session_nums, run_nums,tasks = [],[],[],[]
        for i in filenames.values():
            types.append(i[1].get())
            session_nums.append(i[2].get())
            run_nums.append(i[3].get())
            tasks.append(i[4].get())
        miss = []
        # CCEP 数据忽略行为数据
        if ieeg_type=='SEEG':
            must_type = ['ieeg-ieeg','behaviour file','patient info','Fusion','Electrode']
        else:
            must_type = ['ieeg-ieeg', 'patient info', 'Fusion', 'Electrode']
        types = np.asarray(types)
        lack_type = list(set(must_type)-set(types))
        if len(lack_type)>0:
            miss.append(f'{lack_type[0]} is missing')
        ieeg_index = np.where((types=='ieeg-ieeg') | (types=='behaviour file'))[0]#index of ieeg-related data
        ieeg_types = types[ieeg_index]
        session_nums = np.asarray(session_nums)[ieeg_index]
        run_nums = np.asarray(run_nums)[ieeg_index]
        sess_run = list(set(map(lambda x,y:(x,y),session_nums,run_nums)))
        none_index = np.where(ieeg_types=='None')
        none_session,none_run = np.delete(session_nums,none_index), np.delete(run_nums,none_index)
        if '' in none_session:#'' in none_run or
            miss.append('number of session or run is not set')
        ieeg_index = np.where(ieeg_types=='ieeg-ieeg')[0]
        if len(ieeg_index) < len(sess_run):
            i=[]
            for index in ieeg_index:
                i.append((session_nums[index],run_nums[index]))
            diff = list(set(sess_run) - set(i))
            miss.append(f'ieeg of session{diff[0][0]}_run{diff[0][1]} is missing\n')
        if ieeg_type == 'SEEG':
            bahaviour_index = np.where(ieeg_types == 'behaviour file')[0]
            if len(bahaviour_index) < len(sess_run):
                i = []
                for index in ieeg_index:
                    i.append((session_nums[index], run_nums[index]))
                diff = list(set(sess_run) - set(i))
                miss.append(f'bahaviour of session{diff[0][0]}_run{diff[0][1]} is missing\n')
        if len(deri_widgets)!=0:
            for key,value in deri_widgets.items():
                if value[1].get() == '':
                    miss.append(f"The file -{value[0].get()}\n is not set label yet")
         # 暂时允许可缺失文件
        miss1 = []
        source_ieeg_index = np.where(ieeg_types=='source ieeg')[0]
        for index in source_ieeg_index:
            i = (session_nums[index],run_nums[index])
            if i not in sess_run:
                miss.append(f'source ieeg of session{i[0]}_run{i[1]} is missing\n')
        if miss1!=[]:
            messagebox.showinfo('lack files',miss1)
        if miss == []:
            self.move_files()
            self.root.destroy()
            for filename, targetfilename in self.targetinfos:
                if '.edf' in targetfilename:
                    jsonfilename = targetfilename.replace('.edf', '.json')
                    while not os.path.exists(jsonfilename):
                        write_lack_json('ieeg', jsonname=jsonfilename)
        else:
            messagebox.showwarning('lack file',miss[0])
    def move_files(self):
        for filename, targetfilename in self.targetinfos:
            if filename == 'None':
                continue
            parent_path = os.path.split(targetfilename)[0]
            if 'create' in filename:
                continue
            if '.' not in targetfilename:
                if '.' in filename:
                    if not os.path.exists(targetfilename):
                        os.makedirs(targetfilename)
                    shutil.copy(filename,targetfilename)
                else:
                    shutil.copytree(filename, targetfilename)
            else:
                if not os.path.exists(parent_path):
                    os.makedirs(parent_path)
                shutil.copy(filename, targetfilename)
            print(f'{filename} is coping')
        jsons = os.listdir(os.path.join(os.getcwd(), 'jsonfiles'))
        for json_file in jsons:
            if f'{subID}' in json_file:
                shutil.move(os.path.join(os.getcwd(), 'jsonfiles',json_file),
                            os.path.join(targetpath,f'{subID}','anat',json_file))
        shutil.copy(os.path.join(anat_path,subID,f'{subID}_rT1.nii.gz'),os.path.join(targetpath,subID,'anat'))
        shutil.copy(os.path.join(anat_path, subID, f'{subID}_rCT_seeg.nii.gz'), os.path.join(targetpath, subID, 'anat', f'{subID}_CT.nii.gz'))
        if not os.path.exists(os.path.join(targetpath, subID, 'derivatives','Slicer')):
            os.makedirs( os.path.join(targetpath, subID, 'derivatives','Slicer'))
        shutil.copy(os.path.join(anat_path, subID, f'{subID}_Contactor.fcsv'), os.path.join(targetpath, subID, 'derivatives','Slicer'))
        if os.path.exists(os.path.join(anat_path, subID, f'{subID}_Scene.mrml')):
            shutil.copy(os.path.join(anat_path, subID, f'{subID}_Scene.mrml'),
                        os.path.join(targetpath, subID, 'derivatives', 'Slicer'))
        if os.path.exists(os.path.join(os.getcwd(), 'jsonfiles', 'temp')):
            shutil.rmtree(os.path.join(os.getcwd(),'jsonfiles','temp'))
        if not os.path.exists(os.path.join(os.getcwd(),'jsonfiles','temp')):
            os.makedirs(os.path.join(os.getcwd(),'jsonfiles','temp'))
win = Tk()
win.title('BIDS ieeg')
files_info = define_files(win)
files_info.rows_data(all_files)
win.protocol("WM_DELETE_WINDOW", lambda :on_closing(win))
win.mainloop()
#
# print(f'The data of {subID} has been collated')

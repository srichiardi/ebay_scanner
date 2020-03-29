import os
from tkinter import *
from tkinter import filedialog
from modules.eBayGlobalMap import globalSiteMap


##-------------------------------------------------------------##
##-----------------------------GUIs----------------------------##
##-------------------------------------------------------------##

class appDlg(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.title("ELA (eBay Listing App)")
        self.geometry("655x415")
        rootDir = os.path.split(os.path.split(__file__)[0])[0] # default output folder in parent dir
        self.optionsDict = { 'outputFolder' : rootDir,
                            'sites' : [] }
        
        self.wdgts = [{ 'label' : 'Seller ID',
                         'input' : 'entry',
                         'appOpt' : 'sellerId' },
                        { 'label' : 'Search description',
                          'input' : 'option',
                          'appOpt' : 'descriptionSearch' },
                        { 'label' : 'Keywords',
                          'input' : 'entry',
                          'appOpt' : 'keywords' },
                        { 'label' : 'Save to: ',
                          'input' : 'browse',
                          'appOpt' : 'outputPath' }
                        ]
        
        OptMainFrame = Frame(self)
        OptMainFrame.pack(side=TOP,padx=5)
        
        BtnFrame = Frame(self)
        BtnFrame.pack(side=TOP, padx=5, fill=X)
        btnRun = Button(BtnFrame, text="Run", width=6, command=self.close)
        btnRun.pack(side=RIGHT,padx=10)
        
        # right frame for search options
        searchOptFrame = Frame(OptMainFrame)
        searchOptFrame.pack(side=RIGHT,padx=5)
        searchOptLbl = Label(searchOptFrame, text = "Search options:")
        searchOptLbl.pack(side=TOP, padx=5)
        
        for level in self.wdgts:
            frame = Frame(searchOptFrame)
            frame.pack(pady=5,side=TOP,fill=X)
            label = Label(frame,text=level['label'])
            if level['input'] == 'entry':
                wdgt = Entry(frame,width=30)
            elif level['input'] == 'option':
                var = IntVar()
                wdgt = Checkbutton(frame, variable=var)
                level['var'] = var
            elif level['input'] == 'browse':
                wdgt = Button(frame, text="Browse", command=self.outputDir)
            wdgt.pack(side=RIGHT,padx=5)
            label.pack(side=RIGHT,padx=5)
            level['wdgt'] = wdgt
        
        # left frame with site options
        siteOptFrame = Frame(OptMainFrame)
        siteOptFrame.pack(side=RIGHT, padx=5)
        siteOptLbl = Label(siteOptFrame, text = "eBay sites:")
        siteOptLbl.pack(side=TOP, padx=5)
        
        siteOptCont = Frame(siteOptFrame)
        siteOptCont.pack(side=TOP, padx=5)
        
        optsPerCol = 11 # 11 options per column
        optionsList = list(globalSiteMap.keys())
        optionsList.sort()
        optionsMatrix = [optionsList[i:i+optsPerCol] for i in range(0,len(optionsList),optsPerCol)]
        self.siteOpts = {}
        
        for col in optionsMatrix:
            colFrame = Frame(siteOptCont)
            colFrame.pack(side=LEFT, padx=5)
            for opt in col:
                frame = Frame(colFrame)
                frame.pack(side=TOP, padx=5, fill=X)
                label = Label(frame, text=globalSiteMap[opt]['name'])
                var = StringVar()
                wdgt = Checkbutton(frame, variable=var, 
                                   onvalue=opt)
                wdgt.pack(side=RIGHT, padx=5)
                label.pack(side=RIGHT, padx=5)
                wdgt.deselect() # disabled by default
                self.siteOpts[opt] = { 'var' : var, 'wdgt' : wdgt }
                
        selectFrame = Frame(siteOptFrame)
        selectFrame.pack(side=TOP, padx=5, fill=X)
        selAllBtn = Button(selectFrame, text="Select all", command=self.selAll)
        selAllBtn.pack(side=RIGHT, padx=5)
        deSelBtn = Button(selectFrame, text="Clear all", command=self.selNone)
        deSelBtn.pack(side=RIGHT, padx=5)
        euSelBtn = Button(selectFrame, text="EU only", command=self.selEU)
        euSelBtn.pack(side=RIGHT, padx=5)
        

    def outputDir(self):
        self.optionsDict['outputFolder'] = filedialog.askdirectory()
        
        
    def selAll(self):
        for opt in self.siteOpts.keys():
            self.siteOpts[opt]['wdgt'].select()
    
    
    def selNone(self):
        for opt in self.siteOpts.keys():
            self.siteOpts[opt]['wdgt'].deselect()
            
            
    def selEU(self):
        for opt in self.siteOpts.keys():
            if opt in ['FR', 'DE', 'NL', 'PL', 'CH', 'IT', 'AT', 'IE', 'ES', 
                       'BE-FR', 'BE-NL', 'GB']:
                self.siteOpts[opt]['wdgt'].select()
            else:
                self.siteOpts[opt]['wdgt'].deselect()

    
    def close(self):
        for level in self.wdgts:
            if level['input'] == 'entry' and level['wdgt'].get() != '':
                self.optionsDict[level['appOpt']] = level['wdgt'].get()
            elif level['input'] == 'option':
                if level['var'].get() == 1:
                    self.optionsDict[level['appOpt']] = 'true'
                else:
                    self.optionsDict[level['appOpt']] = 'false'
                    
        for opt in self.siteOpts.keys():
            if self.siteOpts[opt]['var'].get() != '0':
                self.optionsDict['sites'].append(self.siteOpts[opt]['var'].get())
        self.destroy()


    def mainloop(self):
        Tk.mainloop(self)
        return self.optionsDict

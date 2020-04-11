import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
import json
import re
from PIL import Image, ImageTk

   
# チェックボタンのラベルをリスト化する
chk_txt = ['年齢','身長','体重','バスト','ウェスト','ヒップ','学生区分']


autocompleteList =[]


#名前検索、サジェスト
class AutocompleteEntry(tk.Entry):
    def __init__(self, autocompleteList, *args, **kwargs):

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 8

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)
                
            self.matchesFunction = matches

        
        tk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.autocompleteList = autocompleteList
        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Return>", self.selection)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        
        self.listboxUp = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                if not self.listboxUp:
                    self.listbox = tk.Listbox(width=self["width"], height=self.listboxLength)
                    self.listbox.bind("<Button-1>", self.selection)
                    self.listbox.bind("<Return>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                
                self.listbox.delete(0, tk.END)
                for w in words:
                    self.listbox.insert(tk.END,w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False
        
    def selection(self, event):
        if self.listboxUp:
            self.var.set(self.listbox.get(tk.ACTIVE))
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(tk.END)

    def moveUp(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
                
            if index != '0':                
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)
                
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '0'
            else:
                index = self.listbox.curselection()[0]
                
            if index != tk.END:                        
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)
                
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index) 

    def comparison(self):
        return [ w for w in self.autocompleteList if self.matchesFunction(self.var.get(), w) ]
if __name__ == '__main__':

    def matches(fieldValue, acListEntry):
        pattern = re.compile(re.escape(fieldValue) + '.*', re.IGNORECASE)
        return re.match(pattern, acListEntry)


#位置を決める変数
kijun_x=550
kijun_y=105
x_marge=60
y_marge=50
entry_var=0

#並び替えの時に使う
show_size=[]
count=0
image_hosyu=[]
#アイドルのプロフィールを表示する
def idol_pr_show(idol):
    #新規ウィンドウの中身
    rooting=tk.Tk()
    # 画面サイズ
    rooting.geometry('700x600')
    # 画面タイトル
    rooting.title('アイドルプロフィール')
    rooting.configure(bg=idol.data[14])
    profile_show=tk.Label(rooting,text="\n\n"+idol.data[0]+"\n\n年齢:"+str(idol.data[1])+"歳\n\n身長:"+str(idol.data[2])+"cm\n\n体重"+str(idol.data[3])+"kg\n\nB:"+str(idol.data[4])+"cm\n\nW:"+str(idol.data[5])+"cm\n\nH:"+str(idol.data[6])+"cm\n\n誕生日:"+idol.data[7]+"\n\n血液型:"+idol.data[8]+"\n\n利き手:"+idol.data[9]+"\n\n趣味:"+idol.data[10]+"\n\n特技:"+idol.data[11]+"\n\n好きなもの:"+idol.data[12]+"\n\n出身地:"+idol.data[13],font=("",14),background=idol.data[14])
    # 画像を開く
    image = Image.open(idol.data[15])
    # tkinter.PhotoImage ではなく ImageTk.PhotoImage() を使う
    photo = ImageTk.PhotoImage(image, master=rooting)
    image_hosyu.append(photo)
    tk.Label(rooting, image = photo).place(x=30,y=130)
    profile_show.place(x=400,y=30)
    

#アイドルボタンの挙動
def idol_btn(name_box,idols):
    for i in range(0,len(idols)):
        idol_name=name_box.get()
        #アイドル検索の方で新しいウィンドウを作る
        global autocompleteList
        if(idol_name==idols[i].data[0] or idol_name==autocompleteList[i] or idol_name==autocompleteList[i+52] or idol_name==autocompleteList[i+52*2]):
            idol_pr_show(idols[i])
            break
        #名前全員不一致
        if(i==len(idols)-1):
            warning()

#アイドル絞り込み関数
def tintin_select(min_get,max_get,seiheki,list_idols):
    global flag
    min_place=0
    max_place=0
    flag="false"
    #min=max
    if(min_get==max_get):
        for t in range(len(list_idols)):
            if(float(min_get)==list_idols[t].data[seiheki]):
                min_place=t-1
                break
        for s in range(len(list_idols)):
            if(float(max_get)==list_idols[len(idols)-s-1].data[seiheki]):
                max_place=len(idols)-s
                break
    #min!=max
    if(min_get!=max_get):
        max_get=int(max_get)+1
        for x in range(0,len(list_idols)):
            if(list_idols[x].data[seiheki]<float(min_get)):
                min_place=x
            if(list_idols[x].data[seiheki]<float(max_get)):
                max_place=x+1

    #リストの中身がゼロになるとき
    if(min_place==len(list_idols)-1 or max_place==0):
        warning()
        flag="true"
        return
    #ならないとき
    marge=len(list_idols)-(max_place-min_place)
    if(min_place!=len(list_idols)-1 and max_place!=0):
        if(marge!=0):
            end=len(list_idols)
            if(min_place!=0):
                for i in range(min_place+1):
                    list_idols.pop(0)
            if(max_place!=end):
                for i in range(max_place,end):
                    list_idols.pop(-1)



#並び替えボタン    
def change_order(list_idols):
    global kind
    global up_or_down
    global chk_txt
    orderby=0
    for i in range(len(chk_txt)):
        if(chk_txt[i]==kind):
            orderby=i+1
            break

    if(up_or_down=="大きい順"):
        for s in range(len(list_idols)-1):
            for t in range(s,len(list_idols)):
                if(float(list_idols[s].data[orderby])<float(list_idols[t].data[orderby])):
                    swap=list_idols[s]
                    list_idols[s]=list_idols[t]
                    list_idols[t]=swap    
    if(up_or_down=="小さい順"):
        for s in range(len(list_idols)-1):
            for t in range(s,len(list_idols)):
                if(float(list_idols[s].data[orderby])>float(list_idols[t].data[orderby])):
                    swap=list_idols[s]
                    list_idols[s]=list_idols[t]
                    list_idols[t]=swap  
    global idols_name
    for i in range(len(idols_name)):
        idols_name[i].destroy()
    idol_button(list_idols)
    #絞り込みに使った値を表示
    global show_size
    global count
    placex=70
    placey=220
    if(count!=0):
        for i in range(len(show_size)):
            show_size[i].place_forget()
    show_size=[]
    if(orderby==1):
        for i in range(len(list_idols)):
            show_size.append(tk.Label(root2,text=str(int(list_idols[i].data[orderby]))+"歳",font=("",16)))
            show_size[i].place(x=placex+(i%7)*160,y=placey+int((i/7))*100)
    if(orderby==3):
        for i in range(len(list_idols)):
            show_size.append(tk.Label(root2,text=str(list_idols[i].data[orderby])+"kg",font=("",16)))
            show_size[i].place(x=placex+(i%7)*160,y=placey+int((i/7))*100)
    else:
        for i in range(len(list_idols)):
            show_size.append(tk.Label(root2,text=str(list_idols[i].data[orderby])+"cm",font=("",16)))
            show_size[i].place(x=placex+(i%7)*160,y=placey+int((i/7))*100)
            
    count=count+1
    
    
#アイドルの情報を表示するボタン            
def idol_button(list_idols):
    global idols_name
    idols_name = []
    for i in range(0,len(list_idols)):
    #名前が長くて隣と重なるので短く
            if(list_idols[i].data[0]=="エミリースチュアート"):
                list_idols[i].data[0]="エミリー"
                #怪しい
            idols_name.append([])
            idols_name[i]=tk.Button(root2,command=partial(idol_pr_show,list_idols[i]),text=list_idols[i].data[0],background=list_idols[i].data[14],font=("",14))
            #表示の時は戻す
            if(list_idols[i].data[0]=="エミリー"):
                list_idols[i].data[0]="エミリースチュアート"
            idols_name[i].place(x=50+(i%7)*160,y=180+int((i/7))*100)
            
    
    
#絞り込み結果表示
def idol_show(list_idols,root):
    #ウィンドウ表示
    root.destroy()
    #新規ウィンドウの中身
    global root2
    root3=tk.Tk()
    # 画面サイズ
    root3.geometry('1200x600')
    # 画面タイトル
    root3.title('絞り込み結果')
    
    # Canvas Widget を生成
    canvas = tk.Canvas(root3)

    # Top Widget上に Scrollbar を生成して配置
    bar = tk.Scrollbar(root3, orient=tk.VERTICAL)
    bar.pack(side=tk.RIGHT, fill=tk.Y)
    bar.config(command=canvas.yview) # ScrollbarでCanvasを制御

    # Canvas Widget をTopWidget上に配置
    canvas.config(yscrollcommand=bar.set) # Canvasのサイズ変更をScrollbarに通知
    canvas.config(scrollregion=(0,0,1200,1000)) #スクロール範囲
    #ホイールでも動かす
    canvas.bind_all("<MouseWheel>", lambda eve:canvas.yview_scroll(int(-eve.delta/120), 'units'))
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Frame Widgetを 生成
    root2 = tk.Frame(canvas)

    # Frame Widgetを Canvas Widget上に配置（）
    canvas.create_window((0,0), window=root2, anchor=tk.NW, width=1200, height=1000)


    #アイドルの名前を表示
    condition=[]
    global idols_name
    idols_name = []
    idol_button(list_idols)           
    #並び変え用 
    frame=tk.Frame(root2,width=700, height=100, bg="pink")
    frame.place(x=250,y=10)
    label=tk.Label(root2,text="並び変え",font=("",20),bg="yellow",fg="blue")
    label.place(x=255,y=15)
    combo_placex=400
    combo_placey=50
    #種類を選ぶドロップダウンメニュー
    global kind
    global up_or_down
    #ドロップダウンを変更したときに実行
    def select_kind(event):
        global kind
        kind=txt1.get()
    def select_updown(event):
        global up_or_down
        up_or_down=txt2.get()
    
    txt1 = tk.StringVar()
    sort_kind = ttk.Combobox(root2, textvariable=txt1,state='readonly',font=("",16),width=8)
    sort_kind.bind('<<ComboboxSelected>>' , select_kind)
    sort_kind['values']=('年齢','身長','体重','バスト','ウェスト','ヒップ')
    sort_kind.set("条件")
    sort_kind.place(x=combo_placex,y=combo_placey)

    #順番を選ぶドロップダウンメニュー
    txt2=tk.StringVar()
    updown_cb= ttk.Combobox(root2,textvariable=txt2, state='readonly',font=("",16),width=8)
    updown_cb.bind('<<ComboboxSelected>>' , select_updown)
    updown_cb["values"]=("小さい順","大きい順")
    updown_cb.set("順番")
    updown_cb.place(x=combo_placex+180,y=combo_placey)
        
    def NHK():
        root3.destroy()
        mainroot()
    back_btn=tk.Button(root2,command=NHK,text="検索画面に戻る",font=("",18))
    back_btn.place(x=combo_placex-380,y=combo_placey-30)
    
    #並び変えボタン
    change_btn=tk.Button(root2,command=partial(change_order,list_idols),text="実行",font=("",18))
    change_btn.place(x=combo_placex+400,y=combo_placey-10)
    
    root3.mainloop()
    
#警告メッセージ表示
def warning():
    message=tk.messagebox.showinfo("警告","条件に合うアイドルは存在しません")
    
kaisuu=0
global list_idols
def mainroot():
    idol_raw_data = None
    global autocompleteList
    global kaisuu
    with open("idol.json",encoding='UTF-8') as file:
        idol_raw_data = json.load(file)
        file.close()
    with open("name.json") as file:
        idol_raw_data2 = json.load(file)
        file.close() 
    idols=[]
    #アイドルの情報
    class idol():
        def __init__(self, name, age,height,weight,b,w,h,birth,blood,dh,hobby,skill,like,born,color,image,st):
            self.data=[name, age,height,weight,b,w,h,birth,blood,dh,hobby,skill,like,born,color,image,st]

    for i in idol_raw_data:
        idols.append(idol(i["name"], float(i["age"][:-1]), float(i["height"][:-2]), float(i["weight"][:-2]),
                float(i["b"][:-2]), float(i["w"][:-2]), float(i["h"][:-2]), i["birth"], i["blood"], i["dh"], i["hobby"], i["skill"], i["like"],i["born"],i["color"],"temp.png",i["status"]))
    #サジェスト用リスト
    if(kaisuu==0):
        for i in idol_raw_data2:
            autocompleteList.append(i["name1"]) 
        for i in idol_raw_data2:
            autocompleteList.append(i["name2"])       
        for i in idol_raw_data2:
            autocompleteList.append(i["name3"])  
    kaisuu=1
    for i in range(52):
        idols[i].data[15]=idol_raw_data2[i]["name4"]
    # Tkクラス生成
    root = tk.Tk()
    # 画面サイズ
    root.geometry('800x550')
    # 画面タイトル
    root.title('Millionlive!プロフィール検索')
    global min_get
    min_get=[0,0,0,0,0,0]
    global max_get
    max_get=[0,0,0,0,0,0]
    #ドロップダウンの値を取得
    def select_min0(event):
        min_get[0]=float(cb_min_st[0].get())
    def select_max0(event):
        max_get[0]=float(cb_max_st[0].get())
    
    def select_min1(event):
        min_get[1]=float(cb_min_st[1].get())
    def select_max1(event):
        max_get[1]=float(cb_max_st[1].get())
    
    def select_min2(event):
        min_get[2]=float(cb_min_st[2].get())
    def select_max2(event):
        max_get[2]=float(cb_max_st[2].get())
    
    def select_min3(event):
        min_get[3]=float(cb_min_st[3].get())
    def select_max3(event):
        max_get[3]=float(cb_max_st[3].get())
    
    def select_min4(event):
        min_get[4]=float(cb_min_st[4].get())
    def select_max4(event):
        max_get[4]=float(cb_max_st[4].get())
    
    def select_min5(event):
        min_get[5]=float(cb_min_st[5].get())
    def select_max5(event):
        max_get[5]=float(cb_max_st[5].get())

    def select_status(event):
        global status_get
        status_get=status_var.get()

    #絞り込みボタン
    def profile_btn(chk_bln):
        global flag
        flag="false"
        list_idols=[]
        list_idols=idols
        #リストの初期化できない
        for j in range(len(chk_bln)-1):
            if chk_bln[j].get():
                #min>max ありえない話！
                if(int(min_get[j])>int(max_get[j])):
                    warning()
                    flag="true"
                    break
                for s in range(len(list_idols)-1):
                    for t in range(s,len(list_idols)):
                        if(float(list_idols[s].data[j+1])>float(list_idols[t].data[j+1])):
                            swap=list_idols[s]
                            list_idols[s]=list_idols[t]
                            list_idols[t]=swap
                tintin_select(min_get[j],max_get[j],j+1,list_idols)
                if(flag=="true"):
                    break
        if(flag=="true"):
            warning()
            return
        if chk_bln[6].get():
            length=len(list_idols)
            for i in range(length):
                if(list_idols[length-1-i].data[16]!=status_get):
                    list_idols.pop(length-1-i)
            if(len(list_idols)==0):
                flag="true"
        if(flag=="true"):
            warning()
            return

        idol_show(list_idols,root)        
        
        
        
        
        
    global chk_txt
    #位置を決める変数
    kijun_x=550
    kijun_y=105
    x_marge=60
    y_marge=50
    entry_var=0
    chk_bln={}
    # チェックボックスON/OFFの状態
    # チェックボタンを動的に作成して配置
    for i in range(len(chk_txt)):
        chk_bln[i] = tk.BooleanVar()
        chk = tk.Checkbutton(root, variable=chk_bln[i], text=chk_txt[i],font=("",14)) 
        chk.place(x=kijun_x-100, y=kijun_y + (i * 50))
    
    
    #名前で検索の部分
    name_label=tk.Label(text="アイドル名で検索",font=("",16))
    name_label.place(x=50,y=50)

    name_box=AutocompleteEntry(autocompleteList, root, listboxLength=6, width=20, matchesFunction=matches,font=("",18))
    name_box.place(x=50,y=130)

    #プロフィールで検索の部分
    profile_label=tk.Label(text="プロフィールから検索",font=("",16))
    profile_label.place(x=kijun_x-150,y=50)


    #値入力,sはsizeのs
    box_s=12
    nami_s=18
    #下限or上限入力ボックス改訂版
    cb_min_st=[tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
    cb_max_st=[tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar(),tk.StringVar()]
    min_box=[]
    max_box=[]

    cb_min_st.append(tk.StringVar())
    cb_max_st.append(tk.StringVar())


    #年齢の下限上限入力    
    min_box.append(ttk.Combobox(root, textvariable=cb_min_st[entry_var],state='readonly',font=("",box_s),width=5))
    min_box[0].bind('<<ComboboxSelected>>' , select_min0)
    min_box[0]["values"]=("10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
    min_box[0].set("下限")
    min_box[0].place(x=kijun_x, y=kijun_y+y_marge*entry_var)
    
    label_nami = tk.Label(text="~",font=("",nami_s))
    label_nami.place(x=kijun_x+x_marge+20, y=kijun_y+y_marge*entry_var)

    max_box.append(ttk.Combobox(root, textvariable=cb_max_st[entry_var],state='readonly',font=("",box_s),width=5))
    max_box[0].bind('<<ComboboxSelected>>' , select_max0)
    max_box[0]["values"]=("10","11","12","13","14","15","16","17","18","19","20","21","22","23","24")
    max_box[0].set("上限")
    max_box[0].place(x=kijun_x+x_marge*2, y=kijun_y+y_marge*entry_var)

    entry_var=entry_var+1

    #身長の上限下限入力
    min_box.append(ttk.Combobox(root, textvariable=cb_min_st[entry_var],state='readonly',font=("",box_s),width=5))
    min_box[1].bind('<<ComboboxSelected>>' , select_min1)
    min_box[1]["values"]=("140","141","142","143","144","145","146","147","148","149","150","151","152","153","154","155","156","157","158","159","160","161","162","163","164","165","166","167","168","169")
    min_box[1].set("下限")
    min_box[1].place(x=kijun_x, y=kijun_y+y_marge*entry_var)
    
    label_nami = tk.Label(text="~",font=("",nami_s))
    label_nami.place(x=kijun_x+x_marge+20, y=kijun_y+y_marge*entry_var)

    max_box.append(ttk.Combobox(root, textvariable=cb_max_st[entry_var],state='readonly',font=("",box_s),width=5))
    max_box[1].bind('<<ComboboxSelected>>' , select_max1)
    max_box[1]["values"]=("140","141","142","143","144","145","146","147","148","149","150","151","152","153","154","155","156","157","158","159","160","161","162","163","164","165","166","167","168","169")
    max_box[1].set("上限")
    max_box[1].place(x=kijun_x+x_marge*2, y=kijun_y+y_marge*entry_var)

    entry_var=entry_var+1

    #体重の上限下限入力
    min_box.append(ttk.Combobox(root, textvariable=cb_min_st[entry_var],state='readonly',font=("",box_s),width=5))
    min_box[2].bind('<<ComboboxSelected>>' , select_min2)
    min_box[2]["values"]=("35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51")
    min_box[2].set("下限")
    min_box[2].place(x=kijun_x, y=kijun_y+y_marge*entry_var)
    
    label_nami = tk.Label(text="~",font=("",nami_s))
    label_nami.place(x=kijun_x+x_marge+20, y=kijun_y+y_marge*entry_var)

    max_box.append(ttk.Combobox(root, textvariable=cb_max_st[entry_var],state='readonly',font=("",box_s),width=5))
    max_box[2].bind('<<ComboboxSelected>>' , select_max2)
    max_box[2]["values"]=("35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51")
    max_box[2].set("上限")
    max_box[2].place(x=kijun_x+x_marge*2, y=kijun_y+y_marge*entry_var)

    entry_var=entry_var+1

    #Bの上限下限入力
    min_box.append(ttk.Combobox(root, textvariable=cb_min_st[entry_var],state='readonly',font=("",box_s),width=5))
    min_box[3].bind('<<ComboboxSelected>>' , select_min3)
    min_box[3]["values"]=("72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93")
    min_box[3].set("下限")
    min_box[3].place(x=kijun_x, y=kijun_y+y_marge*entry_var)
    
    label_nami = tk.Label(text="~",font=("",nami_s))
    label_nami.place(x=kijun_x+x_marge+20, y=kijun_y+y_marge*entry_var)

    max_box.append(ttk.Combobox(root, textvariable=cb_max_st[entry_var],state='readonly',font=("",box_s),width=5))
    max_box[3].bind('<<ComboboxSelected>>' , select_max3)
    max_box[3]["values"]=("72","73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92","93")
    max_box[3].set("上限")
    max_box[3].place(x=kijun_x+x_marge*2, y=kijun_y+y_marge*entry_var)

    entry_var=entry_var+1

    #Wの上限下限入力
    min_box.append(ttk.Combobox(root, textvariable=cb_min_st[entry_var],state='readonly',font=("",box_s),width=5))
    min_box[4].bind('<<ComboboxSelected>>' , select_min4)
    min_box[4]["values"]=("51","52","53","54","55","56","57","58","59","60","61","62","63")
    min_box[4].set("下限")
    min_box[4].place(x=kijun_x, y=kijun_y+y_marge*entry_var)
    
    label_nami = tk.Label(text="~",font=("",nami_s))
    label_nami.place(x=kijun_x+x_marge+20, y=kijun_y+y_marge*entry_var)

    max_box.append(ttk.Combobox(root, textvariable=cb_max_st[entry_var],state='readonly',font=("",box_s),width=5))
    max_box[4].bind('<<ComboboxSelected>>' , select_max4)
    max_box[4]["values"]=("51","52","53","54","55","56","57","58","59","60","61","62","63")
    max_box[4].set("上限")
    max_box[4].place(x=kijun_x+x_marge*2, y=kijun_y+y_marge*entry_var)

    entry_var=entry_var+1

    #Hの上限下限入力
    min_box.append(ttk.Combobox(root, textvariable=cb_min_st[entry_var],state='readonly',font=("",box_s),width=5))
    min_box[5].bind('<<ComboboxSelected>>' , select_min5)
    min_box[5]["values"]=("73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92")
    min_box[5].set("下限")
    min_box[5].place(x=kijun_x, y=kijun_y+y_marge*entry_var)
    
    label_nami = tk.Label(text="~",font=("",nami_s))
    label_nami.place(x=kijun_x+x_marge+20, y=kijun_y+y_marge*entry_var)

    max_box.append(ttk.Combobox(root, textvariable=cb_max_st[entry_var],state='readonly',font=("",box_s),width=5))
    max_box[5].bind('<<ComboboxSelected>>' , select_max5)
    max_box[5]["values"]=("73","74","75","76","77","78","79","80","81","82","83","84","85","86","87","88","89","90","91","92")
    max_box[5].set("上限")
    max_box[5].place(x=kijun_x+x_marge*2, y=kijun_y+y_marge*entry_var)

    entry_var=entry_var+1

    status_var=tk.StringVar()

    status=ttk.Combobox(root, textvariable=status_var,state='readonly',font=("",box_s+4),width=8)
    status.bind('<<ComboboxSelected>>' , select_status)
    status["values"]=("小学生","中学生","高校生","その他")
    status.set("区分")
    status.place(x=kijun_x+x_marge, y=kijun_y+y_marge*entry_var)
    #最初の画面のボタンの定義
    button1 = tk.Button(root,text="検索",command=lambda:idol_btn(name_box,idols),font=("",15))
    button1.place(x=250, y=200)

    button2 = tk.Button(root,text="検索",command=partial(profile_btn,chk_bln),font=("",15))
    button2.place(x=kijun_x+150, y=kijun_y+350)
    
    root.mainloop()

mainroot()
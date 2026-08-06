import numpy as np
import pandas as pd
global number_er, error_25
total_lines = 0
number_er =0
error_25 =pd.DataFrame()
error_Student_Id= pd.DataFrame()
def nhaptenfile():
    while True:
        try:
            filename = input('nhập tên file:')
            df = pd.read_csv(filename + '.txt',engine='python', on_bad_lines = bad_line , sep=",", header = None, index_col = None)
            return df,filename
            break
        except FileNotFoundError:
            print('bạn đã nhập sai tên, hãy nhập lại!')
        finally:
            print('đã duyệt xong file',filename)
          
def bad_line(line): 
    global error_25
    line_df = pd.DataFrame([line]) 
    error_25 = pd.concat([error_25, line_df], ignore_index=True)
    return None
    
def Kiem_tra_dong_hop_le(df): 
    global error_25,number_er,error_Student_Id
    # lỗi số lượng câu trả lời
    df_er = df[df.applymap(lambda x: x is None).any(axis=1)]
    df= df[~df.applymap(lambda x: x is None).any(axis=1)]
    error_25 = pd.concat([error_25,df_er],ignore_index= True)
    # lỗi mã sinh viên
    pattern = r'^N\d{8}$'
    error_Student_Id = df[~df[0].str.match(pattern)]
    df=df[df[0].str.match(pattern)]
    # tổng số dòng lỗi
    number_er = len(error_25[0])+ len(error_Student_Id[0])
    return (df)

def cham_bai(df,answer_key):
    score=pd.DataFrame()
    df_new=df.copy()
    df_new=df_new.drop(columns=[0])
    score['SBD']=df[0].copy()
    for i in range(len(answer_key)):
        df_new[i+1]= df_new[i+1].apply(lambda x: 4 if x == answer_key[i] else (0 if pd.isna(x) else -1))
    #print(df_new)
    score['Score']=df_new.sum(axis=1)
    return(score,df_new)

def trung_vi(point):
    pointn=point.sort_values(ignore_index= True)
    #print(pointn)
    if len(pointn)%2 ==0:
        a=(pointn.iloc[len(pointn)//2]+pointn.iloc[len(pointn)//2-1])/2
    else:
        a =pointn.iloc[(len(pointn)//2)]
    return(a)

def phan_tich(df_point):
    DA_Skip=pd.DataFrame() 
    DA_Skip['số lượng học sinh bỏ qua']=df_point.apply(lambda x: (x==0).sum())
    DA_Skip['tỉ lệ bị bỏ qua']=df_point.apply(lambda x: (x==0).sum()/len(df_point[1]))
    #print(DA_Skip)
    a=pd.DataFrame()
    a=DA_Skip[DA_Skip['tỉ lệ bị bỏ qua']==DA_Skip['tỉ lệ bị bỏ qua'].max()]
    
    DA_wrong=pd.DataFrame() 
    DA_wrong['số lượng học sinh làm sai']=df_point.apply(lambda x: (x==-1).sum())
    DA_wrong['tỉ lệ làm sai']=df_point.apply(lambda x: (x==-1).sum()/len(df_point[1]))
    #print(DA_wrong)
    b=pd.DataFrame()
    b= DA_wrong[DA_wrong['tỉ lệ làm sai']==DA_wrong['tỉ lệ làm sai'].max()]
    #print(b)
    return(a,b)
p=1  
while p==1:
    print('Task 1: Đọc file dư liệu')
    df,filename=nhaptenfile()
    ###############
    print('Task 2 : Dòng không hợp lệ:')
    df=Kiem_tra_dong_hop_le(df)
    total_lines= len(df[0])+number_er
    print(f"dòng lỗi không chứa chính xác 26 giá trị : \n {error_25}")
    print(f"dòng lỗi mã học sinh không hợp lệ! : \n {error_Student_Id}")
    print('2.1 tổng số dòng dữ liệu được lưu trữ trong tệp',total_lines)
    print('2.1 tổng số dòng dữ liệu không hợp lệ',number_er )
    print('2.1 tổng số dòng dữ liệu hợp lệ',len(df[0]))
    ################
    print('Task 3: Chấm bài')
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D".split(',')
    score,df_point=cham_bai(df,answer_key)
    point=score['Score'].copy()
    print('3.1 số lượng học sinh đạt điểm cao (>80): ',sum(point>=80) )
    print('3.2. Điểm trung bình:',sum(point)/len(point))
    print('3.3. Điểm cao nhất:',max(point))
    print('3.4. Điểm thấp nhất:',min(point))
    print('3.5. Miền giá trị của điểm :',max(point)-min(point))
    print('3.6. Giá trị trung vị:',trung_vi(point))
    print('3.7. Trả về các câu hỏi bị học sinh bỏ qua nhiều nhất theo thứ tự: \nsố thứ tự câu hỏi , số lượng học sinh bỏ qua , tỉ lệ bị bỏ qua:')
    a,b= phan_tich(df_point)
    print (a)# (nếu có cùng số lượng cho nhiều câu hỏi bị bỏ thì phải liệt kê ra đầy đủ).
    print('3.8. Trả về các câu hỏi bị học sinh sai qua nhiều nhất theo thứ tự:\n số thứ tự câu hỏi , số lượng học sinh trả lời sai , tỉ lệ bị sai:')
    print(b) #(nếu có cùng số lượng cho nhiều câu hỏi bị sai thì phải liệt kê ra đầy đủ).
    print('task 4 danh sách điểm')
    #print(score)
    with open(filename+'_gradesNC.txt','w') as file:
        pass
    score.to_csv(filename+'_gradesNC.txt', sep='\t', index=False)
    with open(filename+'_gradesNC.txt','r') as file:
        ReadFile=file.read()
        print(ReadFile)
    print('########################################### ĐÃ CHẤM XONG BÀI  ######################################################################')
    p=int(input('nhập 1: nếu muốn tiếp tục chấm lớp tiếp theo\n nhập 0: nếu muốn dừng chương trình\n Ban có muốn tiếp tục chấm điểm không?\n '))
    if p==1:
        print('tiếp tục chấm bài')
    else:
        print('dừng chương trình')
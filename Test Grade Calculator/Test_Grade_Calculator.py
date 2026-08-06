# import thư viện
import re

# hàm phân loại 1 bài làm là hợp lệ hay không hợp lệ nếu hàm hợp lệ trả về 1 nếu không hợp lệ trả về 0
def PhanLoaiDongDATA(FileContent):
    if re.match(r'^N\d{8}',FileContent)==None:
        print('dòng dữ liệu không hợp lệ: Lỗi mã học sinh không hợp lệ! ')
        print(FileContent)
        return 0
    elif len(re.split(r'[,]',FileContent))!=26:
        print('dòng dữ liệu không hợp lệ: không chứa chính xác 26 giá trị ')
        print(FileContent)
        return 0
    else:
        return 1   
 
#hàm chấm bài cho 1 học sinh và trả về lần lượt(điểm của học sinh, list các câu không làm , list các câu làm sai )
def ChamBai(FileContent):
    point=0
    SkipAns=[]
    WrongAns=[]
    answer_key = "B,A,D,D,C,B,D,A,C,C,D,B,A,B,A,C,B,D,A,C,A,A,B,D,D"
    BaiThi=re.split(r'[,\n]',FileContent)
    Answer=re.split(r'[,]',answer_key)    
    for index in range(1,26 ):        
        if BaiThi[index] == '':
            point=point+0
            SkipAns.append(index)
        elif BaiThi[index] == Answer[index-1]:
            point=point+4
        else:    
            point=point-1
            WrongAns.append(index)
    return(point,SkipAns,WrongAns)

# hàm tìm trung vị của một chuỗi giá tri
def TrungVi (chuoi):
    a=len(chuoi)
    b=chuoi[:]
    b.sort()
    if a%2 ==0:
        return((b[int(a/2)]+b[int(a/2)-1])/2)
    else:
        return(b[int(a/2)])

#hàm lấy vào chuỗi a chứa danh sách các câu hỏi và số học sinh trong lớp, phân tích có bao nhiêu giá trị trùng lặp trong chuỗi và trả về list bao gồm thứ tự các câu, tần suất xuất hiện nhiều nhất và tỉ lệ so với số học sinh trong lớp
def PhanTichKetQua(a,length):
    a.sort()
    #print('các câu \n', a)
    Bai=[]
    ThongKe=[]
    dem=1
    while len(a)!=1:
        if a[0]==a[1]:
            dem=dem+1
            a.remove(a[0])
        else:
            ThongKe.append(dem)
            Bai.append(a[0])
            dem=1
            a.remove(a[0])
    #print('danh sách câu :',Bai)    
    #print('danh sách SốL :',ThongKe)
    Kq =[]
    for i in range(len(Bai)):
        if ThongKe[i]==max(ThongKe):
            Kq.append([Bai[i],max(ThongKe),max(ThongKe)/length ])
    return(Kq)  

#khớp điểm với mã số học viên và xuất file lớp_grades.txt
def XuatFileKetQua(filename,Content,Score):
    for i in range(len(Content)):
        data =re.findall(r'^N\d{8}',Content[i])
        _data=data[0]+','+str(Score[i])+'\n'
        with open ('D:/DA/p4/TestGradeCalculator/Data Result/' + filename+'_grades.txt','a+') as grade:
            grade.write(_data)

#task1
def NhapTenFile():
    Content=[] # lưu danh sách các dữ liệu hợp lệ
    Score =[]  # lưu điểm của các bạn trong lớp
    SkipAns=[] # lưu các câu hỏi học sinh đã bỏ qua
    WrongAns=[] # lưu các câu hỏi học sinh đã làm sai
    while True:
        try:
            filename = input('Nhập lớp để chấm điểm(vd class1):')
            #print(filename)
            with open('D:/DA/p4/TestGradeCalculator/Data Files/' + filename + '.txt', "r") as file1:
                  FileContent = file1.readline()
                  Total_Invalid=0
                  Total_Valid=0 
                  while ',' in  FileContent:         
                        if PhanLoaiDongDATA(FileContent)==1:
                            Total_Valid=Total_Valid+1                            
                            #print(ChamBai(FileContent))##################################
                            Content.append(FileContent)
                            [point,SkiAns,WroAns]=ChamBai(FileContent)
                            Score.append(point)  # thêm ddiemr vào danh sách điểm
                            SkipAns.extend(SkiAns)   #thêm các câu đã bị bỏ qua vào danh sách SkipAns
                            WrongAns.extend(WroAns)  #them các câu sai vào danh sách các câu làm sai
                        else:
                            Total_Invalid=Total_Invalid+1                                                  
                        FileContent = file1.readline()              
                  return([filename,Content,Score,Total_Invalid,Total_Valid,SkipAns,WrongAns])
                  break  # Thoát khỏi vòng lặp khi tệp được mở thành công
        except FileNotFoundError:
            print('Bạn đã nhập sai tên lớp! Nhập lại.')
        finally:
            print('Đã kiểm tra  file:', filename)
p=1  
while p==1:
        [filename,Content,Score,Total_Invalid,Total_Valid,SkipAns,WrongAns]=NhapTenFile()
        #task2
        print('2.1 tổng số dòng được dữ liệu được lưu trữ trong tệp: ',Total_Valid+Total_Invalid)
        print('2.2 Tổng số dòng dữ liệu hợp lệ: ',Total_Valid)
        print('2.3 Tổng số dòng dữ liệu không hợp lệ: ',Total_Invalid)
        print('3.1 số lượng học sinh đạt điểm cao (>80): ',len([sc for sc in Score if sc>80]) )
        print('3.2. Điểm trung bình:',sum(Score)/Total_Valid)
        print('3.3. Điểm cao nhất:',max(Score))
        print('3.4. Điểm thấp nhất:',min(Score))
        print('3.5. Miền giá trị của điểm :',max(Score)-min(Score))
        print('3.6. Giá trị trung vị:',TrungVi(Score))
        print('3.7. Trả về các câu hỏi bị học sinh bỏ qua nhiều nhất theo thứ tự: số thứ tự câu hỏi, số lượng học sinh bỏ qua, tỉ lệ bị bỏ qua:')
        print (PhanTichKetQua(SkipAns,Total_Valid))# (nếu có cùng số lượng cho nhiều câu hỏi bị bỏ thì phải liệt kê ra đầy đủ).
        print('3.8. Trả về các câu hỏi bị học sinh sai qua nhiều nhất theo thứ tự: số thứ tự câu hỏi, số lượng học sinh trả lời sai, tỉ lệ bị sai:')
        print( PhanTichKetQua(WrongAns,Total_Valid)) #(nếu có cùng số lượng cho nhiều câu hỏi bị sai thì phải liệt kê ra đầy đủ).
        print('task 4 danh sách điểm')
        with open('D:/DA/p4/TestGradeCalculator/Data Result/' + filename+'_grades.txt','w') as file:
            pass
        XuatFileKetQua(filename,Content,Score)
        with open('D:/DA/p4/TestGradeCalculator/Data Result/' + filename+'_grades.txt','r') as file:
           ReadFile=file.read()
           print(ReadFile)
        print('########################################### ĐÃ CHẤM XONG BÀI  ######################################################################')
        p=int(input('nhập 1: nếu muốn tiếp tục chấm lớp tiếp theo\n nhập 0: nếu muốn dừng chương trình\n Ban có muốn tiếp tục chấm điểm không?\n '))
        if p==1:
            print('tiếp tục chấm bài')
        else:
            print('dừng chương trình')
       

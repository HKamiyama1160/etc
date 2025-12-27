#wave_path = "./digital_wave_test.csv"
print("Wave file name and file path ? :  ", end='')
wave_path = input()
#wave_path = "../hkc.csv"
print(wave_path)

print("csv file line skip count ? :  ", end='')
skip = input()
skip_row_count = int(skip)
wave_file = open(wave_path,'r')

##

HIGH = 1
LOW = 0
X = 2

#
MAX_REC = 5
CLK_LOGIC_TH = 3.0*0.3
DATA_LOGIC_TH = 3.0*0.3 
DET_SMP_INT = 1

#
while skip_row_count !=0:
    row_data = wave_file.readline()
    skip_row_count-=1

#
clk_rise_point=[]
clk_fall_point=[]
detect_data=[]
bit_count = 0
clk_buf =[ 0 for i in range(10)]
data_buf =[ X for i in range(10)]

#
##
row_data = wave_file.readline()
split_data = row_data.split(",")

clk_logic_det_f =[True,False]
data_det_f = False
dt_cnt=0
while row_data:
    index_dt = float(split_data[0])
    ch1_dt = float(split_data[1])
    ch2_dt = float(split_data[2])
#    ch1_dt = float(split_data[2])
#   ch2_dt = float(split_data[3])
    ###########   ##########
    
    #
    ##
    if dt_cnt % DET_SMP_INT == 0:
        #
        for i in range(len(clk_buf)-1):
            clk_buf[len(clk_buf)-1-i] = clk_buf[len(clk_buf)-1-i-1]
        clk_buf[0]=ch1_dt
        #
        for i in range(len(clk_buf)):
            #
            if clk_buf[i] > CLK_LOGIC_TH and clk_logic_det_f[0]==True:
                if i >4 :
                    clk_rise_point.append([index_dt,ch1_dt])
                    clk_logic_det_f =[False,True]
                    #
                    data_det_f = True 
                    break
            #
            elif clk_buf[i] < CLK_LOGIC_TH and clk_logic_det_f[1]==True:
                if i >4 :
                    clk_fall_point.append([index_dt,ch1_dt])
                    clk_logic_det_f =[True,False]
                    break
            else:
                break
            
    #
    if dt_cnt % DET_SMP_INT == 0 and data_det_f==True:
        #
        for i in range(len(data_buf)-1):
            data_buf[len(data_buf)-1-i] = data_buf[len(data_buf)-1-i-1]
        #
        if ch2_dt > DATA_LOGIC_TH:
            data_buf[0]=HIGH
        else:
            data_buf[0]=LOW
        #
        if all([data_buf[i] == HIGH for i in range(len(data_buf))]):
            detect_data.append(HIGH)
            bit_count = bit_count + 1
            data_det_f=False
            data_buf =[ X for i in range(10)]
        elif all(data_buf[i] == LOW for i in range(len(data_buf))):
            detect_data.append(LOW)
            bit_count = bit_count + 1
            data_det_f=False
            data_buf =[ X for i in range(10)]
            
    #######################################
    
    ##
    dt_cnt+=1
    row_data = wave_file.readline()
    split_data = row_data.split(",")
wave_file.close()

#
clk_rise_int=[]
##
for i in range(len(clk_rise_point)-1):
    clk_rise_int.append(clk_rise_point[i+1][0]-clk_rise_point[i][0])
#print("CLK Jitter:"+str(max(clk_rise_int)-min(clk_rise_int)))
    
##
print(str(detect_data))
print(bit_count)

hex_data = []
word_count  = 0
ind = 15
hex_val = 0

for i in range(bit_count):
     if(detect_data[i]  == 1):
        hex_val = hex_val + 2**ind
     ind = ind - 1
     if(ind < 0):
            hex_data.append(format(hex_val, '04x'))
            word_count = word_count + 1
            hex_val = 0
            ind = 15

print(hex_data)
print(word_count)

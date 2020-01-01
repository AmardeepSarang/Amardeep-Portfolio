
def load_data(file_name):
    #open file into 2x2 array
    dataset=[]
    f=open(file_name,"r")
    word_list=[]
    for line in f:
        word_list=line.split(",")
        dataset.append(word_list)
    f.close()
    for i in range(len(dataset)):
        for j in range(len(dataset[i])):
            dataset[i][j] = float(dataset[i][j])
    return dataset

def split_test(data,test_num):
    '''
    splits data depending on fold  number
    '''
    test_set=data[test_num]
    traning_set=data[:test_num]+data[test_num+1:]
    return test_set, traning_set

def gen_names():
    #generate file names
    f_names=[]
    for i in range(1,11):
        s='dataset_'+str(i)+'.txt'
        f_names.append(s)
    return f_names
        
def main():
    
    f_names=gen_names()
    for f_name in f_names:
        #load data
        ab_table=load_data(f_name)
        
        tests_done=0
        tests_correct=0
        
        for fold in range(40):
        #spilt data
            test,train=split_test(ab_table, fold)
            

            result= #<------ ADD classifier function here 
            tests_done+=1
            
            #check if correct prediction was made
            
            if result==test[len(test)-1]:
                tests_correct+=1
                
        accuracy=tests_correct/tests_done
        print(f_name+", "+accuracy)

    
main()

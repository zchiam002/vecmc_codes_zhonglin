##This function backsup the previously saved files before resuming the training 
def pg_backup_before_resume (save_file_name, resume_training_count, save_folder_directory):
       
    ##save_file_name        --- the file name for the trained model 
    ##resume_training_count --- the resume_trainint iteration
    ##save_folder_directory --- the directory for the saved models  
    
    import os 
    import shutil
    from shutil import copyfile
    
    ##Return signal 
    proceed = 0
    
    ##Create new folder name 
    new_folder_name = 'resume_' + str(resume_training_count) + '_starting_point\\'
    
    ##First check if the sub folder directory exists, if it does, delete it 
    sub_folder_path = save_folder_directory + new_folder_name 
    if os.path.exists(sub_folder_path):
        shutil.rmtree(sub_folder_path)    

    ##Now, create the sub folder directory for storing the lp format script for the specific thread
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)    
    
    ##The names and fully directory of the files to be copied 
    file_0 = save_file_name + '.data-00000-of-00001'
    file_1 = save_file_name + '.index'
    file_2 = save_file_name + '.meta'
    file_3 = 'checkpoint'
    
    file_0_curr_dir =  save_folder_directory + file_0
    file_1_curr_dir =  save_folder_directory + file_1
    file_2_curr_dir =  save_folder_directory + file_2
    file_3_curr_dir =  save_folder_directory + file_3

    file_0_new_dir =   sub_folder_path + file_0  
    file_1_new_dir =   sub_folder_path + file_1  
    file_2_new_dir =   sub_folder_path + file_2  
    file_3_new_dir =   sub_folder_path + file_3
    
    copyfile(file_0_curr_dir, file_0_new_dir)
    copyfile(file_1_curr_dir, file_1_new_dir)
    copyfile(file_2_curr_dir, file_2_new_dir)
    copyfile(file_3_curr_dir, file_3_new_dir)
    
    print('###################################')
    print('Starting point files are backed up!')
    print('###################################')   
          
    ##Return signal 
    proceed = 1
    
    return proceed
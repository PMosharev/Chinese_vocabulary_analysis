import os



def get_filenames_from_folder(folder_path):

    directory = os.fsencode(folder_path)
        
    for i, file in enumerate(os.listdir(directory)):
        print(i, file)


if __name__ == "__main__":
    get_filenames_from_folder('D:\Chinese_vocabulary_analysis\data\md')
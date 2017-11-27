import os
import re
import shutil
import errno, stat


def handleRemoveReadonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise

        # shutil.rmtree(new_vid_dir, ignore_errors=False, onerror=handleRemoveReadonly)



        # pathlib.Path(new_vid_dir).mkdir(parents=True, exist_ok=True)
        # os.makedirs("ABC")

        # # root_path = '/whatever/your/root/path/is/'
        # folders = ['T01', 'T02', 'T08']
        # for folder in folders:
        #     subfolder_path = os.path.join(new_vid_dir, folder)
        #     os.mkdir(subfolder_path)
        #     for session in list_session:
        #         os.mkdir(os.path.join(subfolder_path, session))
        #         # with open(os.path.join(subfolder_path, 'Order.csv'), "a+", newline='') as subfolder:
        #         #     writer = csv.writer(subfolder, delimiter=',')
        #         #     writer.writerow([session])
        #         #     subfolder.close()





        # print("\npath+filename:")
        # print(path)
        # print(fname)
        #
        # print("\nsession:")
        # print(session_name)





        # print("\nsplitname:")
        # print(splitname)
        # print("\nname_session:")
        # print(name_session)

        # print("\nfname:")
        # print(fname)



        # print("\nsplitname:")
        # print(splitname)
        # print(name_subject)



        # print("\npath1&2:")
        # print(path1)
        # print(path2)

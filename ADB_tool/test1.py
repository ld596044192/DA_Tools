import public

yuv_path_dir = []
yuv_dirs = public.get_dirs(r'C:\Users\lida\Desktop\ADB_get_yuv\get_yuv1')
print(yuv_dirs)
for yuv_dir_path in yuv_dirs:
    yuv_files = public.get_files(yuv_dir_path)
    print(yuv_files)
    yuv_path_dir.append(yuv_files)
    if '1.yuv' in yuv_path_dir:
        yuv_dir_path_select = yuv_dir_path
        print(yuv_dir_path)
        break

import public

yuv_dirs = public.get_dirs(r'C:\Users\lida\Desktop\ADB_get_yuv\get_yuv8')
print(yuv_dirs)
for yuv_dir_path in yuv_dirs:
    try:
        yuv_files = public.get_files(yuv_dir_path)
        if 'origin_320X240.yuv' in yuv_files:
            yuv_dir_path_select = yuv_dir_path
            print(yuv_dir_path)
            break
    except TypeError:
        pass


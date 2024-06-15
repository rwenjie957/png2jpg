from PIL import Image
from pathlib import Path
import os
import tqdm
from multiprocessing import Process
from math import ceil
import sys


# 将png转换为jpg
def png2jpg(path_list, name):
    for source, destination in tqdm.tqdm(path_list, desc=f"进程：{name+1}", position=name):
        try:
            img = Image.open(source)
            img.convert('RGB').save(destination)
        except Exception as e:
            print(e)


def generator(lis, process_counts):
    part = ceil(len(lis)/process_counts)
    for i in range(process_counts):
        yield lis[i*part:(i+1)*part]


if __name__ == '__main__':
    arg = sys.argv
    if len(arg) >= 2:
        paths = []
        for i in arg[1:]:
            paths.append(Path(i))
    else:
        paths = [Path(input('请输入压缩文件的绝对路径'))]
    origins = []
    # path = Path(r'C:\Users\Admin\Desktop\新建文件夹')
    for path in paths:
        parent = path.parent
        if path.is_dir():
            stem = Path(path.stem)
            print(f'创建根目录{stem}')
            Path.mkdir(stem)

            for root, dirs, files in os.walk(path):
                print(root, dirs, files[0:5])
                # 创建文件目录

                for di in dirs:
                    print(Path(root).relative_to(parent) / di)
                    Path.mkdir(Path(root).relative_to(parent) / di)

                # 记录所有待转化文件
                for file in files:
                    if file.endswith('.png'):
                        src = Path(root) / file
                        dst = (Path(root).relative_to(parent) / file).with_suffix('.jpg')
                        origins.append((src, dst))

        else:
            Path.mkdir(Path('JPG'), exist_ok=True)
            if path.suffix == '.png':
                dst = Path('JPG') / Path(path.name).with_suffix('.jpg')
                origins.append((path, dst))

    print(origins)
    cores = 6                                                       # 使用的线程数，由CPU核心和线程数决定
    ce = generator(origins, cores)
    processes = []
    for core in range(cores):
        p = Process(target=png2jpg, args=(next(ce), core))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    print("转换结束")

"""Script description

    Randomly sample and group the images
    by posture

    Paramters:
    fileDir: source dir of the dataset
    tarDir: target dir of the dataset
    
    source dir should looks like this: dataset/[pose name]/[image name]
    target dir should looks like this: dataset/[pose name]/[group number]/[image name]

    image name: [1_1.jpg/png/webp]
    the first number represent the group id and the second number represent the image id inside group.
        
"""


import os, random, shutil

# 指定列表和每组数量，随机分组
# a: list to group; n: item # per group
def randomGroup(a, n = 3):
  p = True
  groups = []
  while p:
    if len(a) < n: # 避免报错
      groups.append(a) # groups中有可能有不足n的数据
      p = False
      break
    b = random.sample(a, n)
    groups.append(b)
    a=list(set(a).difference(set(b)))  #去除已抽样的数据
    if len(a) > 0:
      p = True
    else:
      p = False
  return groups
    
# 读取目录下所有图片，随机选择需要的300张图片
def sampleAllImage(filedir, targetdir, name_map_file, picknumber):
        pathdir = os.listdir(filedir)    #取图片的原始路径
        filenumber=len(pathdir)
        print(filedir, ' [number of image]:', filenumber)
        
        first_pick = min(picknumber, filenumber)
        if filenumber < picknumber:
          print('[Warning]: Only ', filenumber, ' images included')
        
        # Step1: 从已有的数据中抽出100组图片
        sample_list = random.sample(pathdir, first_pick)  #随机选取picknumber数量的样本图片
        groups = randomGroup(sample_list, 3)
        
        # 补齐group最后一个元素有可能不到3的情况
        last_gap = 3 - len(groups[-1])
        if last_gap > 0:
          groups[-1] = groups[-1] + random.sample(pathdir, last_gap)
        
        # 啊以下是一段令人绝望的代码，用来尽量生成不重复的数据对，处理数据不够300的情况
        # 三指针遍历已经分好组的groups,从不同的三个group中取一组合
        target_len = picknumber / 3
        gap_len = target_len - len(groups)
        if gap_len > 0:
          temp_list = []
          for imindex in range(3):
            for i in range(len(groups) - 2):
              for j in range(i+1, len(groups) - 1):
                for k in range(j+1, len(groups)):
                  temp_list.append([groups[i][imindex], groups[j][imindex], groups[k][imindex]])
          groups = groups + random.sample(temp_list, int(gap_len)) # TODO:这里还要判断一下gap_len 太大的问题，不过我们目前300张不会有这个bug
          print('二次分组：group len = ', len(groups))

        # 粗暴兜底
        # 检查group是否有空缺，有就从最原始的集合中抽一个填上，确保group list 完整
        for i in range(int(picknumber/3)):
          if i < len(groups) and len(groups[i]) == 3: # 有group且group成员齐全
            continue
          elif i < len(groups): # 有group但group成员不齐全
            groups[i] = groups[i] + random.sample(pathdir, 3-len(groups[i]))
          else: # 没有这个group
            groups.append(random.sample(pathdir, 3))
        print('最终分组：group len = ', len(groups))


        # Step2: 创建新的目录结构
        for index, group in enumerate(groups):
          groupid = index + 1
          # 创建group目录
          group_name = 'group' + str(groupid)
          os.makedirs(os.path.join(targetdir, group_name), exist_ok=True)
          # 移动三张图片到新目录下
          for imindex, img in enumerate(group):
            image_new_name = 'g' + str(groupid) + '_' + 'i' + str(imindex+1) + os.path.splitext(img)[-1]
            # print('img new name', image_new_name)
            shutil.copyfile(os.path.join(filedir, img), os.path.join(targetdir, group_name, image_new_name))
            # 给三张图片重命名，保存命名映射到一个文件
            name_map_file.writelines(image_new_name + '   ' + os.path.join(filedir, img) + '\n')
        return
# [('bitilasana', 10),
#  ('chaturanga dandasana', 8),
#  ('vasisthasana', 8),
#  ('salamba sarvangasana', 7),
#  ('ardha uttanasana', 6),
#  ('natarajasana', 6),
#  ('salabhasana', 6),
#  ('virabhadrasana iii', 5),
#  ('utthita trikonasana', 5),
#  ('matsyasana', 5)]

# 这个list 为空表示文件下所有class都处理，不为空则只处理白名单
white_list = ['bitilasana', 'chaturanga dandasana', 'vasisthasana', 'salamba sarvangasana', 'ardha uttanasana',
'natarajasana', 'salabhasana', 'virabhadrasana iii', 'utthita trikonasana', 'matsyasana']

if __name__ == '__main__':
  fileDir = "../yoga_images_origin/"    #源图片文件夹路径
  tarDir = '../test2/'    #移动到新的文件夹路径
  renameFile = 'image_rename_map.txt'
  all_classes = os.listdir(fileDir)
  for posture in all_classes:
    print('Handleing posture ', posture)
    
    # 忽略unix下系统文件
    if posture == '.DS_Store':
      continue

    # 不在白名单里的动作就不要了
    if len(white_list) > 0:
      if posture not in set(white_list):
        continue
    
    # 打开文件保存原始命名与新命名映射
    name_map_file = open(renameFile,"w")

    target_dir = os.path.join(tarDir, posture)
    os.makedirs(target_dir, exist_ok=True)
    # 对单个姿势做整理
    sampleAllImage(os.path.join(fileDir, posture), target_dir, name_map_file, 300)
# Write image group data into Excel
# xlsxwriter document: https://xlsxwriter.readthedocs.io/

import xlsxwriter
import os

FILE_DIR = "../../yoga_data/label_data/dataset"    #数据目录
SAVE_FILE = 'label.xlsx'    #保存的文件

def write_excel():
  workbook = xlsxwriter.Workbook(SAVE_FILE)
  # 设置不同样式
  bold = workbook.add_format({'bold': True})
  regular = workbook.add_format({'bold': False})
  error = workbook.add_format({'bold': True, 'bg_color': 'red'})
  
  all_classes = os.listdir(FILE_DIR)
  if '.DS_Store' in all_classes: # 忽略系统文件
      all_classes.remove('.DS_Store')

  for index, posture in enumerate(all_classes):
    if posture == '.DS_Store': # 忽略unix下系统文件
      continue
    print('Handleing posture ', posture)
    # 每个pose一个表单
    worksheet = workbook.add_worksheet(posture)
    
    # 写第一行标题
    row0 = ["Group ID","Image 1","Score","Image 2","Score","Image 3","Score","Check (Do not modify this column)」"]
    for i in range(0,len(row0)):
      worksheet.write(0,i,row0[i], bold)
    
    # 写每个group的信息
    group_dir = os.path.join(FILE_DIR, posture)
    group_list = os.listdir(group_dir)
    if '.DS_Store' in group_list:
      group_list.remove('.DS_Store')
    group_list.sort(key=lambda x:int(x[5:])) # group分组按名字排个序

    for index, group in enumerate(group_list):
      # print('group name=', group)
      # 写入 1 3 5 7 9 ... 行
      row_number = 1 + index
      worksheet.write(row_number, 0, group, regular)
      
      img_dir = os.path.join(group_dir, group)
      img_list = os.listdir(img_dir)
      img_list.sort(key=lambda name : name.split('_')[1].split('.')[0]) # 拍个序保证0 1 2 顺序显示
      if '.DS_Store' in img_list:
        img_list.remove('.DS_Store')
      
      crow = row_number # 评分的那一行
      for imindex, img in enumerate(img_list):
        col = 2 * imindex + 1
        worksheet.write(row_number, col, img, regular)
        # 下一行放下拉列表
        worksheet.data_validation(crow, col + 1, crow, imindex + 1, 
                                  {'validate': 'list', 'source': ['High', 'Medium', 'Low']})
      
      # 做错误提示
      cr = crow + 1 # excel 从1开始
      formular = f'=IF(OR(COUNTIF(C{cr}:G{cr},C{cr})+COUNTIF(C{cr}:G{cr},E{cr})+COUNTIF(C{cr}:G{cr},G{cr})=3,C{cr}="",E{cr}="",G{cr}=""),"","Error! These three annotations should be different!")'
      error_col = 7
      worksheet.write_formula(crow, error_col, formular)
      worksheet.conditional_format(f'C{cr}:G{cr}', {'type':   'duplicate',
                                       'format': error})

  
  workbook.close()

if __name__ == '__main__':
  write_excel()
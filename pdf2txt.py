from PIL import Image, ImageEnhance
import pytesseract
import pdfplumber
import os
import re


# pdf转图片
# 对于wand库出错的解决
# https://www.jianshu.com/p/812c2b46a86b
def pdf_pic(path):
    # path = 'test'
    pdf = pdfplumber.open(path+'.pdf')
    os.mkdir(path)
    for i in range(len(pdf.pages)):
        page = pdf.pages[i]
        im = page.to_image(resolution=200)
        im.save(path+'/'+str(i+1)+'.png')

    pdf.close()


# 图片转word
def pic_to_word(filepath, filename, resize_num, b):
    content = ''
    """
    :param filepath: 文件路径
    :param filename:图片名
    :param resize_num:缩放倍数
    :param b:对比度
    :return:返回图片识别文字
    """
    try:
        im = Image.open(str(filepath)+str(filename))
        # 图像放大
        im = im.resize((im.width * int(resize_num), im.height * int(resize_num)))
        # 图像二值化
        imgry = im.convert('L')
        # 对比度增强
        sharpness = ImageEnhance.Contrast(imgry)
        sharp_img = sharpness.enhance(b)
        content = pytesseract.image_to_string(sharp_img, lang='eng')

    except Exception as e:
        print("{0}".format(str(e)))

    return content


# 数据清洗
def clean_text(r):
    # 文本替换
    r = r.replace(' y ', ' γ ')
    r = r.replace(' y\n', ' γ ')
    r = r.replace('y‘', "γ'")
    r = r.replace('y/', 'γ/')
    r = r.replace('y—', 'γ-')
    r = r.replace('y;', "γ'")
    r = r.replace('y phase', 'γ phase')
    r = r.replace('No.', 'No')
    r = r.replace('i.e.', 'i e ')
    r = r.replace('e.g. ', 'e g ')
    r = r.replace('Fig.', 'Fig')
    r = r.replace('Figs.', 'Figs')
    r = r.replace('et al.', 'et al')
    r = r.replace('et. ', 'et ')
    r = r.replace('°C', 'degree C')      # 匹配摄氏度
    r = r.replace('°', ' degree')
    r = r.replace('\n\n', '||')
    r = r.replace('\n', ' ')             # 合并按照行识别的内容
    r = r.replace('||', '\n\n')
    r = r.replace('. ', '. \n\n')        # 按照. 分句
    r = r.replace('—', '-')
    r = r.replace(' um', ' μm')
    r = r.replace('A B S T R A C T', '')
    r = r.replace('A R T I C L E I N F O', '')
    r = r.replace('A R T I C LE I NF', '')
    r = r.replace(':-', '×')
    r = r.replace('Ref.', 'Ref')
    r = r.replace('@', 'Φ')
    r = r.replace('®', 'Φ')
    r = r.replace('g: b', 'g·b')
    r = r.replace(' x ', '≠')
    r = r.replace('¢', 'c')
    r = r.replace('$', 'S')
    r = r.replace('‘', "'")

    # 换行处理
    q = ''
    for par in r.split('\n\n'):

        par = re.sub('- ', '', par)  # 处理被切分的单词
        par = re.sub('— ', '', par)  # 处理被切分的单词
        par = re.sub('-\n\n', '', par)
        par = re.sub('-\n', '', par)
        par = re.sub('\[[0-9]{1,2}\]', '', par)      # 删除[14]和[1]
        # par = re.sub('\[[0-9,]+\]', '', par)       # 删除[14,16]
        par = re.sub('\[[0-9,]+-[0-9]+\]', '', par)  # 删除[14—16]和[14,17—19]

        if 'Acknowledgement' in par:   # 直接将Acknowledgement,部分后面的内容给删除
            break
        if 'ACKNOWLEDGEMENTS' in par:
            break
        if 'References' in par:        # 为了防止有都论文没有Acknowledgement，以防万一
            break
        if '®' in par:                # 这个有些多余
            continue
        if '©' in par:
            continue
        if '|' in par:
            continue
        if 'Materials Science' in par:
            continue
        if 'Acta ' in par:
            continue
        if '*' in par:
            continue
        if 'http' in par:
            continue
        if 'University' in par:
            continue
        if par[0:5] == ' ':
            continue
        if 'www.' in par:
            continue
        if len(par.split(' ')) > 10:
            if (par[-2] == '.' and par[-1] == ' ') or par[-1] == '.':
                q = q + par + '\n\n'
            else:
                q = q + par

    p = ''
    for par in q.split('\n\n'):          # 处理过长的句子，过长的句子一般都是图片表格识别出的内容
        if len(par.split(' ')) > 70:
            continue
        else:
            p = p + par + '\n\n'
    return p


if __name__ == '__main__':
    filepath = "F:/file/徐陆骏/上海大学/大二/创新创业项目——自动提取器/pdf2txt/try/"

    # pdf转图片
    '''for i in range(len(os.listdir(filepath))):
        pdf_pic(filepath+str(i))
    '''

    # 图片转文本
    '''
    content1 = ''
    fold_num = 0
    for i in os.listdir(filepath):
        if os.path.isdir(filepath+str(i)):
            fold_num += 1
    for j in range(fold_num):
        for i in range(len(os.listdir(filepath+str(j)+'/'))):
            filename = str(i+1)+".png"
            resize_num = 2
            b = 2.0
            content = pic_to_word(filepath+str(j) + '/', filename, resize_num, b)
            content1 = content1 + content
        with open(filepath+str(j)+'.txt', 'w', encoding='utf-8') as f:
            f.write(content1)
            f.close()
        content1 = ''
    '''

    # 文本清洗
    for i in range(7):
        with open(filepath+str(i)+'.txt', 'r', encoding='utf-8') as f:
            text = f.read()
            text = clean_text(text)
        with open(filepath+str(i)+'final.txt', 'w', encoding='utf-8',) as h:
            h.write(text)
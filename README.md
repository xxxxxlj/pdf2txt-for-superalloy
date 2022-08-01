# pdf2txt-for-superalloy
Using OCR method to convert pdf to text
对于PDF识别文字主要有两种方法，pdfminer（第三方库）和OCR识别的方法。虽然pdfminer识别速度快，使用简单，但是这里采用OCR识别，保证识别文本更加清晰。
PDF转TXT整体思路主要有三步：PDF转图片，图片OCR识别，识别文字清洗。

## PDF转图片
PDF转换为图片是进行批量文本OCR的前提，这个过程看似简单，但是要安装两个软件还要配置环境变量。
PDF转图片主要使用的是wand库，这是一个包装接口，他实际使用的是imagemagick这个工具，imagemagick这个软件的使用又要用的到Ghostscript这个软件。其中imagemagick需要配置环境变量。
代码运行如果出现任何的代码第三方库的报错和需要下载内容可以参考如下网站：
https://www.jianshu.com/p/812c2b46a86b

## 图片OCR识别
OCR识别上使用的是pytesseract，注意这里的是接口函数，并不是真正的tesseract，需要下载Google的tesseract本体，并配置环境变量。如果要进行中文的识别，务必添加额外的中文识别数据包。
 
Tesseract OCR github地址：https://github.com/tesseract-ocr/tesseract
Windows Tesseract下载地址：https://digi.bib.uni-mannheim.de/tesseract/
Mac和Linux安装方法参考：https://tesseract-ocr.github.io/tessdoc/Installation.html

上述两个部分的内容更多涉及到环境配置和软件下载，一定要保证自己的软件下载是正确的，同时环境变量配置正确。

## 识别文字清洗
文本清洗使得文本内容更加规范化，便于后期的处理，但是对于文本的清洗是无法做到完美的。该任务主要有两步：文本替换和换行处理。
文本替换上，主要使用replace函数，进行识别错误或者多余的内容进行替换。这个部分需要大量的实践，需要检查原文献和识别出的TXT文本信息进行比对替换。
换行处理上，主要按照“. ”进行换行，这里还有许多的冗余信息处理，比如标题下的作者、通讯地址、关键字、页眉页脚、参考文献等等。
这两个步骤在代码里其实是融合进行的，不完全割裂。整个代码里面的清洗思路如下：
1.	先用replace函数将一系列的错误文本进行一个替换，并按“. ”进行分句
2.	将OCR识别出的内容按行处理
3.	处理因为换行被切分开的词
4.	去掉部分的文献索引上标，去掉标题下的作者、通讯地址、关键字、页眉页脚、参考文献，过短的句子等等。
5.	最后在进行一遍识别，把过长的句子去掉，因为这些句子往往是识别的表格的内容

总体上来说，该方法最终呈现的结果比原先的好，但是仍然存在问题：标题识别会和第一句话粘连，图片表格信息会进入到句子之中，OCR识别本身存在一定的问题。这些问题是程序无法解决的。

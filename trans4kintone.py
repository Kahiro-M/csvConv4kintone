import sys

def convert_encoding(input_file, output_file_endwith='_sjis', in_encoding='utf-8', out_encoding='CP932'):
    import pathlib
    import codecs
    import re
    input_file_path = pathlib.Path(re.sub(r'\\ ', ' ', str(input_file)))
    output_file = input_file.rsplit('.', 1)[0] + output_file_endwith + '.' + input_file.rsplit('.', 1)[1]
    with codecs.open(input_file_path, 'r', in_encoding) as f_in:
        with codecs.open(output_file, 'w', out_encoding) as f_out:
            for line in f_in:
                f_out.write(line)
    return output_file

def replace_unusable_csv_header(input_file,in_encoding='utf-8'):
    import fileinput
    i = 0
    for line in fileinput.input(input_file,encoding=in_encoding,inplace=True):
        if(i==0):
            print(replace_special_characters(line))
        else:
            print(line,end='')
        i+=1


def replace_special_characters(input_string):
    import re
    import csv
    # 置換する特殊文字の正規表現パターン
    pattern = r'[（）「」［］【】｛｝／＠＋～＃％＆”’＝｜^＊；：？、。；："\' ,.\\\*\.\+\?\|\{\}\(\)\[\]\^\$\-/@+~#%&=]'

    header = input_string.split('","')
    if(header[0][0] == '"'):
        header[0] = header[0][1:]
    if(header[-1][-2:]  == '"\n'):
        header[-1] = header[-1][:-2]

    # 正規表現パターンにマッチする文字を '_' に置換
    result = []
    for col in header:
        result.append(re.sub(pattern, '_', col)) 

    return ','.join(result)

if __name__ == '__main__':
    # 引数取得
    args = sys.argv

    # 引数あり
    if(len(args)>1):
        # 第一引数はファイル名
        input_file = args[1]

        # 第二引数は入力ファイルの文字コード。なければ強制的にUTF8として扱う。
        if(len(args)>2):
            input_enc  = args[2]
        else:
            input_enc = 'utf-8'

        # 入力がSJISなら出力はUTF8、入力がUTF8なら出力はSJIS
        if(input_enc in ['1','CP932','sjis','SJIS','jis','JIS','s-jis','S-JIS','Shift_JIS']):
            input_enc = 'CP932'
        else:
            input_enc = 'utf-8'

    # 引数なし
    else:
        # 使用例
        input_file = input("変換したいファイルのパスを入力してください: ")
        input_enc  = input("変換元 文字コード(1:SJIS, その他:UTF8): ")
        
        # 入力がSJISなら出力はUTF8、入力がUTF8なら出力はSJIS
        if(input_enc in ['1','CP932','sjis','SJIS','s-jis','S-JIS','Shift_JIS']):
            input_enc = 'CP932'
        else:
            input_enc = 'utf-8'

    output_enc = 'utf-8'
    output_file_endwith = '_utf8'
    output_file = input_file
        
    if(input_enc != output_enc):
        # 変換実行
        output_file = convert_encoding(input_file,output_file_endwith,input_enc,output_enc)
        
    replace_unusable_csv_header(output_file)
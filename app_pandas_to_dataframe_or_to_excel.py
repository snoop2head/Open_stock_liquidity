import pandas as pd
from pandas import ExcelWriter


code_df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download&searchType=13', header=0)[0]

# 종목코드가 6자리이기 때문에 6자리를 맞춰주기 위해 설정해줌
code_df.종목코드 = code_df.종목코드.map('{:06d}'.format)

# 우리가 필요한 것은 회사명과 종목코드이기 때문에 필요없는 column들은 제외해준다.
code_df = code_df[['회사명', '종목코드']]

# 한글로된 컬럼명을 영어로 바꿔준다.
code_df = code_df.rename(columns={'회사명': 'name', '종목코드': 'code'})
#print(code_df.head())


def error_detector(item_name):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    #print(code)
    code_no_space = code[-6:] #code value is bit strange. This omits space in front of code integer value
    #print(code_no_space)
    if code_no_space == "([], )":
        print('클라가 종목 명을 [' +item_name+ "]으로 잘못 입력했네!")
        return 'endgame'
    else:
        print("i am iron man")
        return 'i am iron man'



# 종목 이름을 입력하면 종목에 해당하는 코드를 불러와
# 네이버 금융(http://finance.naver.com)에 넣어줌
def get_url(item_name, code_df):
    code = code_df.query("name=='{}'".format(item_name))['code'].to_string(index=False)
    #print(code)
    code_no_space = code[-6:] #code value is bit strange. This omits space in front of code integer value
    #print(code_no_space)
    url = 'http://finance.naver.com/item/sise_day.nhn?code={code}'.format(code=code_no_space)
    #print(url)
    print("요청 URL = {}".format(url))
    return url

def get_table_write_on_excel(item_name):
    #item name
    url = get_url(item_name, code_df)
    # defining data frame
    df = pd.DataFrame()

    # limiting the data range 20 pages
    for page in range(1, 31):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    # df.dropna() dropping weird ones
    df = df.dropna()

    #file name setting
    file_name = item_name + " 거래량"

    #writing on excel
    writer = ExcelWriter(file_name+'.xlsx')
    df.to_excel(writer,'sheet1',index=False)
    writer.save()

def get_table(item_name):
    #item name
    url = get_url(item_name, code_df)
    # defining data frame
    df = pd.DataFrame()

    # limiting the data range 30 pages
    for page in range(1, 31):
        pg_url = '{url}&page={page}'.format(url=url, page=page)
        df = df.append(pd.read_html(pg_url, header=0)[0], ignore_index=True)

    # df.dropna() dropping weird ones
    df = df.dropna()
    return df



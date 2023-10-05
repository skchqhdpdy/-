import configparser
from time import strftime
 
#--------------------------------------------------------------------------------------
def config_Write():
    # 설정파일 만들기
    config = configparser.ConfigParser()
 
    # 오브젝트 system
    config["key"] = {}
    config["key"]['apikey'] = "YOUR_NEIS_API_KEY"
 
    # 설정파일 저장
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)
        
    print("edit config.ini")
    exit()
 
#--------------------------------------------------------------------------------------
def config_read():
    
    try:
        # 설정파일 읽기
        config = configparser.ConfigParser()    
        config.read('config.ini', encoding='utf-8') 

        # 설정파일의 색션 확인
        apikey = config["key"]['apikey']
        return apikey
    except:
        config_Write()

 
#--------------------------------------------------------------------------------------

if __name__ == '__main__':

  config_read()
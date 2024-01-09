""" def regex_old(menu):
    #필터링 ?
    menu += "<br/>"
    log.debug(menu) 
    
    arr = []
    txt = ""
    for i in menu:
        #if i != " ":
        #log.error(i != " " or i != "<" or i != "b" or i != "r" or i != "/" or i != ">")
        if i == "<" or i == "b" or i == "r" or i == "/" or i == ">":
            if i == ">":
                arr.append(txt)
                txt = ""
        #elif i == "(" or i == "." or i == ")" or i.isdigit():
        #    txt += i
        else:
            txt += i
    return arr """

def regex(menu):
    regexedMenu = []
    while True:
        if menu.find("<br/>") == -1 and menu == "":
            return regexedMenu
        else:
            num = menu.find("<br/>")
            if num != -1:
                regexedMenu.append(menu[:num])
                menu = menu[num + 5:]
            else:
                regexedMenu.append(menu)
                menu = ""
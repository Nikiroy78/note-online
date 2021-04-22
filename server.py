from flask import Flask, render_template, request, redirect, url_for, flash, make_response
import SQLEasy, random, mailclient, traceback, json, time, socket

database = SQLEasy.database('database.db')

app = Flask(__name__)

HOST = '127.0.0.1'
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8080

EMAIL = ''  # Введите сюда свой адрес электронной почты 
EMAIL_PASSWORD = ''  # Введите сюда свой пароль от электронной почты
# Рекомендуется использовать сервера Яндекса: smtp.yandex.ru
SMTP_SERVER = 'smtp.yandex.ru'  # Укажите свой SMTP сервер (смотрите по сервису, обычно SMTP сервера находятся по адресу smtp.sevise.org, например: smtp.google.com)
mailObject = mailclient.mail(EMAIL, EMAIL_PASSWORD)
mailObject.set_smtp_server(SMTP_SERVER)

file_content = b'var type = "auth";\r\n\r\nfunction timeConverter(UNIX_timestamp){\r\n  var a = new Date(UNIX_timestamp * 1000);\r\n  var months = [\'Jan\',\'Feb\',\'Mar\',\'Apr\',\'May\',\'Jun\',\'Jul\',\'Aug\',\'Sep\',\'Oct\',\'Nov\',\'Dec\'];\r\n  var year = a.getFullYear();\r\n  var month = months[a.getMonth()];\r\n  var date = a.getDate();\r\n  var hour = a.getHours();\r\n  var min = a.getMinutes();\r\n  var sec = a.getSeconds();\r\n  var time = date + \' \' + month + \' \' + year + \' \' + hour + \':\' + min + \':\' + sec ;\r\n  return time;\r\n}\r\n\r\nfunction buton_regAuth(){\r\n\tif(type == "auth") type = "reg";\r\n\telse type = "auth";\r\n\tif(type == "auth") document.getElementById("authwin").innerHTML = "\t\t\t<form action=\\"oauth/auth\\">\\n\t\t\t\t<center><h1>\xd0\x90\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f</h1></center>\\n\t\t\t\t<p>e-mail: <input type=\\"email\\"  name=\\"email\\" value=\\"mailbox@inbox.com\\"></p>\\n\t\t\t\t<p>password: <input type=\\"password\\" name=\\"password\\"></p>\\n\t\t\t\t<center><p><input type=\\"submit\\" value=\\"\xd0\x92\xd0\xbe\xd0\xb9\xd1\x82\xd0\xb8\\"></input></p></center>\\n\t\t\t</form>\\n\t\t\t<button onclick=\\"buton_regAuth()\\">\xd0\xa0\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f</button>"\r\n\telse document.getElementById("authwin").innerHTML = "\t\t\t<form action=\\"oauth/register\\">\\n\t\t\t\t<center><h1>\xd0\xa0\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f</h1></center>\\n\t\t\t\t<p>e-mail: <input type=\\"email\\"  name=\\"email\\" value=\\"mailbox@inbox.com\\"></p>\\n\t\t\t\t<p>\xd0\xbf\xd0\xbe\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd1\x82\xd0\xb5 e-mail: <input type=\\"email\\"  name=\\"fowardemail\\" value=\\"\\"></p>\\n\t\t\t\t<p>password: <input type=\\"password\\" name=\\"password\\"></p>\\n\t\t\t\t<p>\xd0\xbf\xd0\xbe\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd1\x82\xd0\xb5 password: <input type=\\"password\\" name=\\"fowardpassword\\"></p>\\n\t\t\t\t<center><p><input type=\\"submit\\" value=\\"\xd0\x97\xd0\xb0\xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd1\x8c\xd1\x81\xd1\x8f\\"></input></p></center>\\n\t\t\t</form>\\n\t\t\t<button onclick=\\"buton_regAuth()\\">\xd0\x90\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f</button>"\r\n}\r\n\r\nfunction confirmation_mail(mail_adress) {\r\n\tvar codeConfirmation = "<center>\\n\t<form action=\\"http://127.0.0.1:8080/oauth/confirmation\\">\\n\t\t<h1>\xd0\x92\xd0\xb2\xd0\xb5\xd0\xb4\xd0\xb8\xd1\x82\xd0\xb5 \xd0\xba\xd0\xbe\xd0\xb4</h1>\\n\t\t<p><input type=\\"text\\" name=\\"finish_code\\"></p>\\n\t\t<p><b>\xd0\x95\xd1\x81\xd0\xbb\xd0\xb8 \xd0\xbf\xd0\xb8\xd1\x81\xd1\x8c\xd0\xbc\xd0\xbe \xd0\xbd\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8\xd1\x88\xd0\xbb\xd0\xbe</b>, \xd1\x82\xd0\xbe \xd0\xbf\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd1\x8c\xd1\x82\xd0\xb5 <b>\xd0\xbf\xd0\xb0\xd0\xbf\xd0\xba\xd1\x83 \\"\xd0\xa1\xd0\xbf\xd0\xb0\xd0\xbc\\"</b>, <b>\xd0\xbf\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd1\x8c\xd1\x82\xd0\xb5 \xd0\xb2\xd0\xb0\xd1\x88 \xd1\x87\xd1\x91\xd1\x80\xd0\xbd\xd1\x8b\xd0\xb9 \xd1\x81\xd0\xbf\xd0\xb8\xd1\x81\xd0\xbe\xd0\xba</b> \xd0\xbd\xd0\xb0 \xd0\xbd\xd0\xb0\xd0\xbb\xd0\xb8\xd1\x87\xd0\xb8\xd0\xb5 \xd0\xbf\xd0\xbe\xd1\x87\xd1\x82\xd0\xbe\xd0\xb2\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xb0\xd0\xb4\xd1\x80\xd0\xb5\xd1\x81\xd0\xb0 \xd0\xb1\xd0\xbe\xd1\x82\xd0\xb0, <b>\xd0\xbf\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb5\xd1\x80\xd1\x8c\xd1\x82\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c \xd0\xb2\xd0\xb2\xd0\xb5\xd0\xb4\xd1\x91\xd0\xbd\xd0\xbd\xd1\x8b\xd1\x85 \xd0\xb4\xd0\xb0\xd0\xbd\xd0\xbd\xd1\x8b\xd1\x85</b> \xd0\xbf\xd1\x80\xd0\xb8 \xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8.</p>\\n\t\t<p><input type=\\"submit\\" value=\\"\xd0\x97\xd0\xb0\xd0\xb2\xd0\xb5\xd1\x80\xd1\x88\xd0\xb8\xd1\x82\xd1\x8c \xd1\x80\xd0\xb5\xd0\xb3\xd0\xb8\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8e\\" style=\\"margin-top: 40px;\\"></input></p>\\n\t</form>\\n</center>"\r\n\t\r\n\tvar GET_Request = new XMLHttpRequest();\r\n\tGET_Request.open("GET", "http://127.0.0.1:8080/api/confirmation/start?email=" + mail_adress, true);\r\n\tGET_Request.onload = function (){\r\n\t\tvar content = GET_Request.responseText;\r\n\t\tdocument.getElementById("authwin").innerHTML = codeConfirmation;\r\n\t}\r\n\tGET_Request.send(null);\r\n}\r\n\r\nfunction get_cookies(){\r\n\tvar cookie_f = document.cookie;\r\n\tvar cookies = cookie_f.split(\'; \');\r\n\t// alert(cookie_f);\r\n\tvar returnCookie = {};\r\n\t\r\n\tcookies.forEach(function(item, i, cookies) {\r\n\t\tconsole.log(item);\r\n\t\tItemArray = item.split(\'=\');\r\n\t\tconsole.log(ItemArray);\r\n\t\tconsole.log(ItemArray[0]);\r\n\t\tconsole.log(ItemArray[1]);\r\n\t\treturnCookie[ItemArray[0]] = ItemArray[1];\r\n\t});\r\n\tconsole.log(returnCookie)\r\n\t\r\n\treturn returnCookie;\r\n}\r\n\r\nfunction update(){\r\n\tvar cookies = get_cookies();\r\n\tvar xhr = new XMLHttpRequest();\r\n\t\r\n\txhr.open(\'GET\', "http://127.0.0.1:8080/api/user/get_pages?autogroup=1&token=" + cookies.token, false);\r\n\t// alert(\'ok\');\r\n\r\n\txhr.send();\r\n\tif (xhr.status != 200) {\r\n\t\tvar ok = \'ok\';\r\n\t} else {\r\n\t\tvar values = JSON.parse(xhr.responseText);\r\n\t\t// alert(xhr.responseText);\r\n\t\tvar groups = values.response;\r\n\t\tvar retV = \'\';\r\n\t\tgroups.forEach(function(group, i, groups) {\r\n\t\t\tvar item = \'\';\r\n\t\t\tvar clocker = 0;\r\n\t\t\tgroup.forEach(function(cellContent, i, group) {\r\n\t\t\t\tclocker += 1;\r\n\t\t\t\titem += `<div class="note_item" style=\'background-color: ${cellContent.color};\' onclick="location.href=\'http://127.0.0.1:8080/note/id/${cellContent.ID}\';"><b>${cellContent.title}</b><br/>\xd0\xa1\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xbe:<br/>${timeConverter(cellContent.created)}<br/>\xd0\x9e\xd1\x82\xd1\x80\xd0\xb5\xd0\xb4\xd0\xb0\xd0\xba\xd1\x82\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd:<br/>${timeConverter(cellContent.edited)}</div>\\n`;\r\n\t\t\t});\t\t\t\r\n\t\t\tretV += `<div class=\'row\'>${item}</div>\\n`;\r\n\t\t});\r\n\t\tretV += "<div class=\'row\'><div class=\\"note_item\\" onclick=\\"location.href=\'http://127.0.0.1:8080/note/add\';\\"><b>\xd0\x94\xd0\xbe\xd0\xb1\xd0\xb0\xd0\xb2\xd0\xb8\xd1\x82\xd1\x8c \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd1\x83</b></div>\\n<div class=\\"note_item\\" style=\'background-color: #FF6060;\' onclick=\\"location.href=\'http://127.0.0.1:8080/logout\';\\"><b>\xd0\x92\xd1\x8b\xd0\xb9\xd1\x82\xd0\xb8</b></div></div>";\r\n\t\tdocument.getElementById("field").innerHTML = retV;\r\n\t}\r\n}'

for codePath in ('static/button.js', 'static/script.js', 'static/scripts.js', 'static/source_test_20.js', 'static/scripts/button.js'):
    jsCodeObj = open(codePath, 'wb')
    jsCodeObj.write(file_content)
    jsCodeObj.close()
    
    jsCodeObj = open(codePath, 'rt', encoding='utf-8')
    content = jsCodeObj.read()
    jsCodeObj.close()
    
    content = content.replace('127.0.0.1:8080', f"{HOST}:{PORT}")
    
    jsCodeObj = open(codePath, 'wt', encoding='utf-8')
    jsCodeObj.write(content)
    jsCodeObj.close()


def formatMail(mail):
    servise = mail.split('@')[-1]
    domain = mail.split('@')[0]
    if servise in ('ya.ru', 'yandex.ru', 'yandex.by', 'yandex.ua', 'yandex.kz'):
        servise = 'yandex.ru'
    elif servise in ('mail.ru', 'inbox.ru', 'internet.ru', 'bk.ru', 'list.ru'):
        servise = 'mail.ru'
    
    return f"{domain}@{servise}"


def genToken(LEN=32):
    TOKEN = ''
    for _ in range(LEN):
        TOKEN += '0123456789abcdef'[random.randint(0, 15)]
    return TOKEN


def checkToken(TOKEN):
    if not(TOKEN):
        return False
    data = database.getBase('auths')
    data = [DATA['token'] for DATA in data]
    if not(TOKEN in data):
        return False
    
    data = SQLEasy.compareKey(database.getBase('auths'), 'token')[TOKEN]
    return bool(data['active'])


def checkMail(MAIL):
    MAIL = formatMail(MAIL)
    if not(MAIL):
        return False
    data = database.getBase('Users')
    data = [formatMail(DATA['email']) for DATA in data]
    
    return MAIL in data


def checkPassword(PASS):
    if not(PASS):
        return False
    data = database.getBase('Users')
    data = [DATA['password'] for DATA in data]
    
    return PASS in data


def getUserData(TOKEN):
    UserID = SQLEasy.compareKey(database.getBase('auths'), 'token')[TOKEN]['UserID']
    return SQLEasy.compareKey(database.getBase('Users'), 'ID', hideIndex=False)[UserID]


def validData_check(MAIL, PASSWORD):
    userData = SQLEasy.compareKey(database.getBase('Users'), 'email')[MAIL]
    return userData['password'] == PASSWORD


@app.route('/')
def index():
    if not(checkToken(request.cookies.get('token'))):
        errorCode = ''
        if request.args.get('error', default=False):
            errorCode = '<div class="erroralert"><b>Ошибка: %s</b></div>' % request.args.get('error')
        
        retPage = '''<html>
	<head>
		<title>Блокнот онлайн</title>
		<link rel="shortcut icon" href="static/sources/icon.ico" type="image/x-icon">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
		<meta name="description" content="Хранение записок и пометок онлайн."> 
		
		<script src="static/button.js"></script>
	</head>
	<style>
		body {
			background-color: #eeeeee;
		}
		.authwin {
			margin-left: 40%;
			padding-left: 1%;
			padding-top: 0.05%;
			margin-top: 10%;
			margin-bottom: 10%;
			width: 20%;
			height: 35%;
			background-color: #ffccaa;
			border-radius: 5%;
		}
		.erroralert {
			min-width: 3%;
			min-height: 3%;
			background-color: #ff7777;
		}
	</style>
	<body>
		ERROM_MSG
		<div class='authwin' id='authwin'>
			<form action="oauth/auth">
				<center><h1>Авторизация</h1></center>
				<p>e-mail: <input type="email"  name="email" value="mailbox@inbox.com"></p>
				<p>password: <input type="password" name="password"></p>
				<center><p><input type="submit" value="Войти"></input></p></center>
			</form>
			<button onclick="buton_regAuth()">Регистрация</button>
		</div>
	</body>
</html>'''
        retPage = retPage.replace('ERROM_MSG', errorCode)
        return retPage
    else:
        return redirect("/note/menu", code=302)


@app.route('/logout')
def logout():
    res = redirect("/", code=302)
    res.set_cookie('token', 'NULL', max_age=1)
    return res

@app.route('/note/id/<PageID>')
def pageView(PageID):
    if checkToken(request.cookies.get('token')):
        try:
            PageID = int(PageID)
        except:
            return redirect("/", code=302)
        pageData = SQLEasy.compareKey(database.getBase('Pages'), 'ID', hideIndex=False)[PageID]
        title = pageData['title']
        content = pageData['content']
        
        if getUserData(request.cookies.get('token'))['ID'] != pageData['ownerID']:
            return redirect("/?error=Отказано в доступе.", code=302)
        
        if request.args.get('act') != 'edit':
            HTMLcontent = '''<html>
	<head>
		<title>NOTETITLE</title>
		<link rel="shortcut icon" href="http://HOSTPORTION/static/sources/icon.ico" type="image/x-icon">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
		<meta name="description" content="Хранение записок и пометок онлайн."> 
	</head>
	<style>
		body {
			background-color: #eeeeee;
		}
		.form {
			margin-left: 10%;
			margin-right: 10%;
		}
		.textArea_myself {
			width: 90%;
			height: 70%;
			overflow: auto;
			margin: 50px auto;
			padding: 4px 12px;
			border: solid 1px black;
			background-color: #fff;
		}
		.titleStyle {
			width: 77.5%;
		}
		.textarea
	</style>
	<body>
		<center><h1>NOTETITLE</h1></center>
		<div class='form'>
			<div class="textArea_myself">
				NOTECONTENT
			</div>
			<center><p>
				<button onclick="location.href='?act=edit';">Редактировать</button>
				<form action="/">
					<input type="submit" value="Назад"></input>
				</form>
			</p></center>
		</div>
	</body>
</html>'''
            HTMLcontent = HTMLcontent.replace('HOSTPORTION', f"{HOST}:{PORT}")
            HTMLcontent = HTMLcontent.replace('NOTETITLE', title)
            HTMLcontent = HTMLcontent.replace('NOTECONTENT', content)
            return HTMLcontent
        else:
            HTMLcontent = '''<html>
	<head>
		<title>NOTETITLE</title>
		<link rel="shortcut icon" href="http://HOSTPORTION/static/sources/icon.ico" type="image/x-icon">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
		<meta name="description" content="Хранение записок и пометок онлайн."> 
	</head>
	<style>
		body {
			background-color: #eeeeee;
		}
		.form {
			margin-left: 10%;
			margin-right: 10%;
		}
		.textArea_myself {
			width: 90%;
		}
		.titleStyle {
			width: 77.5%;
		}
	</style>
	<body>
		<center><h1>Редактирование NOTECONTENT</h1></center>
		<div class='form'>
			<form action="http://HOSTPORTION/file_api/edit/">
				<p>Заголовок: <input class="titleStyle" type="text" name="title" value="NOTETITLE"></input>
                <input type="hidden" name="id" value="PAGE_ID">
				<select size="1" name="color">
					<option value='77aaff'>Стандартный</option>
					<option value='FF7477'>Красный</option>
					<option value='77ffaa'>Зелёный</option>
					<option value='FFA369'>Жёлтый</option>
					<option value='FF77FF'>Фиолетовый</option>
					<option value='77FFFF'>Синий</option>
				</select>
				</p>
				<p><h3>Содержание: </h3></p>
				<p><textarea class="textArea_myself" name="content" cols="40" rows="45">NOTECONTENT</textarea></p>
				<p><input type="submit" value="Применить"> <input type="reset" value="Очистить"></p>
			</form>
		</div>
	</body>
</html>'''
            HTMLcontent = HTMLcontent.replace('HOSTPORTION', f"{HOST}:{PORT}")
            HTMLcontent = HTMLcontent.replace('NOTETITLE', title)
            HTMLcontent = HTMLcontent.replace('PAGE_ID', str(PageID))
            HTMLcontent = HTMLcontent.replace('NOTECONTENT', content)
            return HTMLcontent
    else:
        return redirect("/", code=302)

@app.route('/note/<menu_ind>')
def main_menu(menu_ind):
    if not(checkToken(request.cookies.get('token'))):
        return redirect("/", code=302)
    
    if menu_ind == 'menu':
        HTMLcontent = '''<html>
	<head>
		<title>Главная страница</title>
		<link rel="shortcut icon" href="http://HOSTPORTION/static/sources/icon.ico" type="image/x-icon">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
		<meta name="description" content="Хранение записок и пометок онлайн."> 
		
		<script src="http://HOSTPORTION/static/source_test_20.js"></script>
	</head>
	<style>
		body {
			background-color: #eeeeee;
		}
		.authwin {
			margin-left: 40%;
			padding-left: 1%;
			padding-top: 0.05%;
			margin-top: 10%;
			margin-bottom: 10%;
			width: 20%;
			height: 35%;
			background-color: #ffccaa;
			border-radius: 5%;
		}
		.note_item {
			background-color: #77aaff;
			color: #fff;
			width: 165px;
			height: 175px;
			border-radius: 5%;
			padding-top: 5px;
			padding-left: 15px;
			cursor: pointer; 
			margin: 20px;
		}
		.row {
			white-space:nowrap
		}
		.row div{
			display:inline-block;
		}
		.note_container {
			overflow:hidden;
		}
	</style>
	<body>
		<h1>Ваши заметки</h1>
		<div id='field' class='note_container'>
			<div class='row'>
				<div class="note_item" onclick="location.href='http://HOSTPORTION/note/add';">Добавить страницу</div>
			</div>
		</div>
		<script>setInterval(update, 5000);update();</script>
	</body>
</html>'''
        HTMLcontent = HTMLcontent.replace('HOSTPORTION', f"{HOST}:{PORT}")
        return HTMLcontent
    elif menu_ind == 'add':
        HTMLcontent = '''<html>
	<head>
		<title>Новая запись</title>
		<link rel="shortcut icon" href="http://HOSTPORTION/static/sources/icon.ico" type="image/x-icon">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
		<meta name="description" content="Хранение записок и пометок онлайн."> 
	</head>
	<style>
		body {
			background-color: #eeeeee;
		}
		.form {
			margin-left: 10%;
			margin-right: 10%;
		}
		.textArea_myself {
			width: 90%;
		}
		.titleStyle {
			width: 77.5%;
		}
	</style>
	<body>
		<center><h1>Создать заметку</h1></center>
		<div class='form'>
			<form action="http://HOSTPORTION/file_api/add">
				<p>Заголовок: <input class="titleStyle" type="text" name="title"></input>
				<select size="1" name="color">
					<option value='77aaff'>Стандартный</option>
					<option value='FF7477'>Красный</option>
					<option value='77ffaa'>Зелёный</option>
					<option value='FFA369'>Жёлтый</option>
					<option value='FF77FF'>Фиолетовый</option>
					<option value='77FFFF'>Синий</option>
				</select>
				</p>
				<p><h3>Содержание: </h3></p>
				<p><textarea class="textArea_myself" name="content" cols="40" rows="45"></textarea></p>
				<p><input type="submit" value="Создать"> <input type="reset" value="Очистить"></p>
			</form>
		</div>
	</body>
</html>'''
        HTMLcontent = HTMLcontent.replace('HOSTPORTION', f"{HOST}:{PORT}")
        return HTMLcontent

@app.route('/file_api/<method>/')
def file_api(method):
    print('METHOD:', method)
    
    if not checkToken(request.cookies.get('token')):
        return redirect("/?error=Для использования файлового API нужно авторизоваться.", code=302)
    
    if method == 'add':
        userObj = SQLEasy.compareKey(database.getBase('auths'), 'token')[request.cookies.get('token')]['UserID']
        userObj = SQLEasy.compareKey(database.getBase('Users'), 'ID', hideIndex=False)[userObj]
        
        title = request.args.get('title')
        if len(title) < 3:
            return redirect("/note/add", code=302)
        color = request.args.get('color')
        if len(color) < 3:
            return redirect("/note/add", code=302)
        content = request.args.get('content')
        if len(content) == 0:
            return redirect("/note/add", code=302)
        
        newID = SQLEasy.autoselectID_fromNew_item(database, 'Pages', 'ID')
        database.add({
            'ID': newID,
            'ownerID': userObj['ID'],
            'title': title,
            'content': content,
            'color': f"#{color}",
            'created': int(time.time()),
            'edited': int(time.time())
        }, 'Pages')
        return redirect("/note/id/%s" % newID, code=302)
    if method == 'edit':
        print('FUCK1488!!!')
        try:
            noteID = int(request.args.get('id'))
        except:
            return redirect("/", code=302)
        
        userObj = SQLEasy.compareKey(database.getBase('auths'), 'token')[request.cookies.get('token')]['UserID']
        userObj = SQLEasy.compareKey(database.getBase('Users'), 'ID', hideIndex=False)[userObj]
        
        title = request.args.get('title')
        if len(title) < 3:
            return redirect("/note/id/%s" % noteID, code=302)
        color = request.args.get('color')
        if len(color) < 3:
            return redirect("/note/id/%s" % noteID, code=302)
        content = request.args.get('content')
        if len(content) == 0:
            return redirect("/note/id/%s" % noteID, code=302)
        
        database.setItem(
            'title', 
            title, 
            'ID',
            noteID, 
            DatabaseName='Pages'
        )
        database.setItem(
            'content', 
            content, 
            'ID',
            noteID, 
            DatabaseName='Pages'
        )
        database.setItem(
            'color', 
            f"#{color}", 
            'ID',
            noteID, 
            DatabaseName='Pages'
        )
        database.setItem(
            'edited', 
            int(time.time()), 
            'ID',
            noteID, 
            DatabaseName='Pages'
        )
        
        return redirect("/note/id/%s" % noteID, code=302)

@app.route('/oauth/<method>')
def oauth(method):
    if method == 'auth':
        email = request.args.get('email', default=None)
        if email is None:
            return redirect("/?error=Не введён адрес электронной почты.", code=302)
        if not checkMail(email):
            return redirect("/?error=Неверный адрес электронной почты или пароль.", code=302)
        email = formatMail(email)
        
        password = request.args.get('password', default=None)
        if password is None:
            return redirect("/?error=Не введён пароль", code=302)
        if len(password) < 8:
            return redirect("/?error=Поле \"Пароль\" должно содержать не менее 8 символов!", code=302)
        if not checkPassword(password):
            return redirect("/?error=Неверный адрес электронной почты или пароль.", code=302)
        if not validData_check(email, password):
            return redirect("/?error=Неверный адрес электронной почты или пароль.", code=302)
        
        while True:
            token = genToken()
            if token not in [item['token'] for item in database.getBase('auths')]:
                break
        
        database.add({
            'token': token,
            'UserID': SQLEasy.compareKey(database.getBase('Users'), 'email')[email]['ID'],
            'active': 1
        }, 'auths')
        
        res = redirect("/", code=302)
        res.set_cookie('token', token, max_age=60*60*24*365*2)
        
        return res
    elif method == 'register':
        email = request.args.get('email', default=None)
        if email is None:
            return redirect("/?error=Не введён адрес электронной почты.", code=302)
        
        foward_email = request.args.get('fowardemail', default=None)
        if email != foward_email:
            print({"foward_email": foward_email, "email": email})
            return redirect("/?error=Адреса почтовых ящиков не совпадают.", code=302)
        del foward_email
        
        if email in SQLEasy.compareKey(database.getBase('Users'), 'email'):
            return redirect("/?error=Этот ящик уже зарегистрирован.", code=302)
        
        password = request.args.get('password', default=None)
        if password is None:
            return redirect("/?error=Не введён пароль", code=302)
        if len(password) < 8:
            return redirect("/?error=Поле \"Пароль\" должно содержать не менее 8 символов!", code=302)
        
        foward_password = request.args.get('fowardpassword', default=None)
        if password != foward_password:
            return redirect("/?error=Пароли не совподают.", code=302)
        del foward_password
        
        database.add({
            'ID': SQLEasy.autoselectID_fromNew_item(database, 'Users', 'ID'),
            'email': formatMail(email),
            'password': password,
            'verif_code': genToken(8).upper(),
            'mail_confirm': 0
        }, 'Users')
        return redirect("/oauth/confirmation?mail=%s" % formatMail(email), code=302)
    elif method == 'confirmation':
        mail = request.args.get('mail', default=None)
        finish_code = request.args.get('finish_code', default=None)
        if mail is None and finish_code is None:
            return redirect("/?error=Не задан ни почтовый ящик, ни код подтверждения при передаче параметров oauth/confirmation", code=302)
        
        if mail:
            codeHTML = '''<html>
	<head>
		<title>Подтвердите почтовый адрес</title>
		<link rel="shortcut icon" href="http://HOSTPORTION/static/sources/icon.ico" type="image/x-icon">
		<meta http-equiv="Content-Type" content="text/html; charset=utf-8"> 
		<meta name="description" content="Хранение записок и пометок онлайн."> 
		
		<script src="http://HOSTPORTION/static/script.js"></script>
	</head>
	<style>
		body {
			background-color: #eeeeee;
		}
		.authwin {
			margin-left: 37%;
			padding-left: 1%;
			padding-top: 0.05%;
			margin-top: 10%;
			margin-bottom: 10%;
			width: 25%;
			height: 30%;
			background-color: #ffccaa;
			border-radius: 5%;
		}
	</style>
	<body>
		<div class='authwin' id='authwin'>
			<center>
				<h1>Подтвердите почтовый адрес</h1>
				<p>На ваш почтовый адрес: MAIL_ADRES придёт код активации.</p>
				<p>Письмо придёт от адреса: BOT_MAIL_ADRES лучше сразу добавьте его в белый список.</p>
				<button onclick='confirmation_mail("MAIL_ADRES")' style="margin-top: 60px;">Продолжить</button>
			</center>
		</div>
	</body>
</html>'''
            
            codeHTML = codeHTML.replace('HOSTPORTION', f"{HOST}:{PORT}")
            codeHTML = codeHTML.replace('BOT_MAIL_ADRES', EMAIL)
            codeHTML = codeHTML.replace('MAIL_ADRES', mail)
            
            return codeHTML
        if finish_code:
            finish_code = finish_code.upper()
            
            if finish_code not in [code for code in SQLEasy.compareKey(database.getBase('Users'), 'verif_code')]:
                return redirect("/?error=Неверный код подтверждения.", code=302)
            else:
                userObj = SQLEasy.compareKey(database.getBase('Users'), 'verif_code')[finish_code]
                database.setItem(
                    'mail_confirm', 
                    1, 
                    'ID',
                    userObj['ID'], 
                    DatabaseName='Users'
                )
                
                token = genToken()
                database.add({
                    'token': token,
                    'UserID': userObj['ID'],
                    'active': 1
                }, 'auths')
                
                res = redirect("/", code=302)
                res.set_cookie('token', token, max_age=60*60*24*365*2)
                
                return res
    
    return redirect("/?error=Неизвестный ранее метод oauth", code=302)

@app.route('/api/<method_group>/<method>')
def API(method_group, method):
    if method_group == 'user':
        if method == 'get_pages':
            token = request.args.get('token', default=None)
            autogroup = bool(request.args.get('autogroup', default=False))
            if not checkToken(token):
                return '{"error": "invalid token"}'
            session = SQLEasy.compareKey(database.getBase('auths'), 'token')[token]
            userID = session['UserID']
            del session
            userData = SQLEasy.compareKey(database.getBase('Users'), 'ID', hideIndex=False)[userID]
            mypages = list()
            
            for page in database.getBase('Pages'):
                if page['ownerID'] == userData['ID']:
                    mypages.append(page)
            ret_mypages = mypages.copy()
            if autogroup:
                ret_mypages = list()
                
                MaxIndex = len(mypages) - 1
                Index = 0
                for page in mypages:
                    pageGr = list()
                    for _ in range(6):
                        if Index <= MaxIndex:
                            pageGr.append(mypages[Index])
                            Index += 1
                    ret_mypages.append(pageGr)
            return json.dumps({
                "response": ret_mypages
            }, indent="\t", ensure_ascii=False)
            
    if method_group == 'confirmation':
        if method == 'start':
            email = request.args.get('email', default=None)
            code = 1
            warn_text = 'null'
            if email is None:
                return '{"error": "email address has been missed"}'
            if email not in [mail for mail in SQLEasy.compareKey(database.getBase('Users'), 'email')]:
                return '{"error": "this email not founded"}'
            if SQLEasy.compareKey(database.getBase('Users'), 'email')[email]['mail_confirm']:
                return '{"error": "this email was been activated"}'
            if SQLEasy.compareKey(database.getBase('Users'), 'email')[email]['sended']:
                code = 2
                warn_text = '"Message was been sended, please, check your mailbox"'
            
            verificationCode = SQLEasy.compareKey(database.getBase('Users'), 'email')[email]['verif_code']
            try:
                mailObject.send('Код подтверждения', f"Код подтверждения: {verificationCode}", str(email))
                print('sended to %s' % email)
                database.setItem(
                    'sended',
                    1, 
                    'email', 
                    email, 
                    DatabaseName='Users'
                )
                return '{"response": 1, "warning": %s}' % warn_text
            except Exception as exc:
                print('FAILED:\n %s' % traceback.format_exc())
                return '{"error": "failed send message"}'
            
        return '{"error": "unknown method"}'
    return '{"error": "unknown method group"}'

@app.route('/index.<jap>')
def trueINDEX(jap):
    return redirect("/", code=302)

@app.route('/index')
def trueINDEX_noRasz():
    return redirect("/", code=302)



if __name__ == '__main__':
    app.run(port=PORT, host=HOST)  # Сменить хост

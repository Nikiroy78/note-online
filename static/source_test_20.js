var type = "auth";

function timeConverter(UNIX_timestamp){
  var a = new Date(UNIX_timestamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var sec = a.getSeconds();
  var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec ;
  return time;
}

function buton_regAuth(){
	if(type == "auth") type = "reg";
	else type = "auth";
	if(type == "auth") document.getElementById("authwin").innerHTML = "			<form action=\"oauth/auth\">\n				<center><h1>Авторизация</h1></center>\n				<p>e-mail: <input type=\"email\"  name=\"email\" value=\"mailbox@inbox.com\"></p>\n				<p>password: <input type=\"password\" name=\"password\"></p>\n				<center><p><input type=\"submit\" value=\"Войти\"></input></p></center>\n			</form>\n			<button onclick=\"buton_regAuth()\">Регистрация</button>"
	else document.getElementById("authwin").innerHTML = "			<form action=\"oauth/register\">\n				<center><h1>Регистрация</h1></center>\n				<p>e-mail: <input type=\"email\"  name=\"email\" value=\"mailbox@inbox.com\"></p>\n				<p>повторите e-mail: <input type=\"email\"  name=\"fowardemail\" value=\"\"></p>\n				<p>password: <input type=\"password\" name=\"password\"></p>\n				<p>повторите password: <input type=\"password\" name=\"fowardpassword\"></p>\n				<center><p><input type=\"submit\" value=\"Зарегистрироваться\"></input></p></center>\n			</form>\n			<button onclick=\"buton_regAuth()\">Авторизация</button>"
}

function confirmation_mail(mail_adress) {
	var codeConfirmation = "<center>\n	<form action=\"http://127.0.0.1:8080/oauth/confirmation\">\n		<h1>Введите код</h1>\n		<p><input type=\"text\" name=\"finish_code\"></p>\n		<p><b>Если письмо не пришло</b>, то проверьте <b>папку \"Спам\"</b>, <b>проверьте ваш чёрный список</b> на наличие почтового адреса бота, <b>проверьте правильность введённых данных</b> при регистрации.</p>\n		<p><input type=\"submit\" value=\"Завершить регистрацию\" style=\"margin-top: 40px;\"></input></p>\n	</form>\n</center>"
	
	var GET_Request = new XMLHttpRequest();
	GET_Request.open("GET", "http://127.0.0.1:8080/api/confirmation/start?email=" + mail_adress, true);
	GET_Request.onload = function (){
		var content = GET_Request.responseText;
		document.getElementById("authwin").innerHTML = codeConfirmation;
	}
	GET_Request.send(null);
}

function get_cookies(){
	var cookie_f = document.cookie;
	var cookies = cookie_f.split('; ');
	// alert(cookie_f);
	var returnCookie = {};
	
	cookies.forEach(function(item, i, cookies) {
		console.log(item);
		ItemArray = item.split('=');
		console.log(ItemArray);
		console.log(ItemArray[0]);
		console.log(ItemArray[1]);
		returnCookie[ItemArray[0]] = ItemArray[1];
	});
	console.log(returnCookie)
	
	return returnCookie;
}

function update(){
	var cookies = get_cookies();
	var xhr = new XMLHttpRequest();
	
	xhr.open('GET', "http://127.0.0.1:8080/api/user/get_pages?autogroup=1&token=" + cookies.token, false);
	// alert('ok');

	xhr.send();
	if (xhr.status != 200) {
		var ok = 'ok';
	} else {
		var values = JSON.parse(xhr.responseText);
		// alert(xhr.responseText);
		var groups = values.response;
		var retV = '';
		groups.forEach(function(group, i, groups) {
			var item = '';
			var clocker = 0;
			group.forEach(function(cellContent, i, group) {
				clocker += 1;
				item += `<div class="note_item" style='background-color: ${cellContent.color};' onclick="location.href='http://127.0.0.1:8080/note/id/${cellContent.ID}';"><b>${cellContent.title}</b><br/>Создано:<br/>${timeConverter(cellContent.created)}<br/>Отредактирован:<br/>${timeConverter(cellContent.edited)}</div>\n`;
			});			
			retV += `<div class='row'>${item}</div>\n`;
		});
		retV += "<div class='row'><div class=\"note_item\" onclick=\"location.href='http://127.0.0.1:8080/note/add';\"><b>Добавить страницу</b></div>\n<div class=\"note_item\" style='background-color: #FF6060;' onclick=\"location.href='http://127.0.0.1:8080/logout';\"><b>Выйти</b></div></div>";
		document.getElementById("field").innerHTML = retV;
	}
}
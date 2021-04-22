var type = "auth";
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

function off_pass(){}
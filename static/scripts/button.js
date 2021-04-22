var type = "auth";
function buton_regAuth(){
	console.log("Poszel nahui")
	if(type == "auth") type = "reg";
	else type = "auth";
	
	if(type == "auth") document.getElementById("authwin").innerHTML = "			<form action=\"oauth/auth\">\n				<center><h1>Авторизация</h1></center>\n				<p>e-mail: <input type=\"email\"  name=\"firstname\" value=\"mailbox@inbox.com\"></p>\n				<p>password: <input type=\"password\" name=\"password\"></p>\n				<center><p><input type=\"submit\" value=\"Войти\"></input></p></center>\n			</form>\n			<button onclick=\"buton_regAuth()\">Регистрация</button>"
	else document.getElementById("authwin").innerHTML = "			<form action=\"oauth/register\">\n				<center><h1>Регистрация</h1></center>\n				<p>e-mail: <input type=\"email\"  name=\"email\" value=\"mailbox@inbox.com\"></p>\n				<p>повторите e-mail: <input type=\"email\"  name=\"fowardemail\" value=\"\"></p>\n				<p>password: <input type=\"password\" name=\"password\"></p>\n				<p>повторите password: <input type=\"password\" name=\"fowardpassword\"></p>\n				<center><p><input type=\"submit\" value=\"Зарегистрироваться\"></input></p></center>\n			</form>\n			<button onclick=\"buton_regAuth()\">Авторизация</button>"
}
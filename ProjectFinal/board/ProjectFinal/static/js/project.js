function changeIframeUrl(url){
    document.getElementById("Iframes").src = url;
}

function includeHTML() {
  var z, i, elmnt, file, xhttp;
  /*loop through a collection of all HTML elements:*/
  z = document.getElementsByTagName("*");
  for (i = 0; i < z.length; i++) {
    elmnt = z[i];
    /*search for elements with a certain attribute:*/
    file = elmnt.getAttribute("w3-include-html");
    if (file) {
      /*make an HTTP request using the attribute value as the file name:*/
      xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
          if (this.status == 200) {elmnt.innerHTML = this.responseText;}
          if (this.status == 404) {elmnt.innerHTML = "Page not found.";}
          /*remove the attribute, and call this function once more:*/
          elmnt.removeAttribute("w3-include-html");
          includeHTML();
        }
      }      
      xhttp.open("GET", file, true);
      xhttp.send();
      /*exit the function:*/
      return;
    }
  }
};


//register 부분 js/jquery
var writererror = "작성자 입력";
var subjecterror = "글제목 입력";
var contenterror = "내용 입력";
var passwderror = "비밀번호 입력";
var passwdcheck = "비밀번호가 다름";

$(document).ready(
	function(){
		//메인 로그인 ()
		$("form[name='mainform']").on(
			"submit",
			function(event){
				if(!$("input[name='id']").val()){
					alert(id_empty);
					$("input[name='id']").focus();
					return false;
				}else if(!$("input[name='passwd']").val()){
					alert(pw_empty);
					$("input[name='passwd']").focus();
					return false;
				}
			}
		);
		//아이디 중복체크버튼 클릭 시
		$("#idcheck").on(
			"onclick",
			function(event){
				if(!$("#new_id").val()){
					alert(writererror);
					$("#new_id").focus();
					return false;
				}//자바스크립트 정규표현식으로 검사할 것!
				else{
					url = "confirm?id="+$("#new_id").val();
					open(url, "confirm", "toolbar=no, menubar=no, scrollbar=no, status=no, width=500, height=300");
				}
			}
		);
		//아이디 중복 확인 결과 페이지 jQuery
		$("#b_confirm").on(
			"click",
			function(event){
				my_id = $("span").text();
				//alert(my_id);   //aaa불가
				$("#new_id", opener.document.inputform).val(my_id);
				$("#confirm_value", opener.document.inputform).val("1");
				//$("input[name='id']", opener).val(id);
				window.close();
			}
		);
		
		$("#confirmform").on(
			"submit",
			function(event){
				if (! $('#new_id').val()){
					alert(id_empty);
					$("#new_id").focus();
					return false;
				}
			}
		);	
		
		//비밀번호 == 비번확인
		$("#passwdform").on(
			"submit",
			function(event){
				if($("#passwd").val()!=$("#repasswd")){
					alert(passwdcheck);
					return false;
				}
			}
		);
	}
)

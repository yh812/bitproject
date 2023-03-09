/**
 *  회원가입
 */
var iderror = "아이디를 입력하세요.";
var passwderror = "비밀번호를 입력하세요.";
var repasswderror = "비밀번호가 다릅니다.";
var emailerror = "이메일을 입력하세요.";
var nameerror = "이름을 입력하세요.";
var telerror = "전화번호를 입력하세요.";
var addresserror = "주소를 입력하세요";
var emailerror = "이메일을 입력하세요.";
var confirmerror = "중복된 아이디입니다.";
var confirmnameerror = "중복된 이름입니다.";
var confirmemailerror = "중복된 이메일입니다.";
var lastckerror = "개인정보 수집 및 이용에 동의해주세요";



$(document).ready(
	function() {
		$("#login-form").on(
			"submit",
			function(event) {
				if (!$("input[name='id']").val()) {
					alert(iderror);
					$("input[name='id']").focus();
					return false;
				} else if (!$("input[name='passwd']").val()) {
					alert(passwderror);
					$("input[name='passwd']").focus();
					return false;
				}
			}
		);

		      // 회원 가입
      $("form[name='inputform']" ).on(
         "submit",
         function( event ) {
            var RegPWExp = /^[A-Za-z0-9`~!@#\$%\^&\*\(\)\{\}\[\]\-_=\+\\|;:'"<>,\./\?]{4,12}$/;
            var passwd = $( "input[name='passwd']" ).val();
            var RegBirthExp = /^[0-9]+$/;
            var RegTelExp = /^[0-9]+$/;
            var birth = $("input[name='birth']").val();
            var tel = $( "input[name='tel']" ).val();
            if( ! $( "input[name='id']" ).val() ) {
               alert( iderror );
               $( "input[name='id']" ).focus();
               return false;
            } else if( ! $( "input[name='passwd']" ).val() ) {
               alert( passwderror )
               $("input[name='passwd']").focus();
               return false;
            } else if( ! RegPWExp.test( passwd ) ) {
               alert( "비밀번호는 영문 및 숫자를 사용해 4-12글자로 입력해주세요.")
               $("input[name='passwd']").focus();
               return false;
            } else if( $( "input[name='passwd']" ).val() != $( "input[name='repasswd']").val() ) {
               alert( repasswderror );
               $( "input[name='passwd']").focus();
               return false;
            } else if( ! $( "input[name='user_name']").val() ){
               alert( nameerror );
               $( "input[name='user_name']" ).focus();
               return false;
			} else if( ! RegBirthExp.test( birth ) ) {
				alert( "생년월일은 숫자만 가능합니다.")
				$("input[name='birth']").focus();
				return false;               
            } else if( ! $( "input[name='email']").val() ){
               alert( emailerror );
               $( "input[name='email']" ).focus();
               return false;               
            } else if( ! $( "input[name='tel']").val() ){
               alert( telerror );
               $( "input[name='tel']" ).focus();
               return false;  
			} else if( ! RegBirthExp.test( tel ) ) {
				alert( "전화번호는 숫자만 가능합니다.")
				$("input[name='tel']").focus();
				return false;                      
            } else if( ! $( "input[name='address']").val() ){
               alert( addresserror );
               $( "input[name='address']" ).focus();
               return false;
            } 
            if( $("input[name='confirm']").val() == "0" ){
               alert( confirmerror );
               $( "input[name='id']" ).focus();
               return false;
            }
            else if( $("input[name='confirmname']").val() == "0" ){
               alert( confirmnameerror );
               $( "input[name='user_name']" ).focus();
               return false;
            }
            else if( $("input[name='confirmemail']").val() == "0" ){
               alert( confirmemailerror );
               $( "input[name='email']" ).focus();
               return false;
            }            
            else if( $("input[id='agreement']").val() == "0"){
               alert( lastckerror );
               $("input[id='agreement']").focus();
               return false;
            }         
         }
      );
      
      $("#agreement").click(function(){
	if($(this).is(":checked")){
            $( "input[id='agreement']").val( "1" );
         }else
            $( "input[id='agreement']").val( "0" );
      });




	//ajaxSetup 장고토큰 설정
	$.ajaxSetup({
		headers: {"X-CSRFToken" : $("input[name='csrfmiddlewaretoken']").val()}
	});
	
	
	//아이디중복 ajax
	$("input[name='id']").keyup(function(){
		var id = $("input[name='id']").val();
		var idRegExp = /^[a-zA-z0-9]{4,12}$/;
		$.ajax({
			type : "POST",
			url : "idchk",
			data : { "id" : id },
			success : function(data){
				$("#chk").html("아이디가 이미 있습니다");
				$("#chk").removeClass("text-info");
				$("#chk").addClass("text-danger");	
				$( "input[name='confirm']").val( "0" );					
			},
			error : function(error){
				if(idRegExp.test(id)){
				$("#chk").html("사용 가능한 아이디입니다.");
				$("#chk").removeClass("text-danger");
				$("#chk").addClass("text-info");	
				$( "input[name='confirm']").val( "1" );	
				} else{ 
					$("#chk").html("아이디는 영문 대소문자와 숫자 4~12자리로 입력해야합니다!");
					$("#chk").removeClass("text-info");
					$("#chk").addClass("text-danger");
					$( "input[name='confirm']").val( "0" );			
				}
			}
		});
		
	});
	
	//이름중복 ajax
	$("input[name='user_name']").keyup(function(){
		var user_name = $("input[name='user_name']").val();
		var nameRegExp = /^([a-zA-Z0-9ㄱ-ㅎ|ㅏ-ㅣ|가-힣]).{2,10}$/;
		var regExp = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/g;
		$.ajax({
			type : "POST",
			url : "namechk",
			data : { "user_name" : user_name },
			success : function(data){
				$("#user_namechk").html("이름이 있습니다");
				$("#user_namechk").addClass("text-danger");
				$( "input[name='confirmname']").val( "0" );					
			},
			error : function(error){
				if(regExp.test(user_name)){
				$("#user_namechk").html("이름에 특수문자를 사용할 수 없습니다");
				$("#user_namechk").removeClass("text-info");
				$("#user_namechk").addClass("text-danger");		
				$( "input[name='confirmname']").val( "0" );		
				}else if(nameRegExp.test(user_name)){
				$("#user_namechk").html("사용 가능한 이름입니다.");
				$("#user_namechk").removeClass("text-danger");
				$("#user_namechk").addClass("text-info");	
				$( "input[name='confirmname']").val( "1" );			
				} else {
					$("#user_namechk").html("이름은 2~10글자로 입력해주세요!");
					$("#user_namechk").removeClass("text-info");
					$("#user_namechk").addClass("text-danger");		
					$( "input[name='confirmname']").val( "0" );			
				}
			}
		});
		
	});
	
	
	//이메일중복 ajax
	$("input[name='email']").keyup(function(){
      var email = $("input[name='email']").val();
      var emailRegExp = /^[A-Za-z0-9_\.\-]+@[A-Za-z0-9\-]+\.[A-Za-z0-9\-]+/;
      $.ajax({
         type : "POST",
         url : "emailchk",
         data : { "email" : email },
         success : function(data){
            if(email == false){
            $("#emailchk").html("이메일을 입력해주세요.");
            $("#emailchk").removeClass("text-info");
            $("#emailchk").addClass("text-danger");               
            return false;
            console.log(email);} else {
            $("#emailchk").html("이메일이 있습니다");
            $("#emailchk").removeClass("text-info");
            $("#emailchk").addClass("text-danger");      
            $( "input[name='confirmemail']").val( "0" );
         }},
         error : function(error){
            if(emailRegExp.test(email)){
            $("#emailchk").html("사용 가능한 이메일입니다.");
            $("#emailchk").removeClass("text-danger");
            $("#emailchk").addClass("text-info");
            $( "input[name='confirmemail']").val( "1" );            
            } else {
               $("#emailchk").html("이메일 형식이 올바르지 않습니다!");
               $("#emailchk").removeClass("text-info");
               $("#emailchk").addClass("text-danger");      
               $( "input[name='confirmemail']").val( "0" );         
            }
         }
      });
      
   });


	


				
		// 회원탈퇴
		$( "form[name='passwdform']" ).on(
			"submit",
			function( event ) {
				if( ! $("input[name='passwd']" ).val() ) {
					alert( passwderror );
					$("input[name='passwd']" ).focus();
					return false;
				}
			}
		);		
		
		
		
		// 회원정보수정
		$("form[name='modifyform']").on(
			"submit",
			function( event ) {
            var RegPWExp =  /^[A-Za-z0-9`~!@#\$%\^&\*\(\)\{\}\[\]\-_=\+\\|;:'"<>,\./\?]{4,12}$/;
            var passwd = $( "input[name='passwd']" ).val();
            var RegBirthExp = /^[0-9]+$/;
            var RegTelExp = /^[0-9]+$/;
            var birth = $("input[name='birth']").val();
            var tel = $( "input[name='tel']" ).val();				
				if( ! $("input[name='passwd']").val() ){
					alert( passwderror );
					$("input[name='passwd']").focus();
					return false;
				} else if( ! RegBirthExp.test( birth ) ) {
					alert( "생년월일은 숫자만 가능합니다.")
					$("input[name='birth']").focus();
					return false;
				} else if( ! RegBirthExp.test( tel ) ) {
					alert( "전화번호는 숫자만 가능합니다.")
					$("input[name='tel']").focus();
					return false;
	            } else if( ! RegPWExp.test( passwd ) ) {
	               alert( "비밀번호는 영문 및 숫자를 사용해 4-12글자로 입력해주세요.")
	               $("input[name='passwd']").focus();
	               return false;															
				} else if( $("input[name='passwd']").val() != $("input[name='repasswd']").val() ) {
					alert( repasswderror );
					$("input[name='passwd']").focus();
					return false;
				} 
				
			
			}			
		);
		
	//비밀번호 4자리이상
	$("input[name='passwd']").keyup(function(){
	  var RegPWExp = /^[A-Za-z0-9`~!@#\$%\^&\*\(\)\{\}\[\]\-_=\+\\|;:'"<>,\./\?]{4,12}$/;
	  var pw = $("input[name='passwd']").val();
	  if( RegPWExp.test(pw)){
	    $("#pwchk").html("사용가능한 비밀번호입니다.");
	    $("#pwchk").removeClass("text-danger");
		$("#pwchk").addClass("text-info");
	  }else{
	    $("#pwchk").html("비밀번호는 영문 및 숫자를 사용해 4-12글자로 입력해주세요.");
	    $("#pwchk").removeClass("text-info");
		$("#pwchk").addClass("text-danger");    
	  }
	});
			
	//비밀번호 확인
	$("input[name='repasswd']").keyup(function(){
		var pw = $("input[name='passwd']").val();
		var repw = $("input[name='repasswd']").val();
		if(pw != repw){
			$("#repwchk").html("비밀번호가 다릅니다");
	  		$("#repwchk").removeClass("text-info");
			$("#repwchk").addClass("text-danger");		
		}else{
			$("#repwchk").html("비밀번호가 같습니다");
	  		$("#repwchk").removeClass("text-danger");
			$("#repwchk").addClass("text-info");		
		}
	});
				

		
		
		
		
		
	}
);













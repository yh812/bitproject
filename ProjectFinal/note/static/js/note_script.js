/**
 * 
 */
 
 /**
 * 
 */
 
var titleerror = "제목를 입력하세요"
var contenterror = "내용을 입력하세요"

/*$(function() {
      $("#send").click( function() {
         $('#send_form').submit();
         setTimeout(function() {
            window.close();
            }, 100);
         });
      });*/
 
 
 $(document).ready(
   function() {
      
      // 글쓰기
      $("form[name='noteform']").on(
         "submit",
         function( event ) {
            if( ! $("input[name='note_title']").val() ) {
               alert( titleerror );
               $("input[name='note_title']").focus();
               return false;
            } else if( ! $("textarea[name='note_content']").val() ) {
               alert( contenterror );
               $("textarea[name='note_content']").focus();
               return false;
            } else{
			alert("쪽지보내기 성공");
			}
         }         
      );
   }   
);
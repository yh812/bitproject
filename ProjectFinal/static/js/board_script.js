/**
 * 
 */
 
var titleerror = "제목를 입력하세요"
var fileerror = "그림파일을 올려주세요"
var msfileerror = "음악파일을 올려주세요"
var substanceerror = "내용를 입력하세요"

 
 $(document).ready(
   function() {
      
      // 글쓰기
      $("form[name='inputform']").on(
         "submit",
         function( event ) {
            if( ! $("input[name='title']").val() ) {
               alert( titleerror );
               $("input[name='title']").focus();
               return false;
            } else if( ! $("input[name='files']").val() ) {
               alert( fileerror );
               $("input[name='files']").focus();
               return false;
            
            } else if( ! $("textarea[name='substance']").val() ) {
               alert( substanceerror );
               $("textarea[name='substance']").focus();
               return false;
            } 
         }         
      );
      
      $("form[name='boardinputform']").on(
         "submit",
         function( event ) {
            if( ! $("input[name='title']").val() ) {
               alert( titleerror );
               $("input[name='title']").focus();
               return false;
            } else if( ! $("input[name='files']").val() ) {
               alert( msfileerror );
               $("input[name='files']").focus();
               return false;
            
            } else if( ! $("textarea[name='substance']").val() ) {
               alert( substanceerror );
               $("textarea[name='substance']").focus();
               return false;
            } 
         }         
      );
      
      
      
      // 글수정
      $("form[name='pc_board_modifyform']").on(
         "submit",
         function( event ) {
            if( ! $("input[name='title']").val() ) {
               alert( titleerror );
               $("input[name='title']").focus();
               return false;
            } else if( ! $("input[name='files']").val() ) {
               alert( fileerror );
               $("input[name='files']").focus();
               return false;
            } else if( ! $("textarea[name='comment']").val() ) {
               alert( commenterror );
               $("textarea[name='comment']").focus();
               return false;
            } 
         }         
      );
      
      // 음악글수정
      $("form[name='ms_board_modifyform']").on(
         "submit",
         function( event ) {
            if( ! $("input[name='title']").val() ) {
               alert( titleerror );
               $("input[name='title']").focus();
               return false;
            } else if( ! $("input[name='files']").val() ) {
               alert( msfileerror );
               $("input[name='files']").focus();
               return false;
            } else if( ! $("textarea[name='comment']").val() ) {
               alert( commenterror );
               $("textarea[name='comment']").focus();
               return false;
            } 
         }         
      );

   }   
);
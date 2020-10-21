function showPages(id){
    var totalNumberOfPages = 8;
    for(var i=1; i<=totalNumberOfPages; i++){

        if (document.getElementById('page'+i)) {

            document.getElementById('page'+i).style.display='none';
        }

    }
        if (document.getElementById('page'+id)) {

            document.getElementById('page'+id).style.display='block';
        }
};

function showQues(){
    var page1Ques = document.getElementById("page1");
    page1Ques.style.display='block'
}

$(document).ready(function(){
  
    $(".has_children").click(function(){
      $(this).addClass("highlight")
      .children("a").show().end()
      
      .siblings().removeClass("highlight")
      .children("a").hide(); 
      
    });
    
    });
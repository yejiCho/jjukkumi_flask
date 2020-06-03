function search_movie(){
    var movie = $('#movie').val();
    if (movie == ''){
    alert('입력해주세요.');
    }
    $.ajax({
    url : '/recom/test',
    contentType : 'application/json',
    method : 'POST',
    data : JSON.stringify({
        movie : $('#movie').val()
    }),
    success:function(data){
        window.location='/recom/test';
    }
    })
}

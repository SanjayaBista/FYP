$(document).ready(function(){
    $(document).on('click','.js-add-wishlist', function(){
        var _pid=$(this).attr('data-product');
        var _vm=$(this);
        //Ajax
        $.ajax({
            url: '/add_wishlist',
            data: {
              product: _pid
            },
            dataType: 'json',
            success:function(res){
                if(res.bool==true){
                    _vm.addClass('disabled').removeClass('js-add-wishlist');
                }
            }
        });
        //EndAjax
    });
});
//end document.ready
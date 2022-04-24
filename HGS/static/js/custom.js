$(document).ready(function(){
    // $(document).on('click','.js-add-wishlist', function(){
    //     var _pid=$(this).attr('data-product');
    //     var _vm=$(this);
    //     //Ajax
    //     $.ajax({
    //         url: '/add_wishlist',
    //         data: {
    //           product: _pid
    //         },
    //         dataType: 'json',
    //         success:function(res){
    //             if(res.bool==true){
    //                 _vm.addClass('disabled').removeClass('js-remove-wishlist');
    //             }
    //         }
    //     });
    //     //EndAjax
    // });
});
//end document.ready
function get(name) {
    if (name = (new RegExp('[?&]' + encodeURIComponent(name) + '=([^&]*)')).exec(location.search))  //location.search give query sling part
      return decodeURIComponent(name[1]);
  }

if(get('ordering'))
    document.getElementById('placeholder').innerHTML =  document.getElementById(get('ordering')).innerHTML;


function finalurl() {
    var url = new URL(window.location.href);
    var search_params = url.searchParams;
    search_params.set('ordering', document.getElementById("sort-list").value);
    url.search = search_params.toString();
    var new_url = url.toString();
    return new_url
  }


  

function bookmark_product(product_id, csrf){
    $.ajax({
        headers: {'X-CSRFTOKEN': csrf},
        type: "post",
        url: "/bookmark-product/"+product_id,
        beforeSend: bookmark_state(product_id, 'js-update'),
        success: function(answer) {
            console.log(answer)
            bookmark_state(product_id, answer.bookmark_state);
        }
    });
}

function bookmark_state(product_id, state){
    
    var _product_id = '#' + product_id;
    var child_elts = $(_product_id).children();
    child_elts.css({'display': 'none'});

    if (state == true) {
        var _classname = '.is-bookmark';
    } else if (state == false) {
        var _classname = '.is-not-bookmark';
    } else {
        var _classname = '.js-update';
    }
    child_elts.siblings(_classname).css({'display': 'inline'});
}

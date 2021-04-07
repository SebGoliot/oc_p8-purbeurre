
function bookmark_product(old_product_id, product_id, csrf){
    $.ajax({
        headers: {'X-CSRFTOKEN': csrf},
        type: "post",
        url: "/bookmark/",
        contentType: 'application/json',
        dataType:'json',
        data: JSON.stringify({
            'old_product_id': old_product_id,
            'product_id': product_id,
        }),
        beforeSend: bookmark_state(product_id, 'js-update'),
        success: function(answer) {
            bookmark_state(product_id, answer.bookmark_state);
        },
        error: function(answer) {
            bookmark_state(product_id, false);
        }
    });
}

function bookmark_state(product_id, state){
    // This function changes the visibility of the most relevant 
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

// Enable tooltips
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();   
  });

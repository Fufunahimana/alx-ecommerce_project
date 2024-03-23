$('.plus-cart').click(function(){ 
    var id = $(this).attr("pid").toString();
    var eml = $(this).siblings("#quantity");
    console.log("pid =", id);
    $.ajax({ 
        type: "GET",
        url: "/pluscart/",
        data: { prod_id: id },
        success: function(data) {
            console.log("data =", data);
            eml.text(data.quantity);
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
        }
    });
});

$('.minus-cart').click(function(){ 
    var id = $(this).attr("pid").toString();
    var eml = $(this).siblings("#quantity");
    console.log("pid =", id);
    $.ajax({ 
        type: "GET",
        url: "/minuscart/",
        data: { prod_id: id },
        success: function(data) {
            console.log("data =", data);
            eml.text(data.quantity);
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
        }
    });
});

$('.remove-cart').click(function(){ 
    var id = $(this).attr("pid").toString();
    var row = $(this).closest('.row');
    console.log("pid =", id);
    $.ajax({ 
        type: "GET",
        url: "/removecart/",
        data: { prod_id: id },
        success: function(data) {
            console.log("data =", data);
            $("#amount").text(data.amount);
            $("#totalamount").text(data.totalamount);
            row.remove();
        }
    });
});

$('.plus-wishlist').click(function() {
        var id = $(this).attr("pid").toString();
        $.ajax({
            type: "GET",
            url: "/pluswishlist",
            data: {
                prod_id: id
            },
            //alert(data.message)
            success: function(data) {
                window.location.href = 'http://localhost:8000/product-detail/${id}'
            },
        });
    });

$('.minus-wishlist').click(function(e) {
            var id = $(this).attr("pid");
            $.ajax({
            type: "GET",
            url: "/minuswishlist/",
            data: {
                prod_id: id
            },
            success: function(data) {
                window.location.href = 'http://localhost:8000/product-detail/${id}'
            }
    });
});

const subcategory_change = () => {
    const category_id = document.querySelector('#category').value
    const url = `/categories/${category_id}`


    fetch(url).then(response => response.json()).then((response) => {
        console.log(response)
    })
}

const category = document.querySelector('#category')
category.addEventListener('change', () => {
    subcategory_change();
})


subcategory_change();
//    function subcategory_change() {
//        var category_id = $("#category").val();
//        $.ajax({
//            type: "GET",
//            url: "/categories/" + category_id
//        }).done(function (data) {
//            $("#subcategory").empty();
//            if ($("#category").hasClass("category-filter")) {
//                $("#subcategory").append(
//                    $("<option></option>").attr("value", "0").text(" --- ")
//                );
//            }
//            $.each(data.subcategories, function (index, value) {
//                $("#subcategory").append(
//                    $("<option></option>").attr("value", value[0]).text(value[1])
//                );
//            });
//        });
//    }
//    $("#category").change(function () {
//        subcategory_change();
//    });


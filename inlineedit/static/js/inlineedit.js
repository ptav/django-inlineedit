/*
    Django-Inline-Edit
*/

// Called when document is ready (hides editing form and buttons)
$(function() {
    $(".inlineedit-form").hide();
    $(".inlineedit-toggle").hide();
});


// Mouse enters toggle area
$(".inlineedit-toggle-area").mouseenter(
    function() {
        var id = $(this).attr("id");
        $(".inlineedit-toggle#" + id).show();
    }
);


// Mouse leaves toggle area
$(".inlineedit-toggle-area").mouseleave(
    function() {
        var id = $(this).attr("id");
        $(".inlineedit-toggle#" + id).fadeOut(4000);
    }
);


// Click in edit icon (toggles field editor on)
$(".inlineedit-toggle").click(
    function() {
        var id = $(this).attr("id");
        $(".inlineedit-value#" + id).hide();
        $(".inlineedit-toggle#" + id).hide();
        $(".inlineedit-form#" + id).show();
    }
);


// Cancel editing
function inlineedit_exit_editing(object) {
    var id = $(object).closest('form').attr('id');
    $(".inlineedit-form#" + id).hide();
    $(".inlineedit-value#" + id).show();
};


// Override form submit action to prevent page refresh
$('.inlineedit-form').on('submit', function(event)
{
	event.preventDefault(); //prevent default action

    var url = $(this).attr("action"); //get form action url
    if (!url || url.length < 3) {
        url = "/inlineedit/inlineedit_form_submit/";
    }

    var param = {
        url : url,
        type: $(this).attr("method"), // GET/POST method
        data : new FormData(this), // Serialised form data
        contentType: false,
		cache: false,
		processData: false
    };

    $.ajax(param).done(
        function(response) {
            if (response.success) {
                $(".inlineedit-value#" + response.uuid).html(response.value)
            }

            $(".inlineedit-form#" + response.uuid).hide();
            $(".inlineedit-value#" + response.uuid).show();
        }
    );
});
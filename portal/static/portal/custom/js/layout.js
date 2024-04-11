$(document).ready(function () {
    $("#search").on("keyup", function () {
        var searchText = $(this).val().toLowerCase();

        $(".treeview").each(function () {
            var hasMatchingLink = false;
            $(this).find(".treeview-menu a").each(function () {
                if ($(this).text().toLowerCase().indexOf(searchText) > -1) {
                    hasMatchingLink = true;
                }
            });

            $(this).toggle(hasMatchingLink);
        });
    });
});
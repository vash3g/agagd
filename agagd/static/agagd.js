$(function() {
    var async_table_url_params = {};

    // Send hashchanges to async tables if it's appropriate
    function process_hashchange() {
        var url_hash = window.location.hash.replace("#", ""),
            url_params = url_hash? $.deserialize(url_hash) : {},
            new_table_params = {},
            tables_to_reload = [],
            key, is_async_table_key, table_id, i;
        for (key in url_params) {
            is_async_table_key = key.split("__").length == 2 && (key.split("__")[1] == "page" || key.split("__")[1] == "sort");
            if (is_async_table_key) {
                new_table_params[key] = url_params[key];
                table_id = key.split("__")[0];
                if (new_table_params[key] == async_table_url_params[key]) {
                    delete async_table_url_params[key];
                } else {
                    if (tables_to_reload.indexOf(table_id) < 0) {
                        tables_to_reload.push(table_id);
                    }
                }
            }
        }

        for (key in async_table_url_params) {
            table_id = key.split("__")[0];
            if (tables_to_reload.indexOf(table_id) < 0) {
                tables_to_reload.push(table_id);
            }
        }

        for (i = 0; i < tables_to_reload.length; i++) {
            table_id = tables_to_reload[i];
            $.async_table.go_to_page(
                table_id,
                new_table_params[table_id + "__page"],
                new_table_params[table_id + "__sort"]
            );
        }
        async_table_url_params = new_table_params;
    }
    process_hashchange();
    $(window).on("hashchange", process_hashchange);

    // Change the hash when async table loads happen
    $(window).on("async_table_loaded", function(event) {
        var url_hash = window.location.hash.replace("#", ""),
            url_params = url_hash? $.deserialize(url_hash) : {}, key;
        if (event.page || event.sort) {
            if (event.page) {
                async_table_url_params[event.table_id + "__page"] = event.page;
            }
            if (event.sort) {
                async_table_url_params[event.table_id + "__sort"] = event.sort;
            }
            for (key in async_table_url_params) {
                url_params[key] = async_table_url_params[key];
            }
            window.location.hash = $.param(url_params);
        }
    });
});

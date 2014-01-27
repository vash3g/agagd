(function($) {
    var table_template = [
            "<table class='table table-striped table-hover'>",
                "<thead><tr>HEADERS</tr></thead>",
                "<tbody>CONTENTS</tbody>",
            "</table>"
        ].join(""),
        row_template = "<tr>CONTENTS</tr>",
        cell_template = "<td>CONTENTS</td>",
        link_cell_template = "<td><a href='LINK'>LABEL</a></td>",
        header_cell_template = "<th data-sort-key='SORT_KEY'>CONTENTS</th>",
        loader_template = [
            "<div id='TABLE_ID-loader'>",
                "<div id='TABLE_ID-loader-block-1'></div>",
                "<div id='TABLE_ID-loader-block-2'></div>",
                "<div id='TABLE_ID-loader-block-3'></div>",
            "</div>"
        ].join(""),
        failure_template = [
            "<div id='TABLE_ID-failed-load'>",
                "Something broke :(",
            "</div>"
        ].join(""),
        previous_link_template = "<span class='previous'>Previous</span>",
        next_link_template = "<span class='next'>Next</span>",
        paginator_template = "<div class='paginator'>CONTENTS</div>",
        cache = {};

    $.async_table = {};

    $.async_table.init = function(config) {
        $(function() {
            init_async_table(config);
        });
    };

    $.async_table.go_to_page = function(table_id, page, sort) {
        if (table_id in cache) {
            config = cache[table_id];
            if (page) {
                config.data.page = parseInt(page);
            }
            if (sort) {
                config.data.sort = sort;
            }
            config.reload();
        }
    };

    function init_async_table(config) {
        function check_config() {
            var has_required_fields = config && config.id && config.remote_url;

            if (!has_required_fields) {
                throw config.id + " has already been created!";
            } else if (config.id in cache) {
                throw "Config is missing some required fields!";
            } else {
                cache[config.id] = config;
            }

            // Optional fields
            if (!config.data) {
                config.data = {};
            }

            // For external API
            config.reload = load_remote_url;
        }

        function load_remote_url(data) {
            var $container = $("#" + config.id);

            function failed_load_view() {
                $container.html(failure_template.replace(/TABLE_ID/g, config.id));
            }
            function loading_table_view() {
                $container.html(loader_template.replace(/TABLE_ID/g, config.id));
            }
            function populate_table(response) {
                var header_html = $.map(
                        response.headers,
                        function(header) {
                            return header_cell_template.replace("CONTENTS", header.label).replace("SORT_KEY", header.key);
                        }
                    ).join(""),
                    rows_html = $.map(
                        response.results,
                        function(cell) {
                            var cells_html = $.map(
                                response.headers,
                                function(header) {
                                    var value = cell[header.key];
                                    if (typeof value === "string") {
                                        return cell_template.replace("CONTENTS", value);
                                    } else {
                                        if (value.type === "link") {
                                            return link_cell_template.replace("LINK", value.link).replace("LABEL", value.label);
                                        } else {
                                            return cell_template.replace("CONTENTS", "");
                                        }
                                    }
                                }
                            ).join("");

                            return row_template.replace("CONTENTS", cells_html);
                        }
                    ).join(""),
                    pages = [],
                    pages_html;

                config.current_page = parseInt(response.page);
                config.total_pages = parseInt(response.total_pages);

                if (config.current_page > 1) {
                    pages.push(previous_link_template);
                }
                pages.push("<span>Page " + config.current_page + " of " + config.total_pages + "</span>");
                if (config.current_page < config.total_pages) {
                    pages.push(next_link_template);
                }

                pages_html = pages.join("");

                $container.html([
                    table_template.replace("HEADERS", header_html).replace("CONTENTS", rows_html),
                    paginator_template.replace("CONTENTS", pages_html)
                ].join(""));

                // Add events
                $container.find(".previous").click(function() {
                    data.page = config.current_page - 1;
                    load_remote_url(data);
                });
                $container.find(".next").click(function() {
                    data.page = config.current_page + 1;
                    load_remote_url(data);
                });
                $container.find("th").click(function() {
                    var sort_key = $(this).attr("data-sort-key");
                    if (sort_key === data.sort) {
                        data.sort = "-" + sort_key;
                    } else {
                        data.sort = sort_key;
                    }
                    data.page = 1;
                    load_remote_url(data);
                });

                // Trigger loaded events for external notifications
                $("body").trigger({
                    type: "async_table_loaded",
                    table_id: config.id,
                    sort: data.sort,
                    page: data.page
                });
            }

            data = data || config.data;
            loading_table_view();
            $.ajax({
                url: config.remote_url,
                data: data,
                success: populate_table,
                error: failed_load_view
            });
        }

        check_config();
        load_remote_url();
    }
})(jQuery);

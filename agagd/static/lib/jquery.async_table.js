(function($, window) {
    var table_template = _.template([
            "<table class='table table-striped table-hover'>",
                "<thead><tr>",
                    "<% _.each(headers, function(header) { %>",
                        "<th data-sort-key='<%= header.key %>'><%= header.label %></th>",
                    "<% }); %>",
                "</tr></thead>",
                "<tbody>",
                    "<% _.each(results, function(row) { %>",
                        "<tr>",
                        "<% _.each(headers, function(header) { %>",
                            "<% if (row[header.key].type == 'link') { %>",
                                "<td><a href='<%= row[header.key].link %>'><%= row[header.key].label %></a></td>",
                            "<% } else { %>",
                                "<td><%= row[header.key] %></td>",
                            "<% } %>",
                        "<% }); %>",
                        "</tr>",
                    "<% }); %>",
                "</tbody>",
            "</table>",
            "<div class='paginator'>",
                "<% if (page != 1) { %>",
                    "<span class='previous'>Previous</span>",
                "<% } %>",
                "Page <%= page %> of <%= total_pages %>",
                "<% if (page != total_pages) { %>",
                    "<span class='next'>Next</span>",
                "<% } %>",
            "</div>"
        ].join("")),
        deferred_go_to = {},
        cache = {};

    $.async_table = {};
    $.async_table.init = function(config) {
        $(function() {
            cache[config.id] = new AsyncTable(config);
            cache[config.id].reload();
        });
    };
    $.async_table.go_to_page = function(table_id, page, sort) {
        var async_table = cache[table_id],
            data = async_table? async_table.data : {};

        if (page) {
            data.page = parseInt(page);
        } else {
            delete data.page;
        }

        if (sort) {
            data.sort = sort;
        } else {
            delete data.sort;
        }

        if (async_table) {
            async_table.reload();
        } else {
            deferred_go_to[table_id] = data;
        }
    };

    function AsyncTable(config) {
        var self = this,
            $container = $("#" + config.id);

        // Required
        self.remote_url = config.remote_url;
        self.id = config.id;

        // Optional
        self.data = deferred_go_to[config.id] || config.data || {};
        self.extra_parameters = config.extra_parameters || {};

        // Methods
        self.reload = function() {
            var request_data = JSON.parse(JSON.stringify(self.data)), key;
            for (key in self.extra_parameters) {
                request_data[key] = self.extra_parameters[key];
            }

            self.loading_table_view();
            $.ajax({
                url: self.remote_url,
                data: request_data,
                success: self.populate_table,
                error: self.failed_load_view
            });
        };

        self.populate_table = function(response) {
            $container.html(table_template(response));

            self.current_page = parseInt(response.page);
            self.total_pages = parseInt(response.total_pages);

            // Add events
            $container.find(".previous").click(function() {
                self.data.page = self.current_page - 1;
                self.reload();
            });
            $container.find(".next").click(function() {
                self.data.page = self.current_page + 1;
                self.reload();
            });
            $container.find("th").click(function() {
                var sort_key = $(this).attr("data-sort-key");
                if (sort_key === data.sort) {
                    self.data.sort = "-" + sort_key;
                } else {
                    self.data.sort = sort_key;
                }
                self.data.page = 1;
                self.reload();
            });

            // Trigger loaded events for external notifications
            $(window).trigger({
                type: "async_table_loaded",
                table_id: self.id,
                sort: self.data.sort,
                page: self.data.page
            });
        };

        self.failed_load_view = function() {
            // TODO Notify user of failure
        };

        self.loading_table_view = function() {
            // TODO Loading view
        };
    }
})(jQuery, window);

var NodesTree = function() {}

NodesTree.prototype = {

    renderTree: function(url, parentElement) {
        var that = this;

        $.ajax({ url: url, dataType: 'json' })
        .success(function(response) {
            var $nodeTree = $('<nav class="nodefs" />');

            that.buildTree(response, $nodeTree);

            parentElement.append($nodeTree);
            that.prepareEvents();

        });
    },

    prepareEvents: function() {
        var that = this;

        $('.node .toggler').click(function() {
            var $node = $(this).parent('.node');

            if ($node.hasClass('open')) {
                that.registerNodeClose($node.attr('id'));
                $node.removeClass('open').addClass('closed');
            } else if ($node.hasClass('closed')) {
                that.registerNodeOpen($node.attr('id'));
                $node.removeClass('closed').addClass('open');
            }

            console.log($.cookie('nodefs_' + $node.attr('id')), $node.attr('id'));

        });
    },

    nodeIsOpen: function(nodeId) {
        return $.cookie('nodefs_' + nodeId) != null;
    },

    registerNodeOpen: function(nodeId) {
        $.cookie('nodefs_' + nodeId, 'open', { expires: 7, path: '/' });
    },

    registerNodeClose: function(nodeId) {
        $.cookie('nodefs_' + nodeId, null, { expires: 7, path: '/' });
    },

    buildTree: function(tree, parentElement) {
        parentElement.append(this.buildNodeList(tree));
    },

    buildNode: function(node, parentElement) {
        var that = this,
            nodeElement = $('<li/>', { 'class': 'node', id: node.id });

        nodeElement.addClass(this.nodeIsOpen(node.id) ? 'open' : 'closed');

        if (node.label) {
            nodeElement.append(node.label);
        }

        if (node.children && node.children.length > 0) {
            nodeElement.append('<span class="toggler" />');
            nodeElement.append(this.buildNodeList(node.children));
        }

        return nodeElement;
    },

    buildNodeList: function(nodeList) {
        var that = this,
            list = [],
            nodeListElement = $('<ul class="tree" />');

        $(nodeList).each(function(idx, node) {
            list.push(that.buildNode(node, nodeListElement));
        });

        nodeListElement.append(list);

        return nodeListElement;
    }
}


$.fn.nodesTree = function(options) {
    var nt = new NodesTree()
        jsonUrl = this.attr('data-url');

    if (options) {
        if (options.url) {
            jsonUrl = options.url;
        }
    }

    nt.renderTree(jsonUrl, this);
}

function initSvg() {
    'use strict';

    var $svg = $('svg');

    var zoomIn = function(factor) {
        $svg.width($svg.width() * factor);
        $svg.height($svg.height() * factor);
    };

    var zoomOut = function(factor) {
        $svg.width($svg.width() / factor);
        $svg.height($svg.height() / factor);
    };

    $('#zoomOut').on('click', zoomOut.bind(window, 1.5));
    $('#zoomIn').on('click', zoomIn.bind(window, 1.5));

    $svg.on('mousewheel', function(e) {
        var zoomK = 1.3;
        var event = e.originalEvent;
        e.preventDefault();

        var offset = $svg.offset();
        var onSvgX =  event.pageX - offset.left;
        var onSvgY = event.pageY - offset.top;
        var k = (event.wheelDelta > 0 ? zoomK : 1 / zoomK) - 1;
        var dx = onSvgX * k;
        var dy = onSvgY * k;

        (event.wheelDelta > 0 ? zoomIn : zoomOut)(zoomK);

        var marginDx = window.scrollX + dx;
        if (marginDx < 0) {
            window.scrollBy(-window.scrollX, 0);
            $svg.css('margin-left', 0);
        } else {
            window.scrollBy(dx, 0);
        }

        var marginDy = window.scrollY + dy;
        if (marginDy < 0) {
            window.scrollBy(0, -window.scrollY);
            $svg.css('margin-top', 0);
        } else {
            window.scrollBy(0, dy);
        }
    });

    zoomOut($svg.width() / $(window).width());
}

function highlightEdge(edge) {
    'use strict';

    window.highlightedEdges.push(edge);
    edge.path.setAttribute('stroke-width', '7px');
    edge.path.setAttribute('stroke', 'red');
}


function highlight(elem, c) {
    'use strict';

    if (!elem) return;

    var color = c || '#00ffff';

    window.highlighted.push(elem);

    elem.ellipse.style.fill = color;

    elem.children.forEach(function(el) {
        highlight(el);
    });

    elem.outEdges.forEach(highlightEdge);
}


function unHighlightAll() {
    'use strict';

    window.highlighted.forEach(function(el) {
        el.ellipse.style.fill = 'white';
    });

    window.highlighted = [];

    window.highlightedEdges.forEach(function(edge) {
        edge.path.setAttribute('stroke-width', '');
        edge.path.setAttribute('stroke', 'black');
    });

    window.highlightedEdges = [];
}


function highlightClick(elem, e) {
    'use strict';

    unHighlightAll();
    highlight(elem, 'gray');
}


function loadSvg(name, loadTemplates) {
    'use strict';

    window.nodes = {};
    window.edges = {};
    window.highlighted = [];
    window.highlightedEdges = [];

    var $container = $('#container');
    $container.empty();

    $.ajax({url: loadTemplates ? '/svg_templates' : '/svg',
        data: {file: name},
        success: function(response) {
            $('g', response.documentElement).each(function(index, el) {
                var text = $('title', el).text();
                var className = el.className.baseVal;

                if (className === 'node') {
                    var elem = window.nodes[text] = window.nodes[text] || {};

                    elem.type = 'node';
                    elem.element = el;
                    elem.$element = $(el);
                    elem.inEdges = [];
                    elem.outEdges = [];
                    elem.ellipse = $('ellipse', el)[0];
                    elem.ellipse.style.fill = 'white';
                    elem.children = [];

                    elem.$element.on('click', highlightClick.bind(this, elem));

                } else if (className === 'edge') {
                    var splited = text.split('--');

                    var nodeFrom = window.nodes[splited[0]] = window.nodes[splited[0]] || {children: [], inEdges: [], outEdges: []};
                    var nodeTo = window.nodes[splited[1]] = window.nodes[splited[1]] || {children: [], inEdges: [], outEdges: []};

                    var edge = window.edges[text] = window.edges[text] || {};
                    edge.type = 'edge';
                    edge.path = $('path', el)[0];
                    edge.element = el;

                    nodeFrom.children.push(nodeTo);
                    nodeFrom.outEdges.push(edge);
                    nodeTo.inEdges.push(edge);
                }

                unHighlightAll();
            });

            $('#container').append(response.documentElement);
            initSvg();
            if (name) {
                highlight(window.nodes[name]);
            }
        }});

}

$(document).ready(function() {
    'use strict';

    var $input = $('#filename')
    var input = $input[0];
    var $getSvgButton = $('#getSvg');
    var $invalidateButton = $('#invalidate');
    var $headerContainer = $('#header-container');
    var $header = $('#header');
    var $checkbox = $('#templatesCheckbox');
    var state = 'away';
    var hideTimer;

    loadSvg();

    function getSvgFromInput() {
        var name = input.value;
        if (!name) { return; }

        loadSvg(name, $checkbox.prop('checked'));
    }

    function onSuccessSvgLoad(res) {
        $(input).autocomplete({source: res,
                             appendTo: $header});
    }

    function getSuggest() {
        var value = input.value;
        if (!value || value.length < 2) {
            $getSvgButton.attr('disabled', true);
            return;
        }

        $getSvgButton.attr('disabled', false);

        $.ajax({
            url: '/file_suggest',
            data: {'name': input.value},
            dataType: 'json',
            success: onSuccessSvgLoad
        });
    }

    $input.bind('keyup', getSuggest);
    $input.autocomplete();

    $getSvgButton.on('click', getSvgFromInput.bind(this));

    $invalidateButton.on('click', function() {
        $invalidateButton.attr('disabled', true);

        $.ajax({
            url: '/cache_invalidate',
            success: getSvgFromInput.bind(this),
            complete: function() {
                $invalidateButton.attr('disabled', false);
            }
        });
    });


    function toggleHeader(show) {
        var top = show ? '0px' : '-100px';
        var duration = show ? 0 : 500;
        if (!show) {
            $input.autocomplete('close');
        }
        $header.animate({'top': top}, {duration: duration});
    }

    $headerContainer.on('mouseover', function(e) {
        if (state === 'leaving') {
            window.clearTimeout(hideTimer);
        } else if (state === 'away') {
            toggleHeader(true);
        }
        state = 'over';
    });

    $headerContainer.on('mouseleave', function(e) {
        if (state === 'over') {
            hideTimer = window.setTimeout(function() {
                toggleHeader(false);
                state = 'away';
            }, 300);
            state = 'leaving';
        }
    }.bind(this));

});



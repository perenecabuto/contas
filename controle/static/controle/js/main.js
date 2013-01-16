$(window).on('ready', function() {
    if ($.support.pjax) {
        var container = $('#base-content-pjax-container');
        var keepOnPjax = function(event) {
            if ( $(this).attr('href').indexOf('/media/') == 0 ) {
                return;
            }

            event.preventDefault();

            if (window.location.href == this.href) {
                return;
            }

            $.pjax({ url: $(this).attr('href'), container: container});
        };

        $('#left-panel').on('click', 'a', keepOnPjax);
        $('#content').on('click', '[href]', keepOnPjax);

        $(document).on('pjax:send', function() {
            $('#loading').show();
        });

        $(document).on('pjax:complete', function() {
            ModalBox.refresh();
            $('#loading').hide();
        });
    }
    else {
        $('input[type=button][href]').on('click', function() {
            location.href = $(this).attr('href');
        });
    }


});

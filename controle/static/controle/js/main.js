$(window).on('ready', function() {
    if ($.support.pjax) {
        var container = $('#base-content-pjax-container');

        $('#left-panel').on('click', 'a', function(event) {
            if ( $(this).attr('href').indexOf('/media/') == 0 ) {
                return;
            }

            event.preventDefault();

            if (window.location.href == this.href) {
                return;
            }

            $.pjax.click(event, {container: container});
        });

        $(document).on('pjax:send', function() {
          $('#loading').show();
        });

        $(document).on('pjax:complete', function() {
          $('#loading').hide();
        });

        $('input[type=button][href]').on('click', function() {
            location.href = $(this).attr('href');
        });
    }
});

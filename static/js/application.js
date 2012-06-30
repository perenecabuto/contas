$(window).ready(function () {
    $('#modal-box').click(function(e) {
        if (e.target == this) {
            ModalBox.clear();
        }
    });
});

ModalBox = {
    container: function() {
        if (!this._container) {
            this._container = $('#modal-box-container');
        }

        return this._container;
    },

    load: function(url) {
        this.show();
        this.container().html("Loading ...");

        $.ajax({
            url: url,
            success: function(content){
                ModalBox.container().html(content);
            }
        });
    },

    clear: function() {
        this.container().html("");
        this.hide();
    },

    show: function() {
        $('#modal-box').css({'display': 'block'});
    },

    hide: function() {
        $('#modal-box').css({'display': 'none'});
    }
};


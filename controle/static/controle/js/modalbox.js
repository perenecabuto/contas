$(window).ready(function () {
    ModalBox.getContainer().on('click', function(e) {
        if (e.target == this) {
            ModalBox.clear();
        }
    });

    $('.openonmodalbox').on('click', function(e) {
        ModalBox.load($(this).attr('href'));
        return false;
    });
});

var ModalBox = {
    getContainer: function() {
        if (!this._container) {
            this._container = $('#modal-box-container');
        }

        return this._container;
    },

    getBox: function() {
        if (!this._box) {
            this._box = $('#modal-box');
        }

        return this._box;
    },

    load: function(url) {
        this.show();
        this.getBox().html("Loading ...");

        $.ajax({
            url: url,
            success: function(content){
                ModalBox.getBox().html(content);
            }
        });
    },

    clear: function() {
        this.getBox().html("");
        this.hide();
    },

    show: function() {
        this.getContainer().show();
    },

    hide: function() {
        this.getContainer().hide();
    }
};


$.fn.clearForm = function() {
  $('.errorlist').remove();

  // iterate each matching form
  return this.each(function() {
    // iterate the elements within the form
    $(':input', this).each(function() {
      var type = this.type, tag = this.tagName.toLowerCase();
      if (type == 'text' || type == 'password' || tag == 'textarea')
        this.value = '';
      else if (type == 'checkbox' || type == 'radio')
        this.checked = false;
      else if (tag == 'select')
        this.selectedIndex = -1;
    });
  });
};

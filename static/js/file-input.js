document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.file-upload').forEach(function(wrapper) {
    var input   = wrapper.querySelector('input[type="file"]');
    var nameEl  = wrapper.querySelector('.file-upload__name');
    var labelEl = wrapper.querySelector('.file-upload__label');
    var container = wrapper.closest('.field--full') || wrapper.parentElement;
    var preview = container ? container.querySelector('.file-preview') : null;

    if (!input) return;

    input.addEventListener('change', function() {
      var file = this.files[0];
      if (!file) return;

      if (nameEl) {
        nameEl.textContent = file.name;
        nameEl.classList.add('visible');
      }
      if (labelEl) {
        labelEl.style.display = 'none';
      }

      if (preview && file.type.startsWith('image/')) {
        var reader = new FileReader();
        reader.onload = function(e) {
          preview.src = e.target.result;
          preview.classList.add('visible');
        };
        reader.readAsDataURL(file);
      }
    });
  });
});

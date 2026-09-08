document.querySelectorAll('.toggle-password').forEach((button) => {
  button.addEventListener('click', () => {
    const input = button.previousElementSibling;
    const isPassword = input.type === 'password';
    input.type = isPassword ? 'text' : 'password';
    button.textContent = isPassword ? 'Hide' : 'Show';
    button.setAttribute('aria-label', `${isPassword ? 'Hide' : 'Show'} password`);
  });
});

document.querySelectorAll('[data-demo-form]').forEach((form) => {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const message = form.querySelector('.form-feedback');
    if (!form.checkValidity()) {
      form.reportValidity();
      message.textContent = 'Please complete the highlighted fields.';
      message.classList.add('is-visible');
      return;
    }
    message.textContent = 'You’re all set! Account sign-in will be connected next.';
    message.classList.add('is-visible', 'success');
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const editor = document.getElementById('editor');
  const footer = document.getElementById('footer');

  const code = `def welcome_message() {
    return {
      'name': 'Jay',
      'role': 'Software Developer',
      'site_purpose': 'Personal portfolio exploring technology',
      'message': 'Welcome to Prokope.io!',
      'call_to_action': {
        'buttons': [
          'Github',
          'LinkedIn',
          'Medium'
        ]
      }
    };
}`;

  let index = 0;
  let displayed = '';

  function typeCode() {
    if (index <= code.length) {
      displayed = code.slice(0, index++);
      const highlighted = Prism.highlight(displayed, Prism.languages.python, 'python');
      editor.innerHTML = highlighted + '<span class="cursor">&nbsp;</span>';
      updateFooter(displayed);
      setTimeout(typeCode, 50);
    }
  }

  function updateFooter(text) {
    const lines = text.split('\n');
    const line = lines.length;
    const col = lines[lines.length - 1].length + 1;
    footer.textContent = `Ln ${line}, Col ${col}`;
  }

  typeCode();
});
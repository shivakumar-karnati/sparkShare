const input = document.querySelector('input[name="q"]');

if (input) {
      input.focus();

      // Move cursor to end
      const val = input.value;
      input.value = "";
      input.value = val;
  }


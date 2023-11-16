browserCheck();

function browserCheck() {
  const supportSaveFile = 'showSaveFilePicker' in window;
  if (!supportSaveFile) document.querySelector(".alert").style.display = "flex";
}
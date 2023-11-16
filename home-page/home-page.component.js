browserCheck();

function browserCheck() {
  const supportSaveFile = 'showSaveFilePicker' in window;
  console.log(supportSaveFile);
  if (!supportSaveFile) document.querySelector(".alert").style.display = "flex";
}
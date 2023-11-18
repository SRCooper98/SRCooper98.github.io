browserCheck();

function browserCheck() {
  const supportSaveFile = 'showSaveFilePicker' in window;
  if (!supportSaveFile) document.querySelector("#browserAlert").style.display = "flex";
}

//potential file size checker

// function fileSizeCheck(files) {
//   document.querySelector('#sizeAlert').style.display = "none"
//   const fileSize = files[0].size
//   console.log(fileSize);
//   //Limit 240,000 b
//   if (fileSize > 240000) {
//     document.querySelector('#sizeAlert').style.display = "flex"
//     return false;
//   }
//   return true;
// }
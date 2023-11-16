function handleFileSelect(event) {
  const fileInput = event.target;
  const file = fileInput.files[0];

  if (file) {
    const reader = new FileReader();

    reader.onload = function(e) {
      const contents = e.target.result;
      displayContents(contents);
      //Iterate through contents variable
    };

    reader.readAsText(file);
  } else {
    alert('Failed to load file');
  }
}

function displayContents(contents) {
  const outputDiv = document.getElementById('output');
  outputDiv.innerText = contents;
}

document.getElementById('fileInput').addEventListener('change', handleFileSelect)
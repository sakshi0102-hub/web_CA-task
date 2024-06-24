const form = document.getElementById('upload-form');
const outputDiv = document.getElementById('output');

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const groupCsv = document.getElementById('group-csv').files[0];
  const hostelCsv = document.getElementById('hostel-csv').files[0];

  // Send the CSV files to the backend for processing
  fetch('/allocate', {
    method: 'POST',
    body: JSON.stringify({ groupCsv, hostelCsv }),
    headers: { 'Content-Type': 'application/json' }
  })
 .then(response => response.json())
.then((data) => {
    const outputHtml = '';
    data.forEach((row) => {
      outputHtml += `${row.groupId} - ${row.hostelName} - ${row.roomNumber} - ${row.membersAllocated}<br>`;
    });
    outputDiv.innerHTML = outputHtml;
  })
 .catch((error) => {
    console.error(error);
  });
});

// Add a button to download the allocation CSV file
const downloadButton = document.createElement('button');
downloadButton.textContent = 'Download Allocation CSV';
outputDiv.appendChild(downloadButton);

downloadButton.addEventListener('click', () => {
  fetch('/download')
 .then(response => response.blob())
 .then((blob) => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'allocation.csv';
    a.click();
  })
 .catch((error) => {
    console.error(error);
  });
});
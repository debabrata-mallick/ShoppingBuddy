function updateComparisonReport(category, urlList) {
  input = {
    'urls': urlList,
    'category': category
  }

  fetch('http://127.0.0.1:5000/compare/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(input),
  })
    .then(response => response.json())
    .then(data => {
      if (data.status == 200) {
        console.log('Success:', data);
        renderTable(data);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function renderTable(_data) {

  comparison_columns = [{ title: "", field: "feature" }]
  for(i=0; i<_data.url_count; i++) 
  {
    comparison_columns.push({ title: _data.titles[i], field: "Product"+(i+1), width: 100/_data.url_count + "%", formatter: "textarea", hozAlign: "left" })
  }

  var table = new Tabulator("#comparison-table", {  
    tooltipsHeader:true,
    data: _data.products, 
    columns: comparison_columns,
  });
}
